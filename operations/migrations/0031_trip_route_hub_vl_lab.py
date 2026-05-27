from django.db import migrations, models


def migrate_facility_route_kinds(apps, schema_editor):
    RiderTripEntry = apps.get_model("operations", "RiderTripEntry")
    RiderTripEntry.objects.filter(route_kind="facility_to_facility").update(
        route_kind="hub_to_hub"
    )
    RiderTripEntry.objects.filter(route_kind="facility_to_lab").update(
        route_kind="hub_to_lab"
    )
    RiderTripEntry.objects.filter(route_kind="lab_to_facility").update(
        route_kind="lab_to_hub"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0030_trip_visit_purpose_choices"),
    ]

    operations = [
        migrations.RunPython(migrate_facility_route_kinds, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="ridertripentry",
            name="route_kind",
            field=models.CharField(
                blank=True,
                choices=[
                    ("hub_to_hub", "Hub to hub"),
                    ("hub_to_lab", "Hub to VL Lab"),
                    ("lab_to_hub", "VL Lab to hub"),
                    ("lab_to_lab", "VL Lab to VL Lab"),
                ],
                max_length=40,
                verbose_name="Trip Route",
            ),
        ),
    ]
