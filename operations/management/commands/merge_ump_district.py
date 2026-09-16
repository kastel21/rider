"""Fold shorthand districts (UMP) into their official names without changing rider PKs when possible."""

from django.core.management.base import BaseCommand
from django.db import transaction

from operations.services.district_merge import merge_aliased_districts


class Command(BaseCommand):
    help = (
        "Merge alias districts (UMP, Murehwa, Mt. Darwin, Kadoma, …) into the rider "
        "canonical name, keeping the older district id so mobile district_id stays stable."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Preview only; roll back")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        with transaction.atomic():
            results = merge_aliased_districts()
            if not results:
                self.stdout.write("No aliased districts needed merging or renaming.")
            for row in results:
                absorbed = row["absorbed_ids"] or "—"
                self.stdout.write(
                    f"{row['province']}: kept id={row['kept_id']} as {row['renamed_to']!r}, "
                    f"absorbed {absorbed}"
                )
            if dry_run:
                transaction.set_rollback(True)
                self.stdout.write(self.style.WARNING("Dry run - rolled back."))
            else:
                self.stdout.write(self.style.SUCCESS("Done."))
