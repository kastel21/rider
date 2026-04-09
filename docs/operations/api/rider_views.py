"""
Rider mobile REST API.
JWT auth, profile, bootstrap (reference data), submit-report (single), sync (batch).
"""
from datetime import date, datetime
from decimal import Decimal
import uuid as uuid_lib

from django.utils import timezone

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from operations.api.permissions import IsRider

from operations.models import (
    Bike,
    Facility,
    Lab,
    RiderDevice,
    RiderRemoteConfig,
    RiderWeeklyReport,
    ReportStatus,
    SampleRejection,
    TransportRouteType,
)
from operations.services.report_service import ReportService


User = get_user_model()


def _rider_from_request(request):
    """Return RiderProfile for request.user or None."""
    return getattr(request.user, 'operations_rider_profile', None)


def _is_rider(user):
    if not user or not user.is_authenticated:
        return False
    try:
        profile = getattr(user, 'operations_profile', None)
        return profile and getattr(profile, 'role', None) in ('RIDER', 'DRIVER')
    except Exception:
        return False


def _get_device_for_sync(rider, device_id):
    """
    Return (RiderDevice, None) if device exists and is active; else (None, Response).
    Caller should return the Response on error.
    """
    if not device_id or not str(device_id).strip():
        return None, Response(
            {'error': 'device_id required'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    device_id = str(device_id).strip()
    device = RiderDevice.objects.filter(rider=rider, device_id=device_id).first()
    if not device:
        return None, Response(
            {'error': 'Device not registered. Call POST /api/rider/register-device/ first.'},
            status=status.HTTP_403_FORBIDDEN,
        )
    if not device.is_active:
        return None, Response(
            {'error': 'Device is disabled. Contact support.'},
            status=status.HTTP_403_FORBIDDEN,
        )
    return device, None


# --- Login (JWT) ---


class RiderLoginView(APIView):
    """POST /api/rider/login/  Accept username/password, return JWT tokens and minimal rider info."""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {'error': 'username and password required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, username=username.strip(), password=password)
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not _is_rider(user):
            return Response(
                {'error': 'Not a rider account'},
                status=status.HTTP_403_FORBIDDEN,
            )
        rider = getattr(user, 'operations_rider_profile', None)
        if not rider:
            return Response(
                {'error': 'Rider profile not found'},
                status=status.HTTP_403_FORBIDDEN,
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'expires_in': 3600,
            'user': {
                'id': user.pk,
                'username': user.get_username(),
                'rider_id': rider.pk,
                'district_id': rider.district_id,
                'province_id': rider.province_id or (rider.district.province_id if rider.district_id else None),
            },
        }, status=status.HTTP_200_OK)


# --- Profile ---


class RiderProfileView(APIView):
    """GET /api/rider/profile/  Return rider profile for JWT-authenticated rider."""
    permission_classes = [IsAuthenticated, IsRider]

    def get(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {'error': 'Rider profile not found'},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = rider.user
        return Response({
            'rider_id': rider.pk,
            'user_id': user.pk,
            'username': user.get_username(),
            'district': {
                'id': rider.district_id,
                'name': rider.district.name if rider.district_id else None,
                'province_id': rider.district.province_id if rider.district_id else None,
            } if rider.district_id else None,
            'province': {
                'id': rider.province_id,
                'name': rider.province.name if rider.province_id else None,
            } if rider.province_id else None,
            'pepfar_support_type': rider.pepfar_support_type or '',
            'facility': {
                'id': rider.facility_id,
                'name': rider.facility.name if rider.facility_id else None,
            } if rider.facility_id else None,
            'bike': {
                'id': rider.bike_id,
                'registration_number': rider.bike.registration_number if rider.bike_id else None,
            } if rider.bike_id else None,
            'is_relief_rider': rider.is_relief_rider,
        }, status=status.HTTP_200_OK)


# --- Device registration & config ---


class RiderRegisterDeviceView(APIView):
    """POST /api/rider/register-device/  Register or update device. Body: device_id, device_model?, app_version?."""
    permission_classes = [IsAuthenticated, IsRider]

    def post(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {'error': 'Rider profile not found'},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data if isinstance(request.data, dict) else {}
        device_id = (data.get('device_id') or '').strip()
        if not device_id:
            return Response(
                {'error': 'device_id required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        device_model = (data.get('device_model') or '')[:120]
        app_version = (data.get('app_version') or '')[:60]

        device, _ = RiderDevice.objects.update_or_create(
            rider=rider,
            device_id=device_id,
            defaults={
                'device_model': device_model,
                'app_version': app_version,
                'is_active': True,
                'last_seen': timezone.now(),
            },
        )
        return Response({
            'status': 'ok',
            'device_id': device.device_id,
            'message': 'Device registered',
        }, status=status.HTTP_200_OK)


class RiderConfigView(APIView):
    """GET /api/rider/config/  Remote config for rider app (sync_interval, max_batch_size, latest_app_version, update_required)."""
    permission_classes = [IsAuthenticated, IsRider]

    def get(self, request):
        config, _ = RiderRemoteConfig.objects.get_or_create(
            pk=1,
            defaults={
                'sync_interval': 60,
                'max_batch_size': 10,
                'latest_app_version': '',
                'update_required': False,
            },
        )
        return Response({
            'sync_interval': config.sync_interval,
            'max_batch_size': config.max_batch_size,
            'latest_app_version': config.latest_app_version or '',
            'update_required': config.update_required,
        }, status=status.HTTP_200_OK)


# --- Bootstrap (reference data for offline) ---


def _parse_since_param(since_str):
    """Parse ?since= (epoch ms or ISO datetime). Returns timezone-aware datetime or None."""
    if not since_str or not str(since_str).strip():
        return None
    s = str(since_str).strip()
    try:
        ms = int(s)
        return datetime.fromtimestamp(ms / 1000.0, tz=timezone.get_current_timezone())
    except (ValueError, TypeError):
        pass
    try:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return dt
    except (ValueError, TypeError):
        return None


class RiderBootstrapView(APIView):
    """GET /api/rider/bootstrap/  Facilities, labs, transport types, sample types for offline caching.
    Query param: since= (epoch ms or ISO datetime) for delta sync; only entities with updated_at > since are returned."""
    permission_classes = [IsAuthenticated, IsRider]

    def get(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {'error': 'Rider profile not found'},
                status=status.HTTP_403_FORBIDDEN,
            )
        district_id = rider.district_id
        province_id = rider.province_id or (rider.district.province_id if rider.district_id else None)
        since = _parse_since_param(request.query_params.get('since'))

        facilities_district = []
        facilities_province = []
        hubs = []
        if district_id:
            qs_district = Facility.objects.filter(district_id=district_id)
            if since is not None:
                qs_district = qs_district.filter(updated_at__gt=since)
            facilities_district = list(
                qs_district.values('id', 'name', 'code', 'district_id', 'is_hub', 'updated_at')
            )
            qs_hubs = Facility.objects.filter(district_id=district_id, is_hub=True)
            if since is not None:
                qs_hubs = qs_hubs.filter(updated_at__gt=since)
            hubs = list(
                qs_hubs.values('id', 'name', 'code', 'district_id', 'updated_at')
            )
        if province_id:
            qs_province = Facility.objects.filter(district__province_id=province_id).select_related('district')
            if since is not None:
                qs_province = qs_province.filter(updated_at__gt=since)
            facilities_province = list(
                qs_province.values('id', 'name', 'code', 'district_id', 'district__name', 'updated_at')
            )
            facilities_province = [
                {**f, 'district_name': f.pop('district__name', '')}
                for f in facilities_province
            ]

        qs_labs = Lab.objects.all()
        if since is not None:
            qs_labs = qs_labs.filter(updated_at__gt=since)
        labs = list(qs_labs.values('id', 'name', 'code', 'updated_at'))

        transport_route_types = [
            {'value': c[0], 'label': c[1]}
            for c in TransportRouteType.choices
        ]
        sample_types = [
            {'value': c[0], 'label': c[1]}
            for c in SampleRejection.SampleType.choices
        ]

        bikes = []
        if district_id:
            qs_bikes = Bike.objects.filter(district_id=district_id, is_active=True)
            if since is not None:
                qs_bikes = qs_bikes.filter(updated_at__gt=since)
            bikes = list(
                qs_bikes.values('id', 'registration_number', 'updated_at')
            )

        server_time = timezone.now()
        return Response({
            'facilities_district': facilities_district,
            'facilities_province': facilities_province,
            'hubs': hubs,
            'labs': labs,
            'transport_route_types': transport_route_types,
            'sample_types': sample_types,
            'bikes': bikes,
            'district_id': district_id,
            'province_id': province_id,
            'server_time': server_time.isoformat(),
        }, status=status.HTTP_200_OK)


# --- Report submission (single + batch) ---


def _parse_report_payload(payload, rider):
    """Validate and return (client_uuid, week, report_kwargs, rejections, action). Raises ValueError."""
    client_uuid_str = payload.get('client_uuid')
    if not client_uuid_str:
        raise ValueError('client_uuid required')
    try:
        client_uuid = uuid_lib.UUID(str(client_uuid_str))
    except (ValueError, TypeError):
        raise ValueError('Invalid client_uuid')

    week_str = payload.get('week')
    if not week_str:
        raise ValueError('week required')
    try:
        week = datetime.strptime(week_str[:10], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        raise ValueError('Invalid week')

    specimens = payload.get('specimens') or {}
    results = payload.get('results') or {}
    rejections = payload.get('rejections') or []

    bike_pk = payload.get('bike')
    bike_registration = ''
    if bike_pk:
        bike = Bike.objects.filter(pk=bike_pk).first()
        if bike:
            bike_registration = bike.registration_number or ''

    report_kwargs = {
        'rider': rider,
        'province': rider.province,
        'district': rider.district,
        'pepfar_support_type': getattr(rider, 'pepfar_support_type', '') or '',
        'client_uuid': client_uuid,
        'status': ReportStatus.DRAFT,
        'week': week,
        'date': date.today(),
        'relief_rider_name': (payload.get('relief_rider_name') or '').strip(),
        'is_relief_rider': False,
        'bike_registration': bike_registration,
        'facility_id': payload.get('facility') or None,
        'to_facility_id': payload.get('to_facility') or None,
        'transport_route_type': (payload.get('transport_route_type') or '').strip() or None,
        'from_lab_id': payload.get('from_lab') or None,
        'to_lab_id': payload.get('to_lab') or None,
        'vl_plasma': int(specimens.get('vl_plasma') or 0),
        'vl_dbs': int(specimens.get('vl_dbs') or 0),
        'eid_blood': int(specimens.get('eid_blood') or 0),
        'eid_dbs': int(specimens.get('eid_dbs') or 0),
        'sputum': int(specimens.get('sputum') or 0),
        'sputum_culture_dr': int(specimens.get('sputum_culture_dr') or 0),
        'hpv': int(specimens.get('hpv') or 0),
        'other_specimen': int(specimens.get('other_specimen') or 0),
        'other_specimen_description': (specimens.get('other_specimen_description') or '')[:200],
        'results_vl_plasma': int(results.get('results_vl_plasma') or 0),
        'results_vl_dbs': int(results.get('results_vl_dbs') or 0),
        'results_eid_blood': int(results.get('results_eid_blood') or 0),
        'results_eid_dbs': int(results.get('results_eid_dbs') or 0),
        'results_sputum': int(results.get('results_sputum') or 0),
        'results_sputum_culture_dr': int(results.get('results_sputum_culture_dr') or 0),
        'results_hpv': int(results.get('results_hpv') or 0),
        'results_other_specimen': int(results.get('results_other_specimen') or 0),
        'results_other_specimen_description': (results.get('results_other_specimen_description') or '')[:200],
        'fuel_allocated': Decimal(str(payload.get('fuel_allocated') or 0)),
        'fuel_used': Decimal(str(payload.get('fuel_used') or 0)),
        'distance_travelled': Decimal(str(payload.get('distance_travelled') or 0)),
        'average_datalogger_temperature': (
            Decimal(str(payload.get('average_datalogger_temperature')))
            if payload.get('average_datalogger_temperature') not in (None, '', 'null')
            else None
        ),
        'first_time_transport': payload.get('first_time_transport') if payload.get('first_time_transport') is not None else None,
    }
    valid_sample_types = {c[0] for c in SampleRejection.SampleType.choices}
    rejection_rows = []
    for i, row in enumerate(rejections):
        if row.get('rejected_total', 0) == 0 and not row.get('sample_type'):
            continue
        raw_type = (row.get('sample_type') or 'other').strip()
        sample_type = raw_type if raw_type in valid_sample_types else 'other'
        rejection_rows.append({
            'sample_type': sample_type,
            'rejected_total': int(row.get('rejected_total') or 0),
            'rejected_too_old': int(row.get('rejected_too_old') or 0),
            'rejected_patient_info_mismatch': int(row.get('rejected_patient_info_mismatch') or 0),
            'rejected_request_form_missing': int(row.get('rejected_request_form_missing') or 0),
            'rejected_sample_missing': int(row.get('rejected_sample_missing') or 0),
            'rejected_other': int(row.get('rejected_other') or 0),
            'order': int(row.get('order', i)),
        })
    action = payload.get('action') or 'save'
    return client_uuid, week, report_kwargs, rejection_rows, action


def _create_report_from_payload(rider, payload, request_user):
    """
    Create/update RiderWeeklyReport + SampleRejections from payload. Upsert by client_uuid.
    Returns (report_or_none, created: bool, error_message or None).
    """
    try:
        client_uuid, week, report_kwargs, rejection_rows, action = _parse_report_payload(payload, rider)
    except ValueError as e:
        return None, False, str(e)

    with transaction.atomic():
        existing = RiderWeeklyReport.objects.filter(client_uuid=report_kwargs['client_uuid']).first()
        if existing and existing.rider_id != rider.id:
            return None, False, 'client_uuid belongs to another rider'
        report = existing or RiderWeeklyReport(client_uuid=report_kwargs['client_uuid'])
        for key, value in report_kwargs.items():
            setattr(report, key, value)
        report.save()
        SampleRejection.objects.filter(report=report).delete()
        for row in rejection_rows:
            SampleRejection.objects.create(
                report=report,
                sample_type=row['sample_type'],
                rejected_total=row['rejected_total'],
                rejected_too_old=row['rejected_too_old'],
                rejected_patient_info_mismatch=row['rejected_patient_info_mismatch'],
                rejected_request_form_missing=row['rejected_request_form_missing'],
                rejected_sample_missing=row['rejected_sample_missing'],
                rejected_other=row['rejected_other'],
                order=row['order'],
            )
        if action == 'submit':
            ReportService.submit(report, request_user)
    return report, existing is None, None


class RiderSubmitReportView(APIView):
    """POST /api/rider/submit-report/  Submit a single report (client_uuid for deduplication)."""
    permission_classes = [IsAuthenticated, IsRider]

    def post(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {'error': 'Rider profile not found'},
                status=status.HTTP_403_FORBIDDEN,
            )
        payload = request.data if isinstance(request.data, dict) else {}
        report, created, err = _create_report_from_payload(rider, payload, request.user)
        if err:
            return Response(
                {'error': err},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not created:
            return Response(
                {'status': 'ok', 'updated': True, 'message': 'Report replaced by client_uuid'},
                status=status.HTTP_200_OK,
            )
        return Response(
            {'status': 'ok', 'id': report.pk, 'client_uuid': str(report.client_uuid)},
            status=status.HTTP_201_CREATED,
        )


class RiderSyncView(APIView):
    """POST /api/rider/sync/  Batch sync. Body: { "device_id": "...", "reports": [ {...}, ... ] }. device_id required."""
    permission_classes = [IsAuthenticated, IsRider]

    def post(self, request):
        rider = _rider_from_request(request)
        if not rider:
            return Response(
                {'error': 'Rider profile not found'},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data if isinstance(request.data, dict) else {}
        device, err_response = _get_device_for_sync(rider, data.get('device_id'))
        if err_response is not None:
            return err_response
        device.last_seen = timezone.now()
        device.save(update_fields=['last_seen'])

        reports = data.get('reports')
        if not isinstance(reports, list):
            return Response(
                {'error': 'reports array required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        synced = []
        updated = []
        errors = []

        try:
            with transaction.atomic():
                for i, payload in enumerate(reports):
                    if not isinstance(payload, dict):
                        errors.append({'index': i, 'error': 'Invalid report object'})
                        continue
                    client_uuid_str = payload.get('client_uuid')
                    report, created, err = _create_report_from_payload(rider, payload, request.user)
                    if err:
                        errors.append({'index': i, 'client_uuid': client_uuid_str, 'error': err})
                        continue
                    if not created:
                        updated.append({'index': i, 'id': report.pk, 'client_uuid': str(report.client_uuid)})
                    else:
                        synced.append({'index': i, 'id': report.pk, 'client_uuid': str(report.client_uuid)})
                if errors:
                    raise ValueError('Batch had validation errors')
        except ValueError:
            return Response(
                {'error': 'Batch validation failed', 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            'status': 'ok',
            'synced': synced,
            'updated': updated,
            'errors': errors,
            'summary': {
                'synced_count': len(synced),
                'updated_count': len(updated),
                'error_count': len(errors),
            },
        }, status=status.HTTP_200_OK)
