"""Weekly rider submissions by province: submitted vs not, trips, PC reviews."""

from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from operations.models import (
    District,
    PCProfile,
    Province,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    TripRouteKind,
    TripTransportKind,
    TripVisitPurpose,
    UserProfile,
)
from operations.services import report_service
from operations.services.rider_week_submission_report import (
    build_rider_week_submission_report,
    pc_review_csv_rows,
    province_summary_csv_rows,
    rider_detail_csv_rows,
)


def _operations_test_databases():
    names = {"default"}
    if "sqlite" in settings.DATABASES:
        names.add("sqlite")
    return names


def _make_trip(report, sequence=1):
    return RiderTripEntry.objects.create(
        report=report,
        sequence=sequence,
        transport_kind=TripTransportKind.LEGACY,
        visit_purpose=TripVisitPurpose.SPECIMENS_RESULTS_TRANSPORT,
        route_kind=TripRouteKind.HUB_TO_LAB,
        sputum=1,
    )


class RiderWeekSubmissionReportServiceTests(TestCase):
    databases = _operations_test_databases()

    def _set_role(self, user, role):
        profile, _ = UserProfile.objects.update_or_create(
            user=user, defaults={"role": role}
        )
        profile.role = role
        profile.save(update_fields=["role"])
        user.profile = profile
        return user

    def setUp(self):
        User = get_user_model()
        self.week = date(2026, 9, 14)
        self.other_week = self.week - timedelta(days=7)

        self.me_user = self._set_role(
            User.objects.create_user(username="me_sub", password="pass123"),
            UserProfile.Role.ME,
        )

        self.prov_a = Province.objects.create(name="Harare")
        self.prov_b = Province.objects.create(name="Manicaland")
        self.dist_a = District.objects.create(name="Chitungwiza", province=self.prov_a)
        self.dist_b = District.objects.create(name="Mutasa", province=self.prov_b)

        self.high = self._rider("high_trips", "Ada High", self.prov_a, self.dist_a)
        self.low = self._rider("low_trips", "Ben Low", self.prov_a, self.dist_a)
        self.missing = self._rider("no_submit", "Cara Missing", self.prov_a, self.dist_a)
        self.other_prov = self._rider("other_prov", "Dan East", self.prov_b, self.dist_b)
        self.draft_only = self._rider("draft_only", "Eve Draft", self.prov_b, self.dist_b)

        high_report = RiderWeeklyReport.objects.create(
            rider=self.high,
            week_start=self.week,
            status=RiderWeeklyReport.Status.SUBMITTED,
            submitted_at=timezone.now(),
        )
        _make_trip(high_report, 1)
        _make_trip(high_report, 2)
        _make_trip(high_report, 3)

        low_report = RiderWeeklyReport.objects.create(
            rider=self.low,
            week_start=self.week,
            status=RiderWeeklyReport.Status.APPROVED,
            submitted_at=timezone.now(),
        )
        _make_trip(low_report, 1)

        report_service.complete_review(low_report, self.me_user, approved=True)

        # Wrong week must not count toward this week's trips or submission.
        other_week_report = RiderWeeklyReport.objects.create(
            rider=self.missing,
            week_start=self.other_week,
            status=RiderWeeklyReport.Status.SUBMITTED,
            submitted_at=timezone.now(),
        )
        _make_trip(other_week_report, 1)
        _make_trip(other_week_report, 2)

        other_report = RiderWeeklyReport.objects.create(
            rider=self.other_prov,
            week_start=self.week,
            status=RiderWeeklyReport.Status.UNDER_REVIEW,
            submitted_at=timezone.now(),
        )
        _make_trip(other_report, 1)
        _make_trip(other_report, 2)

        draft = RiderWeeklyReport.objects.create(
            rider=self.draft_only,
            week_start=self.week,
            status=RiderWeeklyReport.Status.DRAFT,
        )
        _make_trip(draft, 1)

    def _rider(self, username, full_name, province, district):
        User = get_user_model()
        first, last = full_name.split(" ", 1)
        user = User.objects.create_user(
            username=username, password="pass123", first_name=first, last_name=last
        )
        self._set_role(user, UserProfile.Role.RIDER)
        RiderProfile.objects.update_or_create(
            user=user,
            defaults={"province": province, "district": district},
        )
        return user

    def _by_province(self, data):
        return {p["province_name"]: p for p in data["provinces"]}

    def test_submitted_riders_have_trip_counts(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        harare = self._by_province(data)["Harare"]
        names = {r["rider_name"]: r["trip_count"] for r in harare["submitted_riders"]}
        self.assertEqual(names["Ada High"], 3)
        self.assertEqual(names["Ben Low"], 1)

    def test_non_submitters_appear(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        harare = self._by_province(data)["Harare"]
        missing = [r["rider_name"] for r in harare["not_submitted_riders"]]
        self.assertEqual(missing, ["Cara Missing"])
        self.assertEqual(harare["not_submitted_riders"][0]["trip_count"], 0)

        manicaland = self._by_province(data)["Manicaland"]
        not_sub = {r["rider_name"]: r for r in manicaland["not_submitted_riders"]}
        self.assertIn("Eve Draft", not_sub)
        self.assertEqual(not_sub["Eve Draft"]["status_display"], "Draft")
        self.assertEqual(not_sub["Eve Draft"]["trip_count"], 1)

    def test_sorted_by_trips_descending(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        harare = self._by_province(data)["Harare"]
        trips = [r["trip_count"] for r in harare["submitted_riders"]]
        self.assertEqual(trips, sorted(trips, reverse=True))
        self.assertEqual(trips[0], 3)

    def test_province_grouping_and_filter(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        self.assertEqual({p["province_name"] for p in data["provinces"]}, {"Harare", "Manicaland"})
        harare = self._by_province(data)["Harare"]
        self.assertEqual(harare["rider_count"], 3)
        self.assertEqual(harare["submitted_count"], 2)
        self.assertEqual(harare["not_submitted_count"], 1)

        filtered = build_rider_week_submission_report(
            user=self.me_user, week_start=self.week, province_id=self.prov_b.pk
        )
        self.assertEqual([p["province_name"] for p in filtered["provinces"]], ["Manicaland"])
        self.assertEqual(filtered["totals"]["rider_count"], 2)

    def test_week_window_ignores_other_weeks(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        harare = self._by_province(data)["Harare"]
        missing = harare["not_submitted_riders"][0]
        self.assertEqual(missing["rider_name"], "Cara Missing")
        self.assertFalse(missing["submitted"])

    def test_province_summary_submitted_vs_riders(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        headers, rows = province_summary_csv_rows(data)
        self.assertIn("Submitted", headers)
        self.assertIn("Riders", headers)
        by_name = {row[0]: row for row in rows}
        # Harare: 3 riders, 2 submitted
        self.assertEqual(by_name["Harare"][1], "3")
        self.assertEqual(by_name["Harare"][2], "2")
        self.assertEqual(by_name["Harare"][3], "1")

    def test_pc_reviews_vs_need_to_submit(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        harare = self._by_province(data)["Harare"]
        self.assertEqual(harare["needs_to_submit"], 3)
        self.assertEqual(harare["pc_reviewed_count"], 1)
        self.assertEqual(harare["submitted_pending_review"], 1)

        headers, rows = pc_review_csv_rows(data)
        self.assertEqual(headers[1], "PC reviewed")
        self.assertEqual(headers[2], "Need to submit")
        by_name = {row[0]: row for row in rows}
        self.assertEqual(by_name["Harare"][1], "1")
        self.assertEqual(by_name["Harare"][2], "3")

    def test_rider_csv_marks_submitted_and_not(self):
        data = build_rider_week_submission_report(user=self.me_user, week_start=self.week)
        _headers, rows = rider_detail_csv_rows(data)
        labels = {(row[2], row[1]) for row in rows}
        self.assertIn(("Ada High", "Submitted"), labels)
        self.assertIn(("Cara Missing", "Not submitted"), labels)


class RiderWeekSubmissionReportViewTests(TestCase):
    databases = _operations_test_databases()

    def setUp(self):
        User = get_user_model()
        self.week = date(2026, 9, 14)
        self.province = Province.objects.create(name="Midlands")
        self.other_province = Province.objects.create(name="Bulawayo")
        self.district = District.objects.create(name="Gweru", province=self.province)
        self.other_district = District.objects.create(name="Bulawayo City", province=self.other_province)

        self.me_user = User.objects.create_user(username="me_view", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.me_user, defaults={"role": UserProfile.Role.ME}
        )
        self.pc_user = User.objects.create_user(username="pc_view", password="pass123")
        UserProfile.objects.update_or_create(
            user=self.pc_user, defaults={"role": UserProfile.Role.PC}
        )
        pc_profile, _ = PCProfile.objects.get_or_create(user=self.pc_user)
        pc_profile.provinces.add(self.province)

        self.rider_user = User.objects.create_user(
            username="rider_view", password="pass123", first_name="Fay", last_name="Rider"
        )
        UserProfile.objects.update_or_create(
            user=self.rider_user, defaults={"role": UserProfile.Role.RIDER}
        )
        RiderProfile.objects.update_or_create(
            user=self.rider_user,
            defaults={"province": self.province, "district": self.district},
        )

        self.out_of_scope = User.objects.create_user(
            username="out_scope", password="pass123", first_name="Gus", last_name="Out"
        )
        UserProfile.objects.update_or_create(
            user=self.out_of_scope, defaults={"role": UserProfile.Role.RIDER}
        )
        RiderProfile.objects.update_or_create(
            user=self.out_of_scope,
            defaults={"province": self.other_province, "district": self.other_district},
        )

        report = RiderWeeklyReport.objects.create(
            rider=self.rider_user,
            week_start=self.week,
            status=RiderWeeklyReport.Status.SUBMITTED,
            submitted_at=timezone.now(),
        )
        _make_trip(report)
        self.url = reverse("operations:rider_week_submissions")

    def test_me_can_open_report(self):
        self.client.force_login(self.me_user)
        response = self.client.get(self.url, {"week": self.week.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fay Rider")
        self.assertContains(response, "Gus Out")
        self.assertContains(response, "Submitted")
        self.assertContains(response, "Not submitted")

    def test_pc_is_scoped_to_assigned_provinces(self):
        self.client.force_login(self.pc_user)
        response = self.client.get(self.url, {"week": self.week.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fay Rider")
        self.assertNotContains(response, "Gus Out")

    def test_rider_cannot_access(self):
        self.client.force_login(self.rider_user)
        response = self.client.get(self.url, {"week": self.week.isoformat()})
        self.assertEqual(response.status_code, 403)

    def test_csv_downloads(self):
        self.client.force_login(self.me_user)
        for name in (
            "operations:rider_week_submissions_summary_csv",
            "operations:rider_week_submissions_riders_csv",
            "operations:rider_week_submissions_pc_reviews_csv",
        ):
            response = self.client.get(reverse(name), {"week": self.week.isoformat()})
            self.assertEqual(response.status_code, 200, name)
            self.assertIn("text/csv", response["Content-Type"])
            self.assertIn("attachment", response.get("Content-Disposition", ""))
            body = response.content.decode("utf-8-sig")
            self.assertTrue(body.strip())
        riders_csv = self.client.get(
            reverse("operations:rider_week_submissions_riders_csv"),
            {"week": self.week.isoformat()},
        ).content.decode("utf-8-sig")
        self.assertIn("Fay Rider", riders_csv)
        self.assertIn("Submitted", riders_csv)
        summary_csv = self.client.get(
            reverse("operations:rider_week_submissions_summary_csv"),
            {"week": self.week.isoformat()},
        ).content.decode("utf-8-sig")
        self.assertIn("Midlands", summary_csv)
        self.assertIn("Need to submit", summary_csv)
        reviews_csv = self.client.get(
            reverse("operations:rider_week_submissions_pc_reviews_csv"),
            {"week": self.week.isoformat()},
        ).content.decode("utf-8-sig")
        self.assertIn("PC reviewed", reviews_csv)
