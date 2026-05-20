"""
Build upsert_report payloads for remote JWT sync (Android / PWA).
"""
from decimal import Decimal

from ..models import RiderTripEntry, RiderWeeklyReport, SampleRejection


def _decimal_str(value) -> str:
    if value is None:
        return "0"
    if isinstance(value, Decimal):
        return str(value)
    return str(value)


def trip_entry_to_sync_row(entry: RiderTripEntry) -> dict:
    row = {
        "row_uuid": str(entry.row_uuid) if entry.row_uuid else None,
        "sequence": entry.sequence,
        "transport_kind": entry.transport_kind,
        "entry_date": entry.entry_date.isoformat() if entry.entry_date else None,
        "vl_blood_plasma": entry.vl_blood_plasma,
        "vl_dbs": entry.vl_dbs,
        "eid_blood": entry.eid_blood,
        "eid_dbs": entry.eid_dbs,
        "sputum": entry.sputum,
        "sputum_culture_dr": entry.sputum_culture_dr,
        "hpv": entry.hpv,
        "specimens_other_specify": entry.specimens_other_specify or "",
        "results_vl_blood_plasma": entry.results_vl_blood_plasma,
        "results_vl_dbs": entry.results_vl_dbs,
        "results_eid_blood": entry.results_eid_blood,
        "results_eid_dbs": entry.results_eid_dbs,
        "results_sputum": entry.results_sputum,
        "results_sputum_culture_dr": entry.results_sputum_culture_dr,
        "results_hpv": entry.results_hpv,
        "results_other_specify": entry.results_other_specify or "",
        "fuel_allocated": _decimal_str(entry.fuel_allocated),
        "fuel_used": _decimal_str(entry.fuel_used),
        "distance_travelled": _decimal_str(entry.distance_travelled),
    }
    if entry.visit_purpose:
        row["visit_purpose"] = entry.visit_purpose
    if entry.route_kind:
        row["route_kind"] = entry.route_kind
    if entry.origin_facility_id:
        row["origin_facility_id"] = entry.origin_facility_id
    if entry.destination_facility_id:
        row["destination_facility_id"] = entry.destination_facility_id
    return row


def rejection_to_sync_row(rej: SampleRejection) -> dict:
    return {
        "sample_type": rej.sample_type,
        "rejected_total": rej.rejected_total,
        "rejected_too_old": rej.rejected_too_old,
        "rejected_patient_info_mismatch": rej.rejected_patient_info_mismatch,
        "rejected_request_form_missing": rej.rejected_request_form_missing,
        "rejected_sample_missing": rej.rejected_sample_missing,
        "rejected_other": rej.rejected_other,
        "order": rej.order,
    }


def build_report_sync_payload(report: RiderWeeklyReport) -> dict:
    """Payload for apply_sync_batch upsert_report (matches sync_service._upsert_report)."""
    report = (
        RiderWeeklyReport.objects.filter(pk=report.pk)
        .select_related("bike", "car")
        .prefetch_related("trip_entries", "sample_rejections")
        .first()
    )
    if not report:
        return {}

    trip_rows = [
        trip_entry_to_sync_row(e)
        for e in report.trip_entries.order_by("sequence", "pk")
    ]
    rejections = [
        rejection_to_sync_row(r)
        for r in report.sample_rejections.order_by("order", "pk")
    ]

    payload = {
        "week_start": report.week_start.isoformat(),
        "title": report.title or "",
        "notes": report.notes or "",
        "samples_collected": report.samples_collected,
        "extra_data": dict(report.extra_data or {}),
        "trip_rows": trip_rows,
        "rejections": rejections,
        "average_datalogger_temperature": report.average_datalogger_temperature,
    }
    if report.bike_id:
        payload["bike_id"] = report.bike_id
    if report.car_id:
        payload["car_id"] = report.car_id
    return payload


def report_sync_envelope(report: RiderWeeklyReport) -> dict:
    """Client envelope: idempotency_key + payload."""
    key = str(report.client_uuid) if report.client_uuid else ""
    return {
        "idempotency_key": key,
        "payload": build_report_sync_payload(report),
        "report_id": report.pk,
        "status": report.status,
    }
