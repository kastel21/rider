"""M&E overview aggregates (build_me_metrics + analytics extensions)."""

from datetime import date, datetime
from decimal import Decimal
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from operations.models import (
    District,
    Facility,
    PCDistrictWeeklyTransportStat,
    Province,
    ReferredSample,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    RiderWeekFuelSummary,
    SampleRejection,
    TripRouteKind,
    TripTransportKind,
    TripVisitPurpose,
    UserProfile,
)
from operations.services.me_metrics_service import build_me_metrics, parse_weeks_param
from operations.services.me_overview_analytics import _week_start_key


class ParseWeeksParamTests(TestCase):
    def test_default_is_one_week(self):
        self.assertEqual(parse_weeks_param(None), 1)
        self.assertEqual(parse_weeks_param(""), 1)
        self.assertEqual(parse_weeks_param("  "), 1)


class WeeklyDeliveryTrendsTests(TestCase):
    def test_week_start_key_normalizes_datetime(self):
        dt = datetime(2026, 7, 6, 15, 30, 0)
        self.assertEqual(_week_start_key(dt), date(2026, 7, 6))
        self.assertEqual(_week_start_key("2026-07-06"), date(2026, 7, 6))

class BuildMeMetricsOverviewTests(TestCase):
    databases = {"default"}

    @patch("operations.services.me_metrics_service.monday_of_local_today")
    def test_analytics_window_and_delivery(self, mock_monday):
        """Rolling window ends on previous Monday; trip specimen totals aggregate."""
        mock_monday.return_value = date(2026, 7, 13)

        User = get_user_model()
        rider = User.objects.create_user(username="me_ov_r", password="x")
        UserProfile.objects.update_or_create(
            user=rider, defaults={"role": UserProfile.Role.RIDER}
        )
        prov = Province.objects.create(name="MEProvOv")
        dist = District.objects.create(name="MEDistOv", province=prov)
        RiderProfile.objects.update_or_create(
            user=rider,
            defaults={"province": prov, "district": dist},
        )
        ws = date(2026, 7, 6)
        report = RiderWeeklyReport.objects.create(
            rider=rider,
            week_start=ws,
            status=RiderWeeklyReport.Status.APPROVED,
            samples_collected=50,
            scheduled_visits=10,
            average_datalogger_temperature=24,
            distance_travelled=Decimal("20"),
            me_reviewed_at=timezone.make_aware(datetime(2026, 7, 8, 12, 0, 0)),
            me_reviewed_by=rider,
        )
        RiderTripEntry.objects.create(
            report=report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SAMPLE_COLLECTION,
            route_kind=TripRouteKind.FACILITY_TO_LAB,
            vl_blood_plasma=3,
            vl_dbs=2,
            fuel_allocated=Decimal("10"),
            fuel_used=Decimal("4"),
            distance_travelled=Decimal("20"),
        )
        RiderTripEntry.objects.create(
            report=report,
            sequence=2,
            transport_kind=TripTransportKind.LEGACY,
            results_vl_dbs=5,
        )
        SampleRejection.objects.create(
            report=report,
            sample_type=SampleRejection.SampleType.VL_DBS,
            rejected_total=4,
            rejected_too_old=2,
            rejected_patient_info_mismatch=2,
        )
        RiderWeekFuelSummary.objects.create(
            rider=rider,
            week_start=ws,
            fuel_allocated=Decimal("100"),
            fuel_used=Decimal("40"),
            distance_travelled=Decimal("0"),
        )
        lab = Facility.objects.create(
            district=dist,
            name="LabOut",
            kind=Facility.Kind.LAB,
        )
        lab2 = Facility.objects.create(
            district=dist,
            name="LabRef",
            kind=Facility.Kind.LAB,
        )
        rs = ReferredSample.objects.create(
            from_facility=lab,
            to_facility=lab2,
            sample_type=ReferredSample.SampleType.DBS,
            test_type=ReferredSample.TestType.VL,
            total_samples_referred_out=11,
        )
        ReferredSample.objects.filter(pk=rs.pk).update(
            created_at=timezone.make_aware(datetime(2026, 7, 7, 10, 0, 0))
        )
        PCDistrictWeeklyTransportStat.objects.create(
            week_start=ws,
            district=dist,
            rider_accidents=2,
            incomplete_bike_transport_trips=3,
            specimens_non_ist_total=7,
            specimens_ambulance=7,
        )

        m = build_me_metrics(weeks=2)

        self.assertEqual(m["window_start"], date(2026, 6, 29))
        self.assertEqual(m["window_end"], date(2026, 7, 6))
        self.assertEqual(m["delivery"]["specimens_by_type"]["total"], 5)
        self.assertEqual(m["delivery"]["results_by_type"]["vl_dbs"], 5)
        self.assertEqual(m["rejections_window"]["rejected_total"], 4)
        self.assertEqual(m["fuel_distance"]["period_fuel_allocated"], 100.0)
        self.assertEqual(m["fuel_distance"]["period_distance_km"], 20.0)
        self.assertEqual(m["fuel_distance"]["samples_per_km_in_period"], 2.5)
        self.assertEqual(m["referred_window"]["referral_records"], 1)
        self.assertEqual(m["referred_window"]["samples_referred_out"], 11)
        self.assertEqual(m["pc_transport_window"]["rider_accidents"], 2)
        self.assertEqual(m["pc_transport_window"]["incomplete_bike_transport_trips"], 3)

        wk = m["operations_kpis"]["window"]
        self.assertEqual(wk["reports_total_n"], 1)
        self.assertEqual(wk["reports_with_temperature_n"], 1)
        self.assertEqual(wk["me_reviewed_n"], 1)
        self.assertEqual(wk["approved_n"], 1)
        self.assertEqual(wk["scheduled_visits_sum"], 10)
        self.assertEqual(wk["trip_rows_as_actual_visits_sum"], 2)
        self.assertEqual(wk["visit_completion_pct"], 20.0)

        chart = m["chart"]
        self.assertEqual(len(chart["labels"]), 2)
        self.assertIn("fuel_allocated", chart)

        trends = m["chart_delivery_trends"]
        self.assertEqual(len(trends["labels"]), 2)
        self.assertEqual(trends["weeks"], 2)
        self.assertEqual(trends["labels"][-1], "2026-07-06")
        self.assertEqual(trends["vl"]["specimens"], [0, 5])
        self.assertEqual(trends["vl"]["results"], [0, 5])
        self.assertEqual(trends["hpv"]["specimens"], [0, 0])
        self.assertEqual(trends["tb"]["specimens"], [0, 0])

        prov_vl = m["chart_province_vl"]
        self.assertEqual(prov_vl["labels"], ["MEProvOv"])
        self.assertEqual(prov_vl["specimens"]["vl_plasma"], [3])
        self.assertEqual(prov_vl["specimens"]["vl_dbs"], [2])
        self.assertEqual(prov_vl["results"]["vl_plasma"], [0])
        self.assertEqual(prov_vl["results"]["vl_dbs"], [5])
        self.assertEqual(m["chart_province_hpv"]["labels"], [])

        top_p = [x["name"] for x in m["delivery"]["province_top_specimens"]]
        self.assertIn("MEProvOv", top_p)


def _me_view_test_databases():
    """Include optional ``sqlite`` alias when configured (e.g. import path); avoids MSSQL threaded-client errors."""
    names = {"default"}
    if "sqlite" in settings.DATABASES:
        names.add("sqlite")
    return names


class MEMetricsOverviewViewTests(TestCase):
    databases = _me_view_test_databases()

    @patch("operations.services.me_metrics_service.monday_of_local_today")
    def test_me_overview_200(self, mock_monday):
        mock_monday.return_value = date(2026, 7, 13)
        User = get_user_model()
        me_user = User.objects.create_user(username="me_role_ov", password="secret123")
        UserProfile.objects.update_or_create(
            user=me_user, defaults={"role": UserProfile.Role.ME}
        )
        client = Client()
        self.assertTrue(client.login(username="me_role_ov", password="secret123"))
        resp = client.get(reverse("operations:me_metrics"), {"weeks": "4"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Program delivery")
        self.assertContains(resp, "Transport by program")
        self.assertContains(resp, "By province")
        self.assertContains(resp, "me-chart-trend-vl")
        self.assertContains(resp, "me-chart-province-vl-specimens")
        self.assertContains(resp, "me-chart-province-hpv")

    @patch("operations.services.me_metrics_service.monday_of_local_today")
    def test_me_overview_defaults_to_previous_week_only(self, mock_monday):
        mock_monday.return_value = date(2026, 7, 13)
        User = get_user_model()
        me_user = User.objects.create_user(username="me_role_ov2", password="secret123")
        UserProfile.objects.update_or_create(
            user=me_user, defaults={"role": UserProfile.Role.ME}
        )
        client = Client()
        self.assertTrue(client.login(username="me_role_ov2", password="secret123"))
        resp = client.get(reverse("operations:me_metrics"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "06 Jul 2026")
        self.assertContains(resp, "12 Jul 2026")
