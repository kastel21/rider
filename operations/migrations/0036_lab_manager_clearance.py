import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0035_merge_district_aliases"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="riderweeklyreport",
            name="lab_cleared_at",
            field=models.DateTimeField(
                blank=True,
                help_text="When the district lab manager released this report to the PC.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="riderweeklyreport",
            name="lab_cleared_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reports_lab_cleared",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="riderweeklyreport",
            name="lab_notes",
            field=models.TextField(
                blank=True,
                help_text="Reason from the lab manager when the report is sent back to the rider.",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="role",
            field=models.CharField(
                choices=[
                    ("rider", "Rider"),
                    ("driver", "Driver"),
                    ("pc", "Program Coordinator"),
                    ("lab_manager", "Lab manager"),
                    ("me", "Monitoring & Evaluation"),
                    ("admin", "Administrator"),
                ],
                default="rider",
                max_length=32,
            ),
        ),
        migrations.CreateModel(
            name="LabManagerProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="lab_managers",
                        to="operations.district",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lab_manager_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
