"""
Import Province / District / Facility rows from a tab-separated file (province, district, facility name).
Sets Facility.support_type (default TA-SDI). Optionally sets District.support_type for touched districts.

Bundled fixtures:
  operations/fixtures/facilities_ta_sdi.tsv  (default) --support TA-SDI
  operations/fixtures/facilities_dsd.tsv     use: --file ... --support DSD
  operations/fixtures/facility_labs.tsv        use: --file ... --facility-kind lab --blank-support

Usage:
  python manage.py import_facilities_ta_sdi
  python manage.py import_facilities_ta_sdi --file operations/fixtures/facilities_dsd.tsv --support DSD
  python manage.py import_facilities_ta_sdi --file operations/fixtures/facility_labs.tsv --facility-kind lab --blank-support
  python manage.py import_facilities_ta_sdi --file path/to/list.tsv --dry-run
"""

from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from operations.models import District, Facility, Province, SupportType


def _infer_kind(name: str) -> str:
    n = name.lower()
    if "lab" in n and "laboratory" not in n:
        return Facility.Kind.LAB
    if any(x in n for x in ("hospital", "rhc", "health centre", "health center", "polyclinic")):
        return Facility.Kind.CLINIC
    return Facility.Kind.CLINIC


class Command(BaseCommand):
    help = "Import facilities from TSV (province \\t district \\t facility) and set support type."

    def add_arguments(self, parser):
        default = Path(__file__).resolve().parent.parent.parent / "fixtures" / "facilities_ta_sdi.tsv"
        parser.add_argument(
            "--file",
            type=str,
            default=str(default),
            help="TSV path (default: operations/fixtures/facilities_ta_sdi.tsv)",
        )
        parser.add_argument(
            "--support",
            type=str,
            default=SupportType.TA_SDI,
            help=(
                f"PEPFAR support type on Facility (default: {SupportType.TA_SDI}). "
                "Ignored when --blank-support is set."
            ),
        )
        parser.add_argument(
            "--blank-support",
            action="store_true",
            help="Leave Facility.support_type empty (e.g. reference labs / non-PEPFAR sites).",
        )
        parser.add_argument(
            "--facility-kind",
            type=str,
            default="",
            help="Force Facility.kind: hub, lab, or clinic (default: infer from name). Use 'lab' for laboratory sites.",
        )
        parser.add_argument(
            "--update-districts",
            action="store_true",
            help="Also set District.support_type for districts created/updated by this import.",
        )
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        path = Path(options["file"])
        blank_support = options["blank_support"]
        support = "" if blank_support else options["support"]
        if not blank_support and support not in {c.value for c in SupportType}:
            valid = ", ".join(c.value for c in SupportType)
            self.stderr.write(self.style.ERROR(f"Invalid --support {support!r}. Choose one of: {valid}"))
            return

        fk = (options["facility_kind"] or "").strip().lower()
        kind_map = {
            "hub": Facility.Kind.HUB,
            "lab": Facility.Kind.LAB,
            "clinic": Facility.Kind.CLINIC,
        }
        if fk and fk not in kind_map:
            self.stderr.write(
                self.style.ERROR(f"--facility-kind must be one of: {', '.join(kind_map)} (got {fk!r})")
            )
            return
        fixed_kind = kind_map[fk] if fk else None

        if not path.is_file():
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        raw = path.read_text(encoding="utf-8")
        created_p = created_d = created_f = updated_f = updated_d = 0
        skipped = 0

        with transaction.atomic():
            for line_no, line in enumerate(raw.splitlines(), start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) < 3:
                    self.stderr.write(self.style.WARNING(f"Line {line_no}: expected 3+ tab columns, skipping"))
                    skipped += 1
                    continue
                prov_name = parts[0].strip()
                dist_name = parts[1].strip()
                fac_name = "\t".join(parts[2:]).strip()
                if not prov_name or not dist_name or not fac_name:
                    skipped += 1
                    continue

                province, p_created = Province.objects.get_or_create(name=prov_name)
                if p_created:
                    created_p += 1

                if options["update_districts"] and not blank_support:
                    district, d_created = District.objects.get_or_create(
                        province=province,
                        name=dist_name,
                        defaults={"support_type": support},
                    )
                else:
                    district, d_created = District.objects.get_or_create(
                        province=province,
                        name=dist_name,
                    )
                if d_created:
                    created_d += 1
                elif options["update_districts"] and not blank_support and district.support_type != support:
                    district.support_type = support
                    district.save(update_fields=["support_type"])
                    updated_d += 1

                kind = fixed_kind if fixed_kind is not None else _infer_kind(fac_name)
                fac_defaults = {"kind": kind, "support_type": support}
                fac, f_created = Facility.objects.get_or_create(
                    district=district,
                    name=fac_name,
                    defaults=fac_defaults,
                )
                if f_created:
                    created_f += 1
                else:
                    changed = False
                    if not blank_support and fac.support_type != support:
                        fac.support_type = support
                        changed = True
                    elif blank_support and fac.support_type:
                        fac.support_type = ""
                        changed = True
                    if fac.kind != kind:
                        fac.kind = kind
                        changed = True
                    if changed:
                        fac.save()
                        updated_f += 1

            if options["dry_run"]:
                transaction.set_rollback(True)

        self.stdout.write(
            f"Provinces created: {created_p}, districts created: {created_d}, "
            f"facilities created: {created_f}, facilities updated: {updated_f}, "
            f"districts support updated: {updated_d}, lines skipped: {skipped}"
        )
        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("Dry run - rolled back."))
