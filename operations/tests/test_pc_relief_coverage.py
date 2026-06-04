from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from operations.models import (
    District,
    PCProfile,
    Province,
    RiderProfile,
    RiderWeekReliefCoverage,
    RiderWeeklyReport,
    UserProfile,
)
from operations.services.me_report_resolvers import _relief_rider_name
from operations.services.weekly_review_service import build_weekly_review_snapshot, create_weekly_review_record


def _relief_test_databases():
    names = {"default"}
    if "sqlite" in settings.DATABASES:
        names.add("sqlite")
    return names


class PCReliefCoverageTests(TestCase):
    databases = _relief_test_databases()

    def setUp(self):
        User = get_user_model()
        self.pc_user = User.objects.create_user(username="pc_relief", password="pass123")
        self.relief_user = User.objects.create_user(
            username="relief_submitter",
            password="pass123",
            first_name="Relief",
            last_name="Submitter",
        )
        self.absent_user = User.objects.create_user(
            username="absent_regular",
            password="pass123",
            first_name="Regular",
            last_name="Absent",
        )
        for u, role in (
            (self.pc_user, UserProfile.Role.PC),
            (self.relief_user, UserProfile.Role.RIDER),
            (self.absent_user, UserProfile.Role.RIDER),
        ):
            UserProfile.objects.update_or_create(user=u, defaults={"role": role})
        self.province = Province.objects.create(name="PRelief")
        self.district = District.objects.create(name="DRelief", province=self.province)
        pc_profile, _ = PCProfile.objects.get_or_create(user=self.pc_user)
        pc_profile.provinces.add(self.province)
        for u in (self.relief_user, self.absent_user):
            RiderProfile.objects.get_or_create(
                user=u,
                defaults={"province": self.province, "district": self.district},
            )
        self.week = date(2026, 6, 8)
        self.report = RiderWeeklyReport.objects.create(
            rider=self.relief_user,
            week_start=self.week,
            status=RiderWeeklyReport.Status.SUBMITTED,
        )
        RiderWeekReliefCoverage.objects.create(
            rider=self.relief_user,
            week_start=self.week,
            is_relief_submission=True,
            relieved_rider=self.absent_user,
            relief_reason="special",
        )

    def test_snapshot_includes_relief_coverage(self):
        payload = build_weekly_review_snapshot(rider=self.relief_user, week_start=self.week)
        relief = payload["relief_coverage"]
        self.assertTrue(relief["is_relief_submission"])
        self.assertEqual(relief["relieved_rider_id"], self.absent_user.pk)
        self.assertEqual(relief["relieved_rider_name"], "Regular Absent")
        self.assertEqual(relief["relief_reason"], "special")
        self.assertEqual(relief["relief_reason_display"], "Special leave")

    def test_review_record_snapshot_has_relief_coverage(self):
        record = create_weekly_review_record(source_report=self.report, reviewer=self.pc_user)
        self.assertIn("relief_coverage", record.snapshot)
        self.assertTrue(record.snapshot["relief_coverage"]["is_relief_submission"])

    def test_me_resolver_returns_relieved_rider_name(self):
        name = _relief_rider_name(self.report)
        self.assertEqual(name, "Regular Absent")

    def test_me_resolver_falls_back_to_extra_data(self):
        RiderWeekReliefCoverage.objects.filter(
            rider=self.relief_user, week_start=self.week
        ).delete()
        self.report.extra_data = {"relief_rider_name": "Legacy Name"}
        self.report.save(update_fields=["extra_data"])
        self.assertEqual(_relief_rider_name(self.report), "Legacy Name")
