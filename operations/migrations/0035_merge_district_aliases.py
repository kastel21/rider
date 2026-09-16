from django.db import migrations


def merge_district_aliases(apps, schema_editor):
    from operations.services.district_merge import merge_aliased_districts

    merge_aliased_districts(apps=apps)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0034_merge_ump_district"),
    ]

    operations = [
        migrations.RunPython(merge_district_aliases, noop_reverse),
    ]
