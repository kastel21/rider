from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0037_facility_unique_name_per_kind"),
    ]

    operations = [
        migrations.AddField(
            model_name="riderremoteconfig",
            name="min_version_code",
            field=models.PositiveIntegerField(
                default=0,
                help_text=(
                    "Android versionCode phones must be on. The build that checks for updates is "
                    "versionCode 3. Leave this at 0 until an APK is uploaded and you are ready to force it."
                ),
            ),
        ),
        migrations.AlterField(
            model_name="riderremoteconfig",
            name="latest_app_version",
            field=models.CharField(
                blank=True,
                help_text="Version name shown on the phone, for example 1.3.",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="riderremoteconfig",
            name="update_required",
            field=models.BooleanField(
                default=False,
                help_text="When on, Android apps older than the minimum version code cannot sign in or sync.",
            ),
        ),
        migrations.CreateModel(
            name="RiderAppRelease",
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
                    "application_id",
                    models.CharField(
                        db_index=True,
                        help_text=(
                            "Must match the installed app. E-Collect 64-bit is com.ecollect.app.bit64, "
                            "32-bit is com.ecollect.app.bit32. Rider 64-bit is com.operations.rider.bit64, "
                            "32-bit is com.operations.rider.bit32."
                        ),
                        max_length=120,
                    ),
                ),
                (
                    "version_code",
                    models.PositiveIntegerField(
                        help_text="Android versionCode baked into this APK. Must be greater than or equal to the minimum you enforce.",
                    ),
                ),
                (
                    "version_name",
                    models.CharField(
                        blank=True,
                        help_text="Shown on the phone, for example 1.3.",
                        max_length=60,
                    ),
                ),
                ("apk", models.FileField(upload_to="app_releases/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Rider app release",
                "ordering": ["-version_code", "-pk"],
            },
        ),
        migrations.AddConstraint(
            model_name="riderapprelease",
            constraint=models.UniqueConstraint(
                fields=("application_id", "version_code"),
                name="uniq_rider_app_release_version",
            ),
        ),
    ]
