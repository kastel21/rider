"""
Rider mobile REST API.
JWT auth, profile, bootstrap, device registration, and idempotent sync (same semantics as POST /api/sync/).
"""
from datetime import datetime

from django.utils import timezone

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from operations.api.permissions import IsRider

from operations.models import (
    Bike,
    District,
    Facility,
    Lab,
    Province,
    RiderDevice,
    RiderProfile,
    RiderRemoteConfig,
    SampleRejection,
    TransportRouteType,
    UserProfile,
)
from operations.services.sync_service import apply_sync_batch


User = get_user_model()


def _rider_from_request(request):
    """Return RiderProfile for request.user or None."""
    return getattr(request.user, "rider_profile", None)


def _is_rider(user):
    if not user or not user.is_authenticated:
        return False
    try:
        from operations.models import UserProfile

        profile = getattr(user, "profile", None)
        if not profile:
            return False
        role = getattr(profile, "role", None)
        return role in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER)
    except Exception:
        return False


def _get_device_for_sync(rider, device_id):
    """
    Return (RiderDevice, None). Auto-registers device on first apply-sync (mobile APK).
    """
    if not device_id or not str(device_id).strip():
        return None, Response(
            {"error": "device_id required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    device_id = str(device_id).strip()
    device = RiderDevice.objects.filter(rider=rider, device_id=device_id).first()
    if not device:
        device, _ = RiderDevice.objects.update_or_create(
            rider=rider,
            device_id=device_id,
            defaults={
                "device_model": "",
                "app_version": "",
                "is_active": True,
                "last_seen": timezone.now(),
            },
        )
    if not device.is_active:
        return None, Response(
            {"error": "Device is disabled. Contact support."},
            status=status.HTTP_403_FORBIDDEN,
        )
    return device, None


# --- Health (connectivity probe) ---


class RiderHealthView(APIView):
    """GET /api/rider/health/ — lightweight probe for offline-sync reachability."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"ok": True}, status=status.HTTP_200_OK)


# --- Login (JWT) ---


class RiderLoginView(APIView):
    """POST /api/rider/login/ — username/password, return JWT tokens and minimal rider info."""

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"error": "username and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, username=username.strip(), password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not _is_rider(user):
            return Response(
                {"error": "Not a rider account"},
                status=status.HTTP_403_FORBIDDEN,
            )
        rider = getattr(user, "rider_profile", None)
        if not rider:
            return Response(
                {"error": "Rider profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "expires_in": 3600,
                "user": {
                    "id": user.pk,
                    "username": user.get_username(),
                    "rider_id": rider.pk,
                    "district_id": rider.district_id,
                    "province_id": rider.province_id
                    or (rider.district.province_id if rider.district_id else None),
                },
            },
            status=status.HTTP_200_OK,
        )


class RiderLocalSessionView(APIView):
    """
    POST /api/rider/local-session/
    Establish a Django session from a remote-issued JWT (same signing key as backend API).

    Body: { "access": "<jwt>", "user": { ... optional mirror of /api/rider/login/ user } }
    """

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        access = request.data.get("access")
        user_payload = request.data.get("user")
        if not isinstance(user_payload, dict):
            user_payload = {}
        if not access or not str(access).strip():
            return Response(
                {"error": "access token required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            validated = AccessToken(str(access).strip())
            user_id = validated["user_id"]
        except TokenError:
            return Response(
                {"error": "invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        username = (user_payload.get("username") or "").strip() or f"rider_{user_id}"
        if User.objects.filter(username=username).exclude(pk=user_id).exists():
            username = f"rider_{user_id}"

        user, created = User.objects.update_or_create(
            pk=int(user_id),
            defaults={"username": username},
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        UserProfile.objects.get_or_create(
            user=user,
            defaults={"role": UserProfile.Role.RIDER},
        )

        rp, _ = RiderProfile.objects.get_or_create(user=user)
        district_id = user_payload.get("district_id")
        province_id = user_payload.get("province_id")
        if district_id and District.objects.filter(pk=district_id).exists():
            rp.district_id = int(district_id)
        if province_id and Province.objects.filter(pk=province_id).exists():
            rp.province_id = int(province_id)
        rp.save()

        login(request, user)
        return Response({"ok": True, "user_id": user.pk}, status=status.HTTP_200_OK)


# --- Profile ---


class RiderProfileView(APIView):
    """GET /api/rider/profile/ — rider profile for JWT-authenticated user."""

    permission_classes = [IsAuthenticated, IsRider]

    def get(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {"error": "Rider profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = rider.user
        bike_payload = None
        if rider.bike_id and rider.bike:
            bike_payload = {
                "id": rider.bike_id,
                "registration_number": rider.bike.code,
            }
        car_payload = None
        if rider.car_id and rider.car:
            car_payload = {
                "id": rider.car_id,
                "code": rider.car.code,
            }
        return Response(
            {
                "rider_id": rider.pk,
                "user_id": user.pk,
                "username": user.get_username(),
                "district": {
                    "id": rider.district_id,
                    "name": rider.district.name if rider.district_id else None,
                    "province_id": rider.district.province_id if rider.district_id else None,
                }
                if rider.district_id
                else None,
                "province": {
                    "id": rider.province_id,
                    "name": rider.province.name if rider.province_id else None,
                }
                if rider.province_id
                else None,
                "pepfar_support_type": rider.support_type or "",
                "facility": {
                    "id": rider.facility_id,
                    "name": rider.facility.name if rider.facility_id else None,
                }
                if rider.facility_id
                else None,
                "bike": bike_payload,
                "car": car_payload,
                "is_relief_rider": False,
            },
            status=status.HTTP_200_OK,
        )


# --- Device registration & config ---


class RiderRegisterDeviceView(APIView):
    """POST /api/rider/register-device/"""

    permission_classes = [IsAuthenticated, IsRider]

    def post(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {"error": "Rider profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data if isinstance(request.data, dict) else {}
        device_id = (data.get("device_id") or "").strip()
        if not device_id:
            return Response(
                {"error": "device_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        device_model = (data.get("device_model") or "")[:120]
        app_version = (data.get("app_version") or "")[:60]

        device, _ = RiderDevice.objects.update_or_create(
            rider=rider,
            device_id=device_id,
            defaults={
                "device_model": device_model,
                "app_version": app_version,
                "is_active": True,
                "last_seen": timezone.now(),
            },
        )
        return Response(
            {
                "status": "ok",
                "device_id": device.device_id,
                "message": "Device registered",
            },
            status=status.HTTP_200_OK,
        )


class RiderConfigView(APIView):
    """GET /api/rider/config/"""

    permission_classes = [IsAuthenticated, IsRider]

    def get(self, request):
        config, _ = RiderRemoteConfig.objects.get_or_create(
            pk=1,
            defaults={
                "sync_interval": 60,
                "max_batch_size": 10,
                "latest_app_version": "",
                "update_required": False,
            },
        )
        return Response(
            {
                "sync_interval": config.sync_interval,
                "max_batch_size": config.max_batch_size,
                "latest_app_version": config.latest_app_version or "",
                "update_required": config.update_required,
            },
            status=status.HTTP_200_OK,
        )


# --- Bootstrap (reference data for offline) ---


def _parse_since_param(since_str):
    """Parse ?since= (epoch ms or ISO datetime)."""
    if not since_str or not str(since_str).strip():
        return None
    s = str(since_str).strip()
    try:
        ms = int(s)
        return datetime.fromtimestamp(ms / 1000.0, tz=timezone.get_current_timezone())
    except (ValueError, TypeError):
        pass
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return dt
    except (ValueError, TypeError):
        return None


class RiderBootstrapView(APIView):
    """GET /api/rider/bootstrap/ — reference data for offline caching."""

    permission_classes = [IsAuthenticated, IsRider]

    def get(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {"error": "Rider profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )
        district_id = rider.district_id
        province_id = rider.province_id or (
            rider.district.province_id if rider.district_id else None
        )
        since = _parse_since_param(request.query_params.get("since"))

        facilities_district = []
        facilities_province = []
        hubs = []
        if district_id:
            qs_district = Facility.objects.filter(district_id=district_id)
            facilities_district = list(
                qs_district.values("id", "name", "district_id", "kind", "support_type")
            )
            qs_hubs = Facility.objects.filter(district_id=district_id, kind=Facility.Kind.HUB)
            hubs = list(
                qs_hubs.values("id", "name", "district_id", "kind", "support_type")
            )
        if province_id:
            qs_province = Facility.objects.filter(district__province_id=province_id).select_related(
                "district"
            )
            facilities_province = list(
                qs_province.values("id", "name", "district_id", "district__name", "kind", "support_type")
            )
            facilities_province = [
                {**f, "district_name": f.pop("district__name", "")} for f in facilities_province
            ]

        qs_labs = Lab.objects.all()
        if since is not None:
            qs_labs = qs_labs.filter(updated_at__gt=since)
        labs = list(qs_labs.values("id", "name", "code", "updated_at"))

        transport_route_types = [
            {"value": c[0], "label": c[1]} for c in TransportRouteType.choices
        ]
        sample_types = [
            {"value": c[0], "label": c[1]} for c in SampleRejection.SampleType.choices
        ]

        bikes = []
        if district_id:
            qs_bikes = Bike.objects.filter(district_id=district_id, active=True)
            bikes_raw = list(qs_bikes.values("id", "code"))
            bikes = [
                {
                    "id": b["id"],
                    "registration_number": b["code"],
                    "updated_at": None,
                }
                for b in bikes_raw
            ]

        server_time = timezone.now()
        return Response(
            {
                "facilities_district": facilities_district,
                "facilities_province": facilities_province,
                "hubs": hubs,
                "labs": labs,
                "transport_route_types": transport_route_types,
                "sample_types": sample_types,
                "bikes": bikes,
                "district_id": district_id,
                "province_id": province_id,
                "server_time": server_time.isoformat(),
            },
            status=status.HTTP_200_OK,
        )


# --- Sync (JWT): same batch semantics as session POST /api/sync/ ---


class RiderApplySyncView(APIView):
    """
    POST /api/rider/apply-sync/
    Body: { "operations": [ { "op", "idempotency_key", "payload" }, ... ], "device_id": "..." }
    device_id required when enforcing RiderDevice registration.
    """

    permission_classes = [IsAuthenticated, IsRider]

    def post(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {"error": "Rider profile not found"},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data if isinstance(request.data, dict) else {}
        device, err_response = _get_device_for_sync(rider, data.get("device_id"))
        if err_response is not None:
            return err_response
        device.last_seen = timezone.now()
        device.save(update_fields=["last_seen"])

        operations = data.get("operations")
        if not isinstance(operations, list):
            return Response(
                {"ok": False, "error": "operations must be a list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        out = apply_sync_batch(request.user, operations)
        return Response(out, status=status.HTTP_200_OK)


# Backwards-compatible name for URL include (same implementation).
RiderSyncView = RiderApplySyncView
