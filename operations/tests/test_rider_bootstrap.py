from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from operations.models import District, Facility, Province, RiderProfile, UserProfile
from operations.services.embedded_bootstrap_import import apply_embedded_bootstrap

User = get_user_model()


class RiderBootstrapFacilitiesTests(TestCase):
    def setUp(self):
        self.harare = Province.objects.create(name="Harare", code="")
        self.mash_east = Province.objects.create(name="Mashonaland East", code="")
        self.harare_dist = District.objects.create(province=self.harare, name="Harare", support_type="")
        self.mudzi = District.objects.create(province=self.mash_east, name="Mudzi", support_type="")
        self.harare_clinic = Facility.objects.create(
            name="Harare Clinic", district=self.harare_dist, kind=Facility.Kind.CLINIC
        )
        self.chingwena = Facility.objects.create(
            name="Chingwena Clinic", district=self.mudzi, kind=Facility.Kind.HUB
        )

        self.sync_user = User.objects.create_user(username="emmanuel_takawengwa", password="x")
        UserProfile.objects.update_or_create(
            user=self.sync_user, defaults={"role": UserProfile.Role.RIDER}
        )
        RiderProfile.objects.update_or_create(
            user=self.sync_user,
            defaults={"district": self.harare_dist, "province": self.harare},
        )

        self.normal_user = User.objects.create_user(username="gibson_chikwizo", password="x")
        UserProfile.objects.update_or_create(
            user=self.normal_user, defaults={"role": UserProfile.Role.RIDER}
        )
        RiderProfile.objects.update_or_create(
            user=self.normal_user,
            defaults={"district": self.mudzi, "province": self.mash_east},
        )

        self.client = APIClient()

    def _names(self, rows):
        return {row["name"] for row in rows}

    def test_normal_rider_bootstrap_stays_province_scoped(self):
        self.client.force_authenticate(user=self.normal_user)
        res = self.client.get("/api/rider/bootstrap/")
        self.assertEqual(res.status_code, 200, res.content)
        body = res.json()
        self.assertEqual(body.get("bootstrap_scope"), "province")
        self.assertIn("Chingwena Clinic", self._names(body["facilities_province"]))
        self.assertNotIn("Harare Clinic", self._names(body["facilities_province"]))
        self.assertNotIn("Harare Clinic", self._names(body["facilities_district"]))

    @override_settings(OPS_MOBILE_SYNC_USERNAMES=frozenset({"emmanuel_takawengwa"}))
    def test_sync_user_bootstrap_includes_all_facilities(self):
        self.client.force_authenticate(user=self.sync_user)
        res = self.client.get("/api/rider/bootstrap/")
        self.assertEqual(res.status_code, 200, res.content)
        body = res.json()
        self.assertEqual(body.get("bootstrap_scope"), "all")
        self.assertIn("Chingwena Clinic", self._names(body["facilities_province"]))
        self.assertIn("Harare Clinic", self._names(body["facilities_province"]))
        self.assertIn("Chingwena Clinic", self._names(body["hubs"]))
        chingwena = next(r for r in body["facilities_province"] if r["name"] == "Chingwena Clinic")
        self.assertEqual(chingwena["district_id"], self.mudzi.id)
        self.assertEqual(chingwena["province_id"], self.mash_east.id)
        self.assertEqual(chingwena["district_name"], "Mudzi")


class EmbeddedBootstrapImportGeoTests(TestCase):
    def test_import_uses_facility_province_id_for_new_districts(self):
        harare = Province.objects.create(id=6, name="Harare", code="")
        District.objects.create(id=3, province=harare, name="Harare", support_type="")
        stats = apply_embedded_bootstrap(
            {
                "profile": {
                    "province": {"id": 6, "name": "Harare"},
                    "district": {"id": 3, "name": "Harare", "province_id": 6},
                },
                "bootstrap": {
                    "province_id": 6,
                    "district_id": 3,
                    "facilities_province": [
                        {
                            "id": 9001,
                            "name": "Chingwena Clinic",
                            "district_id": 22,
                            "district_name": "Mudzi",
                            "province_id": 5,
                            "province_name": "Mashonaland East",
                            "kind": Facility.Kind.HUB,
                            "support_type": "",
                        }
                    ],
                    "facilities_district": [],
                    "hubs": [],
                    "labs": [],
                    "bikes": [],
                },
            }
        )
        self.assertEqual(stats["facilities"], 1)
        mudzi = District.objects.get(pk=22)
        self.assertEqual(mudzi.name, "Mudzi")
        self.assertEqual(mudzi.province_id, 5)
        self.assertEqual(Province.objects.get(pk=5).name, "Mashonaland East")
        fac = Facility.objects.get(pk=9001)
        self.assertEqual(fac.name, "Chingwena Clinic")
        self.assertEqual(fac.district_id, 22)
        self.assertEqual(fac.kind, Facility.Kind.HUB)
