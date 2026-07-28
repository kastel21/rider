"""Catalog of user-facing Android apps reported from rider handsets."""
from django.db.models import F
from django.utils import timezone

from operations.models import AccessibleApp


def upsert_reported_user_apps(apps: list[dict]) -> int:
    """
    Merge launcher user-app reports from a device.

    Each item: ``{"package": "com.example", "label": "Example"}``.
    System packages should be filtered out on the client before calling.
    """
    now = timezone.now()
    updated = 0
    for item in apps:
        if not isinstance(item, dict):
            continue
        pkg = (item.get("package") or item.get("package_name") or "").strip()
        if not pkg:
            continue
        label = (item.get("label") or "").strip()[:255]
        is_system = bool(item.get("is_system", False))
        obj, created = AccessibleApp.objects.get_or_create(
            package_name=pkg,
            defaults={
                "label": label,
                "is_system": is_system,
                "last_seen_at": now,
                "report_count": 1,
            },
        )
        if created:
            updated += 1
            continue
        fields = {
            "last_seen_at": now,
            "report_count": F("report_count") + 1,
        }
        if label:
            fields["label"] = label
        if is_system:
            fields["is_system"] = True
        AccessibleApp.objects.filter(pk=obj.pk).update(**fields)
        updated += 1
    return updated


def allowed_package_names() -> list[str]:
    return list(
        AccessibleApp.objects.filter(is_allowed=True, is_system=False)
        .order_by("label", "package_name")
        .values_list("package_name", flat=True)
    )
