from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from operations.geo_names import canon_district_name
from operations.models import (
    District,
    Facility,
    PCDistrictWeeklyTransportStat,
    Province,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    UserProfile,
)
from operations.services.district_merge import get_or_create_district, merge_aliased_districts

User = get_user_model()


class DistrictAliasTests(TestCase):
    databases = {"default"}

    def setUp(self):
        self.province = Province.objects.create(name="Mashonaland East")

    def test_ump_canonical_name(self):
        self.assertEqual(canon_district_name("UMP"), "Uzumba Maramba Pfungwe")
        self.assertEqual(canon_district_name("ump"), "Uzumba Maramba Pfungwe")

    def test_spelling_aliases(self):
        self.assertEqual(canon_district_name("Murehwa"), "Murewa")
        self.assertEqual(canon_district_name("Mt. Darwin"), "Mount Darwin")
        self.assertEqual(canon_district_name("mt darwin"), "Mount Darwin")
        self.assertEqual(canon_district_name("Kadoma"), "Kadoma Sanyati")

    def test_get_or_create_reuses_ump_row_and_renames(self):
        ump = District.objects.create(province=self.province, name="UMP", support_type="TA-SDI")
        district, created = get_or_create_district(self.province, "Uzumba Maramba Pfungwe")
        self.assertFalse(created)
        self.assertEqual(district.pk, ump.pk)
        ump.refresh_from_db()
        self.assertEqual(ump.name, "Uzumba Maramba Pfungwe")
        self.assertEqual(District.objects.filter(province=self.province).count(), 1)

    def test_get_or_create_ump_uses_existing_official_name(self):
        official = District.objects.create(
            province=self.province, name="Uzumba Maramba Pfungwe", support_type="TA-SDI"
        )
        district, created = get_or_create_district(self.province, "UMP")
        self.assertFalse(created)
        self.assertEqual(district.pk, official.pk)
        self.assertEqual(District.objects.filter(province=self.province).count(), 1)


class MergeUmpDistrictTests(TestCase):
    databases = {"default"}

    def setUp(self):
        self.province = Province.objects.create(name="Mashonaland East")
        self.ump = District.objects.create(province=self.province, name="UMP", support_type="TA-SDI")
        self.official = District.objects.create(
            province=self.province, name="Uzumba Maramba Pfungwe", support_type="TA-SDI"
        )
        self.hub = Facility.objects.create(
            name="Mutawatawa District Hospital",
            district=self.ump,
            kind=Facility.Kind.HUB,
            support_type="TA-SDI",
        )
        self.clinic_dup = Facility.objects.create(
            name="Mutawatawa District Hospital",
            district=self.official,
            kind=Facility.Kind.CLINIC,
            support_type="TA-SDI",
        )
        self.clinic = Facility.objects.create(
            name="Maramba Clinic",
            district=self.official,
            kind=Facility.Kind.CLINIC,
            support_type="TA-SDI",
        )
        self.user = User.objects.create_user(username="ump_merge_rider_test", password="x")
        UserProfile.objects.update_or_create(
            user=self.user, defaults={"role": UserProfile.Role.RIDER}
        )
        self.profile = RiderProfile.objects.update_or_create(
            user=self.user,
            defaults={"province": self.province, "district": self.ump},
        )[0]

    def test_merge_keeps_ump_id_and_moves_clinics(self):
        ump_id = self.ump.pk
        results = merge_aliased_districts()
        self.assertTrue(any(r["kept_id"] == ump_id for r in results))

        kept = District.objects.get(pk=ump_id)
        self.assertEqual(kept.name, "Uzumba Maramba Pfungwe")
        self.assertFalse(District.objects.filter(pk=self.official.pk).exists())
        self.assertFalse(Facility.objects.filter(pk=self.clinic_dup.pk).exists())

        self.hub.refresh_from_db()
        self.assertEqual(self.hub.district_id, ump_id)
        self.assertEqual(self.hub.kind, Facility.Kind.HUB)

        self.clinic.refresh_from_db()
        self.assertEqual(self.clinic.district_id, ump_id)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.district_id, ump_id)

        names = set(Facility.objects.filter(district_id=ump_id).values_list("name", flat=True))
        self.assertEqual(names, {"Mutawatawa District Hospital", "Maramba Clinic"})

    def test_merge_repoints_trips_and_pc_stats(self):
        report = RiderWeeklyReport.objects.create(rider=self.user, week_start="2026-09-07")
        trip = RiderTripEntry.objects.create(
            report=report,
            origin_facility=self.clinic,
            destination_facility=self.clinic_dup,
        )
        PCDistrictWeeklyTransportStat.objects.create(
            week_start="2026-09-07",
            district=self.ump,
            rider_accidents=1,
        )
        PCDistrictWeeklyTransportStat.objects.create(
            week_start="2026-09-07",
            district=self.official,
            rider_accidents=2,
        )

        merge_aliased_districts()
        trip.refresh_from_db()
        self.assertEqual(trip.origin_facility_id, self.clinic.pk)
        self.assertEqual(trip.destination_facility_id, self.hub.pk)

        stats = PCDistrictWeeklyTransportStat.objects.filter(district_id=self.ump.pk)
        self.assertEqual(stats.count(), 1)
        self.assertEqual(stats.get().rider_accidents, 3)

    def test_ump_rider_bootstrap_includes_ump_clinics_and_hub(self):
        merge_aliased_districts()
        client = APIClient()
        client.force_authenticate(user=self.user)
        res = client.get("/api/rider/bootstrap/")
        self.assertEqual(res.status_code, 200, res.content)
        body = res.json()
        self.assertEqual(body["district_id"], self.ump.pk)
        district_names = {row["name"] for row in body["facilities_district"]}
        hub_names = {row["name"] for row in body["hubs"]}
        self.assertIn("Maramba Clinic", district_names)
        self.assertIn("Mutawatawa District Hospital", district_names)
        self.assertIn("Mutawatawa District Hospital", hub_names)


class MergeMurewaDistrictTests(TestCase):
    databases = {"default"}

    def setUp(self):
        self.province = Province.objects.create(name="Mashonaland East Merge")
        self.murewa = District.objects.create(province=self.province, name="Murewa", support_type="DSD")
        self.murehwa = District.objects.create(province=self.province, name="Murehwa", support_type="DSD")
        self.clinic = Facility.objects.create(
            name="Macheke Clinic",
            district=self.murehwa,
            kind=Facility.Kind.CLINIC,
            support_type="DSD",
        )
        self.hospital = Facility.objects.create(
            name="Murewa District Hospital",
            district=self.murehwa,
            kind=Facility.Kind.CLINIC,
            support_type="DSD",
        )
        self.user = User.objects.create_user(username="murewa_merge_rider_test", password="x")
        UserProfile.objects.update_or_create(
            user=self.user, defaults={"role": UserProfile.Role.RIDER}
        )
        self.profile = RiderProfile.objects.update_or_create(
            user=self.user,
            defaults={"province": self.province, "district": self.murewa},
        )[0]

    def test_merge_keeps_murewa_id_and_moves_clinics(self):
        murewa_id = self.murewa.pk
        merge_aliased_districts()
        kept = District.objects.get(pk=murewa_id)
        self.assertEqual(kept.name, "Murewa")
        self.assertFalse(District.objects.filter(pk=self.murehwa.pk).exists())
        self.clinic.refresh_from_db()
        self.hospital.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.clinic.district_id, murewa_id)
        self.assertEqual(self.hospital.district_id, murewa_id)
        self.assertEqual(self.profile.district_id, murewa_id)

    def test_murewa_rider_bootstrap_includes_clinics(self):
        merge_aliased_districts()
        client = APIClient()
        client.force_authenticate(user=self.user)
        res = client.get("/api/rider/bootstrap/")
        self.assertEqual(res.status_code, 200, res.content)
        body = res.json()
        self.assertEqual(body["district_id"], self.murewa.pk)
        names = {row["name"] for row in body["facilities_district"]}
        self.assertIn("Macheke Clinic", names)
        self.assertIn("Murewa District Hospital", names)
