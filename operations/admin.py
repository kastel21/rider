from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Bike,
    Car,
    District,
    Facility,
    PCDistrictWeeklyTransportStat,
    PCProfile,
    Province,
    RegisteredDevice,
    ReportAuditLog,
    ReportEditSnapshot,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    SampleRejection,
    UserProfile,
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "support_type")
    search_fields = ("name",)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "site_code", "kind", "support_type", "district")
    list_filter = ("support_type", "kind", "district__province")
    search_fields = ("name", "site_code")


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ("code", "district", "active")
    search_fields = ("code",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("code", "district", "active")
    search_fields = ("code",)


@admin.register(PCProfile)
class PCProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("provinces",)


@admin.register(PCDistrictWeeklyTransportStat)
class PCDistrictWeeklyTransportStatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "week_start",
        "district",
        "rider_accidents",
        "incomplete_bike_transport_trips",
        "updated_at",
    )
    list_filter = ("week_start", "district__province")
    list_select_related = ("district", "district__province")
    autocomplete_fields = ("district",)
    search_fields = ("district__name", "comments")
    ordering = ("-week_start", "district__province__name", "district__name")


@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "province", "district", "support_type", "facility", "bike", "car")


class SampleRejectionInline(admin.TabularInline):
    model = SampleRejection
    extra = 0


@admin.register(RiderWeeklyReport)
class RiderWeeklyReportAdmin(admin.ModelAdmin):
    list_display = ("id", "rider", "bike", "car", "updated_at", "status", "client_uuid")
    list_filter = ("status",)
    search_fields = ("title", "notes", "rider__username", "bike__code", "car__code")
    list_select_related = ("rider", "bike", "car")
    autocomplete_fields = ("bike", "car")
    inlines = (SampleRejectionInline,)


@admin.register(SampleRejection)
class SampleRejectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "report",
        "sample_type",
        "rejected_total",
        "rejected_too_old",
        "rejected_patient_info_mismatch",
        "rejected_request_form_missing",
        "rejected_sample_missing",
        "rejected_other",
        "order",
    )
    list_filter = ("sample_type",)
    list_select_related = ("report",)


@admin.register(RiderTripEntry)
class RiderTripEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "report",
        "sequence",
        "transport_kind",
        "entry_date",
        "visit_purpose",
        "route_kind",
        "origin_facility",
        "destination_facility",
        "fuel_allocated",
        "fuel_used",
    )
    list_filter = ("transport_kind", "entry_date", "visit_purpose", "route_kind")
    list_select_related = ("report", "origin_facility", "destination_facility")
    autocomplete_fields = ("origin_facility", "destination_facility")


@admin.register(ReportAuditLog)
class ReportAuditLogAdmin(admin.ModelAdmin):
    list_display = ("report", "action", "actor", "created_at")


@admin.register(ReportEditSnapshot)
class ReportEditSnapshotAdmin(admin.ModelAdmin):
    list_display = ("report", "editor", "summary", "created_at")


@admin.register(RegisteredDevice)
class RegisteredDeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "device_id", "platform", "last_seen_at")
