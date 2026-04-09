"""PC-specific report editing (full form)."""
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from operations.forms import RiderWeeklyReportForm, SampleRejectionFormSet
from operations.models import RiderWeeklyReport
from operations.permissions import OperationsLoginRequiredMixin, PCRequiredMixin
from operations.selectors import get_reports_queryset


class PCReportEditView(OperationsLoginRequiredMixin, PCRequiredMixin, UpdateView):
    model = RiderWeeklyReport
    form_class = RiderWeeklyReportForm
    template_name = 'operations/reports/report_form.html'
    context_object_name = 'report'
    success_url = reverse_lazy('operations:pc_reports')

    def get_queryset(self):
        return get_reports_queryset(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs['province_id'] = self.object.province_id
            kwargs['district_id'] = self.object.district_id
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        report = self.object
        ctx['is_rider_form'] = False
        ctx['is_pc_form'] = True
        ctx['is_driver_form'] = False
        ctx.setdefault('sections_modified_by_pc', [])
        ctx.setdefault('show_edit_history', True)
        if report:
            ctx['report_location'] = {
                'province_name': report.province.name if report.province_id else '—',
                'district_name': report.district.name if report.district_id else '—',
                'pepfar_support_type': report.pepfar_support_type or '—',
            }
            if 'rejection_formset' in kwargs:
                ctx['rejection_formset'] = kwargs['rejection_formset']
            else:
                ctx['rejection_formset'] = SampleRejectionFormSet(
                    self.request.POST if self.request.method == 'POST' else None,
                    instance=report,
                    prefix='rejections',
                )
        else:
            ctx['rejection_formset'] = None
        try:
            ctx['report_facilities_ajax_url'] = self.request.build_absolute_uri(
                reverse('operations:report_facilities_ajax')
            )
        except Exception:
            ctx['report_facilities_ajax_url'] = ''
        return ctx

    def form_valid(self, form):
        rejection_formset = SampleRejectionFormSet(
            self.request.POST, instance=form.instance, prefix='rejections',
        )
        if not rejection_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, rejection_formset=rejection_formset)
            )
        self.object = form.save()
        rejection_formset.instance = self.object
        rejection_formset.save()
        messages.success(self.request, 'Report updated.')
        return redirect(self.get_success_url())
