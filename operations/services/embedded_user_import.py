"""
Apply central mobile-user-export JSON into local SQLite (embedded Android).

Replicates Django password hashes; run after reference bootstrap so FK targets exist.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction

from operations.models import Bike, Car, District, Facility, Province, RiderProfile, SupportType, UserProfile

from .pk_retry import run_with_incrementing_pk

User = get_user_model()


@transaction.atomic
def apply_embedded_user_import(payload: dict) -> dict:
    """
    payload: { "users": [ { id, username, email, password, is_active, userprofile, riderprofile }, ... ] }
    """
    users = payload.get("users")
    if not isinstance(users, list):
        raise ValueError("users must be a list")

    stats: dict = {"users": 0, "profiles": 0, "rider_profiles": 0, "pk_remaps": []}

    for row in users:
        if not isinstance(row, dict):
            continue
        uid = row.get("id")
        if uid is None:
            continue
        username = (row.get("username") or "").strip() or f"user_{uid}"
        email = (row.get("email") or "").strip()
        is_active = bool(row.get("is_active", True))
        password_hash = row.get("password") or ""
        if not password_hash:
            continue

        desired_pk = int(uid)

        def _save_user(pk: int):
            u, _ = User.objects.update_or_create(
                pk=pk,
                defaults={
                    "username": username[:150],
                    "email": email[:254] if email else "",
                    "is_active": is_active,
                },
            )
            u.password = password_hash
            u.save(update_fields=["password"])
            return u

        user, used_pk = run_with_incrementing_pk(desired_pk, _save_user)
        if used_pk != desired_pk:
            stats["pk_remaps"].append({"from": desired_pk, "to": used_pk})
        stats["users"] += 1

        up = row.get("userprofile")
        role = UserProfile.Role.RIDER
        if isinstance(up, dict) and up.get("role") in dict(UserProfile.Role.choices):
            role = up["role"]
        UserProfile.objects.update_or_create(
            user=user,
            defaults={"role": role},
        )
        stats["profiles"] += 1

        rp_in = row.get("riderprofile") if isinstance(row.get("riderprofile"), dict) else {}
        rp_defaults: dict = {}
        did = rp_in.get("district_id")
        if did is not None and District.objects.filter(pk=did).exists():
            rp_defaults["district_id"] = int(did)
        pid = rp_in.get("province_id")
        if pid is not None and Province.objects.filter(pk=pid).exists():
            rp_defaults["province_id"] = int(pid)
        fid = rp_in.get("facility_id")
        if fid is not None and Facility.objects.filter(pk=fid).exists():
            rp_defaults["facility_id"] = int(fid)
        bid = rp_in.get("bike_id")
        if bid is not None and Bike.objects.filter(pk=bid).exists():
            rp_defaults["bike_id"] = int(bid)
        cid = rp_in.get("car_id")
        if cid is not None and Car.objects.filter(pk=cid).exists():
            rp_defaults["car_id"] = int(cid)
        st = rp_in.get("support_type") or ""
        if st and st in {c[0] for c in SupportType.choices}:
            rp_defaults["support_type"] = st[:20]

        RiderProfile.objects.update_or_create(user=user, defaults=rp_defaults)
        stats["rider_profiles"] += 1

    return stats
