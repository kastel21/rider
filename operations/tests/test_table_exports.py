"""CSV / Excel export endpoints for reporting tables."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from operations.models import UserProfile


class TableExportViewTests(TestCase):
    databases = {"default"}

    def setUp(self):
        User = get_user_model()
        self.me_user = User.objects.create_user(username="me_export", password="secret123")
        UserProfile.objects.update_or_create(
            user=self.me_user, defaults={"role": UserProfile.Role.ME}
        )
        self.client = Client()
        self.client.login(username="me_export", password="secret123")
        self.week = date(2026, 5, 12)

    def test_weekly_report_rider_csv(self):
        resp = self.client.get(
            reverse("operations:weekly_report_riders_export_csv"),
            {"week": self.week.isoformat()},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/csv", resp["Content-Type"])
        self.assertIn("attachment", resp.get("Content-Disposition", ""))

    def test_overview_xlsx(self):
        resp = self.client.get(
            reverse("operations:me_metrics_overview_export_xlsx"),
            {"weeks": "1"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("spreadsheetml", resp["Content-Type"])
