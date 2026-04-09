"""
Import drivers from drivers.csv — same pattern as import_riders_csv:
Province, User + UserProfile(role driver), RiderProfile (province + vehicle as Car).

Drivers have no district in the CSV; RiderProfile.district and Car.district stay unset unless
you later assign them in admin.
"""
import csv
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from operations.models import Car, Province, RiderProfile, UserProfile

DEFAULT_PASSWORD = "Test123?"

# Shorthand in CSV → full province name (also used by import_riders_csv).
PROVINCE_ALIASES = {
    "mat north": "Matabeleland North",
    "mat south": "Matabeleland South",
    "mash east": "Mashonaland East",
    "mash west": "Mashonaland West",
    "mash central": "Mashonaland Central",
}


def _norm_text(v):
    return " ".join((v or "").strip().split())


def _canon_province(name):
    n = _norm_text(name)
    return PROVINCE_ALIASES.get(n.lower(), n)


def _username_base(name):
    base = slugify(_norm_text(name)).replace("-", "_")
    return (base or "driver")[:150]


def _alloc_username(base, exclude_pk=None):
    candidate = base
    i = 2
    while True:
        qs = User.objects.filter(username=candidate)
        if exclude_pk is not None:
            qs = qs.exclude(pk=exclude_pk)
        if not qs.exists():
            return candidate
        candidate = f"{base}_{i}"
        i += 1


class Command(BaseCommand):
    help = (
        "Import drivers from drivers.csv (Name of Driver, Vehicle Registration Number, Province). "
        f"Default password: {DEFAULT_PASSWORD!r}."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=None,
            help="CSV path (default BASE_DIR/drivers.csv)",
        )
        parser.add_argument("--dry-run", action="store_true", help="Preview only")

    def handle(self, *args, **options):
        csv_path = Path(options["file"]) if options["file"] else Path(settings.BASE_DIR) / "drivers.csv"
        if not csv_path.is_file():
            raise CommandError(f"CSV not found: {csv_path}")
        dry_run = options["dry_run"]

        with csv_path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise CommandError("CSV has no headers.")
            headers = {h.strip(): h for h in reader.fieldnames}
            required = [
                "Name of Driver",
                "Vehicle Registration Number",
                "Province",
            ]
            missing = [r for r in required if r not in headers]
            if missing:
                raise CommandError(f"Missing required headers: {missing}")

            created_users = 0
            updated_users = 0
            skipped = 0

            for row in reader:
                driver_name = _norm_text(row.get(headers["Name of Driver"], ""))
                vehicle_code = _norm_text(
                    row.get(headers["Vehicle Registration Number"], "")
                ).upper()
                province_name = _canon_province(row.get(headers["Province"], ""))

                if not driver_name or not province_name or not vehicle_code:
                    skipped += 1
                    continue

                first_name, _, last_name = driver_name.partition(" ")

                with transaction.atomic():
                    province, _ = Province.objects.get_or_create(name=province_name)

                    car, _ = Car.objects.get_or_create(
                        code=vehicle_code,
                        defaults={"district": None},
                    )

                    username_base = _username_base(driver_name)
                    user = User.objects.filter(username=username_base).first()
                    if user is None:
                        user = User.objects.filter(
                            first_name=first_name[:150], last_name=last_name[:150]
                        ).first()
                    if user is None and car is not None:
                        user = User.objects.filter(rider_profile__car=car).first()

                    if user is None:
                        username = _alloc_username(username_base)
                        user = User(username=username)
                        created_users += 1
                    else:
                        username = _alloc_username(username_base, exclude_pk=user.pk)
                        updated_users += 1

                    user.username = username
                    user.first_name = first_name[:150]
                    user.last_name = last_name[:150]
                    user.set_password(DEFAULT_PASSWORD)
                    if not dry_run:
                        user.save()

                    if not dry_run:
                        profile, _ = UserProfile.objects.get_or_create(
                            user=user,
                            defaults={"role": UserProfile.Role.DRIVER},
                        )
                        profile.role = UserProfile.Role.DRIVER
                        profile.save(update_fields=["role"])

                        rprof, _ = RiderProfile.objects.get_or_create(user=user)
                        rprof.province = province
                        rprof.district = None
                        rprof.car = car
                        rprof.bike = None
                        rprof.support_type = ""
                        rprof.save()

                self.stdout.write(
                    f"{'[DRY]' if dry_run else '[OK]'} {driver_name} -> {province_name}, "
                    f"vehicle={vehicle_code}"
                )

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run - no changes saved."))
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. users created={created_users}, users updated={updated_users}, rows skipped={skipped}"
            )
        )
