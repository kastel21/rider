"""
Apply idempotent PWA sync operations (session-authenticated rider).
"""
import logging
from decimal import Decimal

from django.db import transaction
from django.utils import timezone as dj_timezone
from django.utils.dateparse import parse_date

from ..permissions import can_edit_report_as_rider
from ..models import (
    Bike,
    Car,
    Facility,
    RegisteredDevice,
    ReportAuditLog,
    RiderTripEntry,
    RiderWeeklyReport,
    SampleRejection,
    TripTransportKind,
    TripRouteKind,
    TripVisitPurpose,
    UserProfile,
)
from .distance_km import round_distance_km
from .trip_facilities import (
    facility_matches_route_endpoint,
    normalize_route_kind,
    route_endpoint_roles,
)

logger = logging.getLogger(__name__)


def register_device(user, device_id: str, platform: str = "", user_agent: str = ""):
    if not device_id:
        return {"ok": False, "error": "device_id required"}
    obj, _ = RegisteredDevice.objects.update_or_create(
        user=user,
        device_id=device_id[:128],
        defaults={
            "platform": platform[:64] if platform else "",
            "user_agent": user_agent[:512] if user_agent else "",
        },
    )
    return {"ok": True, "device_id": obj.device_id}


def _parse_week(s):
    d = parse_date(s) if isinstance(s, str) else s
    return d


def apply_sync_batch(user, operations: list) -> dict:
    """
    Each operation: { "op": "upsert_report", "idempotency_key": "<uuid>", "payload": {...} }
    One failed op must not roll back the rest (MSSQL/SQLite savepoints).
    """
    results = []
    for i, raw in enumerate(operations):
        if not isinstance(raw, dict):
            results.append({"ok": False, "error": "operation must be an object", "index": i})
            continue
        op = raw.get("op")
        key = raw.get("idempotency_key") or raw.get("client_uuid")
        payload = raw.get("payload") or {}
        try:
            with transaction.atomic():
                if op == "upsert_report":
                    res = _upsert_report(user, key, payload)
                else:
                    res = {"ok": False, "error": f"unknown op: {op}"}
        except Exception as e:
            logger.warning("apply_sync_batch op %s failed: %s", i, e)
            res = {"ok": False, "error": str(e)}
        res["index"] = i
        if not res.get("ok"):
            logger.warning("apply_sync_batch result %s: %s", i, res.get("error"))
        results.append(res)
    return {"ok": True, "results": results}


def _apply_payload_status(report, payload):
    """Honor client status; JWT apply-sync defaults missing status to submitted."""
    want = (payload.get("status") or "").strip().lower()
    if want != RiderWeeklyReport.Status.SUBMITTED:
        return
    if report.status in (
        RiderWeeklyReport.Status.APPROVED,
        RiderWeeklyReport.Status.UNDER_REVIEW,
    ):
        return
    report.status = RiderWeeklyReport.Status.SUBMITTED
    if not report.submitted_at:
        report.submitted_at = dj_timezone.now()


def _upsert_report(user, idempotency_key, payload):
    """
    Server-wins if report already approved; otherwise last-write from client payload.
    """
    client_uuid = None
    if idempotency_key:
        try:
            import uuid

            client_uuid = uuid.UUID(str(idempotency_key))
        except (ValueError, TypeError):
            client_uuid = None

    week_raw = payload.get("week_start")
    week_start = _parse_week(week_raw)
    if not week_start:
        return {"ok": False, "error": "week_start required"}

    title = (payload.get("title") or "")[:256]
    notes = payload.get("notes") or ""
    samples = int(payload.get("samples_collected") or 0)
    extra = payload.get("extra_data") or {}
    trip_rows = payload.get("trip_rows") or []
    rejection_rows = payload.get("rejections") or []

    qs = RiderWeeklyReport.objects.filter(rider=user)
    report = None
    if client_uuid:
        report = qs.filter(client_uuid=client_uuid).first()

    if report is None:
        report = RiderWeeklyReport(
            rider=user,
            week_start=week_start,
            client_uuid=client_uuid,
        )
    elif client_uuid and report.client_uuid is None:
        report.client_uuid = client_uuid

    if report.status == RiderWeeklyReport.Status.APPROVED:
        return {
            "ok": True,
            "skipped": True,
            "reason": "server_wins_approved",
            "report_id": report.id,
        }

    if report.pk and not can_edit_report_as_rider(user, report):
        return {
            "ok": True,
            "skipped": True,
            "reason": "not_editable_status",
            "report_id": report.id,
        }

    report.title = title
    report.notes = notes
    report.samples_collected = max(0, samples)
    report.extra_data = extra
    _apply_payload_status(report, payload)

    if "average_datalogger_temperature" in payload:
        raw_temp = payload.get("average_datalogger_temperature")
        if raw_temp in (None, "", "null"):
            report.average_datalogger_temperature = None
        else:
            try:
                report.average_datalogger_temperature = int(raw_temp)
            except (TypeError, ValueError):
                raise ValueError("average_datalogger_temperature must be an integer") from None

    if getattr(user, "profile", None) and user.profile.role != UserProfile.Role.DRIVER:
        if "bike_id" in payload or "bike" in payload:
            bike_raw = payload["bike_id"] if "bike_id" in payload else payload.get("bike")
            if bike_raw in (None, ""):
                report.bike = None
            else:
                try:
                    bid = int(bike_raw)
                except (TypeError, ValueError):
                    bid = None
                bike = Bike.objects.filter(pk=bid).first() if bid is not None else None
                if bike:
                    rp = getattr(user, "rider_profile", None)
                    if not (
                        rp
                        and rp.district_id
                        and bike.district_id
                        and bike.district_id != rp.district_id
                    ):
                        report.bike = bike

    if getattr(user, "profile", None) and user.profile.role == UserProfile.Role.DRIVER:
        if "car_id" in payload or "car" in payload:
            car_raw = payload["car_id"] if "car_id" in payload else payload.get("car")
            if car_raw in (None, ""):
                report.car = None
            else:
                try:
                    cid = int(car_raw)
                except (TypeError, ValueError):
                    cid = None
                car = Car.objects.filter(pk=cid).first() if cid is not None else None
                if car:
                    rp = getattr(user, "rider_profile", None)
                    if not (
                        rp
                        and rp.district_id
                        and car.district_id
                        and car.district_id != rp.district_id
                    ):
                        report.car = car
                report.bike = None

    report.save()
    if isinstance(trip_rows, list):
        _upsert_trip_rows(user, report, trip_rows)
        report.samples_collected = _recalc_samples_total(report)
        report.save(update_fields=["samples_collected", "updated_at"])
    if isinstance(rejection_rows, list):
        _upsert_rejection_rows(report, rejection_rows)
    ReportAuditLog.objects.create(
        report=report,
        actor=user,
        action="sync_upsert",
        payload={"client": str(client_uuid) if client_uuid else None},
    )
    return {"ok": True, "report_id": report.id, "updated_at": report.updated_at.isoformat()}


def _recalc_samples_total(report):
    return sum(
        (
            r.vl_blood_plasma
            + r.vl_dbs
            + r.eid_blood
            + r.eid_dbs
            + r.sputum
            + r.sputum_culture_dr
            + r.hpv
        )
        for r in report.trip_entries.all()
    )


def _trip_row_dict_has_content(row: dict) -> bool:
    for k in (
        "vl_blood_plasma",
        "vl_dbs",
        "eid_blood",
        "eid_dbs",
        "sputum",
        "sputum_culture_dr",
        "hpv",
    ):
        if int(row.get(k) or 0) > 0:
            return True
    for k in (
        "results_vl_blood_plasma",
        "results_vl_dbs",
        "results_eid_blood",
        "results_eid_dbs",
        "results_sputum",
        "results_sputum_culture_dr",
        "results_hpv",
    ):
        if int(row.get(k) or 0) > 0:
            return True
    if (row.get("specimens_other_specify") or "").strip():
        return True
    if (row.get("results_other_specify") or "").strip():
        return True
    if float(row.get("fuel_allocated") or 0) > 0 or float(row.get("fuel_used") or 0) > 0:
        return True
    if float(row.get("distance_travelled") or 0) > 0:
        return True
    if row.get("visit_purpose") or row.get("route_kind"):
        return True
    if row.get("origin_facility_id") or row.get("destination_facility_id"):
        return True
    if row.get("origin_facility") or row.get("destination_facility"):
        return True
    return False


def _parse_fk_id(row, *keys):
    for k in keys:
        v = row.get(k)
        if v in (None, ""):
            continue
        try:
            return int(v)
        except (TypeError, ValueError):
            continue
    return None


def _upsert_trip_rows(user, report, trip_rows):
    import uuid

    for idx, row in enumerate(trip_rows, start=1):
        if not isinstance(row, dict):
            continue
        try:
            _upsert_one_trip_row(user, report, row, idx)
        except Exception as e:
            logger.warning("sync trip row %s on report %s: %s", idx, report.pk, e)


def _upsert_one_trip_row(user, report, row, idx):
    import uuid

    raw_uuid = row.get("row_uuid")
    row_uuid = None
    if raw_uuid:
        try:
            row_uuid = uuid.UUID(str(raw_uuid))
        except (ValueError, TypeError):
            row_uuid = None
    if row_uuid is None:
        row_uuid = uuid.uuid4()

    obj, _ = RiderTripEntry.objects.get_or_create(
        report=report,
        row_uuid=row_uuid,
        defaults={
            "sequence": idx,
            "transport_kind": TripTransportKind.LEGACY,
        },
    )
    obj.sequence = int(row.get("sequence") or idx)
    tk = (row.get("transport_kind") or "").strip()
    if tk in {e.value for e in TripTransportKind}:
        obj.transport_kind = tk
    if obj.entry_date is None:
        obj.entry_date = _parse_week(row.get("entry_date")) or dj_timezone.localdate()
    obj.vl_blood_plasma = int(row.get("vl_blood_plasma") or 0)
    obj.vl_dbs = int(row.get("vl_dbs") or 0)
    obj.eid_blood = int(row.get("eid_blood") or 0)
    obj.eid_dbs = int(row.get("eid_dbs") or 0)
    obj.sputum = int(row.get("sputum") or 0)
    obj.sputum_culture_dr = int(row.get("sputum_culture_dr") or 0)
    obj.hpv = int(row.get("hpv") or 0)
    obj.specimens_other_specify = (row.get("specimens_other_specify") or "")[:255]
    obj.results_vl_blood_plasma = int(row.get("results_vl_blood_plasma") or 0)
    obj.results_vl_dbs = int(row.get("results_vl_dbs") or 0)
    obj.results_eid_blood = int(row.get("results_eid_blood") or 0)
    obj.results_eid_dbs = int(row.get("results_eid_dbs") or 0)
    obj.results_sputum = int(row.get("results_sputum") or 0)
    obj.results_sputum_culture_dr = int(row.get("results_sputum_culture_dr") or 0)
    obj.results_hpv = int(row.get("results_hpv") or 0)
    obj.results_other_specify = (row.get("results_other_specify") or "")[:255]
    obj.fuel_allocated = row.get("fuel_allocated") or 0
    obj.fuel_used = row.get("fuel_used") or 0
    obj.distance_travelled = Decimal(round_distance_km(row.get("distance_travelled") or 0))

    vp = (row.get("visit_purpose") or "").strip()
    rk = (row.get("route_kind") or "").strip()
    if vp == TripVisitPurpose.RELAY:
        rk = TripRouteKind.HUB_TO_HUB
    oid = _parse_fk_id(row, "origin_facility_id", "origin_facility")
    did = _parse_fk_id(row, "destination_facility_id", "destination_facility")
    origin = (
        Facility.objects.filter(pk=oid).select_related("district", "district__province").first()
        if oid
        else None
    )
    dest = (
        Facility.objects.filter(pk=did).select_related("district", "district__province").first()
        if did
        else None
    )
    rk_norm = normalize_route_kind(rk) if rk else ""
    roles = route_endpoint_roles(rk_norm) if rk_norm else None
    routing_ok = bool(
        vp
        and rk_norm
        and origin
        and dest
        and roles
        and facility_matches_route_endpoint(origin, roles[0])
        and facility_matches_route_endpoint(dest, roles[1])
    )
    if routing_ok:
        obj.visit_purpose = TripVisitPurpose.normalize(vp)
        obj.route_kind = rk_norm[:40]
        obj.origin_facility = origin
        obj.destination_facility = dest
    elif vp:
        obj.visit_purpose = TripVisitPurpose.normalize(vp)
        obj.route_kind = (rk_norm or rk)[:40]
        obj.origin_facility = origin
        obj.destination_facility = dest
    else:
        obj.visit_purpose = ""
        obj.route_kind = ""
        obj.origin_facility_id = None
        obj.destination_facility_id = None

    obj.save()


def _upsert_rejection_rows(report, rejection_rows: list) -> None:
    valid_sample_types = {c[0] for c in SampleRejection.SampleType.choices}
    SampleRejection.objects.filter(report=report).delete()
    for i, row in enumerate(rejection_rows):
        if not isinstance(row, dict):
            continue
        rtot = int(row.get("rejected_total") or 0)
        st = (row.get("sample_type") or "").strip()
        if rtot == 0 and not st:
            continue
        sample_type = st if st in valid_sample_types else "other"
        too_old = int(row.get("rejected_too_old") or 0)
        pinfo = int(row.get("rejected_patient_info_mismatch") or 0)
        rqfm = int(row.get("rejected_request_form_missing") or 0)
        rsm = int(row.get("rejected_sample_missing") or 0)
        rother = int(row.get("rejected_other") or 0)
        order = int(row.get("order") if row.get("order") is not None else i)
        if rtot > 0 and too_old + pinfo + rqfm + rsm + rother != rtot:
            rother = max(0, rtot - (too_old + pinfo + rqfm + rsm))
        SampleRejection.objects.create(
            report=report,
            sample_type=sample_type,
            rejected_total=rtot,
            rejected_too_old=too_old,
            rejected_patient_info_mismatch=pinfo,
            rejected_request_form_missing=rqfm,
            rejected_sample_missing=rsm,
            rejected_other=rother,
            order=order,
        )
