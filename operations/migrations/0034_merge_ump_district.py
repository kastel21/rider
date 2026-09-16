from django.db import migrations


def merge_ump_alias(apps, schema_editor):
    from operations.services.district_merge import merge_aliased_districts

    merge_aliased_districts(apps=apps)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0033_accessibleapp"),
    ]

    operations = [
        migrations.RunPython(merge_ump_alias, noop_reverse),
    ]
