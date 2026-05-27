import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from operations.models import (
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    SampleRejection,
    UserProfile,
)
from operations.services.sync_payload import build_report_sync_payload, report_sync_envelope
from operations.services.sync_service import apply_sync_batch

User = get_user_model()


@override_settings(OPS_SYNC_MODE="jwt", OPS_REMOTE_API_BASE="https://example.test")
class SyncPayloadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="rider1", password="pass")
        UserProfile.objects.update_or_create(
            user=self.user, defaults={"role": UserProfile.Role.RIDER}
        )
        RiderProfile.objects.get_or_create(user=self.user)
        self.report = RiderWeeklyReport.objects.create(
            rider=self.user,
            week_start="2026-04-06",
            client_uuid=uuid.uuid4(),
            title="Test",
            samples_collected=0,
        )
        RiderTripEntry.objects.create(
            report=self.report,
            sequence=1,
            vl_blood_plasma=2,
        )
        SampleRejection.objects.create(
            report=self.report,
            sample_type="vl_plasma",
            rejected_total=1,
            rejected_other=1,
            order=0,
        )

    def test_build_report_sync_payload_includes_children(self):
        payload = build_report_sync_payload(self.report)
        self.assertEqual(payload["week_start"], "2026-04-06")
        self.assertEqual(len(payload["trip_rows"]), 1)
        self.assertEqual(payload["trip_rows"][0]["vl_blood_plasma"], 2)
        self.assertEqual(len(payload["rejections"]), 1)
        self.assertEqual(payload["rejections"][0]["rejected_total"], 1)

    def test_report_sync_envelope(self):
        env = report_sync_envelope(self.report)
        self.assertEqual(env["idempotency_key"], str(self.report.client_uuid))
        self.assertIn("trip_rows", env["payload"])

    def test_apply_sync_batch_accepts_payload(self):
        env = report_sync_envelope(self.report)
        # Trip in setUp has specimens but no route/facilities; omit trips for batch apply test.
        env["payload"]["trip_rows"] = []
        env["payload"]["rejections"] = []
        out = apply_sync_batch(
            self.user,
            [
                {
                    "op": "upsert_report",
                    "idempotency_key": env["idempotency_key"],
                    "payload": env["payload"],
                }
            ],
        )
        self.assertTrue(out["ok"])
        self.assertTrue(out["results"][0]["ok"], out["results"][0].get("error"))

    def test_sync_payload_view(self):
        self.client.force_login(self.user)
        url = reverse("operations:report_sync_payload", kwargs={"pk": self.report.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["idempotency_key"], str(self.report.client_uuid))
        self.assertEqual(len(data["payload"]["trip_rows"]), 1)


class RiderHealthApiTests(TestCase):
    def test_health_endpoint(self):
        client = APIClient()
        res = client.get("/api/rider/health/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"ok": True})

    def test_health_cors_for_embedded_webview(self):
        client = APIClient(HTTP_ORIGIN="http://127.0.0.1:8765")
        res = client.get("/api/rider/health/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["Access-Control-Allow-Origin"], "http://127.0.0.1:8765")
