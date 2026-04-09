"""Helpers for PC edits vs rider sections 4–6 enforcement."""
from operations.models import RiderWeeklyReport


def get_section_4_6_snapshot(report: RiderWeeklyReport) -> dict:
    """Return field values for SECTION_4_6_FIELD_NAMES from the given report instance."""
    out = {}
    for fname in RiderWeeklyReport.SECTION_4_6_FIELD_NAMES:
        if hasattr(report, fname):
            out[fname] = getattr(report, fname)
    return out
