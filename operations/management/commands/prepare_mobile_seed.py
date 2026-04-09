import json
from pathlib import Path

from django.core.management.base import BaseCommand

from operations.models import Facility, Lab


class Command(BaseCommand):
    help = "Generate static/mobile-seed.json for standalone mobile mode."

    def add_arguments(self, parser):
        parser.add_argument(
            "--sync-base-url",
            dest="sync_base_url",
            default="",
            help="Remote backend base URL for upload sync (e.g. https://api.example.com).",
        )

    def handle(self, *args, **options):
        sync_base_url = (options.get("sync_base_url") or "").strip().rstrip("/")
        facilities = list(
            Facility.objects.select_related("district")
            .exclude(kind=Facility.Kind.HUB)
            .values("id", "name", "district_id", "district__name", "district__province_id")
            .order_by("district__name", "name")
        )
        hubs = list(
            Facility.objects.select_related("district")
            .filter(kind=Facility.Kind.HUB)
            .values("id", "name", "district_id", "district__name", "district__province_id")
            .order_by("district__name", "name")
        )
        labs = list(Lab.objects.values("id", "name", "code").order_by("name"))

        def norm_fac(rows):
            out = []
            for row in rows:
                out.append(
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "district_id": row["district_id"],
                        "district_name": row.get("district__name") or "",
                        "province_id": row.get("district__province_id"),
                    }
                )
            return out

        payload = {
            "sync_base_url": sync_base_url,
            "facilities": norm_fac(facilities),
            "hubs": norm_fac(hubs),
            "labs": labs,
        }

        out_path = Path("static") / "mobile-seed.json"
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"Wrote {out_path}"))
