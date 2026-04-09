# Data migration: driver-linked bikes → Car records; clear bike FK on driver profiles/reports.

from django.db import migrations


def migrate_driver_bikes_to_cars(apps, schema_editor):
    UserProfile = apps.get_model("operations", "UserProfile")
    RiderProfile = apps.get_model("operations", "RiderProfile")
    RiderWeeklyReport = apps.get_model("operations", "RiderWeeklyReport")
    Bike = apps.get_model("operations", "Bike")
    Car = apps.get_model("operations", "Car")

    bike_defaults = (
        "district_id",
        "notes",
        "active",
        "snp_bike_breakdown",
        "snp_bike_routine_service",
        "snp_bike_no_fuel",
        "snp_rider_sick_leave",
        "snp_rider_annual_leave",
        "snp_inclement_weather",
        "snp_bike_accident",
        "snp_clinical_ip",
        "snp_other",
        "snp_other_specify",
        "mitigation_measures",
    )

    for rp in RiderProfile.objects.filter(bike__isnull=False).iterator():
        try:
            up = UserProfile.objects.get(user_id=rp.user_id)
        except UserProfile.DoesNotExist:
            continue
        if up.role != "driver":
            continue
        bike = Bike.objects.get(pk=rp.bike_id)
        defaults = {k: getattr(bike, k) for k in bike_defaults}
        car, created = Car.objects.get_or_create(code=bike.code, defaults=defaults)
        if created:
            ids = list(bike.affected_facilities.values_list("pk", flat=True))
            if ids:
                car.affected_facilities.set(ids)
        rp.car_id = car.pk
        rp.bike_id = None
        rp.save(update_fields=["car_id", "bike_id"])

    for report in RiderWeeklyReport.objects.filter(bike__isnull=False).iterator():
        try:
            up = UserProfile.objects.get(user_id=report.rider_id)
        except UserProfile.DoesNotExist:
            continue
        if up.role != "driver":
            continue
        bike = Bike.objects.get(pk=report.bike_id)
        car = Car.objects.filter(code=bike.code).first()
        if not car:
            defaults = {k: getattr(bike, k) for k in bike_defaults}
            car = Car.objects.create(code=bike.code, **defaults)
            ids = list(bike.affected_facilities.values_list("pk", flat=True))
            if ids:
                car.affected_facilities.set(ids)
        report.car_id = car.pk
        report.bike_id = None
        report.save(update_fields=["car_id", "bike_id"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0015_car_model_and_vehicle_links"),
    ]

    operations = [
        migrations.RunPython(migrate_driver_bikes_to_cars, noop_reverse),
    ]
