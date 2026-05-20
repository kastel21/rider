from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, BaseModelFormSet, inlineformset_factory, modelformset_factory
from django.utils import timezone

from .models import (
    Bike,
    Car,
    District,
    Facility,
    PCAccidentDetail,
    PCDistrictWeeklyTransportStat,
    ReferredSample,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    SampleRejection,
    SupportType,
    TripVisitPurpose,
    TripTransportKind,
    UserProfile,
)
from .selectors import (
    bikes_queryset_for_rider_district,
    get_bikes_queryset,
    get_districts_queryset,
    get_facilities_queryset,
    get_riders_queryset,
)
from .services.trip_facilities import (
    facilities_for_rider_endpoint,
    facility_allowed_for_user,
    route_endpoint_kinds,
)


class RiderReportForm(forms.ModelForm):
    class Meta:
        model = RiderWeeklyReport
        fields = [
            "bike",
            "car",
            "average_datalogger_temperature",
            "distance_travelled",
            "notes",
        ]
        widgets = {
            "bike": forms.Select(attrs={"class": "report-bike-select"}),
            "car": forms.Select(attrs={"class": "report-bike-select"}),
            "average_datalogger_temperature": forms.NumberInput(
                attrs={"class": "report-num-input", "step": "1", "inputmode": "numeric"}
            ),
            "distance_travelled": forms.NumberInput(
                attrs={
                    "class": "report-num-input",
                    "step": "0.01",
                    "min": "0",
                    "inputmode": "decimal",
                }
            ),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "bike": "Bike registration number",
            "car": "Vehicle registration number",
            "average_datalogger_temperature": "Data logger average temperature",
            "distance_travelled": "Distance travelled (week, km)",
        }

    def __init__(self, *args, rider_user=None, **kwargs):
        from .selectors import cars_queryset_for_driver

        self._rider_user = rider_user
        super().__init__(*args, **kwargs)
        role = getattr(getattr(rider_user, "profile", None), "role", None)
        if role == UserProfile.Role.DRIVER:
            self.fields.pop("bike", None)
            qs = cars_queryset_for_driver(rider_user)
            self.fields["car"].queryset = qs
            self.fields["car"].required = False
            if qs.exists():
                self.fields["car"].empty_label = "Select vehicle…"
            else:
                self.fields["car"].empty_label = "No vehicles assigned or in your district"
        else:
            self.fields.pop("car", None)
            qs = bikes_queryset_for_rider_district(rider_user)
            self.fields["bike"].queryset = qs
            self.fields["bike"].required = False
            if qs.exists():
                self.fields["bike"].empty_label = "Select bike…"
            else:
                self.fields["bike"].empty_label = "No bikes in your district"


class PCReportForm(forms.ModelForm):
    """Bike is read-only for PCs (shown in template); riders set it on their own form."""

    class Meta:
        model = RiderWeeklyReport
        fields = [
            "pc_notes",
            "scheduled_visits",
            "distance_travelled",
        ]
        widgets = {
            "pc_notes": forms.Textarea(attrs={"rows": 4}),
            "scheduled_visits": forms.NumberInput(
                attrs={"class": "report-num-input", "min": "0"}
            ),
            "distance_travelled": forms.NumberInput(
                attrs={
                    "class": "report-num-input",
                    "step": "0.01",
                    "min": "0",
                    "inputmode": "decimal",
                }
            ),
        }
        labels = {
            "scheduled_visits": "Scheduled visits",
            "distance_travelled": "Distance travelled (week, km)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ReportReviewForm(forms.Form):
    pc_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))


class SampleRejectionForm(forms.ModelForm):
    class Meta:
        model = SampleRejection
        fields = (
            "sample_type",
            "rejected_total",
            "rejected_too_old",
            "rejected_patient_info_mismatch",
            "rejected_request_form_missing",
            "rejected_sample_missing",
            "rejected_other",
            "order",
        )
        widgets = {
            "order": forms.HiddenInput,
            "sample_type": forms.Select(attrs={"class": "rejection-select"}),
            "rejected_total": forms.NumberInput(
                attrs={"class": "rejection-num", "min": "0"}
            ),
            "rejected_too_old": forms.NumberInput(
                attrs={"class": "rejection-num", "min": "0"}
            ),
            "rejected_patient_info_mismatch": forms.NumberInput(
                attrs={"class": "rejection-num", "min": "0"}
            ),
            "rejected_request_form_missing": forms.NumberInput(
                attrs={"class": "rejection-num", "min": "0"}
            ),
            "rejected_sample_missing": forms.NumberInput(
                attrs={"class": "rejection-num", "min": "0"}
            ),
            "rejected_other": forms.NumberInput(
                attrs={"class": "rejection-num", "min": "0"}
            ),
        }


SampleRejectionFormSet = inlineformset_factory(
    RiderWeeklyReport,
    SampleRejection,
    form=SampleRejectionForm,
    extra=1,
    can_delete=True,
)


_SPECIMEN_FIELDS = (
    "vl_blood_plasma",
    "vl_dbs",
    "eid_blood",
    "eid_dbs",
    "sputum",
    "sputum_culture_dr",
    "hpv",
)
_RESULT_FIELDS = (
    "results_vl_blood_plasma",
    "results_vl_dbs",
    "results_eid_blood",
    "results_eid_dbs",
    "results_sputum",
    "results_sputum_culture_dr",
    "results_hpv",
)
_DECIMAL_TRIP_FIELDS = ("fuel_allocated", "fuel_used")


def _row_has_substantive_trip_data(cleaned: dict) -> bool:
    if cleaned.get("DELETE"):
        return False
    if any((cleaned.get(f) or 0) > 0 for f in _SPECIMEN_FIELDS):
        return True
    if any((cleaned.get(f) or 0) > 0 for f in _RESULT_FIELDS):
        return True
    if (cleaned.get("specimens_other_specify") or "").strip():
        return True
    if (cleaned.get("results_other_specify") or "").strip():
        return True
    fa = cleaned.get("fuel_allocated")
    fu = cleaned.get("fuel_used")
    if fa is not None and fa != "" and Decimal(str(fa)) > 0:
        return True
    if fu is not None and fu != "" and Decimal(str(fu)) > 0:
        return True
    if cleaned.get("visit_purpose") or cleaned.get("route_kind"):
        return True
    if cleaned.get("origin_facility") or cleaned.get("destination_facility"):
        return True
    return False


def _int_clean(cleaned: dict, f: str) -> int:
    v = cleaned.get(f)
    if v is None or v == "":
        return 0
    return int(v)


def _driver_explicit_zero_row(cleaned: dict) -> bool:
    """All numerics are zero, no route/purpose/facilities/other text — driver 'nothing to report' row."""
    if cleaned.get("DELETE"):
        return False
    if _row_has_substantive_trip_data(cleaned):
        return False
    for f in _SPECIMEN_FIELDS + _RESULT_FIELDS:
        if _int_clean(cleaned, f) != 0:
            return False
    for f in _DECIMAL_TRIP_FIELDS:
        v = cleaned.get(f)
        if v is None or v == "":
            return False
        if Decimal(str(v)) != 0:
            return False
    return True


def _row_should_save(cleaned: dict, *, driver_dual_mode: bool) -> bool:
    if cleaned.get("DELETE"):
        return False
    if driver_dual_mode:
        return _row_has_substantive_trip_data(cleaned) or _driver_explicit_zero_row(cleaned)
    return _row_has_substantive_trip_data(cleaned)


class RiderTripEntryForm(forms.ModelForm):
    class Meta:
        model = RiderTripEntry
        fields = [
            "transport_kind",
            "entry_date",
            "visit_purpose",
            "route_kind",
            "origin_facility",
            "destination_facility",
            "vl_blood_plasma",
            "vl_dbs",
            "eid_blood",
            "eid_dbs",
            "sputum",
            "sputum_culture_dr",
            "hpv",
            "specimens_other_specify",
            "results_vl_blood_plasma",
            "results_vl_dbs",
            "results_eid_blood",
            "results_eid_dbs",
            "results_sputum",
            "results_sputum_culture_dr",
            "results_hpv",
            "results_other_specify",
            "fuel_allocated",
            "fuel_used",
        ]
        labels = {
            "specimens_other_specify": "others",
            "results_other_specify": "others",
        }
        widgets = {
            "transport_kind": forms.HiddenInput,
            "entry_date": forms.HiddenInput,
            "visit_purpose": forms.Select(attrs={"class": "trip-visit-purpose"}),
            "route_kind": forms.Select(attrs={"class": "trip-route-kind"}),
            "origin_facility": forms.Select(attrs={"class": "trip-origin-facility"}),
            "destination_facility": forms.Select(attrs={"class": "trip-destination-facility"}),
            "specimens_other_specify": forms.TextInput(attrs={"placeholder": "e.g. 8 CD4, 10 FBC"}),
            "results_other_specify": forms.TextInput(attrs={"placeholder": "e.g. 7 CD4, 5 Stool"}),
        }

    def __init__(self, *args, user=None, pc_province_ids=None, **kwargs):
        self.driver_numeric_required = kwargs.pop("driver_numeric_required", False)
        self.include_transport_kind = kwargs.pop("include_transport_kind", False)
        self._pc_aggregate_fuel = kwargs.pop("pc_aggregate_fuel", False)
        self._entry_user = user
        self._pc_province_ids = pc_province_ids
        super().__init__(*args, **kwargs)
        if self._pc_aggregate_fuel:
            # Per-row fuel is captured via week fuel + rollup; remove trip inputs.
            # clean() still writes zeros into cleaned_data — temporarily drop those
            # keys in _post_clean() so Django 6 construct_instance() never does
            # form["fuel_allocated"] while the fields are absent.
            for name in _DECIMAL_TRIP_FIELDS:
                self.fields.pop(name, None)
        if not self.include_transport_kind:
            self.fields.pop("transport_kind", None)
        elif self._pc_province_ids is not None:
            self.fields["transport_kind"].widget = forms.Select(
                attrs={"class": "trip-transport-kind"}
            )
        self.fields["visit_purpose"].required = False
        # No blank "---------" option; choices only (model has blank=True for empty trip rows).
        self.fields["visit_purpose"].choices = list(TripVisitPurpose.choices)
        self.fields["route_kind"].required = False
        self.fields["origin_facility"].required = False
        self.fields["destination_facility"].required = False
        self.fields["entry_date"].required = False
        if getattr(self.instance, "pk", None) and self.instance.entry_date is not None:
            self.initial.setdefault("entry_date", self.instance.entry_date)
        else:
            self.initial.setdefault("entry_date", timezone.localdate())
        if self.driver_numeric_required:
            num_attrs = {"class": "report-num-input", "min": "0", "inputmode": "numeric", "required": True}
            dec_attrs = {"class": "report-num-input", "min": "0", "step": "0.01", "inputmode": "decimal", "required": True}
            for name in _SPECIMEN_FIELDS + _RESULT_FIELDS:
                self.fields[name].widget.attrs.update(num_attrs)
                self.fields[name].required = True
            for name in _DECIMAL_TRIP_FIELDS:
                if name not in self.fields:
                    continue
                self.fields[name].widget.attrs.update(dec_attrs)
                self.fields[name].required = True
        self._apply_facility_querysets()

    def has_trip_row_fuel_fields(self) -> bool:
        """True when trip rows show editable fuel (aggregate mode drops trip fields)."""
        return "fuel_allocated" in self.fields

    def _post_clean(self):
        """Avoid Django 6 construct_instance() indexing removed aggregate-fuel fields."""
        stash = {}
        cd = getattr(self, "cleaned_data", None)
        if getattr(self, "_pc_aggregate_fuel", False) and isinstance(cd, dict):
            for k in _DECIMAL_TRIP_FIELDS:
                if k in cd:
                    stash[k] = cd.pop(k)
        try:
            super()._post_clean()
        finally:
            if stash and isinstance(getattr(self, "cleaned_data", None), dict):
                self.cleaned_data.update(stash)

    def _clean_driver_required_numerics(self, cleaned: dict) -> None:
        for f in _SPECIMEN_FIELDS + _RESULT_FIELDS:
            raw = cleaned.get(f)
            if raw is None or raw == "":
                self.add_error(f, "Enter a number (use 0 if there is nothing to report).")
            else:
                try:
                    iv = int(raw)
                    if iv < 0:
                        self.add_error(f, "Use zero or a positive number.")
                    else:
                        cleaned[f] = iv
                except (TypeError, ValueError):
                    self.add_error(f, "Enter a valid whole number.")
        for f in _DECIMAL_TRIP_FIELDS:
            raw = cleaned.get(f)
            if raw is None or raw == "":
                self.add_error(f, "Enter a number (use 0 if there is nothing to report).")
            else:
                try:
                    cleaned[f] = Decimal(str(raw))
                    if cleaned[f] < 0:
                        self.add_error(f, "Use zero or a positive number.")
                except Exception:
                    self.add_error(f, "Enter a valid number.")

    def _route_kind_value(self) -> str:
        rk = ""
        if self.data:
            rk = (self.data.get(f"{self.prefix}-route_kind") or "").strip()
        if not rk:
            rk = (self.initial.get("route_kind") or "").strip()
        if not rk and getattr(self.instance, "pk", None):
            rk = (self.instance.route_kind or "").strip()
        return rk

    def _province_ids_for_endpoint(self):
        if self._pc_province_ids is not None:
            return self._pc_province_ids
        return None

    def _apply_facility_querysets(self):
        u = self._entry_user
        rk = self._route_kind_value()
        p_kw = {}
        pids = self._province_ids_for_endpoint()
        if pids is not None:
            p_kw["province_ids"] = pids

        if rk and u is not None:
            self.fields["origin_facility"].queryset = facilities_for_rider_endpoint(
                u, rk, "from", **p_kw
            )
            self.fields["destination_facility"].queryset = facilities_for_rider_endpoint(
                u, rk, "to", **p_kw
            )
            return

        ids = []
        for fname in ("origin_facility", "destination_facility"):
            val = None
            if self.data:
                raw = self.data.get(f"{self.prefix}-{fname}")
                if raw not in (None, ""):
                    try:
                        val = int(raw)
                    except (TypeError, ValueError):
                        pass
            if val is None:
                val = getattr(self.instance, f"{fname}_id", None)
            if val:
                ids.append(val)
        base = Facility.objects.select_related("district", "district__province").order_by("name")
        q = base.filter(pk__in=ids) if ids else base.none()
        self.fields["origin_facility"].queryset = q
        self.fields["destination_facility"].queryset = q

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("DELETE"):
            return cleaned
        if getattr(self, "_pc_aggregate_fuel", False):
            cleaned["fuel_allocated"] = Decimal("0")
            cleaned["fuel_used"] = Decimal("0")
            if getattr(self.instance, "pk", None) and self.instance.entry_date is not None:
                cleaned["entry_date"] = self.instance.entry_date
            else:
                cleaned["entry_date"] = timezone.localdate()
            substantive = _row_has_substantive_trip_data(cleaned)
            explicit_zero = self.driver_numeric_required and _driver_explicit_zero_row(cleaned)
            if not substantive and not explicit_zero:
                return cleaned
            if explicit_zero and not substantive:
                return cleaned
            purpose = (cleaned.get("visit_purpose") or "").strip()
            rk = (cleaned.get("route_kind") or "").strip()
            origin = cleaned.get("origin_facility")
            dest = cleaned.get("destination_facility")
            if not purpose:
                self.add_error("visit_purpose", "Select visit purpose for each trip row with data.")
            if not rk:
                self.add_error("route_kind", "Select route type for each trip row with data.")
            if not origin:
                self.add_error("origin_facility", "Select the From facility.")
            if not dest:
                self.add_error("destination_facility", "Select the To facility.")
            if not (purpose and rk and origin and dest):
                return cleaned
            pair = route_endpoint_kinds(rk)
            if not pair:
                self.add_error("route_kind", "Invalid route type.")
                return cleaned
            u = self._entry_user
            if u is None:
                return cleaned
            p_kw = {}
            if self._pc_province_ids is not None:
                p_kw["province_ids"] = self._pc_province_ids
            if origin.kind != pair[0]:
                self.add_error("origin_facility", "From site does not match this route type.")
            elif not facility_allowed_for_user(u, origin, rk, "from", **p_kw):
                self.add_error("origin_facility", "From site is not valid for your scope.")
            if dest.kind != pair[1]:
                self.add_error("destination_facility", "To site does not match this route type.")
            elif not facility_allowed_for_user(u, dest, rk, "to", **p_kw):
                self.add_error("destination_facility", "To site is not valid for your scope.")
            return cleaned
        if self.driver_numeric_required:
            self._clean_driver_required_numerics(cleaned)
            if self._errors:
                return cleaned

        # Entry date is system-managed (read-only in UI).
        if getattr(self.instance, "pk", None) and self.instance.entry_date is not None:
            cleaned["entry_date"] = self.instance.entry_date
        else:
            cleaned["entry_date"] = timezone.localdate()

        fuel_allocated = cleaned.get("fuel_allocated")
        fuel_used = cleaned.get("fuel_used")
        if fuel_allocated is None or fuel_allocated == "":
            fuel_allocated = Decimal("0")
        else:
            fuel_allocated = Decimal(str(fuel_allocated))
        if fuel_used is None or fuel_used == "":
            fuel_used = Decimal("0")
        else:
            fuel_used = Decimal(str(fuel_used))
        cleaned["fuel_allocated"] = fuel_allocated
        cleaned["fuel_used"] = fuel_used

        if fuel_used > fuel_allocated:
            self.add_error("fuel_used", "Fuel used cannot exceed fuel allocated.")

        substantive = _row_has_substantive_trip_data(cleaned)
        explicit_zero = self.driver_numeric_required and _driver_explicit_zero_row(cleaned)

        if not substantive and not explicit_zero:
            return cleaned
        if explicit_zero and not substantive:
            return cleaned

        purpose = (cleaned.get("visit_purpose") or "").strip()
        rk = (cleaned.get("route_kind") or "").strip()
        origin = cleaned.get("origin_facility")
        dest = cleaned.get("destination_facility")

        if not purpose:
            self.add_error("visit_purpose", "Select visit purpose for each trip row with data.")
        if not rk:
            self.add_error("route_kind", "Select route type for each trip row with data.")
        if not origin:
            self.add_error("origin_facility", "Select the From facility.")
        if not dest:
            self.add_error("destination_facility", "Select the To facility.")

        if not (purpose and rk and origin and dest):
            return cleaned

        pair = route_endpoint_kinds(rk)
        if not pair:
            self.add_error("route_kind", "Invalid route type.")
            return cleaned

        u = self._entry_user
        if u is None:
            return cleaned

        p_kw = {}
        if self._pc_province_ids is not None:
            p_kw["province_ids"] = self._pc_province_ids

        if origin.kind != pair[0]:
            self.add_error("origin_facility", "From site does not match this route type.")
        elif not facility_allowed_for_user(u, origin, rk, "from", **p_kw):
            self.add_error("origin_facility", "From site is not valid for your scope.")

        if dest.kind != pair[1]:
            self.add_error("destination_facility", "To site does not match this route type.")
        elif not facility_allowed_for_user(u, dest, rk, "to", **p_kw):
            self.add_error("destination_facility", "To site is not valid for your scope.")

        return cleaned


class RiderTripEntryInlineFormSet(BaseInlineFormSet):
    def __init__(
        self,
        *args,
        user=None,
        pc_province_ids=None,
        fixed_transport_kind=None,
        driver_dual_mode=False,
        include_transport_kind=False,
        **kwargs,
    ):
        self._form_user = user
        self._pc_province_ids = pc_province_ids
        self.fixed_transport_kind = fixed_transport_kind
        self.driver_dual_mode = driver_dual_mode
        self.include_transport_kind = include_transport_kind
        self.pc_aggregate_fuel = kwargs.pop("pc_aggregate_fuel", False)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs["user"] = self._form_user
        kwargs["pc_province_ids"] = self._pc_province_ids
        kwargs["driver_numeric_required"] = self.driver_dual_mode
        kwargs["include_transport_kind"] = self.include_transport_kind
        kwargs["pc_aggregate_fuel"] = self.pc_aggregate_fuel
        form = super()._construct_form(i, **kwargs)
        if self.driver_dual_mode and self.fixed_transport_kind is not None and not form.instance.pk:
            form.instance.transport_kind = self.fixed_transport_kind
        return form

    def save(self, commit=True):
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data:
                continue
            cd = form.cleaned_data
            if cd.get("DELETE"):
                continue
            if not _row_should_save(cd, driver_dual_mode=self.driver_dual_mode):
                continue
            if self.include_transport_kind:
                pass
            elif self.fixed_transport_kind is not None:
                form.instance.transport_kind = self.fixed_transport_kind
            else:
                form.instance.transport_kind = TripTransportKind.LEGACY
        return super().save(commit=commit)


RiderTripEntryFormSet = inlineformset_factory(
    RiderWeeklyReport,
    RiderTripEntry,
    form=RiderTripEntryForm,
    formset=RiderTripEntryInlineFormSet,
    extra=1,
    can_delete=True,
)

# PC review/edit: no blank trailing row (riders use extra=1 to add trips).
RiderTripEntryPCFormSet = inlineformset_factory(
    RiderWeeklyReport,
    RiderTripEntry,
    form=RiderTripEntryForm,
    formset=RiderTripEntryInlineFormSet,
    extra=0,
    can_delete=True,
)


# --- PC master data (bikes, facilities, riders) ---

_BIKE_SNP_INT_FIELDS = (
    "snp_bike_breakdown",
    "snp_bike_routine_service",
    "snp_bike_no_fuel",
    "snp_rider_sick_leave",
    "snp_rider_annual_leave",
    "snp_inclement_weather",
    "snp_bike_accident",
    "snp_clinical_ip",
    "snp_other",
)


class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = [
            "code",
            "district",
            "notes",
            "active",
            *_BIKE_SNP_INT_FIELDS,
            "snp_other_specify",
            "mitigation_measures",
            "affected_facilities",
        ]
        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "pc-bike-input",
                    "autocomplete": "off",
                    "placeholder": "e.g. BIKE-001",
                }
            ),
            "district": forms.Select(attrs={"class": "report-bike-select pc-bike-district"}),
            "notes": forms.Textarea(
                attrs={"rows": 3, "class": "pc-bike-notes", "placeholder": "Optional notes…"}
            ),
            "active": forms.CheckboxInput(attrs={"class": "pc-bike-checkbox"}),
            "mitigation_measures": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "pc-bike-mitigation",
                    "placeholder": "Describe mitigation or follow-up actions…",
                }
            ),
            "affected_facilities": forms.CheckboxSelectMultiple,
            "snp_other_specify": forms.Textarea(
                attrs={
                    "class": "pc-snp-specify",
                    "rows": 2,
                    "placeholder": "E.g. 1 Public Holiday; vacant post; rider reassigned…",
                }
            ),
            **{
                name: forms.NumberInput(attrs={"class": "report-num-input", "min": "0"})
                for name in _BIKE_SNP_INT_FIELDS
            },
        }
        labels = {
            "snp_bike_breakdown": "Bike breakdown",
            "snp_bike_routine_service": "Bike on routine service / maintenance",
            "snp_bike_no_fuel": "Bike had no fuel",
            "snp_rider_sick_leave": "Rider on sick leave",
            "snp_rider_annual_leave": "Rider on annual leave",
            "snp_inclement_weather": "Inclement weather",
            "snp_bike_accident": "Bike accident / damaged",
            "snp_clinical_ip": "Clinical IPs related issues",
            "snp_other": "other reasons (days)",
            "snp_other_specify": "other reasons",
            "mitigation_measures": "Mitigation measures",
            "affected_facilities": "Affected facilities",
        }

    def __init__(self, *args, pc_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pc_user is not None:
            from .selectors import get_districts_queryset, get_facilities_queryset

            self.fields["district"].queryset = get_districts_queryset(pc_user)
            district_id = None
            if self.data and self.data.get("district"):
                try:
                    district_id = int(self.data.get("district"))
                except (TypeError, ValueError):
                    district_id = None
            elif getattr(self.instance, "district_id", None):
                district_id = self.instance.district_id
            af = self.fields["affected_facilities"]
            if district_id:
                af.queryset = get_facilities_queryset(pc_user, district_id=district_id).order_by(
                    "name"
                )
            else:
                af.queryset = Facility.objects.none()
            af.required = False

    def clean_affected_facilities(self):
        facilities = self.cleaned_data.get("affected_facilities")
        if not facilities:
            return []
        district = self.cleaned_data.get("district")
        if district is None and self.instance.pk:
            district = self.instance.district
        if district is None:
            raise ValidationError("Choose a district before selecting affected facilities.")
        bad = [f for f in facilities if f.district_id != district.id]
        if bad:
            raise ValidationError(
                "Each affected facility must belong to the bike's district."
            )
        return facilities


class CarForm(forms.ModelForm):
    """PC vehicle (car) master data — same specimen non-pickup status grid as bikes."""

    class Meta:
        model = Car
        fields = [
            "code",
            "district",
            "notes",
            "active",
            *_BIKE_SNP_INT_FIELDS,
            "snp_other_specify",
            "mitigation_measures",
            "affected_facilities",
        ]
        widgets = {
            "code": forms.TextInput(
                attrs={
                    "class": "pc-bike-input",
                    "autocomplete": "off",
                    "placeholder": "e.g. GHCC3159",
                }
            ),
            "district": forms.Select(attrs={"class": "report-bike-select pc-bike-district"}),
            "notes": forms.Textarea(
                attrs={"rows": 3, "class": "pc-bike-notes", "placeholder": "Optional notes…"}
            ),
            "active": forms.CheckboxInput(attrs={"class": "pc-bike-checkbox"}),
            "mitigation_measures": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "pc-bike-mitigation",
                    "placeholder": "Describe mitigation or follow-up actions…",
                }
            ),
            "affected_facilities": forms.CheckboxSelectMultiple,
            "snp_other_specify": forms.Textarea(
                attrs={
                    "class": "pc-snp-specify",
                    "rows": 2,
                    "placeholder": "E.g. 1 Public Holiday; vacant post; driver reassigned…",
                }
            ),
            **{
                name: forms.NumberInput(attrs={"class": "report-num-input", "min": "0"})
                for name in _BIKE_SNP_INT_FIELDS
            },
        }
        labels = {
            "snp_bike_breakdown": "Vehicle breakdown",
            "snp_bike_routine_service": "Vehicle on routine service / maintenance",
            "snp_bike_no_fuel": "Vehicle had no fuel",
            "snp_rider_sick_leave": "Driver on sick leave",
            "snp_rider_annual_leave": "Driver on annual leave",
            "snp_inclement_weather": "Inclement weather",
            "snp_bike_accident": "Vehicle accident / damaged",
            "snp_clinical_ip": "Clinical IPs related issues",
            "snp_other": "other reasons (days)",
            "snp_other_specify": "other reasons",
            "mitigation_measures": "Mitigation measures",
            "affected_facilities": "Affected facilities",
        }

    def __init__(self, *args, pc_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pc_user is not None:
            from .selectors import get_districts_queryset, get_facilities_queryset

            self.fields["district"].queryset = get_districts_queryset(pc_user)
            district_id = None
            if self.data and self.data.get("district"):
                try:
                    district_id = int(self.data.get("district"))
                except (TypeError, ValueError):
                    district_id = None
            elif getattr(self.instance, "district_id", None):
                district_id = self.instance.district_id
            af = self.fields["affected_facilities"]
            if district_id:
                af.queryset = get_facilities_queryset(pc_user, district_id=district_id).order_by(
                    "name"
                )
            else:
                af.queryset = Facility.objects.none()
            af.required = False

    def clean_affected_facilities(self):
        facilities = self.cleaned_data.get("affected_facilities")
        if not facilities:
            return []
        district = self.cleaned_data.get("district")
        if district is None and self.instance.pk:
            district = self.instance.district
        if district is None:
            raise ValidationError("Choose a district before selecting affected facilities.")
        bad = [f for f in facilities if f.district_id != district.id]
        if bad:
            raise ValidationError(
                "Each affected facility must belong to the vehicle's district."
            )
        return facilities


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ["district", "name", "site_code", "kind", "support_type"]

    def __init__(self, *args, pc_user=None, hub_only=False, **kwargs):
        super().__init__(*args, **kwargs)
        if pc_user is not None:
            from .selectors import get_districts_queryset

            self.fields["district"].queryset = get_districts_queryset(pc_user)
        if hub_only:
            self.fields["kind"].initial = Facility.Kind.HUB
            self.fields["kind"].widget = forms.HiddenInput()


class RiderProfileEditForm(forms.ModelForm):
    password1 = forms.CharField(
        label="New password",
        required=False,
        strip=False,
        widget=forms.PasswordInput,
        help_text="Leave blank to keep the current password.",
    )
    password2 = forms.CharField(
        label="Confirm new password",
        required=False,
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = RiderProfile
        fields = ["province", "district", "support_type", "facility", "bike", "car"]
        widgets = {
            "bike": forms.Select(attrs={"class": "report-bike-select"}),
            "car": forms.Select(attrs={"class": "report-bike-select"}),
        }
        labels = {
            "bike": "Bike registration number",
            "car": "Vehicle registration number",
        }

    def __init__(self, *args, pc_user=None, **kwargs):
        self._pc_user = pc_user
        super().__init__(*args, **kwargs)
        if pc_user is None:
            return
        from .selectors import (
            get_bikes_queryset,
            get_cars_queryset,
            get_districts_queryset,
            get_facilities_queryset,
            get_provinces_queryset,
        )

        self.fields["province"].queryset = get_provinces_queryset(pc_user)
        self.fields["district"].queryset = get_districts_queryset(pc_user)
        district_id = None
        if self.data and self.data.get("district"):
            try:
                district_id = int(self.data.get("district"))
            except (TypeError, ValueError):
                district_id = None
        elif self.instance.pk and self.instance.district_id:
            district_id = self.instance.district_id

        role = None
        if self.instance.pk:
            try:
                role = self.instance.user.profile.role
            except Exception:
                role = None

        if role == UserProfile.Role.DRIVER:
            self.fields.pop("bike", None)
            if district_id:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user, district_id=district_id)
                self.fields["car"].queryset = get_cars_queryset(pc_user, district_id=district_id)
            else:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user)
                self.fields["car"].queryset = get_cars_queryset(pc_user)
            self.field_order = [
                "province",
                "district",
                "support_type",
                "facility",
                "car",
                "password1",
                "password2",
            ]
        else:
            self.fields.pop("car", None)
            if district_id:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user, district_id=district_id)
                self.fields["bike"].queryset = get_bikes_queryset(pc_user, district_id=district_id)
            else:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user)
                self.fields["bike"].queryset = get_bikes_queryset(pc_user)
            self.field_order = [
                "province",
                "district",
                "support_type",
                "facility",
                "bike",
                "password1",
                "password2",
            ]

    def clean(self):
        cleaned = super().clean()
        district = cleaned.get("district")
        facility = cleaned.get("facility")
        bike = cleaned.get("bike")
        car = cleaned.get("car")
        if district and facility and facility.district_id != district.id:
            self.add_error("facility", "Facility must belong to the selected district.")
        try:
            role = self.instance.user.profile.role
        except Exception:
            role = None
        if role == UserProfile.Role.DRIVER:
            if district and car and car.district_id and car.district_id != district.id:
                self.add_error("car", "Vehicle must belong to the selected district.")
        else:
            if district and bike and bike.district_id and bike.district_id != district.id:
                self.add_error("bike", "Bike must belong to the selected district.")

        p1 = cleaned.get("password1") or ""
        p2 = cleaned.get("password2") or ""
        if p1 or p2:
            if p1 != p2:
                self.add_error("password2", "The two password fields do not match.")
            elif p1:
                validate_password(p1, user=self.instance.user)
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        if obj.district_id:
            obj.province = obj.district.province
        try:
            role = self.instance.user.profile.role
        except Exception:
            role = None
        if role == UserProfile.Role.DRIVER:
            obj.bike_id = None
        elif role == UserProfile.Role.RIDER:
            obj.car_id = None
        new_password = self.cleaned_data.get("password1")
        if commit:
            obj.save()
            if new_password:
                u = obj.user
                u.set_password(new_password)
                u.save(update_fields=["password"])
        return obj


class RiderCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, strip=False)
    district = forms.ModelChoiceField(queryset=District.objects.none())
    support_type = forms.ChoiceField(choices=[("", "---------")] + list(SupportType.choices), required=False)
    facility = forms.ModelChoiceField(queryset=Facility.objects.none(), required=False)
    bike = forms.ModelChoiceField(queryset=Bike.objects.none(), required=False)
    car = forms.ModelChoiceField(
        queryset=Car.objects.none(),
        required=False,
        label="Vehicle registration number",
    )

    def __init__(self, *args, pc_user=None, profile_role=None, **kwargs):
        self._pc_user = pc_user
        self._profile_role = profile_role or UserProfile.Role.RIDER
        super().__init__(*args, **kwargs)
        if pc_user is None:
            return
        from .selectors import get_bikes_queryset, get_cars_queryset, get_districts_queryset, get_facilities_queryset

        self.fields["district"].queryset = get_districts_queryset(pc_user)
        district_id = None
        if self.data and self.data.get("district"):
            try:
                district_id = int(self.data.get("district"))
            except (TypeError, ValueError):
                district_id = None
        if self._profile_role == UserProfile.Role.DRIVER:
            self.fields.pop("bike", None)
            if district_id:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user, district_id=district_id)
                self.fields["car"].queryset = get_cars_queryset(pc_user, district_id=district_id)
            else:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user)
                self.fields["car"].queryset = get_cars_queryset(pc_user)
        else:
            self.fields.pop("car", None)
            if district_id:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user, district_id=district_id)
                self.fields["bike"].queryset = get_bikes_queryset(pc_user, district_id=district_id)
            else:
                self.fields["facility"].queryset = get_facilities_queryset(pc_user)
                self.fields["bike"].queryset = get_bikes_queryset(pc_user)

    def clean_username(self):
        username = self.cleaned_data["username"]
        User = get_user_model()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("The two password fields do not match.")
        return p2

    def clean(self):
        cleaned = super().clean()
        district = cleaned.get("district")
        facility = cleaned.get("facility")
        bike = cleaned.get("bike")
        car = cleaned.get("car")
        if district and facility and facility.district_id != district.id:
            self.add_error("facility", "Facility must belong to the selected district.")
        if self._profile_role == UserProfile.Role.DRIVER:
            if district and car and car.district_id and car.district_id != district.id:
                self.add_error("car", "Vehicle must belong to the selected district.")
        else:
            if district and bike and bike.district_id and bike.district_id != district.id:
                self.add_error("bike", "Bike must belong to the selected district.")
        return cleaned

    def save(self):
        """Create User, UserProfile (rider or driver role), and RiderProfile."""
        from django.db import transaction

        User = get_user_model()
        data = self.cleaned_data
        with transaction.atomic():
            user = User.objects.create_user(
                username=data["username"],
                email=data.get("email") or "",
                password=data["password1"],
            )
            UserProfile.objects.create(user=user, role=self._profile_role)
            district = data["district"]
            st = data.get("support_type") or ""
            if self._profile_role == UserProfile.Role.DRIVER:
                RiderProfile.objects.create(
                    user=user,
                    province=district.province,
                    district=district,
                    support_type=st,
                    facility=data.get("facility"),
                    car=data.get("car"),
                )
            else:
                RiderProfile.objects.create(
                    user=user,
                    province=district.province,
                    district=district,
                    support_type=st,
                    facility=data.get("facility"),
                    bike=data.get("bike"),
                )
        return user


class ReferredSampleForm(forms.ModelForm):
    class Meta:
        model = ReferredSample
        fields = [
            "from_facility",
            "sample_type",
            "test_type",
            "total_samples_referred_out",
            "to_facility",
            "swift_consignment_number",
            "comments",
        ]
        labels = {
            "from_facility": "Lab (referring site)",
            "to_facility": "Lab samples referred to",
            "sample_type": "Sample type",
            "test_type": "Test type",
            "total_samples_referred_out": "Total number of samples referred out",
            "swift_consignment_number": "Swift consignment number",
            "comments": "Comments",
        }
        widgets = {
            "from_facility": forms.Select(attrs={"class": "report-bike-select"}),
            "to_facility": forms.Select(attrs={"class": "report-bike-select"}),
            "sample_type": forms.Select(attrs={"class": "report-bike-select"}),
            "test_type": forms.Select(attrs={"class": "report-bike-select"}),
            "total_samples_referred_out": forms.NumberInput(
                attrs={"class": "report-num-input", "min": "0", "inputmode": "numeric"}
            ),
            "swift_consignment_number": forms.TextInput(attrs={"class": "report-num-input"}),
            "comments": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)
        fac_qs = get_facilities_queryset(user).order_by("district__name", "name")
        self.fields["from_facility"].queryset = fac_qs
        self.fields["to_facility"].queryset = fac_qs
        self.fields["to_facility"].required = False
        self.fields["to_facility"].empty_label = "—"
        if fac_qs.exists():
            self.fields["from_facility"].empty_label = "Select lab…"
        else:
            self.fields["from_facility"].empty_label = "No facilities in your scope"


PC_TRANS_SAVE_ACCIDENTS = "accidents"
PC_TRANS_SAVE_INCOMPLETE = "incomplete"
PC_TRANS_FORM_PREFIX_ACCIDENTS = "pc_trans_acc"
PC_TRANS_FORM_PREFIX_ACCIDENT_DETAILS = "pc_acc_det"
PC_TRANS_FORM_PREFIX_INCOMPLETE = "pc_trans_inc"

_PC_TRANS_INCOMPLETE_NUM_FIELDS = (
    "incomplete_bike_transport_trips",
    "specimens_non_ist_total",
    "specimens_ambulance",
    "specimens_alternative_ip_transport",
    "specimens_mohcc_arranged_transport",
    "specimens_courier",
    "specimens_other_non_ist",
)

_PC_TRANS_DISTRICT_WIDGET = forms.Select(attrs={"class": "report-bike-select pc-trans-district"})
_PC_TRANS_COMMENTS_WIDGET = forms.Textarea(attrs={"rows": 2, "class": "pc-trans-comments"})
_PC_TRANS_NUM_ATTRS = {"class": "report-num-input", "min": "0", "inputmode": "numeric"}


def _pc_trans_apply_district_field(form, pc_user):
    form.fields["district"].queryset = get_districts_queryset(pc_user).select_related("province").order_by(
        "province__name", "name"
    )
    form.fields["district"].required = False
    form.fields["district"].empty_label = "Select district…"


class PCDistrictWeeklyTransportStatAccidentsForm(forms.ModelForm):
    class Meta:
        model = PCDistrictWeeklyTransportStat
        fields = ["district", "rider_accidents"]
        widgets = {"district": _PC_TRANS_DISTRICT_WIDGET}
        labels = {"rider_accidents": "Number of rider accidents"}

    def __init__(self, *args, pc_user=None, **kwargs):
        self._pc_user = pc_user
        super().__init__(*args, **kwargs)
        _pc_trans_apply_district_field(self, pc_user)
        self.fields["rider_accidents"].required = False
        self.fields["rider_accidents"].widget.attrs.update(_PC_TRANS_NUM_ATTRS)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("DELETE"):
            return cleaned
        ra = cleaned.get("rider_accidents")
        if ra is None or ra == "":
            cleaned["rider_accidents"] = 0
        else:
            cleaned["rider_accidents"] = int(ra)
        d = cleaned.get("district")
        if d is None and cleaned["rider_accidents"] == 0:
            return cleaned
        if d is None:
            raise ValidationError({"district": "Select a district for this row, or clear the accident count."})
        if self._pc_user is not None and not get_districts_queryset(self._pc_user).filter(pk=d.pk).exists():
            raise ValidationError({"district": "District not in your scope."})
        return cleaned

    def _post_clean(self):
        if not hasattr(self, "cleaned_data") or not self.cleaned_data:
            return super()._post_clean()
        if self.cleaned_data.get("DELETE"):
            return super()._post_clean()
        d = self.cleaned_data.get("district")
        ra = int(self.cleaned_data.get("rider_accidents") or 0)
        if d is None and ra == 0:
            return
        super()._post_clean()


_PC_ACC_RIDER_BIKE_WIDGET = forms.Select(attrs={"class": "report-bike-select pc-trans-district"})
_PC_ACC_CAUSE_WIDGET = forms.Textarea(attrs={"rows": 3, "class": "pc-trans-comments"})
_PC_ACC_STATUS_WIDGET = forms.Select(attrs={"class": "report-bike-select pc-trans-district"})


class PCAccidentDetailForm(forms.ModelForm):
    class Meta:
        model = PCAccidentDetail
        fields = ["rider", "bike", "accident_cause", "bike_status", "rider_injury_status"]
        widgets = {
            "rider": _PC_ACC_RIDER_BIKE_WIDGET,
            "bike": _PC_ACC_RIDER_BIKE_WIDGET,
            "accident_cause": _PC_ACC_CAUSE_WIDGET,
            "bike_status": _PC_ACC_STATUS_WIDGET,
            "rider_injury_status": _PC_ACC_STATUS_WIDGET,
        }
        labels = {
            "accident_cause": "Cause of accident",
            "bike_status": "Status of bike",
            "rider_injury_status": "Status of rider",
        }

    def __init__(self, *args, pc_user=None, **kwargs):
        self._pc_user = pc_user
        super().__init__(*args, **kwargs)
        r_qs = get_riders_queryset(pc_user).order_by(
            "district__province__name", "district__name", "user__last_name", "user__first_name"
        )
        self.fields["rider"].queryset = r_qs
        self.fields["rider"].required = False
        self.fields["rider"].empty_label = "Select rider…"
        if not r_qs.exists():
            self.fields["rider"].empty_label = "No riders in your scope"
        b_qs = get_bikes_queryset(pc_user).order_by("code")
        self.fields["bike"].queryset = b_qs
        self.fields["bike"].required = False
        self.fields["bike"].empty_label = "Select bike…"
        if not b_qs.exists():
            self.fields["bike"].empty_label = "No bikes in your scope"
        if "DELETE" in self.fields:
            self.fields["DELETE"].label = "Remove"
            self.fields["DELETE"].widget.attrs.setdefault("class", "pc-acc-del")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("DELETE"):
            return cleaned
        rider = cleaned.get("rider")
        bike = cleaned.get("bike")
        cause = (cleaned.get("accident_cause") or "").strip()
        if rider is None and bike is None and not cause:
            return cleaned
        if rider is None:
            raise ValidationError({"rider": "Select a rider, or clear this row."})
        if bike is None:
            raise ValidationError({"bike": "Select a bike for this accident."})
        if self._pc_user is not None:
            if not get_riders_queryset(self._pc_user).filter(pk=rider.pk).exists():
                raise ValidationError({"rider": "Rider not in your scope."})
            if not get_bikes_queryset(self._pc_user).filter(pk=bike.pk).exists():
                raise ValidationError({"bike": "Bike not in your scope."})
        return cleaned

    def _post_clean(self):
        if not hasattr(self, "cleaned_data") or not self.cleaned_data:
            return super()._post_clean()
        if self.cleaned_data.get("DELETE"):
            return super()._post_clean()
        rider = self.cleaned_data.get("rider")
        bike = self.cleaned_data.get("bike")
        if rider is None and bike is None:
            return
        super()._post_clean()


class PCAccidentDetailBaseFormSet(BaseModelFormSet):
    def __init__(self, *args, pc_user=None, week_start=None, **kwargs):
        self._pc_user = pc_user
        self._week_start = week_start
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs["pc_user"] = self._pc_user
        return super()._construct_form(i, **kwargs)

    def save(self, commit=True):
        instances = super().save(commit=False)
        instances = [obj for obj in instances if obj.rider_id is not None and obj.bike_id is not None]
        for obj in instances:
            obj.week_start = self._week_start
        if commit:
            for obj in self.deleted_objects:
                obj.delete()
            for obj in instances:
                obj.save()
            self.save_m2m()
        return instances


PCAccidentDetailFormSet = modelformset_factory(
    PCAccidentDetail,
    form=PCAccidentDetailForm,
    formset=PCAccidentDetailBaseFormSet,
    extra=1,
    can_delete=True,
)


class PCDistrictWeeklyTransportStatIncompleteForm(forms.ModelForm):
    class Meta:
        model = PCDistrictWeeklyTransportStat
        fields = [
            "district",
            "incomplete_bike_transport_trips",
            "specimens_non_ist_total",
            "specimens_ambulance",
            "specimens_alternative_ip_transport",
            "specimens_mohcc_arranged_transport",
            "specimens_courier",
            "specimens_other_non_ist",
            "comments",
        ]
        widgets = {"district": _PC_TRANS_DISTRICT_WIDGET, "comments": _PC_TRANS_COMMENTS_WIDGET}
        labels = {
            "incomplete_bike_transport_trips": "Total number of incomplete bike transport trips",
            "specimens_non_ist_total": "Total number of specimens transported by non-IST methods",
            "specimens_ambulance": "Number of specimens transported by ambulance",
            "specimens_alternative_ip_transport": "Number of specimens transported by alternative IP transport",
            "specimens_mohcc_arranged_transport": "Number of specimens transported by MoHCC arranged transport",
            "specimens_courier": "Number of specimens transported by courier",
            "specimens_other_non_ist": "Number of specimens transported by other non-IST methods",
            "comments": "Comments",
        }

    def __init__(self, *args, pc_user=None, **kwargs):
        self._pc_user = pc_user
        super().__init__(*args, **kwargs)
        _pc_trans_apply_district_field(self, pc_user)
        for name in _PC_TRANS_INCOMPLETE_NUM_FIELDS:
            self.fields[name].required = False
            self.fields[name].widget.attrs.update(_PC_TRANS_NUM_ATTRS)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("DELETE"):
            return cleaned
        for f in _PC_TRANS_INCOMPLETE_NUM_FIELDS:
            v = cleaned.get(f)
            if v is None or v == "":
                cleaned[f] = 0
            else:
                cleaned[f] = int(v)
        d = cleaned.get("district")
        nums = sum(int(cleaned.get(f) or 0) for f in _PC_TRANS_INCOMPLETE_NUM_FIELDS)
        comments = (cleaned.get("comments") or "").strip()
        if d is None and nums == 0 and not comments:
            return cleaned
        if d is None:
            raise ValidationError({"district": "Select a district for this row, or clear all values."})
        if self._pc_user is not None and not get_districts_queryset(self._pc_user).filter(pk=d.pk).exists():
            raise ValidationError({"district": "District not in your scope."})
        return cleaned

    def _post_clean(self):
        if not hasattr(self, "cleaned_data") or not self.cleaned_data:
            return super()._post_clean()
        if self.cleaned_data.get("DELETE"):
            return super()._post_clean()
        d = self.cleaned_data.get("district")
        nums = sum(int(self.cleaned_data.get(f) or 0) for f in _PC_TRANS_INCOMPLETE_NUM_FIELDS)
        comments = (self.cleaned_data.get("comments") or "").strip()
        if d is None and nums == 0 and not comments:
            return
        super()._post_clean()


class PCDistrictWeeklyTransportStatBaseFormSet(BaseModelFormSet):
    def __init__(self, *args, pc_user=None, week_start=None, **kwargs):
        self._pc_user = pc_user
        self._week_start = week_start
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs["pc_user"] = self._pc_user
        return super()._construct_form(i, **kwargs)

    def clean(self):
        super().clean()
        if any(self._errors):
            return
        seen = set()
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                continue
            d = form.cleaned_data.get("district")
            if d is None:
                continue
            if d.pk in seen:
                raise ValidationError("Each district can only appear once per week.")
            seen.add(d.pk)
        return

    def save(self, commit=True):
        instances = super().save(commit=False)
        instances = [obj for obj in instances if obj.district_id is not None]
        for obj in instances:
            obj.week_start = self._week_start
        if commit:
            for obj in self.deleted_objects:
                obj.delete()
            for obj in instances:
                obj.save()
            self.save_m2m()
        return instances


PCDistrictWeeklyTransportStatAccidentsFormSet = modelformset_factory(
    PCDistrictWeeklyTransportStat,
    form=PCDistrictWeeklyTransportStatAccidentsForm,
    formset=PCDistrictWeeklyTransportStatBaseFormSet,
    extra=1,
    can_delete=False,
)

PCDistrictWeeklyTransportStatIncompleteFormSet = modelformset_factory(
    PCDistrictWeeklyTransportStat,
    form=PCDistrictWeeklyTransportStatIncompleteForm,
    formset=PCDistrictWeeklyTransportStatBaseFormSet,
    extra=1,
    can_delete=False,
)


# Compatibility aliases inspired by docs/operations forms naming.
RiderOperationalForm = RiderReportForm
RiderWeeklyReportForm = PCReportForm
