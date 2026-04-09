"""Rider report list, create, detail, edit (multi-step form with collapsible sections)."""
from datetime import date, datetime
from decimal import Decimal
import gzip
import json
import uuid as uuid_lib

from django.utils import timezone

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView

from operations.forms import RiderOperationalForm, RiderWeeklyReportForm, SampleRejectionFormSet
from operations.models import (
    Bike,
    Facility,
    Lab,
    RiderDevice,
    RiderWeeklyReport,
    ReportStatus,
    ReportAuditLog,
    ReportVersion,
    SampleRejection,
)
from operations.models import Role
from operations.permissions import (
    OperationsLoginRequiredMixin,
    RiderRequiredMixin,
    PCRequiredMixin,
    can_edit_report,
    RiderSections1To3OnlyMixin,
)
from operations.selectors import get_reports_queryset
from operations.services.report_service import ReportService
from operations.services.report_edit_service import get_section_4_6_snapshot


class RiderReportListView(OperationsLoginRequiredMixin, ListView):
    """List reports (filtered by role: rider sees own, PC/ME/ADMIN see filtered)."""
    model = RiderWeeklyReport
    template_name = 'operations/reports/report_list.html'
    paginate_by = 20
    context_object_name = 'reports'

    def get_queryset(self):
        return get_reports_queryset(self.request.user).select_related('facility').order_by('-week')

    def get_template_names(self):
        try:
            if self.request.user.operations_profile.role in ('RIDER', 'DRIVER'):
                return ['operations/reports/rider_report_list.html']
        except Exception:
            pass
        return ['operations/reports/report_list.html']


class RiderReportCreateView(
    OperationsLoginRequiredMixin, RiderRequiredMixin, RiderSections1To3OnlyMixin, CreateView
):
    model = RiderWeeklyReport
    form_class = RiderOperationalForm
    rider_form_class = RiderOperationalForm
    template_name = 'operations/reports/report_form.html'
    success_url = reverse_lazy('operations:report_create')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('sections_modified_by_pc', [])
        ctx.setdefault('show_edit_history', False)
        ctx['is_rider_form'] = True
        ctx['is_pc_form'] = False
        try:
            profile = self.request.user.operations_profile
            ctx['is_driver_form'] = profile.role == Role.DRIVER
            first_time = self.request.GET.get('first_time')
            ctx['driver_show_tabs_only'] = (
                ctx['is_driver_form'] and first_time not in ('1', '0')
            )
        except Exception:
            ctx['is_driver_form'] = False
            ctx['driver_show_tabs_only'] = False
        # Read-only location: from rider profile (no report yet on create)
        try:
            rider = self.request.user.operations_rider_profile
            ctx['report_location'] = {
                'province_name': getattr(rider.province, 'name', None) or (rider.district.province.name if rider.district_id else '—'),
                'district_name': rider.district.name if rider.district_id else '—',
                'pepfar_support_type': getattr(rider, 'pepfar_support_type', None) or '—',
            }
            # Current week: marked by the date of the Sunday (week ending)
            from datetime import timedelta
            today = date.today()
            week_sunday = today + timedelta(days=(6 - today.weekday()))
            ctx['week_sunday'] = week_sunday
            ctx['week_reports'] = RiderWeeklyReport.objects.filter(
                rider=rider, week=week_sunday
            ).select_related('facility').order_by('-created_at')
        except Exception:
            ctx['report_location'] = {'province_name': '—', 'district_name': '—', 'pepfar_support_type': '—'}
            ctx.setdefault('week_sunday', None)
            ctx.setdefault('week_reports', RiderWeeklyReport.objects.none())
        # Sample Rejections formset: on create use unsaved instance so extra forms render with same names
        if self.request.method == 'POST':
            ctx['rejection_formset'] = SampleRejectionFormSet(
                self.request.POST, instance=RiderWeeklyReport(), prefix='rejections',
            )
        else:
            ctx['rejection_formset'] = SampleRejectionFormSet(
                instance=RiderWeeklyReport(), prefix='rejections',
            )
        ctx['report'] = self.object  # None on create; template uses this
        try:
            rider = self.request.user.operations_rider_profile
            ctx['rider_id'] = rider.pk
        except Exception:
            ctx['rider_id'] = None
        try:
            ctx['report_facilities_ajax_url'] = self.request.build_absolute_uri(reverse('operations:report_facilities_ajax'))
        except Exception:
            ctx['report_facilities_ajax_url'] = ''
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            rider = self.request.user.operations_rider_profile
            province_id = getattr(rider.province, 'pk', None) or (rider.district.province_id if rider.district_id else None)
            kwargs['province_id'] = province_id
            kwargs['district_id'] = rider.district_id
        except Exception:
            kwargs['province_id'] = None
            kwargs['district_id'] = None
        try:
            if self.request.user.operations_profile.role == Role.DRIVER:
                kwargs['is_driver_form'] = True
        except Exception:
            pass
        return kwargs

    def get_success_url(self):
        """Fixed URL (no object); avoid ModelFormMixin using self.object.__dict__ which is None on create."""
        return str(self.success_url)

    def form_valid(self, form):
        rider = getattr(self.request.user, 'operations_rider_profile', None)
        if not rider:
            messages.error(self.request, 'Rider profile not found. Contact administrator.')
            return redirect('operations:rider_reports')
        form.instance.rider = rider
        if self.request.user.operations_profile.role == Role.DRIVER:
            form.instance.first_time_transport = form.cleaned_data.get('first_time_transport')
        bike = form.cleaned_data.get('bike')
        form.instance.bike_registration = bike.registration_number if bike else ''
        form.instance.facility = form.cleaned_data.get('facility') or rider.facility
        form.instance.status = ReportStatus.DRAFT
        today = date.today()
        from datetime import timedelta
        week_sunday = today + timedelta(days=(6 - today.weekday()))
        form.instance.week = week_sunday
        form.instance.date = today
        form.save()
        report = form.instance
        rejection_formset = SampleRejectionFormSet(
            self.request.POST, instance=report, prefix='rejections',
        )
        if rejection_formset.is_valid():
            rejection_formset.save()
            if self.request.POST.get('action') == 'submit':
                ReportService.submit(report, self.request.user)
                messages.success(self.request, 'Report saved and submitted.')
                return redirect('operations:rider_reports')
            messages.success(self.request, 'Report saved. You can add another record below.')
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, rejection_formset=rejection_formset)
        )

    def get_initial(self):
        initial = super().get_initial()
        try:
            rider = self.request.user.operations_rider_profile
            name = rider.user.get_full_name() or rider.user.get_username()
            initial['relief_rider_name'] = name
            if rider.bike_id:
                initial['bike'] = rider.bike_id
            if rider.facility_id:
                initial['facility'] = rider.facility_id
        except Exception:
            pass
        try:
            if self.request.user.operations_profile.role == Role.DRIVER:
                first_time = self.request.GET.get('first_time')
                if first_time == '1':
                    initial['first_time_transport'] = True
                elif first_time == '0':
                    initial['first_time_transport'] = False
        except Exception:
            pass
        return initial


class RiderReportDetailView(OperationsLoginRequiredMixin, DetailView):
    model = RiderWeeklyReport
    template_name = 'operations/reports/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return get_reports_queryset(self.request.user).prefetch_related('sample_rejections')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        report = ctx.get('report')
        ctx['can_edit_report'] = can_edit_report(self.request.user, report) if report else False
        try:
            role = self.request.user.operations_profile.role
            if role == 'PC':
                ctx['back_list_url'] = reverse('operations:pc_reports')
            elif role == 'ME':
                ctx['back_list_url'] = reverse('operations:me_reports')
            else:
                ctx['back_list_url'] = reverse('operations:rider_reports')
        except Exception:
            ctx['back_list_url'] = reverse('operations:rider_reports')
        return ctx


class RiderReportEditView(
    OperationsLoginRequiredMixin, RiderSections1To3OnlyMixin, UpdateView
):
    model = RiderWeeklyReport
    form_class = RiderOperationalForm
    rider_form_class = RiderOperationalForm
    template_name = 'operations/reports/report_form.html'
    context_object_name = 'report'
    success_url = reverse_lazy('operations:rider_reports')

    def get_queryset(self):
        return get_reports_queryset(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs['province_id'] = self.object.province_id
            kwargs['district_id'] = self.object.district_id
        else:
            kwargs['province_id'] = None
            kwargs['district_id'] = None
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        if self.object and self.object.rider_id:
            if not (self.object.relief_rider_name or '').strip():
                name = self.object.rider.user.get_full_name() or self.object.rider.user.get_username()
                initial['relief_rider_name'] = name
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('sections_modified_by_pc', [])
        ctx.setdefault('show_edit_history', False)
        ctx['is_rider_form'] = True
        ctx['is_pc_form'] = False
        report = self.object
        if report:
            ctx['_section_4_6_snapshot'] = get_section_4_6_snapshot(report)
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
            ctx['report_location'] = {'province_name': '—', 'district_name': '—', 'pepfar_support_type': '—'}
            ctx['rejection_formset'] = None
        try:
            rider = self.request.user.operations_rider_profile
            ctx['rider_id'] = rider.pk
        except Exception:
            ctx['rider_id'] = None
        try:
            ctx['report_facilities_ajax_url'] = self.request.build_absolute_uri(reverse('operations:report_facilities_ajax'))
        except Exception:
            ctx['report_facilities_ajax_url'] = ''
        return ctx

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()
        if not can_edit_report(request.user, report):
            messages.error(request, 'You cannot edit this report.')
            return redirect('operations:rider_reports')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        report = form.instance
        bike = form.cleaned_data.get('bike')
        report.bike_registration = bike.registration_number if bike else ''
        report.facility = form.cleaned_data.get('facility')
        # Snapshot Section 4–6 from DB before save; model save() will reapply (backend enforcement)
        existing_snapshot = get_section_4_6_snapshot(
            RiderWeeklyReport.objects.get(pk=report.pk)
        )
        form.save()
        report._revert_section_4_6_to = existing_snapshot
        report.save()
        rejection_formset = SampleRejectionFormSet(
            self.request.POST, instance=report, prefix='rejections',
        )
        if rejection_formset.is_valid():
            rejection_formset.save()
        else:
            return self.render_to_response(
                self.get_context_data(form=form, rejection_formset=rejection_formset)
            )
        messages.success(self.request, 'Report updated.')
        return redirect(self.get_success_url())


class ReportSubmitView(OperationsLoginRequiredMixin, TemplateView):
    """POST: submit report (rider or PC)."""
    def post(self, request, pk):
        report = get_object_or_404(RiderWeeklyReport, pk=pk)
        qs = get_reports_queryset(request.user)
        if not qs.filter(pk=report.pk).exists():
            messages.error(request, 'Report not found.')
            return redirect('operations:rider_reports')
        if report.status != ReportStatus.DRAFT:
            messages.warning(request, 'Report is already submitted.')
        else:
            ReportService.submit(report, request.user)
            messages.success(request, 'Report submitted.')
        return redirect('operations:rider_reports')


class ReportStartReviewView(OperationsLoginRequiredMixin, PCRequiredMixin, TemplateView):
    """POST: PC marks report as under review (SUBMITTED → UNDER_REVIEW)."""
    def post(self, request, pk):
        report = get_object_or_404(RiderWeeklyReport, pk=pk)
        qs = get_reports_queryset(request.user)
        if not qs.filter(pk=report.pk).exists():
            messages.error(request, 'Report not found.')
            return redirect('operations:pc_reports')
        if report.status != ReportStatus.SUBMITTED:
            messages.warning(request, 'Only submitted reports can be started for review.')
        else:
            ReportService.start_review(report, request.user)
            messages.success(request, 'Report is now under review.')
        next_url = request.GET.get('next') or reverse('operations:pc_reports')
        return redirect(next_url)


class ReportReviewView(OperationsLoginRequiredMixin, PCRequiredMixin, TemplateView):
    """POST: PC completes review (SUBMITTED/UNDER_REVIEW → REVIEWED)."""
    def post(self, request, pk):
        report = get_object_or_404(RiderWeeklyReport, pk=pk)
        qs = get_reports_queryset(request.user)
        if not qs.filter(pk=report.pk).exists():
            messages.error(request, 'Report not found.')
            return redirect('operations:pc_reports')
        if report.status not in (ReportStatus.SUBMITTED, ReportStatus.UNDER_REVIEW):
            messages.warning(request, 'Only submitted or under-review reports can be marked reviewed.')
        else:
            ReportService.review(report, request.user)
            messages.success(request, 'Report marked as reviewed.')
        next_url = request.GET.get('next') or reverse('operations:pc_reports')
        return redirect(next_url)


class ReportStartReviewGroupView(OperationsLoginRequiredMixin, PCRequiredMixin, TemplateView):
    """POST: PC marks all reports for (rider_id, week) as under review (SUBMITTED → UNDER_REVIEW)."""
    def post(self, request, rider_id, week_str):
        try:
            week = datetime.strptime(week_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid week.')
            return redirect('operations:pc_reports')
        qs = get_reports_queryset(request.user).filter(rider_id=rider_id, week=week)
        reports = list(qs.filter(status=ReportStatus.SUBMITTED))
        if not reports:
            messages.warning(request, 'No submitted reports found for this rider and week.')
        else:
            for report in reports:
                ReportService.start_review(report, request.user)
            messages.success(request, f'{len(reports)} report(s) now under review.')
        next_url = request.GET.get('next') or reverse('operations:pc_reports')
        return redirect(next_url)


class ReportReviewGroupView(OperationsLoginRequiredMixin, PCRequiredMixin, TemplateView):
    """POST: PC completes review for all reports for (rider_id, week) (SUBMITTED/UNDER_REVIEW → REVIEWED)."""
    def post(self, request, rider_id, week_str):
        try:
            week = datetime.strptime(week_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid week.')
            return redirect('operations:pc_reports')
        qs = get_reports_queryset(request.user).filter(rider_id=rider_id, week=week)
        reports = list(qs.filter(status__in=(ReportStatus.SUBMITTED, ReportStatus.UNDER_REVIEW)))
        if not reports:
            messages.warning(request, 'No submitted or under-review reports found for this rider and week.')
        else:
            for report in reports:
                ReportService.review(report, request.user)
            messages.success(request, f'{len(reports)} report(s) marked as reviewed.')
        next_url = request.GET.get('next') or reverse('operations:pc_reports')
        return redirect(next_url)


class ReportEditHistoryView(OperationsLoginRequiredMixin, PCRequiredMixin, DetailView):
    """PC: view audit log and version history for a report (Sections 1–3 edits)."""
    model = RiderWeeklyReport
    template_name = 'operations/reports/report_edit_history.html'
    context_object_name = 'report'

    def get_queryset(self):
        return get_reports_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        report = self.object
        ctx['audit_logs'] = report.report_audit_logs.select_related('edited_by').order_by('-edited_at')[:100]
        ctx['versions'] = report.report_versions.select_related('created_by').order_by('-version_number')[:50]
        ctx['back_url'] = reverse('operations:pc_report_edit', kwargs={'pk': report.pk})
        return ctx


class ReportAuditLogListView(OperationsLoginRequiredMixin, PCRequiredMixin, ListView):
    """PC: list recent report edit audit log entries (Sections 1–3) for reports in assigned provinces."""
    template_name = 'operations/reports/report_audit_log_list.html'
    context_object_name = 'audit_logs'
    paginate_by = 30

    def get_queryset(self):
        report_ids = get_reports_queryset(self.request.user).values_list('pk', flat=True)
        return (
            ReportAuditLog.objects.filter(report_id__in=report_ids)
            .select_related('report', 'report__rider', 'report__rider__user', 'edited_by')
            .order_by('-edited_at')
        )


class ReportFacilitiesAjaxView(OperationsLoginRequiredMixin, View):
    """AJAX: return facilities, hubs, or labs as JSON. GET params: district_id, province_id, type (facilities|hubs|labs)."""
    def get(self, request):
        data_type = (request.GET.get('type') or 'facilities').strip().lower()
        district_id = request.GET.get('district_id')
        province_id = request.GET.get('province_id')

        if data_type == 'labs':
            qs = Lab.objects.order_by('name')
            data = [{'id': obj.pk, 'name': obj.name, 'district_name': getattr(obj, 'code', '')} for obj in qs]
            return JsonResponse(data, safe=False)

        if data_type == 'hubs':
            if district_id:
                try:
                    qs = Facility.objects.filter(
                        district_id=int(district_id),
                        is_hub=True,
                    ).select_related('district').order_by('name')
                except ValueError:
                    qs = Facility.objects.none()
            else:
                qs = Facility.objects.none()
            data = [{'id': f.pk, 'name': f.name, 'district_name': f.district.name if f.district_id else ''} for f in qs]
            return JsonResponse(data, safe=False)

        # facilities (default)
        if district_id:
            try:
                qs = Facility.objects.filter(district_id=int(district_id)).select_related('district').order_by('name')
            except ValueError:
                qs = Facility.objects.none()
        elif province_id:
            try:
                qs = Facility.objects.filter(district__province_id=int(province_id)).select_related('district').order_by('district__name', 'name')
            except ValueError:
                qs = Facility.objects.none()
        else:
            qs = Facility.objects.none()
        data = [{'id': f.pk, 'name': f.name, 'district_name': f.district.name if f.district_id else ''} for f in qs]
        return JsonResponse(data, safe=False)


def _get_device_for_sync_session(rider, device_id):
    """Return (RiderDevice, None) or (None, JsonResponse) for session sync."""
    if not device_id or not str(device_id).strip():
        return None, JsonResponse({'error': 'device_id required'}, status=400)
    device_id = str(device_id).strip()
    device = RiderDevice.objects.filter(rider=rider, device_id=device_id).first()
    if not device:
        return None, JsonResponse(
            {'error': 'Device not registered. Call POST /api/rider/register-device/ first.'},
            status=403,
        )
    if not device.is_active:
        return None, JsonResponse(
            {'error': 'Device is disabled. Contact support.'},
            status=403,
        )
    return device, None


def _rider_sync_body(request):
    """Return request body as bytes, decompressing if Content-Encoding: gzip."""
    raw = request.body
    if request.META.get('HTTP_CONTENT_ENCODING', '').strip().lower() == 'gzip':
        try:
            return gzip.decompress(raw)
        except (OSError, ValueError):
            return raw
    return raw


def _create_one_report_session(rider, payload, user):
    """Create/update one RiderWeeklyReport + SampleRejections from payload (session flow). Returns (report_or_none, created, error_msg)."""
    client_uuid_str = payload.get('client_uuid')
    if not client_uuid_str:
        return None, False, 'client_uuid required'
    try:
        client_uuid = uuid_lib.UUID(str(client_uuid_str))
    except (ValueError, TypeError):
        return None, False, 'Invalid client_uuid'

    week_str = payload.get('week')
    if not week_str:
        return None, False, 'week required'
    try:
        week = datetime.strptime(week_str[:10], '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None, False, 'Invalid week'

    specimens = payload.get('specimens') or {}
    results = payload.get('results') or {}
    rejections = payload.get('rejections') or []

    bike_pk = payload.get('bike')
    bike_registration = ''
    if bike_pk:
        bike = Bike.objects.filter(pk=bike_pk).first()
        if bike:
            bike_registration = bike.registration_number or ''

    facility_id = payload.get('facility')
    to_facility_id = payload.get('to_facility')
    from_lab_id = payload.get('from_lab')
    to_lab_id = payload.get('to_lab')
    transport_route_type = (payload.get('transport_route_type') or '').strip() or None

    existing = RiderWeeklyReport.objects.filter(client_uuid=client_uuid).first()
    if existing and existing.rider_id != rider.id:
        return None, False, 'client_uuid belongs to another rider'

    report = existing or RiderWeeklyReport(
        rider=rider,
        province=rider.province,
        district=rider.district,
        pepfar_support_type=getattr(rider, 'pepfar_support_type', '') or '',
        client_uuid=client_uuid,
    )
    report.status = ReportStatus.DRAFT
    report.week = week
    report.date = date.today()
    report.relief_rider_name = (payload.get('relief_rider_name') or '').strip()
    report.is_relief_rider = False
    report.bike_registration = bike_registration
    report.facility_id = facility_id or None
    report.to_facility_id = to_facility_id or None
    report.transport_route_type = transport_route_type
    report.from_lab_id = from_lab_id or None
    report.to_lab_id = to_lab_id or None
    report.vl_plasma = int(specimens.get('vl_plasma') or 0)
    report.vl_dbs = int(specimens.get('vl_dbs') or 0)
    report.eid_blood = int(specimens.get('eid_blood') or 0)
    report.eid_dbs = int(specimens.get('eid_dbs') or 0)
    report.sputum = int(specimens.get('sputum') or 0)
    report.sputum_culture_dr = int(specimens.get('sputum_culture_dr') or 0)
    report.hpv = int(specimens.get('hpv') or 0)
    report.other_specimen = int(specimens.get('other_specimen') or 0)
    report.other_specimen_description = (specimens.get('other_specimen_description') or '')[:200]
    report.results_vl_plasma = int(results.get('results_vl_plasma') or 0)
    report.results_vl_dbs = int(results.get('results_vl_dbs') or 0)
    report.results_eid_blood = int(results.get('results_eid_blood') or 0)
    report.results_eid_dbs = int(results.get('results_eid_dbs') or 0)
    report.results_sputum = int(results.get('results_sputum') or 0)
    report.results_sputum_culture_dr = int(results.get('results_sputum_culture_dr') or 0)
    report.results_hpv = int(results.get('results_hpv') or 0)
    report.results_other_specimen = int(results.get('results_other_specimen') or 0)
    report.results_other_specimen_description = (results.get('results_other_specimen_description') or '')[:200]
    report.fuel_allocated = Decimal(str(payload.get('fuel_allocated') or 0))
    report.fuel_used = Decimal(str(payload.get('fuel_used') or 0))
    report.distance_travelled = Decimal(str(payload.get('distance_travelled') or 0))
    avg_temp = payload.get('average_datalogger_temperature')
    report.average_datalogger_temperature = (
        Decimal(str(avg_temp)) if avg_temp not in (None, '', 'null') else None
    )
    report.first_time_transport = payload.get('first_time_transport') if payload.get('first_time_transport') is not None else None
    report.save()

    valid_sample_types = {c[0] for c in SampleRejection.SampleType.choices}
    SampleRejection.objects.filter(report=report).delete()
    for i, row in enumerate(rejections):
        if row.get('rejected_total', 0) == 0 and not row.get('sample_type'):
            continue
        raw_type = (row.get('sample_type') or 'other').strip()
        sample_type = raw_type if raw_type in valid_sample_types else 'other'
        SampleRejection.objects.create(
            report=report,
            sample_type=sample_type,
            rejected_total=int(row.get('rejected_total') or 0),
            rejected_too_old=int(row.get('rejected_too_old') or 0),
            rejected_patient_info_mismatch=int(row.get('rejected_patient_info_mismatch') or 0),
            rejected_request_form_missing=int(row.get('rejected_request_form_missing') or 0),
            rejected_sample_missing=int(row.get('rejected_sample_missing') or 0),
            rejected_other=int(row.get('rejected_other') or 0),
            order=int(row.get('order', i)),
        )

    if payload.get('action') == 'submit':
        ReportService.submit(report, user)
    return report, existing is None, None


class RiderRegisterDeviceView(OperationsLoginRequiredMixin, RiderRequiredMixin, View):
    """POST /api/register-device/ — Session auth: register or update device for current rider. Body: device_id, device_model?, app_version?."""
    http_method_names = ['post']

    def post(self, request):
        try:
            body = _rider_sync_body(request)
            data = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        rider = getattr(request.user, 'operations_rider_profile', None)
        if not rider:
            return JsonResponse({'error': 'Rider profile not found'}, status=403)
        device_id = (data.get('device_id') or '').strip()
        if not device_id:
            return JsonResponse({'error': 'device_id required'}, status=400)
        device_model = (data.get('device_model') or '')[:120]
        app_version = (data.get('app_version') or '')[:60]
        device, _ = RiderDevice.objects.update_or_create(
            rider=rider,
            device_id=device_id,
            defaults={
                'device_model': device_model,
                'app_version': app_version,
                'is_active': True,
                'last_seen': timezone.now(),
            },
        )
        return JsonResponse({'status': 'ok', 'device_id': device.device_id, 'message': 'Device registered'}, status=200)


class RiderSyncView(OperationsLoginRequiredMixin, RiderRequiredMixin, View):
    """PWA offline sync: accept JSON (single report or { reports: [...] }), optionally gzip. Create RiderWeeklyReport + SampleRejections. Idempotent by client_uuid. Batch processed atomically."""
    http_method_names = ['post']

    def post(self, request):
        try:
            body = _rider_sync_body(request)
            payload = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        rider = getattr(request.user, 'operations_rider_profile', None)
        if not rider:
            return JsonResponse({'error': 'Rider profile not found'}, status=403)

        device, err_response = _get_device_for_sync_session(rider, payload.get('device_id'))
        if err_response is not None:
            return err_response
        device.last_seen = timezone.now()
        device.save(update_fields=['last_seen'])

        # Batch: { reports: [ {...}, ... ] }
        if isinstance(payload.get('reports'), list):
            reports = payload['reports']
            synced = []
            updated = []
            errors = []
            try:
                with transaction.atomic():
                    for i, p in enumerate(reports):
                        if not isinstance(p, dict):
                            errors.append({'index': i, 'error': 'Invalid report object'})
                            continue
                        report, created, err = _create_one_report_session(rider, p, request.user)
                        if err:
                            errors.append({'index': i, 'client_uuid': p.get('client_uuid'), 'error': err})
                            continue
                        row = {'index': i, 'id': report.pk, 'client_uuid': str(report.client_uuid)}
                        if created:
                            synced.append(row)
                        else:
                            updated.append(row)
                    if errors:
                        raise ValueError('Batch had errors')
            except ValueError:
                return JsonResponse({
                    'error': 'Batch validation failed',
                    'synced': synced,
                    'updated': updated,
                    'errors': errors,
                }, status=400)
            return JsonResponse({
                'status': 'ok',
                'synced': synced,
                'updated': updated,
                'errors': errors,
                'summary': {
                    'synced_count': len(synced),
                    'updated_count': len(updated),
                    'error_count': len(errors),
                },
            }, status=200)

        # Single report
        report, created, err = _create_one_report_session(rider, payload, request.user)
        if err:
            return JsonResponse({'error': err}, status=400)
        return JsonResponse({'status': 'ok', 'id': report.pk, 'updated': (not created)}, status=201 if created else 200)
