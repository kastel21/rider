"""M&E export: one aggregated row per rider name + bike registration per week."""

from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from operations.models import (
    Bike,
    District,
    Province,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    TripRouteKind,
    TripTransportKind,
    TripVisitPurpose,
    UserProfile,
)
from operations.services.me_report_service import build_me_report_table_for_week


class MeReportWeekAggregateTests(TestCase):
    databases = {"default"}

    def setUp(self):
        User = get_user_model()
        self.rider_user = User.objects.create_user(
            username="david_sango",
            first_name="David",
            last_name="Sango",
        )
        UserProfile.objects.update_or_create(
            user=self.rider_user, defaults={"role": UserProfile.Role.RIDER}
        )
        self.province = Province.objects.create(name="Manicaland")
        self.district = District.objects.create(name="Mutasa", province=self.province)
        self.bike1 = Bike.objects.create(code="AER1429", district=self.district)
        self.bike2 = Bike.objects.create(code="AER4351", district=self.district)
        RiderProfile.objects.update_or_create(
            user=self.rider_user,
            defaults={
                "province": self.province,
                "district": self.district,
                "bike": self.bike1,
                "support_type": "DSD",
            },
        )
        self.week = date(2026, 5, 12)

    def test_two_bikes_two_rows(self):
        r1 = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=self.week,
            bike=self.bike1,
            scheduled_visits=1,
        )
        r2 = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=self.week,
            bike=self.bike2,
            scheduled_visits=23,
        )
        RiderTripEntry.objects.create(
            report=r1,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SAMPLE_COLLECTION,
            route_kind=TripRouteKind.FACILITY_TO_LAB,
            vl_blood_plasma=10,
            vl_dbs=20,
        )
        RiderTripEntry.objects.create(
            report=r2,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SAMPLE_COLLECTION,
            route_kind=TripRouteKind.FACILITY_TO_LAB,
            vl_blood_plasma=30,
            vl_dbs=10,
            sputum=20,
        )

        table = build_me_report_table_for_week(
            week_start=self.week,
            role=UserProfile.Role.RIDER,
        )
        self.assertEqual(table["row_count"], 2)
        by_bike = {}
        for row in table["rows"]:
            by_key = {table["columns"][i]["key"]: row[i]["text"] for i in range(len(row))}
            by_bike[by_key["bike_reg"]] = by_key
        self.assertEqual(by_bike["AER1429"]["name_of_rider"], "David Sango")
        self.assertEqual(by_bike["AER1429"]["sp_vl_bp"], "10")
        self.assertEqual(by_bike["AER1429"]["sp_vl_dbs"], "20")
        self.assertEqual(by_bike["AER1429"]["scheduled_visits"], "1")
        self.assertEqual(by_bike["AER4351"]["sp_vl_bp"], "30")
        self.assertEqual(by_bike["AER4351"]["sp_sputum"], "20")
        self.assertEqual(by_bike["AER4351"]["scheduled_visits"], "23")

    def test_same_bike_two_reports_one_row(self):
        r1 = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=self.week,
            bike=self.bike1,
            scheduled_visits=1,
        )
        r2 = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=self.week,
            bike=self.bike1,
            scheduled_visits=3,
        )
        RiderTripEntry.objects.create(
            report=r1,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SAMPLE_COLLECTION,
            route_kind=TripRouteKind.FACILITY_TO_LAB,
            vl_blood_plasma=10,
        )
        RiderTripEntry.objects.create(
            report=r2,
            sequence=1,
            transport_kind=TripTransportKind.LEGACY,
            visit_purpose=TripVisitPurpose.SAMPLE_COLLECTION,
            route_kind=TripRouteKind.FACILITY_TO_LAB,
            vl_blood_plasma=100,
            fuel_allocated=Decimal("12"),
            fuel_used=Decimal("10"),
            distance_travelled=Decimal("23"),
        )

        table = build_me_report_table_for_week(
            week_start=self.week,
            role=UserProfile.Role.RIDER,
        )
        self.assertEqual(table["row_count"], 1)
        row = table["rows"][0]
        by_key = {table["columns"][i]["key"]: row[i]["text"] for i in range(len(row))}
        self.assertEqual(by_key["bike_reg"], "AER1429")
        self.assertEqual(by_key["sp_vl_bp"], "110")
        self.assertEqual(by_key["scheduled_visits"], "4")
        self.assertEqual(by_key["fuel_allocated"], "12")
        self.assertEqual(by_key["distance"], "23")
