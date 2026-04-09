"""Model forms for rider operational reports and sample rejections."""
from django import forms
from django.forms import inlineformset_factory

from operations.models import RiderWeeklyReport, SampleRejection

_RIDER_EXCLUDE = (
    'rider', 'province', 'district', 'pepfar_support_type', 'status', 'week', 'date',
    'client_uuid', 'created_at', 'updated_at',
)


class RiderOperationalForm(forms.ModelForm):
    """Sections 1–3 + shared fields for rider/driver create/edit."""

    def __init__(self, *args, province_id=None, district_id=None, is_driver_form=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._province_id = province_id
        self._district_id = district_id
        self._is_driver_form = is_driver_form
        if not is_driver_form and 'first_time_transport' in self.fields:
            self.fields['first_time_transport'].widget = forms.HiddenInput()

    class Meta:
        model = RiderWeeklyReport
        exclude = _RIDER_EXCLUDE


class RiderWeeklyReportForm(forms.ModelForm):
    """Full report form for PC (all fields not locked by model save)."""

    class Meta:
        model = RiderWeeklyReport
        exclude = ('rider', 'client_uuid', 'created_at', 'updated_at')


class SampleRejectionForm(forms.ModelForm):
    class Meta:
        model = SampleRejection
        fields = (
            'sample_type', 'rejected_total', 'rejected_too_old',
            'rejected_patient_info_mismatch', 'rejected_request_form_missing',
            'rejected_sample_missing', 'rejected_other', 'order',
        )


SampleRejectionFormSet = inlineformset_factory(
    RiderWeeklyReport,
    SampleRejection,
    form=SampleRejectionForm,
    extra=1,
    can_delete=True,
)


# --- PC module forms (provincial dashboards) ---

from operations.models import (
    Bike,
    IncompleteTripRecord,
    ProvincialDriverWeekly,
    ReferredSample,
    RiderAccidentRecord,
    TransportIncident,
)


class BikeFunctionalityForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = (
            'functionality_status',
            'functionality_notes',
            'status_updated_on',
        )


class _ScopedPCFormMixin:
    """Limit FK querysets to provinces/districts visible to the user."""

    def __init__(self, *args, user=None, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)
        if user is None:
            return
        from operations.selectors import get_districts_queryset, get_facilities_queryset, get_provinces_queryset

        pq = get_provinces_queryset(user)
        dq = get_districts_queryset(user)
        fq = get_facilities_queryset(user)
        if 'province' in self.fields:
            self.fields['province'].queryset = pq
        if 'district' in self.fields:
            self.fields['district'].queryset = dq
        for name in ('facility', 'from_facility', 'to_facility'):
            if name in self.fields:
                self.fields[name].queryset = fq


class ProvincialDriverWeeklyForm(_ScopedPCFormMixin, forms.ModelForm):
    class Meta:
        model = ProvincialDriverWeekly
        fields = '__all__'


class ReferredSampleForm(_ScopedPCFormMixin, forms.ModelForm):
    class Meta:
        model = ReferredSample
        fields = '__all__'


class TransportIncidentForm(_ScopedPCFormMixin, forms.ModelForm):
    class Meta:
        model = TransportIncident
        fields = '__all__'


class RiderAccidentRecordForm(_ScopedPCFormMixin, forms.ModelForm):
    class Meta:
        model = RiderAccidentRecord
        fields = '__all__'


class IncompleteTripRecordForm(_ScopedPCFormMixin, forms.ModelForm):
    class Meta:
        model = IncompleteTripRecord
        fields = '__all__'
