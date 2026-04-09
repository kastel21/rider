from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0016_migrate_driver_bikes_to_cars"),
    ]

    operations = [
        migrations.AddField(
            model_name="ridertripentry",
            name="transport_kind",
            field=models.CharField(
                choices=[
                    ("legacy", "Legacy (rider / historical)"),
                    ("relayed", "Samples relayed (not carried for the first time)"),
                    ("first_transport", "Samples transported for the first time"),
                ],
                db_index=True,
                default="legacy",
                max_length=32,
            ),
            preserve_default=False,
        ),
    ]
