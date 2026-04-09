"""
Load serialized data from DATABASES['sqlite'] (DJANGO_SQLITE_IMPORT_PATH) into default (e.g. MSSQL).

Typical use after schema migrate on SQL Server:
  1. Set DJANGO_SQLITE_IMPORT_PATH to your old db.sqlite3 (absolute path).
  2. Keep DJANGO_DB_ENGINE=mssql so default points at SQL Server.
  3. Run: python manage.py import_sqlite_data --flush-target

--flush-target clears all rows in default before loading (recommended when default only has
empty tables from migrate, or you are replacing dev data). Destructive on production.
"""

import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Copy data from legacy SQLite (DJANGO_SQLITE_IMPORT_PATH) into the default database."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush-target",
            action="store_true",
            help=(
                "Run flush on the default database before loading (removes all rows). "
                "Use when the target DB should be replaced entirely by the SQLite export."
            ),
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            default="",
            help="Write the JSON fixture to this path and exit (no load). Implies --dry-run.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only write the fixture to a temp file and print its path; do not load.",
        )

    def handle(self, *args, **options):
        if "sqlite" not in settings.DATABASES:
            raise CommandError(
                "Add DJANGO_SQLITE_IMPORT_PATH to your environment (.env) with the full path "
                "to your legacy db.sqlite3 file. The file must exist. "
                "Default DB must not be SQLite (otherwise use dumpdata/loaddata manually). "
                "Use forward slashes in .env (backslashes break: \\r in D:\\rider...). "
                "Example: DJANGO_SQLITE_IMPORT_PATH=D:/projects/rider app/db.sqlite3"
            )

        out_path = (options.get("output") or "").strip()
        dry = options["dry_run"] or bool(out_path)
        flush_target = options["flush_target"]

        fixture_path: str | None = None
        try:
            if out_path:
                fixture_path = str(Path(out_path).resolve())
                self._write_fixture(fixture_path)
                self.stdout.write(self.style.SUCCESS(f"Wrote fixture: {fixture_path}"))
                return

            fd, tmp = tempfile.mkstemp(prefix="sqlite_import_", suffix=".json")
            os.close(fd)
            fixture_path = tmp
            self.stdout.write("Dumping from SQLite (this is usually quick)...")
            self._write_fixture(fixture_path)
            self.stdout.write(
                f"Dump complete ({os.path.getsize(fixture_path) // 1024} KiB). "
                "Remote SQL Server load can take several minutes."
            )

            if dry:
                self.stdout.write(self.style.SUCCESS(f"Dry-run fixture: {fixture_path}"))
                return

            if flush_target:
                self.stdout.write("Flushing default database...")
                call_command("flush", database="default", interactive=False, verbosity=1)
                self.stdout.write("Flush complete.")

            self.stdout.write("Loading fixture into default database...")
            call_command("loaddata", fixture_path, database="default", verbosity=1)
            self.stdout.write(self.style.SUCCESS("Import finished."))
        finally:
            if fixture_path and not out_path and not dry and os.path.isfile(fixture_path):
                try:
                    os.remove(fixture_path)
                except OSError:
                    pass

    def _write_fixture(self, path: str) -> None:
        excludes = ["sessions", "admin.logentry"]
        with open(path, "w", encoding="utf-8") as f:
            call_command(
                "dumpdata",
                database="sqlite",
                natural_foreign=True,
                natural_primary=True,
                indent=2,
                stdout=f,
                exclude=excludes,
            )
