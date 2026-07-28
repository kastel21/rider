from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0032_riderweekreliefcoverage"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccessibleApp",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("package_name", models.CharField(db_index=True, max_length=255, unique=True)),
                ("label", models.CharField(blank=True, max_length=255)),
                (
                    "is_system",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text="System/launcher-hidden packages are excluded from the admin picker.",
                    ),
                ),
                (
                    "is_allowed",
                    models.BooleanField(
                        default=False,
                        help_text="When enabled, this app may be accessible on rider devices.",
                    ),
                ),
                ("last_seen_at", models.DateTimeField(blank=True, null=True)),
                ("report_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Accessible app",
                "verbose_name_plural": "Accessible apps",
                "ordering": ["label", "package_name"],
            },
        ),
    ]
