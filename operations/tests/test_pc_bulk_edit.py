from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from operations.models import (
    District,
    PCProfile,
    Province,
    RiderProfile,
    RiderWeeklyReport,
    UserProfile,
    WeeklyRecordReviewed,
)


class PCBulkEditViewTests(TestCase):
    databases = {"default", "sqlite"}

    def setUp(self):
        User = get_user_model()
        self.pc_user = User.objects.create_user(username="pc_bulk", password="pass123")
        self.rider_user = User.objects.create_user(username="rider_bulk", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.pc_user, defaults={"role": UserProfile.Role.PC}
        )
        UserProfile.objects.update_or_create(
            user=self.rider_user, defaults={"role": UserProfile.Role.RIDER}
        )
        self.province = Province.objects.create(name="PBulk")
        self.district = District.objects.create(name="DBulk", province=self.province)
        pc_profile, _ = PCProfile.objects.get_or_create(user=self.pc_user)
        pc_profile.provinces.add(self.province)
        RiderProfile.objects.get_or_create(
            user=self.rider_user,
            defaults={"province": self.province, "district": self.district},
        )
        self.week = date(2026, 6, 1)
        self.report_one = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            samples_collected=0,
        )
        self.report_two = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
            samples_collected=0,
        )
        self.url = reverse(
            "operations:pc_reports_bulk_edit",
            kwargs={"rider_id": self.rider_user.id, "week_str": self.week.isoformat()},
        )

    def _save_payload(self):
        payload = {"action": "save_all"}
        for report in (self.report_one, self.report_two):
            rid = report.pk
            payload[f"report_{rid}-pc_notes"] = f"note-{rid}"
            payload[f"report_{rid}-scheduled_visits"] = "3"
            payload[f"pc_fuel_allocated_total_{rid}"] = "10"
            payload[f"pc_fuel_used_total_{rid}"] = "5"
            payload[f"pc_distance_travelled_total_{rid}"] = "20"

            # PC formset uses extra=0; these reports have no trip rows yet.
            payload[f"trips_{rid}-TOTAL_FORMS"] = "0"
            payload[f"trips_{rid}-INITIAL_FORMS"] = "0"
            payload[f"trips_{rid}-MIN_NUM_FORMS"] = "0"
            payload[f"trips_{rid}-MAX_NUM_FORMS"] = "1000"

            payload[f"rejections_{rid}-TOTAL_FORMS"] = "1"
            payload[f"rejections_{rid}-INITIAL_FORMS"] = "0"
            payload[f"rejections_{rid}-MIN_NUM_FORMS"] = "0"
            payload[f"rejections_{rid}-MAX_NUM_FORMS"] = "1000"
            payload[f"rejections_{rid}-0-sample_type"] = "vl_dbs"
            payload[f"rejections_{rid}-0-rejected_total"] = "0"
            payload[f"rejections_{rid}-0-rejected_too_old"] = "0"
            payload[f"rejections_{rid}-0-rejected_patient_info_mismatch"] = "0"
            payload[f"rejections_{rid}-0-rejected_request_form_missing"] = "0"
            payload[f"rejections_{rid}-0-rejected_sample_missing"] = "0"
            payload[f"rejections_{rid}-0-rejected_other"] = "0"
            payload[f"rejections_{rid}-0-order"] = "0"
        return payload

    def test_bulk_get_lists_all_records(self):
        self.client.force_login(self.pc_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Record #{self.report_one.pk}")
        self.assertContains(response, f"Record #{self.report_two.pk}")

    def test_bulk_save_all_updates_each_report(self):
        self.client.force_login(self.pc_user)
        response = self.client.post(self.url, data=self._save_payload(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.report_one.refresh_from_db()
        self.report_two.refresh_from_db()
        self.assertEqual(self.report_one.pc_notes, f"note-{self.report_one.pk}")
        self.assertEqual(self.report_two.pc_notes, f"note-{self.report_two.pk}")
        self.assertEqual(self.report_one.scheduled_visits, 3)
        self.assertEqual(self.report_two.scheduled_visits, 3)

    def test_bulk_review_all_approves_and_snapshots_each(self):
        self.client.force_login(self.pc_user)
        response = self.client.post(self.url, data={"action": "review_all"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.report_one.refresh_from_db()
        self.report_two.refresh_from_db()
        self.assertEqual(self.report_one.status, RiderWeeklyReport.Status.APPROVED)
        self.assertEqual(self.report_two.status, RiderWeeklyReport.Status.APPROVED)
        self.assertEqual(
            WeeklyRecordReviewed.objects.filter(source_report_id__in=[self.report_one.pk, self.report_two.pk]).count(),
            2,
        )
