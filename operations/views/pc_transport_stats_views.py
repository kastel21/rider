"""PC weekly district-level accidents and incomplete / non-IST transport capture."""

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from ..forms import (
    PC_TRANS_FORM_PREFIX_ACCIDENTS,
    PC_TRANS_FORM_PREFIX_ACCIDENT_DETAILS,
    PC_TRANS_FORM_PREFIX_INCOMPLETE,
    PC_TRANS_SAVE_ACCIDENTS,
    PC_TRANS_SAVE_INCOMPLETE,
    PCAccidentDetailFormSet,
    PCDistrictWeeklyTransportStatAccidentsFormSet,
    PCDistrictWeeklyTransportStatIncompleteFormSet,
)
from ..models import PCAccidentDetail, PCDistrictWeeklyTransportStat
from ..permissions import require_pc
from ..selectors import get_districts_queryset, week_range_label, week_start_from_request


def _accident_details_qs(week_start, district_qs):
    return (
        PCAccidentDetail.objects.filter(week_start=week_start, rider__district__in=district_qs)
        .select_related("rider__user", "bike")
        .order_by("id")
    )


class PCDistrictWeeklyTransportStatView(LoginRequiredMixin, View):
    """Two-tab UI with separate formsets (independent rows and saves per tab)."""

    template_name = "operations/pc/accidents_incomplete.html"

    def dispatch(self, request, *args, **kwargs):
        require_pc(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return self._render(request)

    def post(self, request):
        week_start = week_start_from_request(request)
        district_qs = get_districts_queryset(request.user)
        qs = self._week_queryset(week_start, district_qs)

        if f"{PC_TRANS_FORM_PREFIX_ACCIDENTS}-TOTAL_FORMS" in request.POST:
            return self._post_accidents(request, week_start, qs)
        if f"{PC_TRANS_FORM_PREFIX_INCOMPLETE}-TOTAL_FORMS" in request.POST:
            return self._post_incomplete(request, week_start, qs)

        messages.error(request, "Invalid form submission.")
        return redirect(f"{request.path}?week={week_start.isoformat()}&tab={self._active_tab_from_request(request)}")

    def _week_queryset(self, week_start, district_qs):
        return (
            PCDistrictWeeklyTransportStat.objects.filter(
                week_start=week_start,
                district__in=district_qs,
            )
            .select_related("district", "district__province")
            .order_by("district__province__name", "district__name", "id")
        )

    def _post_accidents(self, request, week_start, qs):
        save_scope = request.POST.get("pc_trans_save_scope")
        if save_scope != PC_TRANS_SAVE_ACCIDENTS:
            messages.error(request, "Use “Save accidents” on the Accidents tab.")
            return redirect(f"{request.path}?week={week_start.isoformat()}&tab={PC_TRANS_SAVE_ACCIDENTS}")
        district_qs = get_districts_queryset(request.user)
        det_qs = _accident_details_qs(week_start, district_qs)
        acc_fs = PCDistrictWeeklyTransportStatAccidentsFormSet(
            request.POST,
            queryset=qs,
            prefix=PC_TRANS_FORM_PREFIX_ACCIDENTS,
            pc_user=request.user,
            week_start=week_start,
        )
        acc_det_fs = PCAccidentDetailFormSet(
            request.POST,
            queryset=det_qs,
            prefix=PC_TRANS_FORM_PREFIX_ACCIDENT_DETAILS,
            pc_user=request.user,
            week_start=week_start,
        )
        if acc_fs.is_valid() and acc_det_fs.is_valid():
            acc_fs.save()
            acc_det_fs.save()
            messages.success(request, "Saved (accidents).")
            return redirect(f"{request.path}?week={week_start.isoformat()}&tab={PC_TRANS_SAVE_ACCIDENTS}")
        inc_fs = PCDistrictWeeklyTransportStatIncompleteFormSet(
            queryset=qs,
            prefix=PC_TRANS_FORM_PREFIX_INCOMPLETE,
            pc_user=request.user,
            week_start=week_start,
        )
        return self._render(
            request,
            week_start=week_start,
            acc_formset=acc_fs,
            acc_detail_formset=acc_det_fs,
            inc_formset=inc_fs,
            active_tab=PC_TRANS_SAVE_ACCIDENTS,
        )

    def _post_incomplete(self, request, week_start, qs):
        save_scope = request.POST.get("pc_trans_save_scope")
        if save_scope != PC_TRANS_SAVE_INCOMPLETE:
            messages.error(request, "Use “Save incomplete trips” on the Incomplete trips tab.")
            return redirect(f"{request.path}?week={week_start.isoformat()}&tab={PC_TRANS_SAVE_INCOMPLETE}")
        inc_fs = PCDistrictWeeklyTransportStatIncompleteFormSet(
            request.POST,
            queryset=qs,
            prefix=PC_TRANS_FORM_PREFIX_INCOMPLETE,
            pc_user=request.user,
            week_start=week_start,
        )
        if inc_fs.is_valid():
            inc_fs.save()
            messages.success(request, "Saved (incomplete trips).")
            return redirect(f"{request.path}?week={week_start.isoformat()}&tab={PC_TRANS_SAVE_INCOMPLETE}")
        district_qs = get_districts_queryset(request.user)
        acc_fs = PCDistrictWeeklyTransportStatAccidentsFormSet(
            queryset=qs,
            prefix=PC_TRANS_FORM_PREFIX_ACCIDENTS,
            pc_user=request.user,
            week_start=week_start,
        )
        acc_det_fs = PCAccidentDetailFormSet(
            queryset=_accident_details_qs(week_start, district_qs),
            prefix=PC_TRANS_FORM_PREFIX_ACCIDENT_DETAILS,
            pc_user=request.user,
            week_start=week_start,
        )
        return self._render(
            request,
            week_start=week_start,
            acc_formset=acc_fs,
            acc_detail_formset=acc_det_fs,
            inc_formset=inc_fs,
            active_tab=PC_TRANS_SAVE_INCOMPLETE,
        )

    def _active_tab_from_request(self, request):
        tab = request.GET.get("tab")
        if tab in (PC_TRANS_SAVE_ACCIDENTS, PC_TRANS_SAVE_INCOMPLETE):
            return tab
        return PC_TRANS_SAVE_ACCIDENTS

    def _render(
        self,
        request,
        acc_formset=None,
        acc_detail_formset=None,
        inc_formset=None,
        week_start=None,
        active_tab=None,
    ):
        week_start = week_start or week_start_from_request(request)
        active_tab = active_tab or self._active_tab_from_request(request)
        district_qs = get_districts_queryset(request.user)
        qs = self._week_queryset(week_start, district_qs)
        if acc_formset is None:
            acc_formset = PCDistrictWeeklyTransportStatAccidentsFormSet(
                queryset=qs,
                prefix=PC_TRANS_FORM_PREFIX_ACCIDENTS,
                pc_user=request.user,
                week_start=week_start,
            )
        if acc_detail_formset is None:
            acc_detail_formset = PCAccidentDetailFormSet(
                queryset=_accident_details_qs(week_start, district_qs),
                prefix=PC_TRANS_FORM_PREFIX_ACCIDENT_DETAILS,
                pc_user=request.user,
                week_start=week_start,
            )
        if inc_formset is None:
            inc_formset = PCDistrictWeeklyTransportStatIncompleteFormSet(
                queryset=qs,
                prefix=PC_TRANS_FORM_PREFIX_INCOMPLETE,
                pc_user=request.user,
                week_start=week_start,
            )
        prev_week = (week_start - timedelta(days=7)).isoformat()
        next_week = (week_start + timedelta(days=7)).isoformat()
        return render(
            request,
            self.template_name,
            {
                "acc_formset": acc_formset,
                "acc_detail_formset": acc_detail_formset,
                "inc_formset": inc_formset,
                "selected_week_start": week_start,
                "week_range_label": week_range_label(week_start),
                "pc_prev_week": prev_week,
                "pc_next_week": next_week,
                "active_tab": active_tab,
            },
        )
