"""Shared loaders for M&E accidents / incomplete transport (read-only national)."""

from __future__ import annotations

from datetime import date, timedelta

from django.http import HttpRequest

from ..models import PCAccidentDetail, PCDistrictWeeklyTransportStat
from ..selectors import monday_of_local_today, week_start_from_request


def me_accidents_week_start_from_request(request: HttpRequest) -> date:
    return week_start_from_request(
        request,
        default_week_monday=monday_of_local_today() - timedelta(days=7),
    )


def load_me_accidents_incomplete_data(*, week_start: date) -> dict[str, list]:
    stats_qs = (
        PCDistrictWeeklyTransportStat.objects.filter(week_start=week_start)
        .select_related("district", "district__province")
        .order_by("district__province__name", "district__name", "id")
    )
    transport_stats: list[dict] = []
    for s in stats_qs:
        prov = getattr(s.district.province, "name", None) if s.district_id else "—"
        transport_stats.append(
            {
                "province_name": prov or "—",
                "district_name": s.district.name if s.district_id else "—",
                "rider_accidents": s.rider_accidents,
                "incomplete_bike_transport_trips": s.incomplete_bike_transport_trips,
                "specimens_non_ist_total": s.specimens_non_ist_total,
                "specimens_ambulance": s.specimens_ambulance,
                "specimens_alternative_ip_transport": s.specimens_alternative_ip_transport,
                "specimens_mohcc_arranged_transport": s.specimens_mohcc_arranged_transport,
                "specimens_courier": s.specimens_courier,
                "specimens_other_non_ist": s.specimens_other_non_ist,
                "comments": s.comments or "",
            }
        )

    detail_qs = (
        PCAccidentDetail.objects.filter(week_start=week_start)
        .select_related("rider__user", "bike")
        .order_by("id")
    )
    accident_details: list[dict] = []
    for d in detail_qs:
        user = getattr(d.rider, "user", None)
        if user:
            rider_display = (user.get_full_name() or "").strip() or user.username
        else:
            rider_display = f"Rider #{d.rider_id}"
        accident_details.append(
            {
                "rider_display": rider_display,
                "bike_code": d.bike.code if d.bike_id else "—",
                "accident_cause": d.accident_cause,
                "bike_status_display": d.get_bike_status_display(),
                "rider_injury_display": d.get_rider_injury_status_display(),
            }
        )

    return {"transport_stats": transport_stats, "accident_details": accident_details}
