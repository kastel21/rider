import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class UserProfile(models.Model):
    class Role(models.TextChoices):
        RIDER = "rider", "Rider"
        DRIVER = "driver", "Driver"
        PC = "pc", "Program Coordinator"
        ME = "me", "Monitoring & Evaluation"
        ADMIN = "admin", "Administrator"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.RIDER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Role(models.TextChoices):
    """docs/operations-compatible role enum names."""
    RIDER = UserProfile.Role.RIDER
    DRIVER = UserProfile.Role.DRIVER
    PC = UserProfile.Role.PC
    ME = UserProfile.Role.ME
    ADMIN = UserProfile.Role.ADMIN


class SupportType(models.TextChoices):
    DSD = "DSD", "DSD"
    TA_SDI = "TA-SDI", "TA-SDI"
    TAT = "TAT", "TAT"
    OTHER = "OTHER", "Other"


class Province(models.Model):
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=128)
    support_type = models.CharField(max_length=20, choices=SupportType.choices, blank=True)

    class Meta:
        unique_together = [("province", "name")]

    def __str__(self):
        return f"{self.name} ({self.province})"


class Facility(models.Model):
    class Kind(models.TextChoices):
        HUB = "hub", "Hub"
        LAB = "lab", "Lab"
        CLINIC = "clinic", "Clinic"

    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="facilities")
    name = models.CharField(max_length=256)
    kind = models.CharField(max_length=32, choices=Kind.choices, default=Kind.HUB)
    support_type = models.CharField(
        max_length=20,
        choices=SupportType.choices,
        blank=True,
        help_text="PEPFAR support model for this site (e.g. TA-SDI).",
    )

    site_code = models.CharField(
        max_length=32,
        blank=True,
        help_text="PEPFAR / site identifier for reports (e.g. lab line: District - code - name).",
    )

    class Meta:
        verbose_name_plural = "facilities"
        unique_together = [("district", "name")]

    def __str__(self):
        return self.name


class Bike(models.Model):
    code = models.CharField(max_length=64, unique=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name="bikes")
    notes = models.CharField(max_length=256, blank=True)
    active = models.BooleanField(default=True)
    # Days specimens were not picked up — maintained by PC under Manage → Bike status.
    snp_bike_breakdown = models.PositiveIntegerField(
        default=0,
        help_text="Days: bike breakdown.",
    )
    snp_bike_routine_service = models.PositiveIntegerField(
        default=0,
        help_text="Days: bike on routine service / maintenance.",
    )
    snp_bike_no_fuel = models.PositiveIntegerField(
        default=0,
        help_text="Days: bike had no fuel.",
    )
    snp_rider_sick_leave = models.PositiveIntegerField(
        default=0,
        help_text="Days: rider on sick leave.",
    )
    snp_rider_annual_leave = models.PositiveIntegerField(
        default=0,
        help_text="Days: rider on annual leave.",
    )
    snp_inclement_weather = models.PositiveIntegerField(
        default=0,
        help_text="Days: inclement weather.",
    )
    snp_bike_accident = models.PositiveIntegerField(
        default=0,
        help_text="Days: bike accident / damaged.",
    )
    snp_clinical_ip = models.PositiveIntegerField(
        default=0,
        help_text="Days: clinical IPs related issues.",
    )
    snp_other = models.PositiveIntegerField(
        default=0,
        help_text="Days: other reasons (see specify).",
    )
    snp_other_specify = models.CharField(
        max_length=512,
        blank=True,
        help_text="E.g. vacant post, rider reassigned, suspension, public holiday.",
    )
    mitigation_measures = models.TextField(
        blank=True,
        help_text="Actions taken to address bike or specimen non-pickup issues.",
    )
    affected_facilities = models.ManyToManyField(
        Facility,
        blank=True,
        related_name="affected_bikes",
        help_text="Facilities in this bike's district impacted by specimen non-pickup or related issues.",
    )

    def __str__(self):
        return self.code


class Car(models.Model):
    """Motor vehicle used by drivers (parallel to Bike for riders). PC-maintained status."""

    code = models.CharField(max_length=64, unique=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name="cars")
    notes = models.CharField(max_length=256, blank=True)
    active = models.BooleanField(default=True)
    snp_bike_breakdown = models.PositiveIntegerField(
        default=0,
        help_text="Days: vehicle breakdown.",
    )
    snp_bike_routine_service = models.PositiveIntegerField(
        default=0,
        help_text="Days: vehicle on routine service / maintenance.",
    )
    snp_bike_no_fuel = models.PositiveIntegerField(
        default=0,
        help_text="Days: vehicle had no fuel.",
    )
    snp_rider_sick_leave = models.PositiveIntegerField(
        default=0,
        help_text="Days: driver on sick leave.",
    )
    snp_rider_annual_leave = models.PositiveIntegerField(
        default=0,
        help_text="Days: driver on annual leave.",
    )
    snp_inclement_weather = models.PositiveIntegerField(
        default=0,
        help_text="Days: inclement weather.",
    )
    snp_bike_accident = models.PositiveIntegerField(
        default=0,
        help_text="Days: vehicle accident / damaged.",
    )
    snp_clinical_ip = models.PositiveIntegerField(
        default=0,
        help_text="Days: clinical IPs related issues.",
    )
    snp_other = models.PositiveIntegerField(
        default=0,
        help_text="Days: other reasons (see specify).",
    )
    snp_other_specify = models.CharField(
        max_length=512,
        blank=True,
        help_text="E.g. vacant post, driver reassigned, suspension, public holiday.",
    )
    mitigation_measures = models.TextField(
        blank=True,
        help_text="Actions taken to address vehicle or specimen non-pickup issues.",
    )
    affected_facilities = models.ManyToManyField(
        Facility,
        blank=True,
        related_name="affected_cars",
        help_text="Facilities in this vehicle's district impacted by specimen non-pickup or related issues.",
    )

    def __str__(self):
        return self.code


class PCProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pc_profile",
    )
    provinces = models.ManyToManyField(Province, blank=True, related_name="pc_profiles")


class RiderProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rider_profile",
    )
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name="riders")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    support_type = models.CharField(max_length=20, choices=SupportType.choices, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
    bike = models.ForeignKey(Bike, on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_profiles")


class RiderWeeklyReport(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        UNDER_REVIEW = "under_review", "Under review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    client_uuid = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
        help_text="Idempotency key for offline-created rows.",
    )
    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weekly_reports",
    )
    week_start = models.DateField(db_index=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT)
    title = models.CharField(max_length=256, blank=True)
    notes = models.TextField(blank=True)
    samples_collected = models.PositiveIntegerField(default=0)
    extra_data = models.JSONField(default=dict, blank=True)

    submitted_at = models.DateTimeField(null=True, blank=True)
    review_started_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_reviewed",
    )
    me_reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When set, M&E has finalized review of this report and PCs may no longer edit it.",
    )
    me_reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_me_reviewed",
    )
    pc_notes = models.TextField(blank=True)
    scheduled_visits = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of visits scheduled for this week (entered by program coordinator).",
    )
    average_datalogger_temperature = models.IntegerField(
        null=True,
        blank=True,
        help_text="Average data logger temperature for this reporting week (whole number, e.g. °C).",
    )
    distance_travelled = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    bike = models.ForeignKey(
        Bike,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="weekly_reports",
        help_text="Bike used for this report (must be in the rider's district).",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="weekly_reports",
        help_text="Vehicle (car) for driver reports when applicable.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-week_start", "-id"]

    def __str__(self):
        return f"Report {self.week_start} ({self.rider})"

    def clean(self):
        super().clean()
        role = None
        if self.rider_id:
            try:
                role = self.rider.profile.role
            except Exception:
                role = None
        if self.bike_id and self.car_id:
            raise ValidationError("Select either a bike or a vehicle (car), not both.")
        if role == UserProfile.Role.DRIVER:
            if self.bike_id:
                raise ValidationError({"bike": "Drivers must use vehicle (car) selection, not bike."})
        elif role == UserProfile.Role.RIDER and self.car_id:
            raise ValidationError({"car": "Riders use bike selection, not vehicle (car)."})
        if self.bike_id and self.rider_id:
            rp = getattr(self.rider, "rider_profile", None)
            bd = getattr(self.bike, "district_id", None)
            if rp and rp.district_id and bd and bd != rp.district_id:
                raise ValidationError(
                    {"bike": "Selected bike must be registered in the rider's district."}
                )
        if self.car_id and self.rider_id:
            rp = getattr(self.rider, "rider_profile", None)
            cd = getattr(self.car, "district_id", None)
            if rp and rp.district_id and cd and cd != rp.district_id:
                raise ValidationError(
                    {"car": "Selected vehicle must be registered in the driver's district."}
                )

    @property
    def trip_entries_total_specimens(self) -> int:
        return sum((e.specimens_total for e in self.trip_entries.all()), 0)

    @property
    def trip_entries_total_results(self) -> int:
        return sum((e.results_total for e in self.trip_entries.all()), 0)


class RiderWeekFuelSummary(models.Model):
    """One row per rider (or driver) per calendar week — week fuel totals independent of weekly reports."""

    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="week_fuel_summaries",
    )
    week_start = models.DateField(db_index=True)
    fuel_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fuel_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_travelled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["rider", "week_start"], name="uniq_rider_week_fuel_summary"),
        ]
        ordering = ["-week_start", "-id"]

    def __str__(self):
        return f"Week fuel {self.week_start} ({self.rider})"


class SampleRejection(models.Model):
    """One row per sample-type group: rejection totals and reason breakdown."""

    class SampleType(models.TextChoices):
        VL_PLASMA = "vl_plasma", "VL Plasma"
        VL_DBS = "vl_dbs", "VL DBS"
        EID_BLOOD = "eid_blood", "EID Blood"
        EID_DBS = "eid_dbs", "EID DBS"
        SPUTUM = "sputum", "Sputum"
        SPUTUM_CULTURE_DR = "sputum_culture_dr", "Sputum Culture DR"
        HPV = "hpv", "HPV"
        OTHER = "other", "Other"

    report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name="sample_rejections",
    )
    sample_type = models.CharField(max_length=50, choices=SampleType.choices)
    rejected_total = models.PositiveIntegerField(
        default=0,
        help_text="Total rejected for this sample type.",
    )
    rejected_too_old = models.PositiveIntegerField(default=0)
    rejected_patient_info_mismatch = models.PositiveIntegerField(default=0)
    rejected_request_form_missing = models.PositiveIntegerField(default=0)
    rejected_sample_missing = models.PositiveIntegerField(default=0)
    rejected_other = models.PositiveIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order within the report.")

    class Meta:
        ordering = ["report", "order", "pk"]
        verbose_name = "Sample rejection"
        verbose_name_plural = "Sample rejections"

    def _rejection_reasons_sum(self) -> int:
        return (
            (self.rejected_too_old or 0)
            + (self.rejected_patient_info_mismatch or 0)
            + (self.rejected_request_form_missing or 0)
            + (self.rejected_sample_missing or 0)
            + (self.rejected_other or 0)
        )

    def clean(self):
        super().clean()
        rej_total = self.rejected_total or 0
        if rej_total > 0:
            reasons_sum = self._rejection_reasons_sum()
            if reasons_sum != rej_total:
                raise ValidationError(
                    {
                        "rejected_other": (
                            f"Sum of rejection reasons must equal total rejected "
                            f"(reasons: {reasons_sum}, total: {rej_total})."
                        )
                    }
                )

    def __str__(self):
        return f"{self.get_sample_type_display()} — {self.rejected_total} rejected"


class ReferredSample(models.Model):
    """PC-tracked referrals: samples sent from one lab/facility to another reference lab."""

    class SampleType(models.TextChoices):
        DBS = "dbs", "DBS"
        PLASMA = "plasma", "Plasma"
        BLOOD = "blood", "Blood"
        OTHER = "other", "Other"

    class TestType(models.TextChoices):
        VL = "vl", "VL"
        EID = "eid", "EID"
        HPV = "hpv", "HPV"
        TB = "tb", "TB"
        OTHER = "other", "Other"

    from_facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="referred_samples_out",
        help_text="Lab (referring site).",
    )
    to_facility = models.ForeignKey(
        Facility,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referred_samples_in",
        help_text="Reference lab samples were referred to.",
    )
    sample_type = models.CharField(max_length=32, choices=SampleType.choices)
    test_type = models.CharField(max_length=32, choices=TestType.choices)
    total_samples_referred_out = models.PositiveIntegerField(default=0)
    swift_consignment_number = models.CharField(
        max_length=64,
        blank=True,
        help_text="Swift consignment / tracking reference.",
    )
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def referring_lab_display(self) -> str:
        return self._facility_line(self.from_facility)

    def referred_to_lab_display(self) -> str:
        if not self.to_facility_id:
            return "—"
        return self._facility_line(self.to_facility)

    @staticmethod
    def _facility_line(facility: Facility) -> str:
        dname = facility.district.name
        code = (facility.site_code or "").strip() or "—"
        return f"{dname} - {code} - {facility.name}"


class TripVisitPurpose(models.TextChoices):
    SPECIMENS_RESULTS_TRANSPORT = (
        "specimens_results_transport",
        "Specimens and Results Transportation",
    )
    ADHOC = "adhoc", "Adhoc"
    RELAY = "relay", "Relay"

    @classmethod
    def normalize(cls, raw: str) -> str:
        """Map legacy stored/sync values to current choice values."""
        v = (raw or "").strip()
        legacy = {
            "sample_collection": cls.SPECIMENS_RESULTS_TRANSPORT,
            "sample_delivery": cls.SPECIMENS_RESULTS_TRANSPORT,
        }
        if v in legacy:
            return legacy[v]
        valid = {choice for choice, _ in cls.choices}
        if v in valid:
            return v
        return v[:32]


class TripTransportKind(models.TextChoices):
    """How this trip row is categorized in weekly reporting (driver has two tabs)."""

    LEGACY = "legacy", "Legacy (rider / historical)"
    RELAYED = "relayed", "Samples relayed (not carried for the first time)"
    FIRST_TRANSPORT = "first_transport", "Samples transported for the first time"


class TripRouteKind(models.TextChoices):
    HUB_TO_HUB = "hub_to_hub", "Hub to hub"
    HUB_TO_LAB = "hub_to_lab", "Hub to VL Lab"
    LAB_TO_HUB = "lab_to_hub", "VL Lab to hub"
    LAB_TO_LAB = "lab_to_lab", "VL Lab to VL Lab"


class RiderTripEntry(models.Model):
    """One capture row under a rider weekly report."""

    TransportKind = TripTransportKind

    report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name="trip_entries",
    )
    row_uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    sequence = models.PositiveIntegerField(default=1)
    entry_date = models.DateField(null=True, blank=True)

    transport_kind = models.CharField(
        max_length=32,
        choices=TripTransportKind.choices,
        default=TripTransportKind.LEGACY,
        db_index=True,
    )

    visit_purpose = models.CharField(
        max_length=32,
        choices=TripVisitPurpose.choices,
        blank=True,
    )
    route_kind = models.CharField(
        max_length=40,
        choices=TripRouteKind.choices,
        blank=True,
        verbose_name="Trip Route",
    )
    origin_facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="trip_origins",
    )
    destination_facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="trip_destinations",
    )

    # Number of specimens transported
    vl_blood_plasma = models.PositiveIntegerField(default=0)
    vl_dbs = models.PositiveIntegerField(default=0)
    eid_blood = models.PositiveIntegerField(default=0)
    eid_dbs = models.PositiveIntegerField(default=0)
    sputum = models.PositiveIntegerField(default=0)
    sputum_culture_dr = models.PositiveIntegerField(default=0)
    hpv = models.PositiveIntegerField(default=0)
    specimens_other_specify = models.CharField(max_length=255, blank=True)

    # Number of results transported
    results_vl_blood_plasma = models.PositiveIntegerField(default=0)
    results_vl_dbs = models.PositiveIntegerField(default=0)
    results_eid_blood = models.PositiveIntegerField(default=0)
    results_eid_dbs = models.PositiveIntegerField(default=0)
    results_sputum = models.PositiveIntegerField(default=0)
    results_sputum_culture_dr = models.PositiveIntegerField(default=0)
    results_hpv = models.PositiveIntegerField(default=0)
    results_other_specify = models.CharField(max_length=255, blank=True)

    fuel_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fuel_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_travelled = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sequence", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["report", "row_uuid"],
                name="uniq_trip_row_uuid_per_report",
            ),
        ]

    @property
    def specimens_total(self) -> int:
        return (
            self.vl_blood_plasma
            + self.vl_dbs
            + self.eid_blood
            + self.eid_dbs
            + self.sputum
            + self.sputum_culture_dr
            + self.hpv
        )

    @property
    def results_total(self) -> int:
        return (
            self.results_vl_blood_plasma
            + self.results_vl_dbs
            + self.results_eid_blood
            + self.results_eid_dbs
            + self.results_sputum
            + self.results_sputum_culture_dr
            + self.results_hpv
        )


class ReportAuditLog(models.Model):
    report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=64)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class ReportEditSnapshot(models.Model):
    """PC edit history entries."""

    report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name="edit_snapshots",
    )
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    summary = models.CharField(max_length=512)
    diff_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class WeeklyRecordReviewed(models.Model):
    """Weekly PC review snapshots persisted as a single aggregated record."""

    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weekly_records_reviewed",
    )
    week_start = models.DateField(db_index=True)
    source_report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name="weekly_review_records",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="weekly_records_reviewed_by",
    )
    reviewed_at = models.DateTimeField(auto_now_add=True)
    snapshot = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "weekly_record_reviewed"
        ordering = ["-reviewed_at", "-id"]


class PCDistrictWeeklyTransportStat(models.Model):
    """
    Weekly PC-entered aggregates per district: rider accidents and incomplete /
    non-IST specimen transport (one row per district per Monday week_start).
    """

    week_start = models.DateField(db_index=True)
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="pc_weekly_transport_stats",
    )
    rider_accidents = models.PositiveIntegerField(default=0)
    incomplete_bike_transport_trips = models.PositiveIntegerField(default=0)
    specimens_non_ist_total = models.PositiveIntegerField(
        default=0,
        help_text="Total specimens transported by non-IST methods.",
    )
    specimens_ambulance = models.PositiveIntegerField(default=0)
    specimens_alternative_ip_transport = models.PositiveIntegerField(default=0)
    specimens_mohcc_arranged_transport = models.PositiveIntegerField(default=0)
    specimens_courier = models.PositiveIntegerField(default=0)
    specimens_other_non_ist = models.PositiveIntegerField(default=0)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["district__province_id", "district__name", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["week_start", "district"],
                name="uniq_pc_district_week_transport_stat",
            ),
        ]

    def __str__(self):
        return f"{self.week_start} / {self.district_id}"


class PCAccidentDetail(models.Model):
    """Per-incident accident line items entered by PC for a given reporting week."""

    class BikeStatus(models.IntegerChoices):
        WORKING = 1, "Working"
        MINOR_DAMAGE = 2, "Minor damage"
        WRITE_OFF = 3, "Write off"
        MAJOR_DAMAGED = 4, "Major damaged"

    class RiderInjuryStatus(models.IntegerChoices):
        MINOR_INJURIES = 1, "Minor injuries"
        MAJOR_INJURIES = 2, "Major injuries"
        DEAD = 3, "Dead"

    week_start = models.DateField(db_index=True)
    rider = models.ForeignKey(
        "RiderProfile",
        on_delete=models.CASCADE,
        related_name="pc_accident_details",
    )
    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name="pc_accident_details",
    )
    accident_cause = models.TextField(blank=True)
    bike_status = models.PositiveSmallIntegerField(
        choices=BikeStatus.choices,
        default=BikeStatus.WORKING,
    )
    rider_injury_status = models.PositiveSmallIntegerField(
        choices=RiderInjuryStatus.choices,
        default=RiderInjuryStatus.MINOR_INJURIES,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.week_start} rider={self.rider_id} bike={self.bike_id}"


class RegisteredDevice(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registered_devices",
    )
    device_id = models.CharField(max_length=128, db_index=True)
    platform = models.CharField(max_length=64, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    last_seen_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "device_id")]


class Lab(models.Model):
    """Reference lab row for rider bootstrap / offline cache."""

    name = models.CharField(max_length=256)
    code = models.CharField(max_length=64, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RiderDevice(models.Model):
    """Registered device for JWT sync (device_id gate)."""

    rider = models.ForeignKey(
        RiderProfile,
        on_delete=models.CASCADE,
        related_name="devices",
    )
    device_id = models.CharField(max_length=255, help_text="Client device identifier.")
    device_model = models.CharField(max_length=120, blank=True)
    app_version = models.CharField(max_length=60, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("rider", "device_id")]
        ordering = ["rider", "-last_seen"]

    def __str__(self):
        return f"{self.device_id} ({self.rider_id})"


class RiderRemoteConfig(models.Model):
    """Singleton-style config row (pk=1) for rider app."""

    sync_interval = models.PositiveIntegerField(default=60)
    max_batch_size = models.PositiveIntegerField(default=10)
    latest_app_version = models.CharField(max_length=60, blank=True)
    update_required = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Rider Remote Config"

    def __str__(self):
        return "Rider app config"


# API bootstrap uses the same route kinds as trip entries.
TransportRouteType = TripRouteKind

# docs/operations-compatible status alias.
ReportStatus = RiderWeeklyReport.Status
