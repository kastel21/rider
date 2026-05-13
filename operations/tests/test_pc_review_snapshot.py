from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from operations.models import (
    District,
    Facility,
    PCProfile,
    Province,
    RiderWeeklyReport,
    RiderProfile,
    UserProfile,
    WeeklyRecordReviewed,
)
from operations.services import report_service
from operations.services.weekly_review_service import create_weekly_review_record
from operations.services.weekly_review_service import build_weekly_review_snapshot


class PCReviewSnapshotFlowTests(TestCase):
    databases = {"default", "sqlite"}

    def setUp(self):
        User = get_user_model()
        self.pc_user = User.objects.create_user(username="pc1", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.pc_user,
            defaults={"role": UserProfile.Role.PC},
        )

        self.rider_user = User.objects.create_user(username="rider1", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.rider_user,
            defaults={"role": UserProfile.Role.RIDER},
        )

        self.province = Province.objects.create(name="P1")
        self.district = District.objects.create(name="D1", province=self.province)
        pc_profile, _ = PCProfile.objects.get_or_create(user=self.pc_user)
        pc_profile.provinces.add(self.province)
        RiderProfile.objects.get_or_create(
            user=self.rider_user,
            defaults={"province": self.province, "district": self.district},
        )
        self.origin = Facility.objects.create(name="Origin", district=self.district, kind=Facility.Kind.CLINIC)
        self.destination = Facility.objects.create(name="Dest", district=self.district, kind=Facility.Kind.LAB)

        self.report = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=date(2026, 5, 4),
            status=RiderWeeklyReport.Status.DRAFT,
            samples_collected=3,
        )

    def test_create_weekly_review_record_persists_snapshot(self):
        record = create_weekly_review_record(source_report=self.report, reviewer=self.pc_user)

        self.assertEqual(WeeklyRecordReviewed.objects.count(), 1)
        self.assertEqual(record.source_report_id, self.report.id)
        self.assertEqual(record.rider_id, self.rider_user.id)
        self.assertEqual(record.reviewed_by_id, self.pc_user.id)
        self.assertEqual(record.week_start, self.report.week_start)
        self.assertIn("reports", record.snapshot)
        self.assertGreaterEqual(len(record.snapshot["reports"]), 1)

    def test_complete_review_keeps_existing_approve_behavior(self):
        report_service.complete_review(
            self.report,
            self.pc_user,
            approved=True,
            pc_notes="ok",
        )
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, RiderWeeklyReport.Status.APPROVED)
        self.assertEqual(WeeklyRecordReviewed.objects.count(), 0)

    def test_snapshot_builder_returns_single_week_structure(self):
        payload = build_weekly_review_snapshot(rider=self.rider_user, week_start=self.report.week_start)

        self.assertEqual(payload["rider_id"], self.rider_user.id)
        self.assertEqual(payload["week_start"], "2026-05-04")
        self.assertEqual(payload["report_count"], 1)
        self.assertIn("totals", payload)
        self.assertIn("reports", payload)
