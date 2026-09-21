"""
Match sites_rev.csv to existing hubs/clinics in the same district.

Default is a dry-run (no writes). VL labs, review rows, and unmatched existing
sites are left alone. --apply renames safe matches and creates unmatched CSV sites.

  python manage.py sync_facilities_from_csv
  python manage.py sync_facilities_from_csv --source db --apply
  python manage.py sync_facilities_from_csv --update-fixtures
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from operations.services.facility_catalog_sync import (
    apply_catalog_plan,
    apply_plan_to_fixtures,
    load_db_facilities,
    load_fixture_facilities,
    parse_sites_csv,
    plan_catalog,
    write_plan_csvs,
)


class Command(BaseCommand):
    help = (
        "Match a sites CSV to existing non-lab facilities. "
        "Dry-run by default; --apply writes rename+create only."
    )

    def add_arguments(self, parser):
        default_csv = Path(settings.BASE_DIR) / "sites_rev.csv"
        parser.add_argument(
            "--file",
            type=str,
            default=str(default_csv),
            help="CSV with Province, District, Site columns (DHIS2 prefixes are stripped).",
        )
        parser.add_argument(
            "--source",
            choices=("fixtures", "db"),
            default="fixtures",
            help="Compare against bundled TSVs (default) or the live Facility table.",
        )
        parser.add_argument(
            "--out-dir",
            type=str,
            default="",
            help="Directory for CSV reports (default: operations/reports/facility_sync_dry_run).",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write rename + create to the database. Does not delete unmatched or labs.",
        )
        parser.add_argument(
            "--update-fixtures",
            action="store_true",
            help="Rewrite clinic/hub TSV fixtures (rename + append creates). Labs TSV is not changed.",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        if not path.is_file():
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        sites, skipped = parse_sites_csv(path)
        if options["source"] == "db":
            existing = load_db_facilities()
            source = "db"
        else:
            existing = load_fixture_facilities()
            source = "fixtures"

        plan = plan_catalog(sites, existing, source=source)
        plan.skipped_csv = skipped
        counts = plan.counts()

        out_dir = Path(options["out_dir"]) if options["out_dir"] else (
            Path(settings.BASE_DIR) / "operations" / "reports" / "facility_sync_dry_run"
        )
        written = write_plan_csvs(plan, out_dir)

        self.stdout.write(f"Source: {source} ({len(existing)} existing rows including labs)", ending="\n")
        self.stdout.flush()
        self.stdout.write(f"CSV sites parsed: {len(sites)}; skipped: {len(skipped)}")
        self.stdout.write(
            f"unchanged={counts['unchanged']} rename={counts['rename']} "
            f"create={counts['create']} review={counts['review']} "
            f"unmatched_existing={counts['unmatched_existing']}"
        )
        for p in written:
            self.stdout.write(f"  wrote {p}")

        if not options["apply"] and not options["update_fixtures"]:
            self.stdout.write(self.style.WARNING("Dry run only — no database or fixture writes."))
            return

        if options["update_fixtures"]:
            if source != "fixtures":
                self.stdout.write("Recomputing fixture plan for TSV update…")
                fixture_plan = plan_catalog(sites, load_fixture_facilities(), source="fixtures")
            else:
                fixture_plan = plan
            fx = apply_plan_to_fixtures(
                fixture_plan,
                Path(settings.BASE_DIR) / "operations" / "fixtures",
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixtures: renamed={fx['renamed']} created={fx['created']}"
                )
            )

        if options["apply"]:
            self.stdout.write("Applying rename + create to the database…")
            self.stdout.flush()
            if source != "db":
                self.stdout.write("Loading live facilities for database apply…")
                db_plan = plan_catalog(sites, load_db_facilities(), source="db")
            else:
                db_plan = plan
            with transaction.atomic():
                stats = apply_catalog_plan(db_plan)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Database: renamed={stats['renamed']} created={stats['created']} "
                    f"rename_skipped={stats['rename_skipped']} create_skipped={stats['create_skipped']} "
                    f"review_left={stats['review_left']} unmatched_kept={stats['unmatched_kept']}"
                )
            )
