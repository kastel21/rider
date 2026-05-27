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
    TripRouteKind,
    TripTransportKind,
    TripVisitPurpose,
    UserProfile,
)
from operations.services.week_fuel_service import (
    apply_week_fuel_distance_rollup,
    parse_week_fuel_pc_post,
    week_fuel_decimals_from_report,
    week_fuel_totals_for_report,
    week_fuel_totals_from_db,
)


def _operations_test_databases():
    names = {"default"}
    if "sqlite" in settings.DATABASES:
        names.add("sqlite")
    return names


class RiderWeekFuelServiceTests(TestCase):
    databases = _operations_test_databases()

    def setUp(self):
        User = get_user_model()
        self.rider = User.objects.create_user(username="rider_fuel", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.rider, defaults={"role": UserProfile.Role.RIDER}
        )
        self.province = Province.objects.create(name="PFuel")
        self.district = District.objects.create(name="DFuel", province=self.province)
        RiderProfile.objects.get_or_create(
            user=self.rider,
            defaults={"province": self.province, "district": self.district},
        )
        self.week = date(2026, 7, 6)
        self.report = RiderWeeklyReport.objects.create(
            rider=self.rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            distance_travelled=Decimal("99.5"),
        )

    def test_apply_rollup_stores_on_first_row(self):
        t1 = RiderTripEntry.objects.create(
            report=self.report,
            sequence=2,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            route_kind=TripRouteKind.HUB_TO_LAB,
            vl_blood_plasma=1,
        )
        t2 = RiderTripEntry.objects.create(
            report=self.report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.RELAY,
            route_kind=TripRouteKind.LAB_TO_HUB,
            vl_dbs=1,
        )
        apply_week_fuel_distance_rollup(self.report, Decimal("40"), Decimal("12"))
        t2.refresh_from_db()
        t1.refresh_from_db()
        self.assertEqual(t2.fuel_allocated, Decimal("40"))
        self.assertEqual(t2.fuel_used, Decimal("12"))
        self.assertEqual(t2.distance_travelled, Decimal("99.5"))
        self.assertEqual(t1.fuel_allocated, Decimal("0"))
        self.assertEqual(t1.fuel_used, Decimal("0"))
        self.assertEqual(t1.distance_travelled, Decimal("0"))

    def test_week_fuel_totals_from_db_sums_all_rows(self):
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            fuel_allocated=Decimal("3"),
            fuel_used=Decimal("1"),
            distance_travelled=Decimal("10"),
        )
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=2,
            transport_kind=TripTransportKind.LEGACY,
            fuel_allocated=Decimal("0"),
            fuel_used=Decimal("0"),
            distance_travelled=Decimal("0"),
        )
        d = week_fuel_totals_from_db(self.report)
        self.assertEqual(Decimal(d["allocated"]), Decimal("3"))
        self.assertEqual(Decimal(d["used"]), Decimal("1"))
        self.assertEqual(Decimal(d["distance"]), Decimal("10"))

    def test_week_fuel_decimals_from_report_uses_report_distance(self):
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            fuel_allocated=Decimal("8"),
            fuel_used=Decimal("2"),
            distance_travelled=Decimal("4"),
        )
        snap = week_fuel_decimals_from_report(self.report)
        self.assertEqual(snap, (Decimal("8"), Decimal("2"), Decimal("99.5")))

    def test_parse_week_fuel_pc_post_accepts_comma_decimal(self):
        from django.http import QueryDict

        qd = QueryDict(mutable=True)
        qd["pc_fuel_allocated_total"] = "10,5"
        qd["pc_fuel_used_total"] = "3"
        a, u = parse_week_fuel_pc_post(qd)
        self.assertEqual(a, Decimal("10.5"))
        self.assertEqual(u, Decimal("3"))

    def test_week_fuel_totals_for_report_prefers_summary_for_fuel_report_for_distance(self):
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            fuel_allocated=Decimal("1"),
            fuel_used=Decimal("1"),
            distance_travelled=Decimal("1"),
        )
        RiderWeekFuelSummary.objects.create(
            rider=self.rider,
            week_start=self.week,
            fuel_allocated=Decimal("100"),
            fuel_used=Decimal("20"),
            distance_travelled=Decimal("50"),
        )
        d = week_fuel_totals_for_report(self.report)
        self.assertEqual(Decimal(d["allocated"]), Decimal("100"))
        self.assertEqual(Decimal(d["used"]), Decimal("20"))
        self.assertEqual(Decimal(d["distance"]), Decimal("99.5"))


class RiderWeekFuelViewTests(TestCase):
    databases = _operations_test_databases()

    def setUp(self):
        User = get_user_model()
        self.rider = User.objects.create_user(username="rider_fuel_view", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.rider, defaults={"role": UserProfile.Role.RIDER}
        )
        self.province = Province.objects.create(name="PFuelV")
        self.district = District.objects.create(name="DFuelV", province=self.province)
        RiderProfile.objects.get_or_create(
            user=self.rider,
            defaults={"province": self.province, "district": self.district},
        )
        self.week = date(2026, 8, 3)
        self.report = RiderWeeklyReport.objects.create(
            rider=self.rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
        )
        self.url = reverse("operations:rider_week_fuel")

    def _post(self, data):
        self.client.get(self.url)
        token = self.client.cookies.get("csrftoken")
        if token:
            data = {**data, "csrfmiddlewaretoken": token.value}
        return self.client.post(self.url, data=data)

    def test_post_saves_rider_week_fuel_summary(self):
        self.client.force_login(self.rider)
        response = self._post(
            {
                "week": self.week.isoformat(),
                "pc_fuel_allocated_total": "25",
                "pc_fuel_used_total": "10",
            },
        )
        self.assertEqual(response.status_code, 302)
        row = RiderWeekFuelSummary.objects.get(rider=self.rider, week_start=self.week)
        self.assertEqual(row.fuel_allocated, Decimal("25"))
        self.assertEqual(row.fuel_used, Decimal("10"))
        self.assertEqual(row.distance_travelled, Decimal("0"))
        self.assertEqual(self.report.trip_entries.count(), 0)

    def test_post_saves_without_any_weekly_report(self):
        User = get_user_model()
        solo = User.objects.create_user(username="rider_fuel_solo", password="pass123")
        UserProfile.objects.update_or_create(user=solo, defaults={"role": UserProfile.Role.RIDER})
        prov = Province.objects.create(name="PSolo")
        d = District.objects.create(name="DSolo", province=prov)
        RiderProfile.objects.get_or_create(
            user=solo,
            defaults={"province": prov, "district": d},
        )
        week = date(2026, 10, 5)
        self.client.force_login(solo)
        response = self._post(
            {
                "week": week.isoformat(),
                "pc_fuel_allocated_total": "11",
                "pc_fuel_used_total": "4",
            },
        )
        self.assertEqual(response.status_code, 302)
        row = RiderWeekFuelSummary.objects.get(rider=solo, week_start=week)
        self.assertEqual(row.fuel_allocated, Decimal("11"))
        self.assertFalse(RiderWeeklyReport.objects.filter(rider=solo, week_start=week).exists())

    def test_post_rejects_used_over_allocated(self):
        self.client.force_login(self.rider)
        response = self._post(
            {
                "week": self.week.isoformat(),
                "pc_fuel_allocated_total": "5",
                "pc_fuel_used_total": "6",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cannot exceed")
