from django.db import migrations


def legacy_driver_trips_to_relayed(apps, schema_editor):
    RiderTripEntry = apps.get_model("operations", "RiderTripEntry")
    RiderTripEntry.objects.filter(
        transport_kind="legacy",
        report__rider__profile__role="driver",
    ).update(transport_kind="relayed")


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0017_ridertripentry_transport_kind"),
    ]

    operations = [
        migrations.RunPython(legacy_driver_trips_to_relayed, noop_reverse),
    ]
