"""
Operations models: geography, assets, profiles, weekly reports, audit.
PostgreSQL-ready; use Django ORM only.
"""
import re
from django.conf import settings
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone


def _slug_code(name, max_chars=5):
    """Generate a short uppercase alphanumeric code from a name."""
    if not name:
        return 'X'
    s = re.sub(r'[^A-Za-z0-9]', '', str(name).upper())[:max_chars]
    return s or 'X'


def _code_exists(qs, code):
    """Check if code exists in qs (case-insensitive) so we match DB UNIQUE behaviour."""
    return qs.filter(code__iexact=code).exists()


def _next_unique_code(qs, base, sep='-', max_length=20, exclude_pk=None):
    """Return base or base-sep-N so that code is unique in qs. Exclude exclude_pk from qs."""
    if exclude_pk is not None:
        qs = qs.exclude(pk=exclude_pk)
    base = (base or '')[:max_length]
    if base and not _code_exists(qs, base):
        return base
    for n in range(1, 10000):
        candidate = f"{base}{sep}{n}"
        if len(candidate) > max_length:
            candidate = base[:max_length - len(sep) - len(str(n))] + sep + str(n)
        if not _code_exists(qs, candidate):
            return candidate
    return f"{base}{sep}1"


# --- Geographic structure ---

class SupportType(models.TextChoices):
    """PEPFAR / site support type (DSD = Differentiated Service Delivery, TAT/TA-SDI = Treatment Acceleration)."""
    DSD = 'DSD', 'DSD'
    TA_SDI = 'TA-SDI', 'TA-SDI'
    TAT = 'TAT', 'TAT'


class Province(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code or not self.code.strip():
            base = _slug_code(self.name, 3)
            qs = Province.objects.all()
            exclude_pk = getattr(self, 'pk', None)
            self.code = _next_unique_code(qs, base, sep='-', max_length=20, exclude_pk=exclude_pk)
            try:
                super().save(*args, **kwargs)
            except IntegrityError as e:
                if 'code' in str(e).lower() or 'operations_province' in str(e):
                    # Collision (e.g. race or case-insensitive DB): force numeric suffix and retry
                    qs_exclude = Province.objects.all()
                    if exclude_pk is not None:
                        qs_exclude = qs_exclude.exclude(pk=exclude_pk)
                    for n in range(1, 10000):
                        self.code = f"{base}-{n}"
                        if not _code_exists(qs_exclude, self.code):
                            super().save(*args, **kwargs)
                            return
                    self.code = f"{base}-1"
                    super().save(*args, **kwargs)
                else:
                    raise
        else:
            super().save(*args, **kwargs)


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.PROTECT, related_name='districts')
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True)
    support_type = models.CharField(
        max_length=20,
        choices=SupportType.choices,
        blank=True,
        help_text='Type of support (e.g. DSD, TAT) from site Excel.',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['province', 'name']
        unique_together = [['province', 'name']]

    def __str__(self):
        return f"{self.name} ({self.province.name})"

    def save(self, *args, **kwargs):
        if not self.code or not self.code.strip():
            prov_code = (self.province.code or '').strip() or _slug_code(self.province.name, 3)
            qs = District.objects.filter(province=self.province)
            self.code = _next_unique_code(qs, prov_code, sep='-', max_length=20, exclude_pk=getattr(self, 'pk', None))
        super().save(*args, **kwargs)


class Facility(models.Model):
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='facilities')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)
    support_type = models.CharField(
        max_length=20,
        choices=SupportType.choices,
        blank=True,
        help_text='Type of support (e.g. DSD, TAT) from site Excel.',
    )
    is_hub = models.BooleanField(
        default=False,
        help_text='Whether this facility is a hub (from hubs CSV).',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['district', 'name']
        unique_together = [['district', 'name']]
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return f"{self.name} ({self.district.name})"

    def save(self, *args, **kwargs):
        if not self.code or not self.code.strip():
            dist_code = (self.district.code or '').strip() or _slug_code(self.district.name, 5)
            qs = Facility.objects.filter(district=self.district)
            self.code = _next_unique_code(qs, dist_code, sep='-', max_length=20, exclude_pk=getattr(self, 'pk', None))
        super().save(*args, **kwargs)


class Lab(models.Model):
    """Laboratory (from labs CSV: name, code, facility type)."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    facility_type = models.CharField(max_length=80, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Labs'

    def __str__(self):
        return f"{self.name} ({self.code})"


# --- Assets ---


class BikeFunctionalityStatus(models.TextChoices):
    FUNCTIONAL = 'FUNCTIONAL', 'Functional'
    UNDER_REPAIR = 'UNDER_REPAIR', 'Under repair'
    OUT_OF_SERVICE = 'OUT_OF_SERVICE', 'Out of service'
    BROKEN_DOWN = 'BROKEN_DOWN', 'Broken down'
    ON_SERVICE = 'ON_SERVICE', 'On service'
    NON_FUNCTIONAL = 'NON_FUNCTIONAL', 'Non-functional'
    RETIRED = 'RETIRED', 'Retired'


class Bike(models.Model):
    registration_number = models.CharField(max_length=60, unique=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='bikes')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    functionality_status = models.CharField(
        max_length=20,
        choices=BikeFunctionalityStatus.choices,
        default=BikeFunctionalityStatus.FUNCTIONAL,
        blank=True,
        help_text='Updated by PC; independent of rider reports.',
    )
    functionality_notes = models.CharField(max_length=255, blank=True)
    functionality_updated_at = models.DateTimeField(null=True, blank=True)
    status_updated_on = models.DateField(
        null=True,
        blank=True,
        help_text='Date the status was last updated (for metrics).',
    )

    class Meta:
        ordering = ['registration_number']

    def __str__(self):
        return f"{self.registration_number} ({self.district.name})"


# --- Roles ---

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    ME = 'ME', 'Monitoring & Evaluation'
    PC = 'PC', 'Provincial Coordinator'
    RIDER = 'RIDER', 'Rider'
    DRIVER = 'DRIVER', 'Driver'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_profile'
    )
    role = models.CharField(max_length=10, choices=Role.choices)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f"{self.user.get_username()} ({self.get_role_display()})"


class PCProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_pc_profile'
    )
    provinces = models.ManyToManyField(Province, related_name='pc_profiles', blank=True)

    class Meta:
        verbose_name = 'PC Profile'
        verbose_name_plural = 'PC Profiles'

    def __str__(self):
        return f"PC: {self.user.get_username()}"


class RiderLeaveType(models.TextChoices):
    ANNUAL = 'ANNUAL', 'Annual leave'
    SICK = 'SICK', 'Sick leave'
    SPECIAL = 'SPECIAL', 'Special leave'


class RiderProfile(models.Model):
    """Province, district, and PEPFAR support type are the source of truth for weekly reports."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_rider_profile'
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='riders',
        null=True,
        blank=True,
        help_text='Derived from district on save if not set.',
    )
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='riders')
    pepfar_support_type = models.CharField(
        max_length=20,
        choices=SupportType.choices,
        blank=True,
    )
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, related_name='riders')
    bike = models.ForeignKey(
        Bike,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_riders'
    )
    leave_type = models.CharField(
        max_length=20,
        choices=RiderLeaveType.choices,
        blank=True,
        help_text='Type of leave: annual, sick, or special. Blank means not on leave.',
    )
    leave_since = models.DateField(
        null=True,
        blank=True,
        help_text='Date leave started (for metrics).',
    )
    is_relief_rider = models.BooleanField(
        default=False,
        help_text='Whether this rider is designated as a relief rider.',
    )

    class Meta:
        verbose_name = 'Rider Profile'
        verbose_name_plural = 'Rider Profiles'

    def __str__(self):
        return f"Rider: {self.user.get_username()} ({self.district.name})"

    def clean(self):
        super().clean()
        if self.facility_id and self.district_id and self.facility.district_id != self.district_id:
            raise ValidationError({'facility': 'Facility must belong to the riders district.'})
        if self.bike_id and self.district_id and self.bike.district_id != self.district_id:
            raise ValidationError({'bike': 'Bike must belong to the riders district.'})

    def save(self, *args, **kwargs):
        if self.district_id and not self.province_id:
            self.province = self.district.province
        self.full_clean()
        super().save(*args, **kwargs)


# --- Rider device & remote config ---


class RiderDevice(models.Model):
    """Registered device for a rider; used to enforce device_id on sync and to disable devices remotely."""
    rider = models.ForeignKey(
        RiderProfile,
        on_delete=models.CASCADE,
        related_name='devices',
    )
    device_id = models.CharField(max_length=255, help_text='Unique device identifier from the client.')
    device_model = models.CharField(max_length=120, blank=True)
    app_version = models.CharField(max_length=60, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text='If False, sync requests from this device are blocked.')

    class Meta:
        verbose_name = 'Rider Device'
        verbose_name_plural = 'Rider Devices'
        unique_together = [['rider', 'device_id']]
        ordering = ['rider', '-last_seen']

    def __str__(self):
        return f"{self.device_id} ({self.rider})"


class RiderRemoteConfig(models.Model):
    """Singleton remote config for rider app (sync interval, batch size, app version, etc.)."""
    sync_interval = models.PositiveIntegerField(
        default=60,
        help_text='Recommended sync interval in seconds.',
    )
    max_batch_size = models.PositiveIntegerField(
        default=10,
        help_text='Max reports per batch.',
    )
    latest_app_version = models.CharField(
        max_length=60,
        blank=True,
        help_text='Latest app version string (e.g. 1.2.0).',
    )
    update_required = models.BooleanField(
        default=False,
        help_text='If True, client should prompt user to update.',
    )

    class Meta:
        verbose_name = 'Rider Remote Config'
        verbose_name_plural = 'Rider Remote Config'

    def __str__(self):
        return 'Rider app config'


# --- Weekly report ---

class TransportRouteType(models.TextChoices):
    """Transport route: From/To can be facility, hub, or lab."""
    FACILITY_FACILITY = 'facility_facility', 'From facility to facility'
    FACILITY_HUB = 'facility_hub', 'From facility to hub'
    FACILITY_LAB = 'facility_lab', 'From facility to lab'
    LAB_FACILITY = 'lab_facility', 'From lab to facility'
    HUB_FACILITY = 'hub_facility', 'From hub to facility'
    HUB_LAB = 'hub_lab', 'From hub to lab'
    LAB_LAB = 'lab_lab', 'From lab to lab'


class ReportStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    REVIEWED = 'REVIEWED', 'Reviewed'
    APPROVED = 'APPROVED', 'Approved'


class RiderWeeklyReport(models.Model):
    """One report per rider per week. Province, district, pepfar_support_type are derived from RiderProfile on creation and are not editable."""

    # Demographics: rider is required; province/district/pepfar_support_type from rider on save (read-only)
    rider = models.ForeignKey(
        'RiderProfile',
        on_delete=models.PROTECT,
        related_name='weekly_reports'
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='rider_weekly_reports',
        null=True,
        blank=True,
        help_text='Set from rider profile on creation; do not edit.',
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='rider_weekly_reports',
        null=True,
        blank=True,
        help_text='Set from rider profile on creation; do not edit.',
    )
    pepfar_support_type = models.CharField(
        max_length=20,
        choices=SupportType.choices,
        blank=True,
        help_text='Set from rider profile on creation; do not edit.',
    )
    relief_rider_name = models.CharField(max_length=120, blank=True)
    is_relief_rider = models.BooleanField(
        default=False,
        help_text='Whether this report is for a relief rider (someone other than the assigned rider).',
    )
    bike_registration = models.CharField(max_length=60, blank=True)
    facility = models.ForeignKey(
        'Facility',
        on_delete=models.PROTECT,
        related_name='rider_weekly_reports',
        null=True,
        blank=True,
        help_text='From facility (riders district).',
    )
    to_facility = models.ForeignKey(
        'Facility',
        on_delete=models.PROTECT,
        related_name='rider_weekly_reports_to_facility',
        null=True,
        blank=True,
        help_text='To facility (district or province).',
    )
    transport_route_type = models.CharField(
        max_length=20,
        choices=TransportRouteType.choices,
        blank=True,
        help_text='Transport route: facility_facility, facility_hub, facility_lab, lab_facility, hub_facility, hub_lab, lab_lab.',
    )
    from_lab = models.ForeignKey(
        'Lab',
        on_delete=models.PROTECT,
        related_name='rider_weekly_reports_from_lab',
        null=True,
        blank=True,
        help_text='From lab (when route type is lab to facility or lab to lab).',
    )
    to_lab = models.ForeignKey(
        'Lab',
        on_delete=models.PROTECT,
        related_name='rider_weekly_reports_to_lab',
        null=True,
        blank=True,
        help_text='To lab (when route type is facility to lab or lab to lab).',
    )

    # Specimens transported
    vl_plasma = models.PositiveIntegerField(default=0)
    vl_dbs = models.PositiveIntegerField(default=0)
    eid_blood = models.PositiveIntegerField(default=0)
    eid_dbs = models.PositiveIntegerField(default=0)
    sputum = models.PositiveIntegerField(default=0)
    sputum_culture_dr = models.PositiveIntegerField(default=0)
    hpv = models.PositiveIntegerField(default=0)
    other_specimen = models.PositiveIntegerField(default=0)
    other_specimen_description = models.CharField(max_length=200, blank=True)

    # Results transported (same structure)
    results_vl_plasma = models.PositiveIntegerField(default=0)
    results_vl_dbs = models.PositiveIntegerField(default=0)
    results_eid_blood = models.PositiveIntegerField(default=0)
    results_eid_dbs = models.PositiveIntegerField(default=0)
    results_sputum = models.PositiveIntegerField(default=0)
    results_sputum_culture_dr = models.PositiveIntegerField(default=0)
    results_hpv = models.PositiveIntegerField(default=0)
    results_other_specimen = models.PositiveIntegerField(default=0)
    results_other_specimen_description = models.CharField(max_length=200, blank=True)

    # Functionality
    fuel_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fuel_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_travelled = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    days_bike_functional = models.PositiveSmallIntegerField(default=0)
    scheduled_visits = models.PositiveIntegerField(default=0)
    actual_visits = models.PositiveIntegerField(default=0)
    ad_hoc_visits = models.PositiveIntegerField(default=0)
    ad_hoc_samples = models.PositiveIntegerField(default=0)
    ad_hoc_results = models.PositiveIntegerField(default=0)

    # Non-pickup days (must sum to 5)
    bike_breakdown = models.PositiveSmallIntegerField(default=0)
    routine_service = models.PositiveSmallIntegerField(default=0)
    no_fuel = models.PositiveSmallIntegerField(default=0)
    sick_leave = models.PositiveSmallIntegerField(default=0)
    annual_leave = models.PositiveSmallIntegerField(default=0)
    inclement_weather = models.PositiveSmallIntegerField(default=0)
    bike_accident = models.PositiveSmallIntegerField(default=0)
    clinical_ip_issue = models.PositiveSmallIntegerField(default=0)
    other_reason = models.CharField(
        max_length=50,
        blank=True,
        default='0',
        help_text='Section 5 Other: 0 or number 15 followed by characters (e.g. 2abc). Number part counts toward non-pickup sum of 5.',
    )

    # Other (Section 6)
    mitigation_measures = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    average_datalogger_temperature = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Average datalogger temperature for this record.',
    )
    date = models.DateField(null=True, blank=True)
    week = models.DateField()  # week marked by the date of the Sunday (week ending)

    # Driver-only: whether this record is for samples transported for the first time (null for rider reports)
    first_time_transport = models.BooleanField(
        null=True,
        blank=True,
        help_text='Driver only: True = first time transport, False = not first time. Null for rider reports.',
    )

    # Section 46 field names: Riders must never modify these (enforced in view + optional revert in save)
    # fuel_allocated, fuel_used are rider-editable; excluded from revert in save()
    SECTION_4_6_FIELD_NAMES = [
        'fuel_allocated', 'fuel_used', 'distance_travelled', 'days_bike_functional',
        'scheduled_visits', 'actual_visits', 'ad_hoc_visits', 'ad_hoc_samples', 'ad_hoc_results',
        'bike_breakdown', 'routine_service', 'no_fuel', 'sick_leave', 'annual_leave',
        'inclement_weather', 'bike_accident', 'clinical_ip_issue', 'other_reason',
        'mitigation_measures', 'comments', 'date', 'week',
    ]
    status = models.CharField(
        max_length=12,
        choices=ReportStatus.choices,
        default=ReportStatus.DRAFT
    )
    # PWA offline sync: client-generated UUID to prevent duplicate submissions when syncing
    client_uuid = models.UUIDField(unique=True, null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-week', '-created_at', 'rider']
        verbose_name = 'Rider Weekly Report'
        verbose_name_plural = 'Rider Weekly Reports'

    @property
    def specimens_total(self):
        return (
            self.vl_plasma + self.vl_dbs + self.eid_blood + self.eid_dbs
            + self.sputum + self.sputum_culture_dr + self.hpv + self.other_specimen
        )

    @property
    def results_total(self):
        return (
            self.results_vl_plasma + self.results_vl_dbs + self.results_eid_blood
            + self.results_eid_dbs + self.results_sputum + self.results_sputum_culture_dr
            + self.results_hpv + self.results_other_specimen
        )

    @property
    def rejection_rows_count(self):
        return self.sample_rejections.count()

    @property
    def rejection_total_sum(self):
        from django.db.models import Sum
        return self.sample_rejections.aggregate(s=Sum('rejected_total'))['s'] or 0

    def _other_reason_numeric(self):
        """Numeric part of other_reason (05) for non-pickup sum."""
        val = (self.other_reason or '').strip()
        if not val or val == '0':
            return 0
        if val[0] in '12345':
            return int(val[0])
        return 0

    def _non_pickup_total(self):
        return (
            self.bike_breakdown + self.routine_service + self.no_fuel
            + self.sick_leave + self.annual_leave + self.inclement_weather
            + self.bike_accident + self.clinical_ip_issue + self._other_reason_numeric()
        )

    def clean(self):
        super().clean()
        non_pickup = self._non_pickup_total()
        bike_functional = self.days_bike_functional or 0
        total = bike_functional + non_pickup
        # Allow 0+0 (draft). Otherwise non-functional days + bike days functional must equal 5.
        if total != 0 and total != 5:
            raise ValidationError(
                {'other_reason': f'Non-functional days (non-pickup) plus bike days functional must equal 5 (current: {non_pickup} + {bike_functional} = {total}).'}
            )
        if self.fuel_used > self.fuel_allocated:
            raise ValidationError(
                {'fuel_used': 'Fuel used cannot exceed fuel allocated.'}
            )
        if self.actual_visits > self.scheduled_visits:
            raise ValidationError(
                {'actual_visits': 'Actual visits cannot exceed scheduled visits.'}
            )
        if self.ad_hoc_samples > 0 and self.ad_hoc_visits == 0:
            raise ValidationError(
                {'ad_hoc_samples': 'Ad hoc samples cannot exist when ad hoc visits is 0.'}
            )

    def save(self, *args, **kwargs):
        # Backend enforcement: if view set _revert_section_4_6_to (Rider edit), reapply those values
        revert_snapshot = getattr(self, '_revert_section_4_6_to', None)
        if isinstance(revert_snapshot, dict):
            rider_editable_s4 = ('fuel_allocated', 'fuel_used', 'distance_travelled')  # rider can edit these; do not revert
            for fname in self.SECTION_4_6_FIELD_NAMES:
                if fname in rider_editable_s4:
                    continue
                if fname in revert_snapshot and hasattr(self, fname):
                    setattr(self, fname, revert_snapshot[fname])
            delattr(self, '_revert_section_4_6_to')
        # Province, district, pepfar_support_type: from RiderProfile only (never from POST). On creation populate; on update keep existing values so tampered POST is ignored and historical accuracy preserved.
        if self.rider_id:
            if not self.pk:
                self.district = self.rider.district
                self.province = getattr(self.rider, 'province', None) or (self.rider.district.province if self.rider.district_id else None)
                self.pepfar_support_type = getattr(self.rider, 'pepfar_support_type', None) or ''
            else:
                existing = RiderWeeklyReport.objects.filter(pk=self.pk).values('province_id', 'district_id', 'pepfar_support_type').first()
                if existing:
                    self.province_id = existing['province_id']
                    self.district_id = existing['district_id']
                    self.pepfar_support_type = existing['pepfar_support_type'] or ''
        if self.facility_id and self.district_id and self.facility.district_id != self.district_id:
            self.facility_id = None  # Facility must be in reports district
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report {self.week}  {self.rider}"


# --- Sample Rejections (multiple rows per report) ---

class SampleRejection(models.Model):
    """One row per rejection group: sample type and rejection counts (sum of reasons = rejected_total)."""
    class SampleType(models.TextChoices):
        VL_PLASMA = 'vl_plasma', 'VL Plasma'
        VL_DBS = 'vl_dbs', 'VL DBS'
        EID_BLOOD = 'eid_blood', 'EID Blood'
        EID_DBS = 'eid_dbs', 'EID DBS'
        SPUTUM = 'sputum', 'Sputum'
        SPUTUM_CULTURE_DR = 'sputum_culture_dr', 'Sputum Culture DR'
        HPV = 'hpv', 'HPV'
        OTHER = 'other', 'Other'

    report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name='sample_rejections',
    )
    sample_type = models.CharField(max_length=50, choices=SampleType.choices)
    rejected_total = models.PositiveIntegerField(
        default=0,
        help_text='Total rejected for this group.',
    )
    rejected_too_old = models.PositiveIntegerField(default=0)
    rejected_patient_info_mismatch = models.PositiveIntegerField(default=0)
    rejected_request_form_missing = models.PositiveIntegerField(default=0)
    rejected_sample_missing = models.PositiveIntegerField(default=0)
    rejected_other = models.PositiveIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0, help_text='Display order within report.')

    class Meta:
        ordering = ['report', 'order', 'pk']
        verbose_name = 'Sample Rejection'
        verbose_name_plural = 'Sample Rejections'

    def _rejection_reasons_sum(self):
        return (
            (self.rejected_too_old or 0) + (self.rejected_patient_info_mismatch or 0)
            + (self.rejected_request_form_missing or 0) + (self.rejected_sample_missing or 0)
            + (self.rejected_other or 0)
        )

    def clean(self):
        super().clean()
        rej_total = self.rejected_total or 0
        if rej_total > 0:
            reasons_sum = self._rejection_reasons_sum()
            if reasons_sum != rej_total:
                raise ValidationError(
                    {'rejected_other': f'Sum of rejection reasons must equal Total rejected (reasons: {reasons_sum}, total: {rej_total}).'}
                )

    def __str__(self):
        return f"{self.get_sample_type_display()}  {self.rejected_total} rejected"


# --- Report audit and version history (Sections 13 edits by PC) ---

class ReportAuditLog(models.Model):
    """One entry per edit to report sections; tamper-proof audit trail."""
    report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name='report_audit_logs'
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='report_audit_entries'
    )
    section = models.CharField(max_length=32)  # e.g. 'section_1', 'section_2', 'section_3'
    old_data = models.JSONField(default=dict)
    new_data = models.JSONField(default=dict)
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f"{self.report_id} {self.section} by {self.edited_by} at {self.edited_at}"


class ReportVersion(models.Model):
    """Full snapshot before each edit to Sections 13 by PC; version_number increments."""
    report = models.ForeignKey(
        RiderWeeklyReport,
        on_delete=models.CASCADE,
        related_name='report_versions'
    )
    version_number = models.PositiveIntegerField()
    snapshot = models.JSONField(default=dict)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='report_versions_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version_number']
        constraints = [
            models.UniqueConstraint(
                fields=['report', 'version_number'],
                name='unique_report_version',
            ),
        ]

    def __str__(self):
        return f"Report {self.report_id} v{self.version_number}"


# --- Audit ---

class AuditAction(models.TextChoices):
    CREATE = 'CREATE', 'Create'
    EDIT = 'EDIT', 'Edit'
    ALLOCATE = 'ALLOCATE', 'Allocate'
    APPROVE = 'APPROVE', 'Approve'
    OVERRIDE = 'OVERRIDE', 'Override'
    SUBMIT = 'SUBMIT', 'Submit'
    REVIEW = 'REVIEW', 'Review'


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='operations_audit_logs'
    )
    action = models.CharField(max_length=12, choices=AuditAction.choices)
    model_name = models.CharField(max_length=80, blank=True)
    object_id = models.CharField(max_length=36, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} by {self.user} at {self.created_at}"


# --- PC-only modules (Provincial Driver Weekly, Referred Samples, Transport Incidents) ---


class ProvincialDriverWeekly(models.Model):
    """Provincial Driver Weekly summary. PC/ME/Admin only; filtered by province/district."""
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='provincial_driver_weekly_entries',
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='provincial_driver_weekly_entries',
    )
    week_ending = models.DateField(help_text='Week ending (Sunday) date.')
    driver_name = models.CharField(max_length=120)
    trips_count = models.PositiveIntegerField(default=0)
    rider_accidents = models.PositiveIntegerField(default=0)
    incomplete_bike_transport_trips = models.PositiveIntegerField(default=0)
    samples_transported = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-week_ending', 'district', 'driver_name']
        verbose_name = 'Provincial Driver Weekly'
        verbose_name_plural = 'Provincial Driver Weekly'

    def __str__(self):
        return f"{self.driver_name}  {self.week_ending} ({self.district.name})"


class ReferredSample(models.Model):
    """Referred sample tracking. PC/ME/Admin only; filtered by province/district."""
    class SampleType(models.TextChoices):
        PLASMA = 'PLASMA', 'Plasma'
        DBS = 'DBS', 'DBS'
        TB = 'TB', 'TB'

    class TestType(models.TextChoices):
        VL = 'VL', 'VL'
        EID = 'EID', 'EID'
        TB = 'TB', 'TB'

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='referred_samples',
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='referred_samples',
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name='referred_samples',
        null=True,
        blank=True,
    )
    from_facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name='referred_samples_from_facility',
        null=True,
        blank=True,
    )
    from_lab = models.ForeignKey(
        Lab,
        on_delete=models.PROTECT,
        related_name='referred_samples_from_lab',
        null=True,
        blank=True,
    )
    to_facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name='referred_samples_to_facility',
        null=True,
        blank=True,
    )
    to_lab = models.ForeignKey(
        Lab,
        on_delete=models.PROTECT,
        related_name='referred_samples_to_lab',
        null=True,
        blank=True,
    )
    sample_type = models.CharField(max_length=20, choices=SampleType.choices, default=SampleType.PLASMA)
    test_type = models.CharField(max_length=20, choices=TestType.choices, default=TestType.VL)
    total_samples_referred_out = models.PositiveIntegerField(default=0)
    swift_consignment_number = models.CharField(max_length=80, blank=True)
    date_referred = models.DateField()
    reference_number = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=60, default='Pending', blank=True)
    notes = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_referred', 'district', 'sample_type']
        verbose_name = 'Referred Sample'
        verbose_name_plural = 'Referred Samples'

    def __str__(self):
        return f"{self.sample_type}  {self.date_referred} ({self.district.name})"


class TransportIncident(models.Model):
    """Accidents / incomplete trips. PC/ME/Admin only; filtered by province/district."""
    class IncidentType(models.TextChoices):
        ACCIDENT = 'ACCIDENT', 'Accident'
        INCOMPLETE_TRIP = 'INCOMPLETE_TRIP', 'Incomplete trip'
        OTHER = 'OTHER', 'Other'

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='transport_incidents',
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='transport_incidents',
    )
    incident_date = models.DateField()
    incident_type = models.CharField(
        max_length=20,
        choices=IncidentType.choices,
        default=IncidentType.OTHER,
    )
    description = models.TextField()
    rider_or_driver_name = models.CharField(max_length=120, blank=True)
    resolved = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-incident_date', 'district']
        verbose_name = 'Transport Incident'
        verbose_name_plural = 'Transport Incidents'

    def __str__(self):
        return f"{self.get_incident_type_display()}  {self.incident_date} ({self.district.name})"


class RiderAccidentRecord(models.Model):
    """PC/ME/Admin accident capture rows (table entry format)."""
    date = models.DateField()
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='rider_accident_records',
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='rider_accident_records',
    )
    number_of_rider_accidents = models.PositiveIntegerField(default=0)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'district']
        verbose_name = 'Rider Accident Record'
        verbose_name_plural = 'Rider Accident Records'

    def __str__(self):
        return f"{self.date}  {self.district.name}: {self.number_of_rider_accidents}"


class IncompleteTripRecord(models.Model):
    """PC/ME/Admin incomplete-trip capture rows (table entry format)."""
    date = models.DateField()
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name='incomplete_trip_records',
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='incomplete_trip_records',
    )
    incomplete_bike_transport_trips = models.PositiveIntegerField(default=0)
    specimens_non_ist_methods = models.PositiveIntegerField(default=0)
    specimens_ambulance = models.PositiveIntegerField(default=0)
    specimens_alternative_ip_transport = models.PositiveIntegerField(default=0)
    specimens_mohcc_arranged_transport = models.PositiveIntegerField(default=0)
    specimens_courier = models.PositiveIntegerField(default=0)
    specimens_other_non_ist_methods = models.PositiveIntegerField(default=0)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'district']
        verbose_name = 'Incomplete Trip Record'
        verbose_name_plural = 'Incomplete Trip Records'

    def __str__(self):
        return f"{self.date}  {self.district.name}: {self.incomplete_bike_transport_trips}"
