"""
Mobile / embedded: export user rows (incl. password hash) for district-scoped SQLite replica.

HIGH RISK: compromise of this response compromises those accounts on offline devices.
Use HTTPS, least privilege, and district scope only.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from operations.models import District

User = get_user_model()


class MobileUserExportView(APIView):
    """
    GET /api/rider/mobile-user-export/?district_id=<id>

    - Staff/superuser: must pass district_id (any district).
    - Rider/driver: may omit district_id (defaults to their rider_profile.district_id) or pass
      district_id equal to their district (cannot export other districts).

    Returns: { "district_id": N, "users": [ { id, username, email, password, is_active,
              userprofile: {role}, riderprofile: { district_id, province_id, ... } }, ... ] }
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        district_id, err = self._resolve_district(request)
        if err is not None:
            return err

        if not District.objects.filter(pk=district_id).exists():
            return Response(
                {"error": "district not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        qs = (
            User.objects.filter(rider_profile__district_id=district_id)
            .select_related("profile", "rider_profile")
            .order_by("id")
        )

        users_out = []
        for u in qs:
            profile = getattr(u, "profile", None)
            rp = getattr(u, "rider_profile", None)
            if not rp:
                continue
            up_payload = {}
            if profile:
                up_payload = {"role": profile.role}
            rp_payload = {
                "district_id": rp.district_id,
                "province_id": rp.province_id,
                "facility_id": rp.facility_id,
                "bike_id": rp.bike_id,
                "car_id": rp.car_id,
                "support_type": rp.support_type or "",
            }
            users_out.append(
                {
                    "id": u.pk,
                    "username": u.get_username(),
                    "email": u.email or "",
                    "password": u.password,
                    "is_active": u.is_active,
                    "userprofile": up_payload,
                    "riderprofile": rp_payload,
                }
            )

        return Response(
            {
                "district_id": district_id,
                "users": users_out,
            },
            status=status.HTTP_200_OK,
        )

    def _resolve_district(self, request):
        """Returns (district_id, None) or (None, Response)."""
        user = request.user
        qp = request.query_params.get("district_id")
        rider_p = getattr(user, "rider_profile", None)

        if user.is_staff or user.is_superuser:
            if not qp or not str(qp).strip().isdigit():
                return None, Response(
                    {"error": "district_id query parameter required for staff"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return int(qp), None

        if qp and str(qp).strip().isdigit():
            did = int(qp)
            if rider_p and rider_p.district_id == did:
                return did, None
            return None, Response(
                {"error": "you may only export your own district"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if rider_p and rider_p.district_id:
            return rider_p.district_id, None

        return None, Response(
            {"error": "district_id required (no rider district on account)"},
            status=status.HTTP_400_BAD_REQUEST,
        )
