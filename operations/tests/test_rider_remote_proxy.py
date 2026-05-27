from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from rest_framework.test import APIClient


@override_settings(
    OPS_RIDER_REMOTE_PROXY=True,
    OPS_REMOTE_API_BASE="https://example.com",
)
class RiderRemoteProxyTests(TestCase):
    def test_proxy_disabled_by_default(self):
        client = APIClient()
        with self.settings(OPS_RIDER_REMOTE_PROXY=False):
            res = client.get("/api/rider-remote/health/")
        self.assertEqual(res.status_code, 404)

    @patch("operations.api.remote_proxy_views.urllib.request.urlopen")
    def test_health_proxied(self, urlopen_mock):
        resp = MagicMock()
        resp.read.return_value = b'{"ok": true}'
        resp.status = 200
        resp.headers = {"Content-Type": "application/json"}
        urlopen_mock.return_value.__enter__.return_value = resp

        client = APIClient()
        res = client.get("/api/rider-remote/health/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"ok": True})
        called_url = urlopen_mock.call_args[0][0].full_url
        self.assertEqual(called_url, "https://example.com/api/rider/health/")

    def test_disallowed_path(self):
        client = APIClient()
        res = client.get("/api/rider-remote/mobile-user-export/")
        self.assertEqual(res.status_code, 403)
