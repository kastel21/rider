from django.contrib.auth.models import User
from django.test import TestCase

from operations.forms import _route_kind_for_visit_purpose
from operations.models import District, Facility, Province, TripRouteKind, TripVisitPurpose, UserProfile
from operations.services.trip_facilities import (
    facilities_for_rider_endpoint,
    facility_matches_route_endpoint,
    normalize_route_kind,
    route_endpoint_roles,
)


class TripRouteKindsTests(TestCase):
    def setUp(self):
        self.province = Province.objects.create(name="Test Province")
        self.district = District.objects.create(name="Test District", province=self.province)
        self.clinic = Facility.objects.create(
            name="District Hospital", district=self.district, kind=Facility.Kind.CLINIC
        )
        self.hub = Facility.objects.create(
            name="PEPFAR Hub", district=self.district, kind=Facility.Kind.HUB
        )
        self.provincial_lab = Facility.objects.create(
            name="Provincial Hospital", district=self.district, kind=Facility.Kind.LAB
        )
        self.district_lab = Facility.objects.create(
            name="Chipinge District Lab", district=self.district, kind=Facility.Kind.HUB
        )
        self.admin = User.objects.create_user(username="relay_lab_admin", password="x")
        self.admin.profile.role = UserProfile.Role.ADMIN
        self.admin.profile.save(update_fields=["role"])

    def test_legacy_facility_routes_normalize(self):
        self.assertEqual(normalize_route_kind("facility_to_lab"), TripRouteKind.HUB_TO_LAB)
        self.assertEqual(normalize_route_kind("lab_to_facility"), TripRouteKind.LAB_TO_HUB)

    def test_hub_endpoint_includes_clinic_and_hub_kinds(self):
        roles = route_endpoint_roles(TripRouteKind.HUB_TO_HUB)
        self.assertEqual(roles, ("hub", "hub"))
        self.assertTrue(facility_matches_route_endpoint(self.clinic, "hub"))
        self.assertTrue(facility_matches_route_endpoint(self.hub, "hub"))
        self.assertFalse(facility_matches_route_endpoint(self.provincial_lab, "hub"))

    def test_vl_lab_endpoint_is_lab_kind_only(self):
        roles = route_endpoint_roles(TripRouteKind.HUB_TO_LAB)
        self.assertEqual(roles, ("hub", "vl_lab"))
        self.assertTrue(facility_matches_route_endpoint(self.provincial_lab, "vl_lab"))
        self.assertFalse(facility_matches_route_endpoint(self.clinic, "vl_lab"))

    def test_only_four_route_choices(self):
        self.assertEqual(len(TripRouteKind.choices), 4)

    def test_relay_from_and_to_are_district_labs_only(self):
        relay_from = facilities_for_rider_endpoint(
            self.admin,
            TripRouteKind.HUB_TO_HUB,
            "from",
            visit_purpose=TripVisitPurpose.RELAY,
        )
        relay_to = facilities_for_rider_endpoint(
            self.admin,
            TripRouteKind.HUB_TO_HUB,
            "to",
            visit_purpose=TripVisitPurpose.RELAY,
        )
        self.assertEqual(list(relay_from.values_list("name", flat=True)), ["Chipinge District Lab"])
        self.assertEqual(list(relay_to.values_list("name", flat=True)), ["Chipinge District Lab"])

        hub_names = set(
            facilities_for_rider_endpoint(
                self.admin,
                TripRouteKind.HUB_TO_HUB,
                "from",
                visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
            ).values_list("name", flat=True)
        )
        self.assertIn("PEPFAR Hub", hub_names)
        self.assertIn("District Hospital", hub_names)
        self.assertNotIn("Chipinge District Lab", hub_names)

    def test_relay_forces_hub_to_hub_route(self):
        rk = _route_kind_for_visit_purpose(
            TripVisitPurpose.RELAY,
            TripRouteKind.HUB_TO_LAB,
        )
        self.assertEqual(rk, TripRouteKind.HUB_TO_HUB)
