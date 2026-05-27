from django.db import migrations, models


def migrate_visit_purposes(apps, schema_editor):
    RiderTripEntry = apps.get_model("operations", "RiderTripEntry")
    RiderTripEntry.objects.filter(visit_purpose="sample_collection").update(
        visit_purpose="specimens_results_transport"
    )
    RiderTripEntry.objects.filter(visit_purpose="sample_delivery").update(
        visit_purpose="specimens_results_transport"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0029_riderweeklyreport_distance_travelled"),
    ]

    operations = [
        migrations.RunPython(migrate_visit_purposes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="ridertripentry",
            name="visit_purpose",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "specimens_results_transport",
                        "Specimens and Results Transportation",
                    ),
                    ("adhoc", "Adhoc"),
                    ("relay", "Relay"),
                ],
                max_length=32,
            ),
        ),
    ]
