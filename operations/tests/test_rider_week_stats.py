from datetime import date
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from operations.models import (
    District,
    Province,
    RiderProfile,
    RiderTripEntry,
    RiderWeekFuelSummary,
    RiderWeeklyReport,
    SampleRejection,
    TripRouteKind,
    TripTransportKind,
    TripVisitPurpose,
    UserProfile,
)
from operations.services.rider_week_stats_service import build_rider_week_stats


def _operations_test_databases():
    names = {"default"}
    if "sqlite" in settings.DATABASES:
        names.add("sqlite")
    return names


class RiderWeekStatsServiceTests(TestCase):
    databases = _operations_test_databases()

    def setUp(self):
        User = get_user_model()
        self.rider = User.objects.create_user(username="rider_stats", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.rider, defaults={"role": UserProfile.Role.RIDER}
        )
        self.other = User.objects.create_user(username="other_stats", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.other, defaults={"role": UserProfile.Role.RIDER}
        )
        self.province = Province.objects.create(name="PStats")
        self.district = District.objects.create(name="DStats", province=self.province)
        RiderProfile.objects.get_or_create(
            user=self.rider,
            defaults={"province": self.province, "district": self.district},
        )
        RiderProfile.objects.get_or_create(
            user=self.other,
            defaults={"province": self.province, "district": self.district},
        )
        self.week = date(2026, 9, 7)

    def test_aggregates_specimens_results_rejections_fuel_distance(self):
        report = RiderWeeklyReport.objects.create(
            rider=self.rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            distance_travelled=Decimal("42.5"),
        )
        RiderTripEntry.objects.create(
            report=report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_LAB,
            vl_blood_plasma=3,
            results_vl_blood_plasma=2,
            eid_dbs=1,
            results_eid_dbs=1,
        )
        RiderTripEntry.objects.create(
            report=report,
            sequence=2,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.RELAY,
            route_kind=TripRouteKind.LAB_TO_HUB,
            hpv=2,
            results_hpv=1,
        )
        SampleRejection.objects.create(
            report=report,
            sample_type=SampleRejection.SampleType.VL_PLASMA,
            rejected_total=4,
            rejected_too_old=2,
            rejected_patient_info_mismatch=1,
            rejected_request_form_missing=1,
        )
        SampleRejection.objects.create(
            report=report,
            sample_type=SampleRejection.SampleType.HPV,
            rejected_total=2,
            rejected_sample_missing=2,
        )
        RiderWeekFuelSummary.objects.create(
            rider=self.rider,
            week_start=self.week,
            fuel_allocated=Decimal("30"),
            fuel_used=Decimal("18"),
        )

        stats = build_rider_week_stats(self.rider, self.week)

        self.assertEqual(stats["report_count"], 1)
        self.assertEqual(stats["specimens_total"], 6)
        self.assertEqual(stats["results_total"], 4)
        self.assertEqual(stats["fuel_allocated"], Decimal("30"))
        self.assertEqual(stats["fuel_used"], Decimal("18"))
        self.assertEqual(stats["distance_km"], Decimal("43"))
        self.assertEqual(stats["rejections"]["rejected_total"], 6)
        self.assertEqual(len(stats["rejections"]["by_sample_type"]), 2)
        vl_row = next(
            r for r in stats["rejections"]["by_sample_type"] if r["key"] == "vl_plasma"
        )
        self.assertEqual(vl_row["rejected_total"], 4)
        self.assertEqual(vl_row["reasons"]["rejected_too_old"], 2)

    def test_sums_across_multiple_reports_same_week(self):
        r1 = RiderWeeklyReport.objects.create(
            rider=self.rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            distance_travelled=Decimal("10"),
        )
        r2 = RiderWeeklyReport.objects.create(
            rider=self.rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            distance_travelled=Decimal("5.25"),
        )
        RiderTripEntry.objects.create(
            report=r1,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_LAB,
            vl_dbs=2,
        )
        RiderTripEntry.objects.create(
            report=r2,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_LAB,
            vl_dbs=3,
        )

        stats = build_rider_week_stats(self.rider, self.week)

        self.assertEqual(stats["report_count"], 2)
        self.assertEqual(stats["specimens_total"], 5)
        self.assertEqual(stats["distance_km"], Decimal("15"))

    def test_does_not_include_other_riders_data(self):
        report = RiderWeeklyReport.objects.create(
            rider=self.other,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            distance_travelled=Decimal("100"),
        )
        RiderTripEntry.objects.create(
            report=report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_LAB,
            vl_blood_plasma=99,
        )

        stats = build_rider_week_stats(self.rider, self.week)

        self.assertFalse(stats["has_data"])
        self.assertEqual(stats["specimens_total"], 0)


class RiderWeekStatsViewTests(TestCase):
    databases = _operations_test_databases()

    def setUp(self):
        User = get_user_model()
        self.rider = User.objects.create_user(username="rider_stats_view", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.rider, defaults={"role": UserProfile.Role.RIDER}
        )
        self.province = Province.objects.create(name="PStatsV")
        self.district = District.objects.create(name="DStatsV", province=self.province)
        RiderProfile.objects.get_or_create(
            user=self.rider,
            defaults={"province": self.province, "district": self.district},
        )
        self.week = date(2026, 9, 14)
        self.report = RiderWeeklyReport.objects.create(
            rider=self.rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            distance_travelled=Decimal("12"),
        )
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_LAB,
            sputum=4,
            results_sputum=3,
        )
        self.url = reverse("operations:rider_week_stats")

    def test_rider_can_view_stats_page(self):
        self.client.force_login(self.rider)
        response = self.client.get(f"{self.url}?week={self.week.isoformat()}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Stats")
        self.assertContains(response, "Sputum")
        self.assertContains(response, "4")
        self.assertContains(response, "12")

    def test_pc_cannot_access_stats_page(self):
        User = get_user_model()
        pc = User.objects.create_user(username="pc_stats", password="pass123")
        UserProfile.objects.update_or_create(user=pc, defaults={"role": UserProfile.Role.PC})
        self.client.force_login(pc)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
