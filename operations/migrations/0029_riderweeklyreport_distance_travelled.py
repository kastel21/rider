from decimal import Decimal

from django.db import migrations, models
from django.db.models import Sum


def backfill_distance_from_trips(apps, schema_editor):
    RiderWeeklyReport = apps.get_model("operations", "RiderWeeklyReport")
    RiderTripEntry = apps.get_model("operations", "RiderTripEntry")
    for r in RiderWeeklyReport.objects.all().iterator(chunk_size=500):
        agg = RiderTripEntry.objects.filter(report_id=r.pk).aggregate(s=Sum("distance_travelled"))
        raw = agg.get("s")
        if raw is None:
            continue
        val = Decimal(str(raw))
        if val != 0:
            RiderWeeklyReport.objects.filter(pk=r.pk).update(distance_travelled=val)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0028_ensure_riderweekfuelsummary_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="riderweeklyreport",
            name="distance_travelled",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.RunPython(backfill_distance_from_trips, noop_reverse),
    ]
