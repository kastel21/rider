import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("operations", "0031_trip_route_hub_vl_lab"),
    ]

    operations = [
        migrations.CreateModel(
            name="RiderWeekReliefCoverage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("week_start", models.DateField(db_index=True)),
                (
                    "is_relief_submission",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this week's record was made by a relief rider.",
                    ),
                ),
                (
                    "relief_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("sick", "Sick leave"),
                            ("annual", "Annual leave"),
                            ("special", "Special leave"),
                        ],
                        help_text="Why the assigned rider is absent (when relief submission).",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "relieved_rider",
                    models.ForeignKey(
                        blank=True,
                        help_text="Assigned rider being relieved this week.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="weeks_covered_by_relief",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="week_relief_coverages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-week_start", "-id"],
            },
        ),
        migrations.AddConstraint(
            model_name="riderweekreliefcoverage",
            constraint=models.UniqueConstraint(
                fields=("rider", "week_start"),
                name="uniq_rider_week_relief_coverage",
            ),
        ),
    ]
