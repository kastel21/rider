"""PC / M&E primary analysis excludes relayed trip rows from sample and result totals."""

from datetime import date
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from operations.models import (
    District,
    PCProfile,
    Province,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    TripRouteKind,
    TripTransportKind,
    TripVisitPurpose,
    UserProfile,
)
from operations.services.me_metrics_service import build_me_metrics
from operations.services.me_report_service import build_me_report_table_for_week
from operations.services.trip_analysis import (
    filter_primary_analysis_trips,
    is_relayed_trip,
    specimens_from_entries,
)
from operations.services.weekly_review_service import build_weekly_review_snapshot


def _operations_test_databases():
    names = {"default"}
    if "sqlite" in settings.DATABASES:
        names.add("sqlite")
    return names


class TripAnalysisHelperTests(TestCase):
    databases = {"default"}

    def test_relayed_kind_is_excluded_from_primary_queryset(self):
        User = get_user_model()
        rider = User.objects.create_user(username="ta_rider", password="x")
        UserProfile.objects.update_or_create(
            user=rider, defaults={"role": UserProfile.Role.RIDER}
        )
        report = RiderWeeklyReport.objects.create(
            rider=rider,
            week_start=date(2026, 7, 6),
            status=RiderWeeklyReport.Status.APPROVED,
        )
        first = RiderTripEntry.objects.create(
            report=report,
            sequence=1,
            transport_kind=TripTransportKind.FIRST_TRANSPORT,
            vl_blood_plasma=4,
        )
        relayed = RiderTripEntry.objects.create(
            report=report,
            sequence=2,
            transport_kind=TripTransportKind.RELAYED,
            vl_blood_plasma=9,
        )
        legacy = RiderTripEntry.objects.create(
            report=report,
            sequence=3,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.RELAY,
            vl_dbs=2,
        )
        self.assertFalse(is_relayed_trip(first))
        self.assertTrue(is_relayed_trip(relayed))
        self.assertFalse(is_relayed_trip(legacy))
        primary = list(filter_primary_analysis_trips(report.trip_entries.all()).order_by("id"))
        self.assertEqual([e.pk for e in primary], [first.pk, legacy.pk])
        self.assertEqual(specimens_from_entries(report.trip_entries.all()), 6)


class MeReportExcludesRelayedTests(TestCase):
    databases = {"default"}

    def setUp(self):
        User = get_user_model()
        self.driver = User.objects.create_user(
            username="relay_driver",
            first_name="Rel",
            last_name="Driver",
            password="x",
        )
        UserProfile.objects.update_or_create(
            user=self.driver, defaults={"role": UserProfile.Role.DRIVER}
        )
        province = Province.objects.create(name="RelProv")
        district = District.objects.create(name="RelDist", province=province)
        RiderProfile.objects.get_or_create(
            user=self.driver,
            defaults={"province": province, "district": district},
        )
        self.week = date(2026, 7, 6)
        self.report = RiderWeeklyReport.objects.create(
            rider=self.driver,
            week_start=self.week,
            status=RiderWeeklyReport.Status.APPROVED,
            samples_collected=30,
            scheduled_visits=2,
        )
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=1,
            transport_kind=TripTransportKind.FIRST_TRANSPORT,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_LAB,
            vl_blood_plasma=10,
            results_vl_blood_plasma=6,
            sputum=1,
        )
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=2,
            transport_kind=TripTransportKind.RELAYED,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_HUB,
            vl_blood_plasma=20,
            results_vl_blood_plasma=15,
            hpv=4,
        )

    def test_weekly_matrix_counts_only_first_transport(self):
        table = build_me_report_table_for_week(
            week_start=self.week,
            role=UserProfile.Role.DRIVER,
        )
        self.assertEqual(table["row_count"], 1)
        by_key = {table["columns"][i]["key"]: table["rows"][0][i]["text"] for i in range(len(table["rows"][0]))}
        self.assertEqual(by_key["sp_vl_bp"], "10")
        self.assertEqual(by_key["res_vl_bp"], "6")
        self.assertEqual(by_key["sp_hpv"], "0")
        self.assertEqual(by_key["sp_sputum"], "1")
        self.assertEqual(by_key["actual_visits"], "1")

    @patch("operations.services.me_metrics_service.monday_of_local_today")
    def test_overview_mixed_dataset_does_not_leak_relayed(self, mock_monday):
        mock_monday.return_value = date(2026, 7, 13)
        m = build_me_metrics(weeks=1)
        self.assertEqual(m["all_time"]["samples_total"], 11)
        self.assertEqual(m["window"]["samples"], 11)
        self.assertEqual(m["delivery"]["specimens_by_type"]["vl_blood_plasma"], 10)
        self.assertEqual(m["delivery"]["specimens_by_type"]["hpv"], 0)
        self.assertEqual(m["delivery"]["results_by_type"]["vl_blood_plasma"], 6)
        self.assertEqual(m["chart"]["samples"], [11])
        self.assertEqual(m["chart_delivery_trends"]["vl"]["specimens"], [10])
        self.assertEqual(m["operations_kpis"]["window"]["trip_rows_as_actual_visits_sum"], 1)

    def test_review_snapshot_totals_isolate_relayed(self):
        payload = build_weekly_review_snapshot(rider=self.driver, week_start=self.week)
        self.assertEqual(payload["totals"]["specimens_transported"], 11)
        self.assertEqual(payload["totals"]["results_transported"], 6)
        self.assertEqual(payload["totals"]["relayed_specimens_transported"], 24)
        self.assertEqual(payload["totals"]["relayed_results_transported"], 15)
        self.assertEqual(len(payload["reports"][0]["trip_entries"]), 2)


class PcReportListNonRelayedSamplesTests(TestCase):
    databases = _operations_test_databases()

    def setUp(self):
        User = get_user_model()
        self.pc = User.objects.create_user(username="pc_relay", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.pc, defaults={"role": UserProfile.Role.PC}
        )
        self.driver = User.objects.create_user(username="drv_relay", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.driver, defaults={"role": UserProfile.Role.DRIVER}
        )
        self.province = Province.objects.create(name="PcRelProv")
        self.district = District.objects.create(name="PcRelDist", province=self.province)
        pc_profile, _ = PCProfile.objects.get_or_create(user=self.pc)
        pc_profile.provinces.add(self.province)
        RiderProfile.objects.get_or_create(
            user=self.driver,
            defaults={"province": self.province, "district": self.district},
        )
        self.week = date(2026, 7, 6)
        report = RiderWeeklyReport.objects.create(
            rider=self.driver,
            week_start=self.week,
            status=RiderWeeklyReport.Status.SUBMITTED,
            samples_collected=99,
        )
        RiderTripEntry.objects.create(
            report=report,
            sequence=1,
            transport_kind=TripTransportKind.FIRST_TRANSPORT,
            vl_blood_plasma=5,
        )
        RiderTripEntry.objects.create(
            report=report,
            sequence=2,
            transport_kind=TripTransportKind.RELAYED,
            vl_blood_plasma=50,
        )
        self.client = Client()

    def test_pc_list_samples_column_excludes_relayed(self):
        self.assertTrue(self.client.login(username="pc_relay", password="pass123"))
        resp = self.client.get(
            reverse("operations:pc_reports"),
            {"week": self.week.isoformat()},
        )
        self.assertEqual(resp.status_code, 200)
        rows = resp.context["pc_driver_report_rows"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["samples_total"], 5)
        self.assertEqual(rows[0]["trip_total"], 2)
        self.assertContains(resp, "non-relayed")
