# Generated manually for rider JWT API support.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0020_pcdistrictweeklytransportstat"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lab",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                ("code", models.CharField(blank=True, max_length=64)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="RiderRemoteConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sync_interval", models.PositiveIntegerField(default=60)),
                ("max_batch_size", models.PositiveIntegerField(default=10)),
                ("latest_app_version", models.CharField(blank=True, max_length=60)),
                ("update_required", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Rider Remote Config",
            },
        ),
        migrations.CreateModel(
            name="RiderDevice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("device_id", models.CharField(help_text="Client device identifier.", max_length=255)),
                ("device_model", models.CharField(blank=True, max_length=120)),
                ("app_version", models.CharField(blank=True, max_length=60)),
                ("last_seen", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "rider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="devices",
                        to="operations.riderprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["rider", "-last_seen"],
                "unique_together": {("rider", "device_id")},
            },
        ),
    ]
