import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("operations", "0026_weeklyrecordreviewed"),
    ]

    operations = [
        migrations.CreateModel(
            name="RiderWeekFuelSummary",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("week_start", models.DateField(db_index=True)),
                ("fuel_allocated", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("fuel_used", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("distance_travelled", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "rider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="week_fuel_summaries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-week_start", "-id"],
            },
        ),
        migrations.AddConstraint(
            model_name="riderweekfuelsummary",
            constraint=models.UniqueConstraint(fields=("rider", "week_start"), name="uniq_rider_week_fuel_summary"),
        ),
    ]
