"""PC-scoped CRUD for bikes, facilities (including hubs), riders, and drivers."""

from django.contrib import messages
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, TemplateView, UpdateView

from ..forms import BikeForm, CarForm, FacilityForm, RiderCreateForm, RiderProfileEditForm
from ..models import Bike, Car, Facility, RiderProfile, RiderTripEntry, RiderWeeklyReport, UserProfile
from ..permissions import OperationsLoginRequiredMixin, PCRequiredMixin
from ..selectors import (
    get_bikes_queryset,
    get_cars_queryset,
    get_drivers_queryset,
    get_facilities_queryset,
    get_riders_queryset,
)


class PCManageIndexView(OperationsLoginRequiredMixin, PCRequiredMixin, TemplateView):
    template_name = "operations/pc/manage/index.html"


# --- Bikes ---


class BikeListView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    model = Bike
    template_name = "operations/pc/manage/bike_list.html"
    context_object_name = "bikes"
    paginate_by = 50

    def get_queryset(self):
        return get_bikes_queryset(self.request.user).select_related("district", "district__province")


class BikeCreateView(OperationsLoginRequiredMixin, PCRequiredMixin, CreateView):
    model = Bike
    form_class = BikeForm
    template_name = "operations/pc/manage/bike_form.html"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def form_valid(self, form):
        messages.success(
            self.request,
            "Bike created. You can now select affected facilities in this district if needed.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_bike_edit", kwargs={"pk": self.object.pk})


class BikeUpdateView(OperationsLoginRequiredMixin, PCRequiredMixin, UpdateView):
    model = Bike
    form_class = BikeForm
    template_name = "operations/pc/manage/bike_form.html"
    context_object_name = "bike"

    def get_queryset(self):
        return get_bikes_queryset(self.request.user)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def form_valid(self, form):
        messages.success(self.request, "Bike updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_bikes")


class BikeDeleteView(OperationsLoginRequiredMixin, PCRequiredMixin, DeleteView):
    model = Bike
    template_name = "operations/pc/manage/bike_confirm_delete.html"
    context_object_name = "bike"
    success_url = reverse_lazy("operations:pc_manage_bikes")

    def get_queryset(self):
        return get_bikes_queryset(self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        report_count = RiderWeeklyReport.objects.filter(bike=self.object).count()
        if report_count:
            self.object.active = False
            self.object.save(update_fields=["active"])
            messages.warning(
                request,
                "This bike is referenced on weekly reports and was deactivated instead of removed.",
            )
            return HttpResponseRedirect(self.get_success_url())
        try:
            self.object.delete()
        except ProtectedError:
            self.object.active = False
            self.object.save(update_fields=["active"])
            messages.warning(
                request,
                "This bike could not be deleted because other records still reference it. It was deactivated.",
            )
            return HttpResponseRedirect(self.get_success_url())
        messages.success(request, "Bike deleted.")
        return HttpResponseRedirect(self.get_success_url())


# --- Cars (driver vehicles; same status grid as bikes) ---


class CarListView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    model = Car
    template_name = "operations/pc/manage/car_list.html"
    context_object_name = "cars"
    paginate_by = 50

    def get_queryset(self):
        return get_cars_queryset(self.request.user).select_related("district", "district__province")


class CarCreateView(OperationsLoginRequiredMixin, PCRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = "operations/pc/manage/car_form.html"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def form_valid(self, form):
        messages.success(
            self.request,
            "Vehicle created. You can select affected facilities in this district if needed.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_car_edit", kwargs={"pk": self.object.pk})


class CarUpdateView(OperationsLoginRequiredMixin, PCRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = "operations/pc/manage/car_form.html"
    context_object_name = "car"

    def get_queryset(self):
        return get_cars_queryset(self.request.user)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def form_valid(self, form):
        messages.success(self.request, "Vehicle updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_cars")


class CarDeleteView(OperationsLoginRequiredMixin, PCRequiredMixin, DeleteView):
    model = Car
    template_name = "operations/pc/manage/car_confirm_delete.html"
    context_object_name = "car"
    success_url = reverse_lazy("operations:pc_manage_cars")

    def get_queryset(self):
        return get_cars_queryset(self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        report_count = RiderWeeklyReport.objects.filter(car=self.object).count()
        if report_count:
            self.object.active = False
            self.object.save(update_fields=["active"])
            messages.warning(
                request,
                "This vehicle is referenced on weekly reports and was deactivated instead of removed.",
            )
            return HttpResponseRedirect(self.get_success_url())
        if RiderProfile.objects.filter(car=self.object).exists():
            self.object.active = False
            self.object.save(update_fields=["active"])
            messages.warning(
                request,
                "This vehicle is assigned to a driver and was deactivated instead of removed.",
            )
            return HttpResponseRedirect(self.get_success_url())
        try:
            self.object.delete()
        except ProtectedError:
            self.object.active = False
            self.object.save(update_fields=["active"])
            messages.warning(
                request,
                "This vehicle could not be deleted because other records still reference it. It was deactivated.",
            )
            return HttpResponseRedirect(self.get_success_url())
        messages.success(request, "Vehicle deleted.")
        return HttpResponseRedirect(self.get_success_url())


# --- Facilities ---


class FacilityListView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    model = Facility
    template_name = "operations/pc/manage/facility_list.html"
    context_object_name = "facilities"
    paginate_by = 50

    def get_queryset(self):
        return (
            get_facilities_queryset(self.request.user)
            .select_related("district", "district__province")
            .order_by("district__name", "name")
        )


class FacilityCreateView(OperationsLoginRequiredMixin, PCRequiredMixin, CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = "operations/pc/manage/facility_form.html"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def form_valid(self, form):
        messages.success(self.request, "Facility created.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_facilities")


class FacilityUpdateView(OperationsLoginRequiredMixin, PCRequiredMixin, UpdateView):
    model = Facility
    form_class = FacilityForm
    template_name = "operations/pc/manage/facility_form.html"
    context_object_name = "facility"

    def get_queryset(self):
        return get_facilities_queryset(self.request.user)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def form_valid(self, form):
        messages.success(self.request, "Facility updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_facilities")


class FacilityDeleteView(OperationsLoginRequiredMixin, PCRequiredMixin, DeleteView):
    model = Facility
    template_name = "operations/pc/manage/facility_confirm_delete.html"
    context_object_name = "facility"
    success_url = reverse_lazy("operations:pc_manage_facilities")

    def get_queryset(self):
        return get_facilities_queryset(self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            trip_count = RiderTripEntry.objects.filter(
                origin_facility=self.object
            ).count() + RiderTripEntry.objects.filter(destination_facility=self.object).count()
            messages.error(
                request,
                "This facility cannot be deleted because it is referenced on one or more trip entries "
                f"({trip_count} row(s)). Remove or change those trips first.",
            )
            return HttpResponseRedirect(reverse("operations:pc_manage_facilities"))
        messages.success(request, "Facility deleted.")
        return HttpResponseRedirect(self.get_success_url())


# --- Hubs (facilities with kind=hub) ---


class HubListView(FacilityListView):
    template_name = "operations/pc/manage/hub_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(kind=Facility.Kind.HUB)


class HubCreateView(FacilityCreateView):
    template_name = "operations/pc/manage/hub_form.html"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["hub_only"] = True
        return kw

    def get_success_url(self):
        return reverse("operations:pc_manage_hubs")


class HubUpdateView(FacilityUpdateView):
    template_name = "operations/pc/manage/hub_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(kind=Facility.Kind.HUB)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["hub_only"] = True
        return kw

    def get_success_url(self):
        return reverse("operations:pc_manage_hubs")


class HubDeleteView(FacilityDeleteView):
    success_url = reverse_lazy("operations:pc_manage_hubs")

    def get_queryset(self):
        return super().get_queryset().filter(kind=Facility.Kind.HUB)


# --- Riders ---


class RiderListView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    model = RiderProfile
    template_name = "operations/pc/manage/rider_list.html"
    context_object_name = "riders"
    paginate_by = 50

    def get_queryset(self):
        return get_riders_queryset(self.request.user)


class RiderCreateView(OperationsLoginRequiredMixin, PCRequiredMixin, FormView):
    form_class = RiderCreateForm
    template_name = "operations/pc/manage/rider_form.html"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Rider account created. They can sign in with the username and password you set.")
        return HttpResponseRedirect(reverse("operations:pc_manage_riders"))


class RiderUpdateView(OperationsLoginRequiredMixin, PCRequiredMixin, UpdateView):
    model = RiderProfile
    form_class = RiderProfileEditForm
    template_name = "operations/pc/manage/rider_edit.html"
    context_object_name = "rider_profile"

    def get_queryset(self):
        return get_riders_queryset(self.request.user)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["rider_user"] = self.object.user
        return ctx

    def form_valid(self, form):
        if form.cleaned_data.get("password1"):
            messages.success(
                self.request,
                "Rider profile updated and password changed.",
            )
        else:
            messages.success(self.request, "Rider profile updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_riders")


class RiderDeactivateView(OperationsLoginRequiredMixin, PCRequiredMixin, DeleteView):
    """Soft-deactivate rider user account (preserves report history)."""

    model = RiderProfile
    template_name = "operations/pc/manage/rider_confirm_deactivate.html"
    context_object_name = "rider_profile"
    success_url = reverse_lazy("operations:pc_manage_riders")

    def get_queryset(self):
        return get_riders_queryset(self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        with transaction.atomic():
            user.is_active = False
            user.save(update_fields=["is_active"])
        messages.success(
            request,
            "The rider account was deactivated. Historical reports are unchanged; the user can no longer sign in.",
        )
        return HttpResponseRedirect(self.get_success_url())


# --- Drivers (same RiderProfile model; UserProfile.role = driver) ---


class DriverListView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    model = RiderProfile
    template_name = "operations/pc/manage/driver_list.html"
    context_object_name = "drivers"
    paginate_by = 50

    def get_queryset(self):
        return get_drivers_queryset(self.request.user)


class DriverCreateView(OperationsLoginRequiredMixin, PCRequiredMixin, FormView):
    form_class = RiderCreateForm
    template_name = "operations/pc/manage/driver_form.html"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        kw["profile_role"] = UserProfile.Role.DRIVER
        return kw

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Driver account created. They can sign in with the username and password you set.",
        )
        return HttpResponseRedirect(reverse("operations:pc_manage_drivers"))


class DriverUpdateView(OperationsLoginRequiredMixin, PCRequiredMixin, UpdateView):
    model = RiderProfile
    form_class = RiderProfileEditForm
    template_name = "operations/pc/manage/driver_edit.html"
    context_object_name = "driver_profile"

    def get_queryset(self):
        return get_drivers_queryset(self.request.user)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["pc_user"] = self.request.user
        return kw

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["driver_user"] = self.object.user
        return ctx

    def form_valid(self, form):
        if form.cleaned_data.get("password1"):
            messages.success(
                self.request,
                "Driver profile updated and password changed.",
            )
        else:
            messages.success(self.request, "Driver profile updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("operations:pc_manage_drivers")


class DriverDeactivateView(OperationsLoginRequiredMixin, PCRequiredMixin, DeleteView):
    """Soft-deactivate driver user account (preserves report history)."""

    model = RiderProfile
    template_name = "operations/pc/manage/driver_confirm_deactivate.html"
    context_object_name = "driver_profile"
    success_url = reverse_lazy("operations:pc_manage_drivers")

    def get_queryset(self):
        return get_drivers_queryset(self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        with transaction.atomic():
            user.is_active = False
            user.save(update_fields=["is_active"])
        messages.success(
            request,
            "The driver account was deactivated. Historical reports are unchanged; the user can no longer sign in.",
        )
        return HttpResponseRedirect(self.get_success_url())
