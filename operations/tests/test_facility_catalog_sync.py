from pathlib import Path
from tempfile import NamedTemporaryFile

from django.test import SimpleTestCase, TestCase

from operations.geo_names import canon_district_name
from operations.models import District, Facility, Province
from operations.services.facility_catalog_sync import (
    CsvSite,
    ExistingFacility,
    apply_catalog_plan,
    name_keys,
    parse_sites_csv,
    plan_catalog,
    strip_org_prefix,
)


def _site(name, district="Bulawayo", province="Bulawayo", line=2):
    return CsvSite(line, province, district, name, "", "", "")


def _fac(name, district="Bulawayo", province="Bulawayo", kind=Facility.Kind.CLINIC, pk=1):
    return ExistingFacility(province, district, name, kind, "DSD", pk)


class PrefixAndAliasTests(SimpleTestCase):
    def test_strip_org_prefix(self):
        self.assertEqual(strip_org_prefix("bu Cowdray Park Clinic"), "Cowdray Park Clinic")
        self.assertEqual(strip_org_prefix("ha Harare  "), "Harare")
        self.assertEqual(strip_org_prefix("St Luke's Mission Hospital"), "St Luke's Mission Hospital")

    def test_sanyati_alias(self):
        self.assertEqual(canon_district_name("Sanyati"), "Kadoma Sanyati")
        self.assertEqual(canon_district_name("sanyati"), "Kadoma Sanyati")

    def test_name_keys_drop_punctuation(self):
        self.assertEqual(name_keys("Dr. Shennan Clinic")[1], name_keys("Dr Shennan Clinic")[1])
        self.assertEqual(name_keys("E.F. Watson Clinic")[1], name_keys("EF Watson Clinic")[1])


class CatalogPlanTests(SimpleTestCase):
    def test_exact_is_unchanged(self):
        plan = plan_catalog(
            [_site("Cowdray Park Clinic")],
            [_fac("Cowdray Park Clinic")],
            source="test",
        )
        self.assertEqual(len(plan.unchanged), 1)
        self.assertEqual(plan.rename, [])
        self.assertEqual(plan.create, [])

    def test_punctuation_rename_same_district(self):
        plan = plan_catalog(
            [_site("Dr Shennan Clinic")],
            [_fac("Dr. Shennan Clinic")],
            source="test",
        )
        self.assertEqual(len(plan.rename), 1)
        self.assertEqual(plan.rename[0].existing.name, "Dr. Shennan Clinic")
        self.assertEqual(plan.rename[0].csv.name, "Dr Shennan Clinic")

    def test_does_not_merge_distinct_khami_sites(self):
        plan = plan_catalog(
            [_site("Khami Road Clinic"), _site("Khami - Ceshhar Clinic")],
            [_fac("Khami Clinic")],
            source="test",
        )
        self.assertEqual(plan.rename, [])
        names = {row.csv.name for row in plan.create + plan.review}
        self.assertEqual(names, {"Khami Road Clinic", "Khami - Ceshhar Clinic"})

    def test_does_not_rename_labs_already_using_the_excel_name(self):
        plan = plan_catalog(
            [_site("Mpilo Central Hospital")],
            [_fac("Mpilo Central Hospital", kind=Facility.Kind.LAB)],
            source="test",
        )
        self.assertEqual(plan.rename, [])
        self.assertEqual([row.csv.name for row in plan.create], ["Mpilo Central Hospital"])

    def test_coded_lab_takes_excel_site_name(self):
        plan = plan_catalog(
            [_site("Mpilo Central Hospital")],
            [_fac("Mpilo - 101041 - Central Hospital", kind=Facility.Kind.LAB, pk=9)],
            source="test",
        )
        self.assertEqual(len(plan.rename), 1)
        self.assertEqual(plan.rename[0].existing.kind, Facility.Kind.LAB)
        self.assertEqual(plan.rename[0].csv.name, "Mpilo Central Hospital")
        self.assertEqual([row.csv.name for row in plan.create], ["Mpilo Central Hospital"])

    def test_district_hospital_hub_takes_excel_name(self):
        plan = plan_catalog(
            [_site("Mutawatawa Hospital", district="Uzumba Maramba Pfungwe", province="Mashonaland East")],
            [
                _fac(
                    "Mutawatawa District Hospital",
                    district="Uzumba Maramba Pfungwe",
                    province="Mashonaland East",
                    kind=Facility.Kind.HUB,
                    pk=4,
                )
            ],
            source="test",
        )
        self.assertEqual(len(plan.rename), 1)
        self.assertEqual(plan.rename[0].csv.name, "Mutawatawa Hospital")
        self.assertEqual(plan.rename[0].existing.kind, Facility.Kind.HUB)
        self.assertEqual(plan.create, [])

    def test_duplicate_excel_clinic_is_absorbed_into_hub(self):
        plan = plan_catalog(
            [_site("Mutawatawa Hospital", district="Uzumba Maramba Pfungwe", province="Mashonaland East")],
            [
                _fac(
                    "Mutawatawa District Hospital",
                    district="Uzumba Maramba Pfungwe",
                    province="Mashonaland East",
                    kind=Facility.Kind.HUB,
                    pk=4,
                ),
                _fac(
                    "Mutawatawa Hospital",
                    district="Uzumba Maramba Pfungwe",
                    province="Mashonaland East",
                    kind=Facility.Kind.CLINIC,
                    pk=5,
                ),
            ],
            source="test",
        )
        self.assertEqual(len(plan.absorb), 1)
        self.assertEqual(plan.absorb[0][0].name, "Mutawatawa Hospital")
        self.assertEqual(plan.absorb[0][1].kind, Facility.Kind.HUB)
        self.assertEqual(plan.create, [])

    def test_relay_district_lab_name_is_not_replaced(self):
        plan = plan_catalog(
            [_site("Chipinge Hospital", district="Chipinge", province="Manicaland")],
            [
                _fac(
                    "Chipinge District Lab",
                    district="Chipinge",
                    province="Manicaland",
                    kind=Facility.Kind.LAB,
                    pk=8,
                )
            ],
            source="test",
        )
        self.assertEqual(plan.rename, [])
        self.assertEqual(plan.absorb, [])
        self.assertEqual([row.csv.name for row in plan.create], ["Chipinge Hospital"])

    def test_trailing_clinic_vs_health_centre(self):
        plan = plan_catalog(
            [_site("Cowdray Park Health Centre")],
            [_fac("Cowdray Park Clinic")],
            source="test",
        )
        self.assertEqual(len(plan.rename), 1)
        self.assertEqual(plan.rename[0].rule, "trailing_type")

    def test_does_not_auto_rename_hospital_to_clinic(self):
        plan = plan_catalog(
            [_site("Honde Mission Clinic")],
            [_fac("Honde Mission Hospital")],
            source="test",
        )
        self.assertEqual(plan.rename, [])
        self.assertTrue(plan.review or plan.create)


class ParseCsvTests(SimpleTestCase):
    def test_parse_header_and_prefix(self):
        with NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as fh:
            fh.write("Province,District,Site\nbu Bulawayo,bu Bulawayo,bu Dr Shennan Clinic\n")
            path = Path(fh.name)
        try:
            sites, skipped = parse_sites_csv(path)
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(skipped, [])
        self.assertEqual(sites[0].province, "Bulawayo")
        self.assertEqual(sites[0].district, "Bulawayo")
        self.assertEqual(sites[0].name, "bu Dr Shennan Clinic")

    def test_sheet_code_is_kept_on_the_facility_name(self):
        plan = plan_catalog(
            [_site("bu Bulawayo Family Health Clinic")],
            [_fac("Bulawayo Family Health Clinic")],
            source="test",
        )
        self.assertEqual(len(plan.rename), 1)
        self.assertEqual(plan.rename[0].csv.name, "bu Bulawayo Family Health Clinic")
        self.assertEqual(plan.rename[0].existing.name, "Bulawayo Family Health Clinic")

    def test_short_sheet_name_keeps_the_code(self):
        plan = plan_catalog(
            [_site("bu CIMAS")],
            [_fac("CIMAS")],
            source="test",
        )
        self.assertEqual(len(plan.rename), 1)
        self.assertEqual(plan.rename[0].csv.name, "bu CIMAS")
        self.assertEqual(plan.create, [])


class ApplyCatalogPlanTests(TestCase):
    databases = {"default"}

    def setUp(self):
        self.province = Province.objects.create(name="Bulawayo")
        self.district = District.objects.create(
            province=self.province, name="Bulawayo", support_type="DSD"
        )
        self.old = Facility.objects.create(
            district=self.district,
            name="Dr. Shennan Clinic",
            kind=Facility.Kind.CLINIC,
            support_type="DSD",
        )
        self.keep = Facility.objects.create(
            district=self.district,
            name="Khami Clinic",
            kind=Facility.Kind.CLINIC,
            support_type="DSD",
        )
        self.lab = Facility.objects.create(
            district=self.district,
            name="Mpilo - 101041 - Central Hospital",
            kind=Facility.Kind.LAB,
        )

    def test_renames_and_creates_without_deleting_unmatched(self):
        sites = [
            _site("Dr Shennan Clinic"),
            _site("Khami Road Clinic"),
            _site("Budiriro Satellite Clinic"),
        ]
        existing = [
            ExistingFacility("Bulawayo", "Bulawayo", "Dr. Shennan Clinic", Facility.Kind.CLINIC, "DSD", self.old.pk),
            ExistingFacility("Bulawayo", "Bulawayo", "Khami Clinic", Facility.Kind.CLINIC, "DSD", self.keep.pk),
            ExistingFacility(
                "Bulawayo",
                "Bulawayo",
                "Mpilo - 101041 - Central Hospital",
                Facility.Kind.LAB,
                "",
                self.lab.pk,
            ),
            ExistingFacility(
                "Bulawayo",
                "Bulawayo",
                "Budiriro Satelite Clinic",
                Facility.Kind.CLINIC,
                "DSD",
                Facility.objects.create(
                    district=self.district,
                    name="Budiriro Satelite Clinic",
                    kind=Facility.Kind.CLINIC,
                    support_type="DSD",
                ).pk,
            ),
        ]
        plan = plan_catalog(sites, existing, source="test")
        stats = apply_catalog_plan(plan)
        self.old.refresh_from_db()
        self.keep.refresh_from_db()
        self.lab.refresh_from_db()
        self.assertEqual(self.old.name, "Dr Shennan Clinic")
        self.assertTrue(Facility.objects.filter(district=self.district, name="Khami Road Clinic").exists())
        self.assertTrue(Facility.objects.filter(pk=self.keep.pk, name="Khami Clinic").exists())
        self.assertEqual(self.lab.name, "Mpilo - 101041 - Central Hospital")
        self.assertTrue(Facility.objects.filter(name="Budiriro Satelite Clinic").exists())
        self.assertFalse(Facility.objects.filter(name="Budiriro Satellite Clinic").exists())
        self.assertEqual(stats["renamed"], 1)
        self.assertEqual(stats["created"], 1)

    def test_hub_takes_excel_name_and_lab_can_share_it(self):
        hub = Facility.objects.create(
            district=self.district,
            name="Mutawatawa District Hospital",
            kind=Facility.Kind.HUB,
            support_type="DSD",
        )
        clinic = Facility.objects.create(
            district=self.district,
            name="Mutawatawa Hospital",
            kind=Facility.Kind.CLINIC,
            support_type="DSD",
        )
        lab = self.lab
        clinic_mpilo = Facility.objects.create(
            district=self.district,
            name="Mpilo Central Hospital",
            kind=Facility.Kind.CLINIC,
            support_type="DSD",
        )
        sites = [
            _site("Mutawatawa Hospital"),
            _site("Mpilo Central Hospital"),
        ]
        existing = [
            ExistingFacility(
                "Bulawayo", "Bulawayo", hub.name, Facility.Kind.HUB, "DSD", hub.pk
            ),
            ExistingFacility(
                "Bulawayo", "Bulawayo", clinic.name, Facility.Kind.CLINIC, "DSD", clinic.pk
            ),
            ExistingFacility(
                "Bulawayo", "Bulawayo", lab.name, Facility.Kind.LAB, "", lab.pk
            ),
            ExistingFacility(
                "Bulawayo",
                "Bulawayo",
                "Mpilo Central Hospital",
                Facility.Kind.CLINIC,
                "DSD",
                clinic_mpilo.pk,
            ),
        ]
        plan = plan_catalog(sites, existing, source="test")
        apply_catalog_plan(plan)
        hub.refresh_from_db()
        lab.refresh_from_db()
        self.assertEqual(hub.name, "Mutawatawa Hospital")
        self.assertFalse(Facility.objects.filter(pk=clinic.pk).exists())
        self.assertEqual(lab.name, "Mpilo Central Hospital")
        self.assertEqual(
            Facility.objects.filter(district=self.district, name="Mpilo Central Hospital").count(),
            2,
        )
