"""Column definitions for the M&E rider matrix on /me/metrics/ (rider-role reports only).

Layout matches the national rider weekly export (tab-separated reference:
``operations/fixtures/mande_rider_report_reference.tsv``). Edit ``source`` to
wire columns to keys in ``me_report_resolvers.SOURCE_RESOLVERS``, or omit for blanks.

Driver export columns live in ``me_driver_report_schema.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

MESection = Literal["basic", "reach", "service", "compare", "outcome", "household", "neutral"]


@dataclass(frozen=True)
class MEReportColumn:
    key: str
    label: str
    section: MESection = "neutral"
    source: str | None = None

    def to_context_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "section": self.section,
        }


# Headers aligned to rider weekly export (46 columns).
ME_REPORT_COLUMNS: tuple[MEReportColumn, ...] = (
    MEReportColumn("name_of_rider", "Name of Rider", "basic", "rider.full_name"),
    MEReportColumn("rider_type", "Rider Type", "basic", "profile.role_lower"),
    MEReportColumn("relief_rider_name", "Relief Rider Name", "basic", "extra.relief_rider_name"),
    MEReportColumn("bike_reg", "BikeRegistrationNumber", "basic", "report.bike_or_car"),
    MEReportColumn("province", "Province ", "basic", "profile.province_name"),
    MEReportColumn("district", "District ", "basic", "profile.district_name"),
    MEReportColumn("pepfar_support", "type of support", "basic", "profile.support_type_display"),
    MEReportColumn("sp_vl_bp", "V L Blood/Plasma ", "reach", "trip.vl_blood_plasma"),
    MEReportColumn("sp_vl_dbs", "VL DBS ", "reach", "trip.vl_dbs"),
    MEReportColumn("sp_eid_blood", "EID Blood", "reach", "trip.eid_blood"),
    MEReportColumn("sp_eid_dbs", "EID DBS", "reach", "trip.eid_dbs"),
    MEReportColumn("sp_sputum", "Sputum", "reach", "trip.sputum"),
    MEReportColumn("sp_sput_dr", "Sputum Culture DR (NTBRL)", "reach", "trip.sputum_culture_dr"),
    MEReportColumn("sp_hpv", "HPV", "reach", "trip.hpv"),
    MEReportColumn(
        "sp_other",
        "others",
        "reach",
        "trip.specimens_other_joined",
    ),
    MEReportColumn("res_vl_bp", "V L Blood/Plasma ", "service", "trip.results_vl_blood_plasma"),
    MEReportColumn("res_vl_dbs", "VL DBS ", "service", "trip.results_vl_dbs"),
    MEReportColumn("res_eid_blood", "EID Blood", "service", "trip.results_eid_blood"),
    MEReportColumn("res_eid_dbs", "EID DBS", "service", "trip.results_eid_dbs"),
    MEReportColumn("res_sputum", "Sputum", "service", "trip.results_sputum"),
    MEReportColumn("res_sput_dr", "Sputum Culture DR (NTBRL)", "service", "trip.results_sputum_culture_dr"),
    MEReportColumn("res_hpv", "HPV", "service", "trip.results_hpv"),
    MEReportColumn(
        "res_other",
        "others",
        "service",
        "trip.results_other_joined",
    ),
    MEReportColumn("fuel_allocated", "Fuel allocated to rider this week", "compare", "trip.fuel_allocated_total"),
    MEReportColumn("fuel_used", "Fuel used by rider this  week", "compare", "trip.fuel_used_total"),
    MEReportColumn("distance", "Distance travelled by this week", "compare", "trip.distance_total"),
    MEReportColumn("days_functional", "Number of days  bike was functional", "compare", "report.days_bike_functional"),
    MEReportColumn("scheduled_visits", "Number of scheduled visits", "compare", "report.scheduled_visits"),
    MEReportColumn("actual_visits", "Number of actual visits", "compare", "trip.actual_visit_row_count"),
    MEReportColumn("adhoc_visits", "Number of Ad hoc visits", "household", "trip.adhoc_visit_row_count"),
    MEReportColumn(
        "adhoc_samples",
        "Number of samples transported during Ad hoc visit",
        "household",
        "trip.adhoc_specimens_total",
    ),
    MEReportColumn(
        "adhoc_results",
        "Number of results transported during Ad hoc visit",
        "household",
        "trip.adhoc_results_total",
    ),
    MEReportColumn("snp_breakdown", "Bike breakdown", "outcome", "vehicle.snp_bike_breakdown"),
    MEReportColumn("snp_service", "Bike on routine service/ maintenance", "outcome", "vehicle.snp_bike_routine_service"),
    MEReportColumn("snp_no_fuel", "Bike had no fuel", "outcome", "vehicle.snp_bike_no_fuel"),
    MEReportColumn("snp_sick", "Rider on sick leave", "outcome", "vehicle.snp_rider_sick_leave"),
    MEReportColumn("snp_annual", "Rider on annual leave", "outcome", "vehicle.snp_rider_annual_leave"),
    MEReportColumn("snp_weather", "Inclement weather", "outcome", "vehicle.snp_inclement_weather"),
    MEReportColumn("snp_accident", "Bike accident damaged", "outcome", "vehicle.snp_bike_accident"),
    MEReportColumn("snp_clinical", "Clinical IPs related issues", "outcome", "vehicle.snp_clinical_ip"),
    MEReportColumn(
        "snp_other_reasons",
        "other reasons",
        "outcome",
        "vehicle.snp_other_specify",
    ),
    MEReportColumn("mitigation", "Mitigation Measures", "outcome", "vehicle.mitigation_measures"),
    MEReportColumn("comments", "Comments", "outcome", "report.notes_full"),
    MEReportColumn("date_col", "date", "neutral", "report.week_end_date_dmY"),
    MEReportColumn("week_col", "Week", "neutral", "report.iso_week_label"),
    MEReportColumn("avg_temp", "Average temperature", "neutral", "report.average_datalogger_temperature"),
)
