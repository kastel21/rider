import os
import tempfile
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from operations.models import District, Province, RiderAppRelease, RiderProfile, RiderRemoteConfig, UserProfile

User = get_user_model()


class AppUpdateTests(TestCase):
    def setUp(self):
        self._media = tempfile.TemporaryDirectory()
        self._media_override = override_settings(MEDIA_ROOT=self._media.name)
        self._media_override.enable()
        prov = Province.objects.create(name="P", code="")
        dist = District.objects.create(province=prov, name="D", support_type="")
        self.user = User.objects.create_user(username="rider1", password="secret")
        UserProfile.objects.update_or_create(
            user=self.user,
            defaults={"role": UserProfile.Role.RIDER},
        )
        RiderProfile.objects.update_or_create(user=self.user, defaults={"district": dist})
        self.client = APIClient()

    def tearDown(self):
        self._media_override.disable()
        self._media.cleanup()

    def _require_version(self, minimum=3):
        RiderRemoteConfig.objects.update_or_create(
            pk=1,
            defaults={
                "update_required": True,
                "min_version_code": minimum,
                "latest_app_version": "1.3",
            },
        )

    def _upload(self, application_id="com.ecollect.app.bit64", version_code=3, payload=b"apk-bytes"):
        return RiderAppRelease.objects.create(
            application_id=application_id,
            version_code=version_code,
            version_name="1.3",
            apk=SimpleUploadedFile("app.apk", payload, content_type="application/vnd.android.package-archive"),
        )

    def test_update_check_requires_upgrade_when_below_minimum(self):
        self._require_version(3)
        self._upload()
        res = self.client.get(
            "/api/rider/app-update/",
            {"version_code": "2", "application_id": "com.ecollect.app.bit64"},
        )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertTrue(body["update_required"])
        self.assertTrue(body["update_available"])
        self.assertEqual(body["min_version_code"], 3)
        self.assertIn("com.ecollect.app.bit64", body["download_path"])

    def test_update_check_allows_current_build(self):
        self._require_version(3)
        self._upload()
        res = self.client.get(
            "/api/rider/app-update/",
            {"version_code": "3", "application_id": "com.ecollect.app.bit64"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json()["update_required"])
        self.assertFalse(res.json()["update_available"])
        self.assertEqual(res.json()["download_path"], "")

    def test_newer_apk_is_offered_before_it_is_required(self):
        self._upload()
        res = self.client.get(
            "/api/rider/app-update/",
            {"version_code": "2", "application_id": "com.ecollect.app.bit64"},
        )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertFalse(body["update_required"])
        self.assertTrue(body["update_available"])
        self.assertIn("com.ecollect.app.bit64", body["download_path"])

    def test_download_serves_apk(self):
        self._require_version(3)
        self._upload(payload=b"not-a-real-apk")
        res = self.client.get(
            "/api/rider/app-download/",
            {"application_id": "com.ecollect.app.bit64"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("application/vnd.android.package-archive", res["Content-Type"])
        self.assertEqual(b"".join(res.streaming_content), b"not-a-real-apk")

    def test_download_rejects_bad_application_id(self):
        res = self.client.get("/api/rider/app-download/", {"application_id": "../secret"})
        self.assertEqual(res.status_code, 400)

    def test_browser_page_lists_release(self):
        self._upload()
        res = self.client.get("/app/update/")
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "E-Collect (64-bit)")
        self.assertContains(res, "com.ecollect.app.bit64")

    def test_legacy_android_login_blocked(self):
        self._require_version(3)
        res = self.client.post(
            "/api/rider/login/",
            {"username": "rider1", "password": "secret"},
            format="json",
            HTTP_USER_AGENT="okhttp/4.12.0",
        )
        self.assertEqual(res.status_code, 426)
        self.assertEqual(res.json()["code"], "update_required")
        self.assertIn("/app/update/", res.json()["error"])

    def test_current_android_login_allowed(self):
        self._require_version(3)
        res = self.client.post(
            "/api/rider/login/",
            {"username": "rider1", "password": "secret"},
            format="json",
            HTTP_USER_AGENT="okhttp/4.12.0",
            HTTP_X_APP_VERSION_CODE="3",
            HTTP_X_APP_ID="com.ecollect.app.bit64",
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json().get("access"))

    def test_browser_login_not_blocked(self):
        self._require_version(3)
        res = self.client.post(
            "/api/rider/login/",
            {"username": "rider1", "password": "secret"},
            format="json",
            HTTP_USER_AGENT="Mozilla/5.0",
        )
        self.assertEqual(res.status_code, 200)

    def test_health_stays_open_for_old_app(self):
        self._require_version(3)
        res = self.client.get("/api/rider/health/", HTTP_USER_AGENT="okhttp/4.12.0")
        self.assertEqual(res.status_code, 200)

    def test_legacy_sync_blocked_until_flag_is_on(self):
        res = self.client.post(
            "/api/rider/login/",
            {"username": "rider1", "password": "secret"},
            format="json",
            HTTP_USER_AGENT="okhttp/4.12.0",
        )
        self.assertEqual(res.status_code, 200)

    def test_embedded_server_does_not_enforce(self):
        self._require_version(3)
        with override_settings(OPS_ENFORCE_APP_VERSION=False):
            res = self.client.post(
                "/api/rider/login/",
                {"username": "rider1", "password": "secret"},
                format="json",
                HTTP_USER_AGENT="okhttp/4.12.0",
            )
        self.assertEqual(res.status_code, 200)

    @patch("operations.api.remote_proxy_views.urllib.request.urlopen")
    def test_proxy_sends_installed_version(self, urlopen_mock):
        resp = MagicMock()
        resp.read.return_value = b'{"ok": true}'
        resp.status = 200
        resp.headers = {"Content-Type": "application/json"}
        urlopen_mock.return_value.__enter__.return_value = resp
        with override_settings(OPS_RIDER_REMOTE_PROXY=True, OPS_REMOTE_API_BASE="https://example.com"):
            with patch.dict(os.environ, {"OPS_APP_VERSION_CODE": "3", "OPS_APP_ID": "com.ecollect.app.bit64"}):
                res = self.client.get("/api/rider-remote/health/")
        self.assertEqual(res.status_code, 200)
        forwarded = urlopen_mock.call_args[0][0]
        self.assertEqual(forwarded.get_header("X-app-version-code"), "3")
        self.assertEqual(forwarded.get_header("X-app-id"), "com.ecollect.app.bit64")
