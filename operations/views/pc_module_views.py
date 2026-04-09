"""Provincial Coordinator / ME / Admin dashboards: bikes, riders, driver weekly, samples, incidents, captures."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView

from operations.forms import (
    BikeFunctionalityForm,
    IncompleteTripRecordForm,
    ProvincialDriverWeeklyForm,
    ReferredSampleForm,
    RiderAccidentRecordForm,
    TransportIncidentForm,
)
from operations.models import Bike, RiderProfile
from operations.permissions import OperationsLoginRequiredMixin, PCRequiredMixin
from operations.selectors import (
    get_bikes_for_functionality_queryset,
    get_incomplete_trip_records_queryset,
    get_provincial_driver_weekly_queryset,
    get_referred_samples_queryset,
    get_rider_accident_records_queryset,
    get_riders_queryset,
    get_transport_incidents_queryset,
)


class PCBikeFunctionalityView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    """List bikes in assigned provinces; link to edit status."""
    template_name = 'operations/pc/bike_functionality.html'
    context_object_name = 'bikes'
    paginate_by = 50

    def get_queryset(self):
        return get_bikes_for_functionality_queryset(self.request.user).select_related(
            'district', 'district__province'
        )


class PCBikeFunctionalityUpdateView(OperationsLoginRequiredMixin, PCRequiredMixin, UpdateView):
    model = Bike
    form_class = BikeFunctionalityForm
    template_name = 'operations/pc/bike_edit.html'
    success_url = reverse_lazy('operations:pc_bike_functionality')

    def get_queryset(self):
        return get_bikes_for_functionality_queryset(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Bike record updated.')
        return super().form_valid(form)


class PCRidersListView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    template_name = 'operations/pc/riders_list.html'
    context_object_name = 'riders'
    paginate_by = 40

    def get_queryset(self):
        return get_riders_queryset(self.request.user).select_related(
            'user', 'district', 'facility', 'bike', 'district__province'
        )


class PCBikeRiderManagementView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    """Same data as riders list; template emphasizes bike assignment."""
    template_name = 'operations/pc/bike_rider_management.html'
    context_object_name = 'riders'
    paginate_by = 40

    def get_queryset(self):
        return get_riders_queryset(self.request.user).select_related(
            'user', 'district', 'facility', 'bike', 'district__province'
        )


class _ListCreateView(OperationsLoginRequiredMixin, PCRequiredMixin, View):
    """GET: list + empty form. POST: create."""
    template_name = ''
    form_class = None
    queryset_fn = staticmethod(lambda user: [])

    def get(self, request):
        qs = self.queryset_fn(request.user)
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'object_list': qs, 'form': form})

    def post(self, request):
        qs = self.queryset_fn(request.user)
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record saved.')
            return redirect(self.success_url_name)
        return render(request, self.template_name, {'object_list': qs, 'form': form})

    @property
    def success_url_name(self):
        raise NotImplementedError


class ProvincialDriverWeeklyModuleView(_ListCreateView):
    template_name = 'operations/pc/driver_weekly.html'
    form_class = ProvincialDriverWeeklyForm
    queryset_fn = staticmethod(get_provincial_driver_weekly_queryset)

    @property
    def success_url_name(self):
        return reverse('operations:pc_driver_weekly_list')


class ReferredSamplesModuleView(_ListCreateView):
    template_name = 'operations/pc/referred_samples.html'
    form_class = ReferredSampleForm
    queryset_fn = staticmethod(get_referred_samples_queryset)

    @property
    def success_url_name(self):
        return reverse('operations:pc_referred_samples_list')


class TransportIncidentsModuleView(_ListCreateView):
    template_name = 'operations/pc/incidents.html'
    form_class = TransportIncidentForm
    queryset_fn = staticmethod(get_transport_incidents_queryset)

    @property
    def success_url_name(self):
        return reverse('operations:pc_incidents_list')


class RiderAccidentCaptureModuleView(_ListCreateView):
    template_name = 'operations/pc/accident_capture.html'
    form_class = RiderAccidentRecordForm
    queryset_fn = staticmethod(get_rider_accident_records_queryset)

    @property
    def success_url_name(self):
        return reverse('operations:pc_accident_capture')


class IncompleteTripCaptureModuleView(_ListCreateView):
    template_name = 'operations/pc/incomplete_trip_capture.html'
    form_class = IncompleteTripRecordForm
    queryset_fn = staticmethod(get_incomplete_trip_records_queryset)

    @property
    def success_url_name(self):
        return reverse('operations:pc_incomplete_trip_capture')
