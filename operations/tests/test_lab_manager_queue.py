from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from operations.models import (
    District,
    LabManagerProfile,
    PCProfile,
    Province,
    RiderProfile,
    RiderWeeklyReport,
    UserProfile,
)
from operations.permissions import can_edit_report_as_rider


def _operations_test_databases():
    names = {"default"}
    if "sqlite" in settings.DATABASES:
        names.add("sqlite")
    return names


class LabManagerQueueTests(TestCase):
    databases = _operations_test_databases()

    def setUp(self):
        User = get_user_model()
        self.manager = User.objects.create_user(username="lab_mgr", password="pass123")
        self.other_manager = User.objects.create_user(username="lab_other", password="pass123")
        self.pc = User.objects.create_user(username="pc_lab", password="pass123")
        self.rider = User.objects.create_user(
            username="rider_lab", password="pass123", first_name="Ada", last_name="Rider"
        )
        self.other_rider = User.objects.create_user(username="rider_other", password="pass123")
        for user, role in (
            (self.manager, UserProfile.Role.LAB_MANAGER),
            (self.other_manager, UserProfile.Role.LAB_MANAGER),
            (self.pc, UserProfile.Role.PC),
            (self.rider, UserProfile.Role.RIDER),
            (self.other_rider, UserProfile.Role.RIDER),
        ):
            UserProfile.objects.update_or_create(user=user, defaults={"role": role})
        self.province = Province.objects.create(name="LabProv")
        self.district = District.objects.create(name="LabDist", province=self.province)
        self.other_district = District.objects.create(name="OtherDist", province=self.province)
        LabManagerProfile.objects.create(user=self.manager, district=self.district)
        LabManagerProfile.objects.create(user=self.other_manager, district=self.other_district)
        pc_profile, _ = PCProfile.objects.get_or_create(user=self.pc)
        pc_profile.provinces.add(self.province)
        RiderProfile.objects.create(user=self.rider, province=self.province, district=self.district)
        RiderProfile.objects.create(
            user=self.other_rider, province=self.province, district=self.other_district
        )
        self.week = date(2026, 6, 1)
        self.report = RiderWeeklyReport.objects.create(
            rider=self.rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.SUBMITTED,
            submitted_at=timezone.now(),
        )
        self.other_report = RiderWeeklyReport.objects.create(
            rider=self.other_rider,
            week_start=self.week,
            status=RiderWeeklyReport.Status.SUBMITTED,
            submitted_at=timezone.now(),
        )
        self.queue_url = reverse("operations:lab_manager_queue") + f"?week={self.week.isoformat()}"
        self.pc_url = reverse("operations:pc_reports") + f"?week={self.week.isoformat()}"

    def test_waiting_report_stays_with_manager_and_is_visible_to_pc(self):
        self.client.force_login(self.manager)
        response = self.client.get(self.queue_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ada Rider")
        self.assertNotContains(response, "rider_other")

        self.client.force_login(self.pc)
        pc_response = self.client.get(self.pc_url)
        self.assertContains(pc_response, "Ada Rider")
        self.assertContains(pc_response, "Not yet approved")
        self.assertFalse(can_edit_report_as_rider(self.rider, self.report))

    def test_approve_locks_edits_and_releases_to_pc(self):
        self.client.force_login(self.manager)
        response = self.client.post(
            self.queue_url,
            {"action": "approve", "rider_id": self.rider.id, "week": self.week.isoformat()},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.report.refresh_from_db()
        self.assertIsNotNone(self.report.lab_cleared_at)
        self.assertEqual(self.report.lab_cleared_by_id, self.manager.id)
        self.assertEqual(self.report.status, RiderWeeklyReport.Status.SUBMITTED)
        self.assertFalse(can_edit_report_as_rider(self.rider, self.report))

        self.client.force_login(self.pc)
        pc_response = self.client.get(self.pc_url)
        self.assertContains(pc_response, "Ada Rider")

    def test_send_back_requires_a_reason_and_stays_editable(self):
        self.client.force_login(self.manager)
        self.client.post(
            self.queue_url,
            {
                "action": "send_back",
                "rider_id": self.rider.id,
                "week": self.week.isoformat(),
                "lab_notes": "   ",
            },
            follow=True,
        )
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, RiderWeeklyReport.Status.SUBMITTED)

        self.client.post(
            self.queue_url,
            {
                "action": "send_back",
                "rider_id": self.rider.id,
                "week": self.week.isoformat(),
                "lab_notes": "Sample counts do not match the log.",
            },
            follow=True,
        )
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, RiderWeeklyReport.Status.REJECTED)
        self.assertEqual(self.report.lab_notes, "Sample counts do not match the log.")
        self.assertIn("Lab manager: Sample counts do not match the log.", self.report.notes)
        self.assertIsNone(self.report.lab_cleared_at)
        self.assertTrue(can_edit_report_as_rider(self.rider, self.report))

        self.client.force_login(self.pc)
        pc_response = self.client.get(self.pc_url)
        self.assertNotContains(pc_response, "Ada Rider")

    def test_resend_returns_the_report_to_the_manager_and_stays_editable(self):
        from operations.services import report_service

        report_service.send_report_back_to_rider(
            self.report, self.manager, "Fix the visit count."
        )
        self.client.force_login(self.rider)
        response = self.client.post(
            reverse("operations:report_submit", kwargs={"pk": self.report.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, RiderWeeklyReport.Status.SUBMITTED)
        self.assertIsNone(self.report.lab_cleared_at)
        self.assertEqual(self.report.lab_notes, "")
        self.assertTrue(can_edit_report_as_rider(self.rider, self.report))

        self.client.force_login(self.manager)
        queue = self.client.get(self.queue_url)
        self.assertContains(queue, "Ada Rider")

        self.client.force_login(self.pc)
        self.assertContains(self.client.get(self.pc_url), "Ada Rider")

    def test_other_district_manager_cannot_approve(self):
        self.client.force_login(self.other_manager)
        self.client.post(
            self.queue_url,
            {"action": "approve", "rider_id": self.rider.id, "week": self.week.isoformat()},
            follow=True,
        )
        self.report.refresh_from_db()
        self.assertIsNone(self.report.lab_cleared_at)
