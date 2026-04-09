from django.core.management.base import BaseCommand
from django.db import transaction

from operations.models import RiderTripEntry, RiderWeeklyReport


class Command(BaseCommand):
    help = "Backfill one synthetic RiderTripEntry for reports without trip entries."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Preview only")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        created = 0
        for report in RiderWeeklyReport.objects.all().prefetch_related("trip_entries"):
            if report.trip_entries.exists():
                continue
            self.stdout.write(f"Backfill report #{report.pk} week={report.week_start}")
            if dry_run:
                continue
            with transaction.atomic():
                RiderTripEntry.objects.create(
                    report=report,
                    sequence=1,
                    entry_date=report.week_start,
                    vl_blood_plasma=report.samples_collected or 0,
                    fuel_allocated=0,
                    fuel_used=0,
                    distance_travelled=0,
                )
                created += 1
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run - no changes saved."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Created {created} synthetic trip entries."))
