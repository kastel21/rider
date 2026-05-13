from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0025_remove_riderweeklyreport_uniq_rider_week"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WeeklyRecordReviewed",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("week_start", models.DateField(db_index=True)),
                ("reviewed_at", models.DateTimeField(auto_now_add=True)),
                ("snapshot", models.JSONField(blank=True, default=dict)),
                (
                    "reviewed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="weekly_records_reviewed_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weekly_records_reviewed",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "source_report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weekly_review_records",
                        to="operations.riderweeklyreport",
                    ),
                ),
            ],
            options={
                "db_table": "weekly_record_reviewed",
                "ordering": ["-reviewed_at", "-id"],
            },
        ),
    ]
