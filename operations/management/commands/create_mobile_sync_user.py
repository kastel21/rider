"""
Create a district-scoped rider account for Android landing sync (OPS_SYNC_USERNAME).

Usage:
  python manage.py create_mobile_sync_user --username mobile_sync --password '...' --district-id 1
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from operations.models import District, RiderProfile, UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update a rider user for APK landing sync (JWT bootstrap)."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument(
            "--district-id",
            type=int,
            required=True,
            help="District whose reference data / riders will be exported on landing sync.",
        )

    def handle(self, *args, **options):
        username = options["username"].strip()
        password = options["password"]
        district_id = options["district_id"]
        district = District.objects.filter(pk=district_id).first()
        if not district:
            self.stderr.write(self.style.ERROR(f"District id={district_id} not found"))
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": ""},
        )
        user.set_password(password)
        user.save()

        UserProfile.objects.update_or_create(
            user=user,
            defaults={"role": UserProfile.Role.RIDER},
        )
        RiderProfile.objects.update_or_create(
            user=user,
            defaults={
                "district": district,
                "province_id": district.province_id,
            },
        )

        verb = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{verb} rider {username!r} for district {district.name} (id={district_id}). "
                "Set OPS_SYNC_USERNAME and OPS_SYNC_PASSWORD in android/local.properties."
            )
        )
