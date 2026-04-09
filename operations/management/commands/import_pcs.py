"""
Import Program Coordinators from PCs.csv.

Creates/updates User, UserProfile (role=PC), PCProfile, and assigns provinces.
Password is set to Test123? for each imported user.

Riders without a district (or rider_profile) are invisible to PCs until assigned;
PC scope is rider.district.province in pc_profile.provinces.
"""
import csv
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from operations.models import PCProfile, Province, UserProfile

DEFAULT_PASSWORD = "Test123?"


def _username_base(pc_name: str) -> str:
    base = slugify(pc_name.strip()).replace("-", "_")
    if not base:
        base = "pc"
    return base[:150]


def _allocate_username(base: str, exclude_pk: int | None = None) -> str:
    candidate = base
    n = 2
    while True:
        qs = User.objects.filter(username=candidate)
        if exclude_pk is not None:
            qs = qs.exclude(pk=exclude_pk)
        if not qs.exists():
            return candidate
        candidate = f"{base}_{n}"
        n += 1


class Command(BaseCommand):
    help = (
        "Import PCs from CSV (columns: PC, Province, email). "
        f"Sets password to {DEFAULT_PASSWORD!r}. "
        "Use --dry-run to print actions without saving. "
        "If your shell treats ? specially, quote the password when testing logins."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=None,
            help="CSV path (default: BASE_DIR/PCs.csv)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not write to the database.",
        )

    def handle(self, *args, **options):
        path = options["file"]
        csv_path = Path(path) if path else Path(settings.BASE_DIR) / "PCs.csv"
        if not csv_path.is_file():
            raise CommandError(f"CSV not found: {csv_path}")

        dry_run = options["dry_run"]

        grouped: dict[str, dict] = defaultdict(lambda: {"provinces": [], "email": ""})
        with csv_path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cols = {c.strip() for c in (reader.fieldnames or [])}
            required = {"PC", "Province"}
            if not required.issubset(cols):
                raise CommandError(
                    f"CSV must include columns: {sorted(required)}. Got: {reader.fieldnames}"
                )
            for row in reader:
                pc_name = (row.get("PC") or "").strip()
                prov_name = (row.get("Province") or "").strip()
                email = (row.get("email") or "").strip()
                if not pc_name or not prov_name:
                    self.stderr.write(f"Skipping row with empty PC/Province: {row!r}")
                    continue
                grouped[pc_name]["provinces"].append(prov_name)
                if email:
                    grouped[pc_name]["email"] = email

        if not grouped:
            raise CommandError("No rows to import.")

        self.stdout.write(f"Found {len(grouped)} PC user(s) in {csv_path}")

        for pc_name, data in sorted(grouped.items()):
            provinces_names = list(dict.fromkeys(data["provinces"]))
            email = data["email"] or ""
            base = _username_base(pc_name)

            user = User.objects.filter(username=base).first()
            if user is None:
                short = pc_name.strip()[:30]
                user = (
                    User.objects.filter(first_name=short, profile__role=UserProfile.Role.PC)
                    .first()
                )

            if user is None:
                username = _allocate_username(base)
            else:
                username = user.username

            province_objs = []
            for pname in provinces_names:
                prov, _ = Province.objects.get_or_create(name=pname)
                province_objs.append(prov)

            self.stdout.write(
                f"  {pc_name!r} -> username={username!r}, "
                f"provinces={[p.name for p in province_objs]}, email={email!r}"
            )

            if dry_run:
                continue

            with transaction.atomic():
                if user is None:
                    user = User(username=username)
                user.first_name = pc_name.strip()[:30]
                user.email = email
                user.set_password(DEFAULT_PASSWORD)
                user.save()

                profile, _ = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={"role": UserProfile.Role.PC},
                )
                profile.role = UserProfile.Role.PC
                profile.save(update_fields=["role"])

                pc_prof, _ = PCProfile.objects.get_or_create(user=user)
                pc_prof.provinces.set(province_objs)

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run - no changes saved."))
        else:
            self.stdout.write(self.style.SUCCESS("Import finished."))
