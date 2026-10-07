from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0036_lab_manager_clearance"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="facility",
            unique_together={("district", "name", "kind")},
        ),
    ]
