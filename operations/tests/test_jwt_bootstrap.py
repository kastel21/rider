from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from operations.models import District, Province, RiderProfile, UserProfile

User = get_user_model()


@override_settings(
    OPS_SYNC_MODE="jwt",
    OPS_REMOTE_API_BASE="https://example.com",
    OPS_ALLOW_LOCAL_JWT_MINT=True,
    SIMPLE_JWT={"SIGNING_KEY": "test-signing-key-for-mint"},
)
class RiderJwtBootstrapTests(TestCase):
    def setUp(self):
        prov = Province.objects.create(name="P", code="")
        dist = District.objects.create(province=prov, name="D", support_type="")
        self.user = User.objects.create_user(username="rider1", password="x")
        UserProfile.objects.update_or_create(
            user=self.user,
            defaults={"role": UserProfile.Role.RIDER},
        )
        RiderProfile.objects.update_or_create(user=self.user, defaults={"district": dist})
        self.client = APIClient()

    def test_bootstrap_requires_login(self):
        res = self.client.get("/api/rider/jwt-bootstrap/")
        self.assertIn(res.status_code, (302, 403))

    def test_bootstrap_mints_token(self):
        self.client.login(username="rider1", password="x")
        res = self.client.get("/api/rider/jwt-bootstrap/")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json().get("access"))
