"""
Import riders and reference data from riders.csv.

Creates/updates:
- Province
- District (with support type)
- Bike (linked to district)
- User + UserProfile(role rider/driver)
- RiderProfile (linked to province/district/bike/support type)
"""
import csv
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from operations.models import Bike, District, Province, RiderProfile, SupportType, UserProfile

DEFAULT_PASSWORD = "Test123?"

# Shorthand → full province name (same as import_drivers_csv).
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


def _canon_support(v):
    s = _norm_text(v).upper()
    if s in {"DSD", "TA-SDI", "TAT"}:
        return s
    return SupportType.OTHER if s else ""


def _username_base(name):
    base = slugify(_norm_text(name)).replace("-", "_")
    return (base or "rider")[:150]


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
        "Import riders from riders.csv and link provinces/districts/bikes/support type. "
        f"Default password: {DEFAULT_PASSWORD!r}."
    )

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, default=None, help="CSV path (default BASE_DIR/riders.csv)")
        parser.add_argument("--dry-run", action="store_true", help="Preview only")
        parser.add_argument("--include-vacant", action="store_true", help="Include rows like 'Vacant Post'")

    def handle(self, *args, **options):
        csv_path = Path(options["file"]) if options["file"] else Path(settings.BASE_DIR) / "riders.csv"
        if not csv_path.is_file():
            raise CommandError(f"CSV not found: {csv_path}")
        dry_run = options["dry_run"]
        include_vacant = options["include_vacant"]

        with csv_path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise CommandError("CSV has no headers.")
            headers = {h.strip(): h for h in reader.fieldnames}
            support_col_key = None
            for cand in ("type of support", "Types of PEPFAR Support"):
                if cand in headers:
                    support_col_key = headers[cand]
                    break
            required = [
                "Name of Rider",
                "Bike Registration Number",
                "Province",
                "District",
            ]
            missing = [r for r in required if r not in headers and f"{r} " not in headers]
            if support_col_key is None:
                missing.append("type of support")
            if missing:
                raise CommandError(f"Missing required headers: {missing}")

            created_users = 0
            updated_users = 0
            skipped = 0

            for row in reader:
                rider_name = _norm_text(row.get(headers.get("Name of Rider", "Name of Rider"), ""))
                bike_code = _norm_text(row.get(headers.get("Bike Registration Number", "Bike Registration Number"), "")).upper()
                province_name = _canon_province(row.get(headers.get("Province", "Province "), ""))
                district_name = _norm_text(row.get(headers.get("District", "District "), ""))
                support_type = _canon_support(row.get(support_col_key, ""))
                rider_type = _norm_text(row.get(headers.get("Rider Type", "Rider Type"), "rider")).lower()

                if not rider_name or not province_name or not district_name:
                    skipped += 1
                    continue
                if (not include_vacant) and rider_name.lower().startswith("vacant post"):
                    skipped += 1
                    continue

                role = UserProfile.Role.DRIVER if rider_type == "driver" else UserProfile.Role.RIDER
                first_name, _, last_name = rider_name.partition(" ")

                with transaction.atomic():
                    province, _ = Province.objects.get_or_create(name=province_name)
                    district, _ = District.objects.get_or_create(
                        province=province,
                        name=district_name,
                    )
                    if support_type and district.support_type != support_type:
                        district.support_type = support_type
                        district.save(update_fields=["support_type"])

                    bike = None
                    if bike_code:
                        bike, _ = Bike.objects.get_or_create(code=bike_code, defaults={"district": district})
                        if bike.district_id != district.id:
                            bike.district = district
                            bike.save(update_fields=["district"])

                    username_base = _username_base(rider_name)
                    user = User.objects.filter(username=username_base).first()
                    if user is None:
                        user = User.objects.filter(first_name=first_name[:150], last_name=last_name[:150]).first()
                    if user is None and bike is not None:
                        user = User.objects.filter(rider_profile__bike=bike).first()

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
                            defaults={"role": role},
                        )
                        profile.role = role
                        profile.save(update_fields=["role"])

                        rprof, _ = RiderProfile.objects.get_or_create(user=user)
                        rprof.province = province
                        rprof.district = district
                        rprof.bike = bike
                        rprof.support_type = support_type
                        rprof.save()

                self.stdout.write(
                    f"{'[DRY]' if dry_run else '[OK]'} {rider_name} -> {province_name}/{district_name}, bike={bike_code}, support={support_type or '-'}"
                )

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run - no changes saved."))
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. users created={created_users}, users updated={updated_users}, rows skipped={skipped}"
            )
        )
