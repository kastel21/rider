"""Django admin for operations (ADMIN role)."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from operations.models import (
    Province,
    District,
    Facility,
    Lab,
    Bike,
    UserProfile,
    PCProfile,
    RiderDevice,
    RiderProfile,
    RiderRemoteConfig,
    RiderWeeklyReport,
    ReportAuditLog,
    ReportVersion,
    AuditLog,
    ProvincialDriverWeekly,
    RiderAccidentRecord,
    IncompleteTripRecord,
    ReferredSample,
    TransportIncident,
)

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    max_num = 1
    can_delete = True
    verbose_name = 'Operations role'
    verbose_name_plural = 'Operations role'


class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'operations_role']
    list_filter = ['is_staff', 'is_active', 'operations_profile__role']
    inlines = [UserProfileInline]

    def operations_role(self, obj):
        try:
            return obj.operations_profile.get_role_display()
        except Exception:
            return ''
    operations_role.short_description = 'Role'


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'code']
    list_filter = ['province']
    search_fields = ['name', 'code']


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'code', 'is_hub']
    list_filter = ['district__province', 'district', 'is_hub']
    search_fields = ['name', 'code']


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'facility_type']
    search_fields = ['name', 'code']


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'district', 'is_active']
    list_filter = ['is_active', 'district__province']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']


@admin.register(PCProfile)
class PCProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['provinces']


@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'district', 'facility', 'bike']
    list_filter = ['district__province', 'district']


@admin.register(RiderDevice)
class RiderDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'rider', 'device_model', 'app_version', 'last_seen', 'is_active']
    list_filter = ['is_active', 'rider__district__province']
    search_fields = ['device_id', 'rider__user__username', 'device_model']
    list_editable = ['is_active']
    readonly_fields = ['last_seen']
    raw_id_fields = ['rider']


@admin.register(RiderRemoteConfig)
class RiderRemoteConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'sync_interval', 'max_batch_size', 'latest_app_version', 'update_required']
    list_display_links = ['id']
    list_editable = ['sync_interval', 'max_batch_size', 'latest_app_version', 'update_required']

    def has_add_permission(self, request):
        return not RiderRemoteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RiderWeeklyReport)
class RiderWeeklyReportAdmin(admin.ModelAdmin):
    list_display = ['week', 'rider', 'district', 'province', 'status', 'updated_at']
    list_filter = ['status', 'week', 'province']
    search_fields = ['rider__user__username', 'bike_registration']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReportAuditLog)
class ReportAuditLogAdmin(admin.ModelAdmin):
    list_display = ['report', 'section', 'edited_by', 'edited_at']
    list_filter = ['section', 'edited_at']
    search_fields = ['report__id', 'edited_by__username']
    readonly_fields = ['report', 'edited_by', 'section', 'old_data', 'new_data', 'edited_at']
    raw_id_fields = ['report', 'edited_by']


@admin.register(ReportVersion)
class ReportVersionAdmin(admin.ModelAdmin):
    list_display = ['report', 'version_number', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['report__id', 'created_by__username']
    readonly_fields = ['report', 'version_number', 'snapshot', 'created_by', 'created_at']
    raw_id_fields = ['report', 'created_by']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'user', 'action', 'model_name', 'object_repr']
    list_filter = ['action', 'model_name']
    search_fields = ['user__username', 'object_repr']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'created_at']


@admin.register(ProvincialDriverWeekly)
class ProvincialDriverWeeklyAdmin(admin.ModelAdmin):
    list_display = [
        'week_ending',
        'driver_name',
        'province',
        'district',
        'trips_count',
        'rider_accidents',
        'incomplete_bike_transport_trips',
        'samples_transported',
    ]
    list_filter = ['province', 'district', 'week_ending']
    search_fields = ['driver_name']


@admin.register(ReferredSample)
class ReferredSampleAdmin(admin.ModelAdmin):
    list_display = ['date_referred', 'sample_type', 'province', 'district', 'status']
    list_filter = ['province', 'district', 'status']
    search_fields = ['sample_type', 'reference_number']


@admin.register(RiderAccidentRecord)
class RiderAccidentRecordAdmin(admin.ModelAdmin):
    list_display = ['date', 'province', 'district', 'number_of_rider_accidents']
    list_filter = ['province', 'district', 'date']
    search_fields = ['district__name', 'province__name', 'comments']


@admin.register(IncompleteTripRecord)
class IncompleteTripRecordAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'province',
        'district',
        'incomplete_bike_transport_trips',
        'specimens_non_ist_methods',
    ]
    list_filter = ['province', 'district', 'date']
    search_fields = ['district__name', 'province__name', 'comments']


@admin.register(TransportIncident)
class TransportIncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_date', 'incident_type', 'province', 'district', 'resolved']
    list_filter = ['province', 'district', 'incident_type', 'resolved']
    search_fields = ['description', 'rider_or_driver_name']


# Register User with custom admin (role inline); unregister default first
if User is not None:
    try:
        admin.site.unregister(User)
    except admin.sites.NotRegistered:
        pass
    admin.site.register(User, CustomUserAdmin)
