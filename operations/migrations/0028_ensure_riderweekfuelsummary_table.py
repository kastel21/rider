"""Repair environments where 0027 is recorded but the table was never created (e.g. MSSQL)."""

from django.db import migrations


def ensure_riderweekfuelsummary_table(apps, schema_editor):
    connection = schema_editor.connection
    table = "operations_riderweekfuelsummary"
    with connection.cursor() as cursor:
        existing = {n.lower() for n in connection.introspection.table_names(cursor)}
    if table.lower() in existing:
        return
    Model = apps.get_model("operations", "RiderWeekFuelSummary")
    schema_editor.create_model(Model)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0027_riderweekfuelsummary"),
    ]

    operations = [
        migrations.RunPython(ensure_riderweekfuelsummary_table, noop_reverse),
    ]
