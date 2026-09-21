"""Primary PC / M&E analysis uses non-relayed trip rows only.

Driver weekly reports split trips into first-time transport vs relayed
(``TripTransportKind.RELAYED``: samples not carried for the first time).
Mixing those buckets double-counts specimens and results. Rider/historical rows
use ``legacy`` and remain in the primary cohort.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from django.db.models import Q, QuerySet, Sum

from ..models import RiderTripEntry, TripTransportKind

SPECIMEN_COUNT_FIELDS: tuple[str, ...] = (
    "vl_blood_plasma",
    "vl_dbs",
    "eid_blood",
    "eid_dbs",
    "sputum",
    "sputum_culture_dr",
    "hpv",
)

RESULT_COUNT_FIELDS: tuple[str, ...] = (
    "results_vl_blood_plasma",
    "results_vl_dbs",
    "results_eid_blood",
    "results_eid_dbs",
    "results_sputum",
    "results_sputum_culture_dr",
    "results_hpv",
)

# For Count("trip_entries", filter=...) on RiderWeeklyReport querysets.
NON_RELAYED_TRIP_COUNT_FILTER = ~Q(trip_entries__transport_kind=TripTransportKind.RELAYED)


def is_relayed_trip(entry: Any) -> bool:
    return (getattr(entry, "transport_kind", None) or "") == TripTransportKind.RELAYED


def non_relayed_trips_q() -> Q:
    return ~Q(transport_kind=TripTransportKind.RELAYED)


def filter_primary_analysis_trips(qs: QuerySet | None = None) -> QuerySet:
    """Trip rows that belong in default PC / M&E sample and result totals."""
    if qs is None:
        qs = RiderTripEntry.objects.all()
    return qs.filter(non_relayed_trips_q())


def iter_primary_analysis_trips(entries: Iterable[Any]):
    for entry in entries:
        if not is_relayed_trip(entry):
            yield entry


def specimens_total_from_agg(row: dict[str, Any]) -> int:
    return sum(int(row.get(field) or 0) for field in SPECIMEN_COUNT_FIELDS)


def results_total_from_agg(row: dict[str, Any]) -> int:
    return sum(int(row.get(field) or 0) for field in RESULT_COUNT_FIELDS)


def sum_specimen_counts(qs: QuerySet) -> int:
    agg = filter_primary_analysis_trips(qs).aggregate(
        **{field: Sum(field) for field in SPECIMEN_COUNT_FIELDS}
    )
    return specimens_total_from_agg(agg)


def specimens_from_entries(entries: Iterable[Any]) -> int:
    return sum(int(e.specimens_total or 0) for e in iter_primary_analysis_trips(entries))


def results_from_entries(entries: Iterable[Any]) -> int:
    return sum(int(e.results_total or 0) for e in iter_primary_analysis_trips(entries))
