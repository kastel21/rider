from decimal import Decimal

from ..models import RiderWeeklyReport, WeeklyRecordReviewed


def _decimal_to_string(value) -> str:
    if value is None:
        return "0"
    if isinstance(value, Decimal):
        return format(value, "f")
    return str(value)


def _iso_date(value):
    return value.isoformat() if value else None


def _iso_datetime(value):
    return value.isoformat() if value else None


def build_weekly_review_snapshot(*, rider, week_start):
    reports = (
        RiderWeeklyReport.objects.filter(rider=rider, week_start=week_start)
        .select_related("bike", "car")
        .prefetch_related("trip_entries", "sample_rejections")
        .order_by("id")
    )
    report_entries = []
    total_samples_collected = 0
    total_specimens = 0
    total_results = 0

    for report in reports:
        trips = []
        for trip in report.trip_entries.all().order_by("sequence", "id"):
            trip_payload = {
                "id": trip.id,
                "sequence": trip.sequence,
                "entry_date": _iso_date(trip.entry_date),
                "transport_kind": trip.transport_kind,
                "visit_purpose": trip.visit_purpose,
                "route_kind": trip.route_kind,
                "origin_facility_id": trip.origin_facility_id,
                "destination_facility_id": trip.destination_facility_id,
                "specimens": {
                    "vl_blood_plasma": trip.vl_blood_plasma,
                    "vl_dbs": trip.vl_dbs,
                    "eid_blood": trip.eid_blood,
                    "eid_dbs": trip.eid_dbs,
                    "sputum": trip.sputum,
                    "sputum_culture_dr": trip.sputum_culture_dr,
                    "hpv": trip.hpv,
                    "other_specify": trip.specimens_other_specify or "",
                    "total": trip.specimens_total,
                },
                "results": {
                    "vl_blood_plasma": trip.results_vl_blood_plasma,
                    "vl_dbs": trip.results_vl_dbs,
                    "eid_blood": trip.results_eid_blood,
                    "eid_dbs": trip.results_eid_dbs,
                    "sputum": trip.results_sputum,
                    "sputum_culture_dr": trip.results_sputum_culture_dr,
                    "hpv": trip.results_hpv,
                    "other_specify": trip.results_other_specify or "",
                    "total": trip.results_total,
                },
                "fuel_allocated": _decimal_to_string(trip.fuel_allocated),
                "fuel_used": _decimal_to_string(trip.fuel_used),
                "distance_travelled": _decimal_to_string(trip.distance_travelled),
            }
            trips.append(trip_payload)
            total_specimens += trip.specimens_total
            total_results += trip.results_total

        rejections = []
        for rej in report.sample_rejections.all().order_by("order", "id"):
            rejections.append(
                {
                    "id": rej.id,
                    "sample_type": rej.sample_type,
                    "rejected_total": rej.rejected_total,
                    "rejected_too_old": rej.rejected_too_old,
                    "rejected_patient_info_mismatch": rej.rejected_patient_info_mismatch,
                    "rejected_request_form_missing": rej.rejected_request_form_missing,
                    "rejected_sample_missing": rej.rejected_sample_missing,
                    "rejected_other": rej.rejected_other,
                    "order": rej.order,
                }
            )

        report_entries.append(
            {
                "id": report.id,
                "status": report.status,
                "title": report.title or "",
                "notes": report.notes or "",
                "pc_notes": report.pc_notes or "",
                "samples_collected": report.samples_collected,
                "scheduled_visits": report.scheduled_visits,
                "average_datalogger_temperature": report.average_datalogger_temperature,
                "bike_id": report.bike_id,
                "bike_code": report.bike.code if report.bike_id else None,
                "car_id": report.car_id,
                "car_code": report.car.code if report.car_id else None,
                "submitted_at": _iso_datetime(report.submitted_at),
                "review_started_at": _iso_datetime(report.review_started_at),
                "reviewed_at": _iso_datetime(report.reviewed_at),
                "reviewed_by_id": report.reviewed_by_id,
                "me_reviewed_at": _iso_datetime(report.me_reviewed_at),
                "me_reviewed_by_id": report.me_reviewed_by_id,
                "created_at": _iso_datetime(report.created_at),
                "updated_at": _iso_datetime(report.updated_at),
                "trip_entries": trips,
                "sample_rejections": rejections,
            }
        )
        total_samples_collected += report.samples_collected or 0

    return {
        "rider_id": rider.id,
        "week_start": _iso_date(week_start),
        "report_count": len(report_entries),
        "totals": {
            "samples_collected": total_samples_collected,
            "specimens_transported": total_specimens,
            "results_transported": total_results,
        },
        "reports": report_entries,
    }


def create_weekly_review_record(*, source_report: RiderWeeklyReport, reviewer):
    snapshot = build_weekly_review_snapshot(
        rider=source_report.rider,
        week_start=source_report.week_start,
    )
    return WeeklyRecordReviewed.objects.create(
        rider=source_report.rider,
        week_start=source_report.week_start,
        source_report=source_report,
        reviewed_by=reviewer,
        snapshot=snapshot,
    )
