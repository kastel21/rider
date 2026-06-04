"""Week-level relief coverage entered by PCs during review."""

from __future__ import annotations

from django.contrib.auth import get_user_model

from ..models import RiderWeekReliefCoverage

User = get_user_model()


def get_week_relief_coverage(*, rider_id: int, week_start) -> RiderWeekReliefCoverage | None:
    return RiderWeekReliefCoverage.objects.filter(rider_id=rider_id, week_start=week_start).first()


def relief_form_initial(*, rider_id: int, week_start) -> dict:
    row = get_week_relief_coverage(rider_id=rider_id, week_start=week_start)
    if not row:
        return {
            "is_relief_submission": False,
            "relieved_rider": None,
            "relief_reason": "",
        }
    return {
        "is_relief_submission": row.is_relief_submission,
        "relieved_rider": row.relieved_rider_id,
        "relief_reason": row.relief_reason or "",
    }


def upsert_rider_week_relief_coverage(*, rider_id: int, week_start, cleaned_data: dict) -> RiderWeekReliefCoverage:
    is_relief = bool(cleaned_data.get("is_relief_submission"))
    relieved = cleaned_data.get("relieved_rider") if is_relief else None
    reason = (cleaned_data.get("relief_reason") or "").strip() if is_relief else ""
    row, _created = RiderWeekReliefCoverage.objects.update_or_create(
        rider_id=rider_id,
        week_start=week_start,
        defaults={
            "is_relief_submission": is_relief,
            "relieved_rider": relieved,
            "relief_reason": reason,
        },
    )
    return row


def relief_coverage_snapshot_dict(*, rider_id: int, week_start) -> dict:
    row = get_week_relief_coverage(rider_id=rider_id, week_start=week_start)
    if not row:
        return {
            "is_relief_submission": False,
            "relieved_rider_id": None,
            "relieved_rider_name": "",
            "relief_reason": "",
            "relief_reason_display": "",
        }
    relieved_name = ""
    if row.relieved_rider_id:
        u = row.relieved_rider
        relieved_name = (u.get_full_name() or u.username or "").strip()
    return {
        "is_relief_submission": row.is_relief_submission,
        "relieved_rider_id": row.relieved_rider_id,
        "relieved_rider_name": relieved_name,
        "relief_reason": row.relief_reason or "",
        "relief_reason_display": row.get_relief_reason_display() if row.relief_reason else "",
    }
