from django.test import TestCase
from django.utils import timezone

from operations.models import AccessibleApp
from operations.services.accessible_apps_service import allowed_package_names, upsert_reported_user_apps


class AccessibleAppsServiceTests(TestCase):
    def test_upsert_skips_system_apps_in_admin_catalog(self):
        upsert_reported_user_apps(
            [
                {"package": "com.whatsapp", "label": "WhatsApp"},
                {"package": "com.android.settings", "label": "Settings", "is_system": True},
            ]
        )
        self.assertEqual(AccessibleApp.objects.count(), 2)
        self.assertFalse(
            AccessibleApp.objects.filter(package_name="com.android.settings").first().is_allowed
        )

    def test_allowed_package_names_excludes_system(self):
        AccessibleApp.objects.create(
            package_name="com.whatsapp",
            label="WhatsApp",
            is_allowed=True,
            last_seen_at=timezone.now(),
        )
        AccessibleApp.objects.create(
            package_name="com.android.settings",
            label="Settings",
            is_system=True,
            is_allowed=True,
            last_seen_at=timezone.now(),
        )
        self.assertEqual(allowed_package_names(), ["com.whatsapp"])
