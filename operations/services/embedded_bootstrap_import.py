"""
Apply remote rider bootstrap + profile JSON into the local SQLite DB (embedded Android).

Landing sync uses a service account. Cloud bootstrap for that username may include every
facility (see OPS_MOBILE_SYNC_USERNAMES). It does not create end-user passwords; local
/login/ still requires User rows from seed or provisioning.
"""

from __future__ import annotations

from django.db import transaction

from operations.models import Bike, District, Facility, Lab, Province


def _dedupe_facilities(rows: list[dict]) -> dict[int, dict]:
    out: dict[int, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        fid = row.get("id")
        if fid is None:
            continue
        out[int(fid)] = row
    return out


_KIND_SET = {c[0] for c in Facility.Kind.choices}
_ST_SET = {c[0] for c in Facility._meta.get_field("support_type").choices}


def _name_taken(model, lookup: dict, pk: int, name: str) -> bool:
    return model.objects.filter(**lookup, name=name).exclude(pk=pk).exists()


def _with_unique_suffix(base: str, owner_id: int, max_len: int, taken) -> str:
    """Build a name that satisfies a unique constraint while keeping ``owner_id``."""
    n = 1
    candidate = base[:max_len]
    while taken(candidate):
        suffix = f" ({owner_id})" if n == 1 else f" ({owner_id}-{n})"
        trimmed = base[: max_len - len(suffix)].rstrip()
        candidate = f"{trimmed}{suffix}" if trimmed else suffix[:max_len]
        n += 1
        if n > 20:
            return candidate
    return candidate


def _upsert_district(district_id: int, name: str, province_id: int, stats: dict) -> int:
    """
    Save a district without violating unique (province, name).

    The phone SQLite enforces that constraint. The central SQL Server copy often
    does not, so a bootstrap can contain the same district name twice, or can
    rename one district onto a name the device already stored.
    """
    desired = (str(name).strip() if name else "")[:128] or f"District {district_id}"
    existing = District.objects.filter(pk=district_id).first()

    def taken(candidate: str, prov: int | None = None) -> bool:
        return _name_taken(
            District,
            {"province_id": province_id if prov is None else prov},
            district_id,
            candidate,
        )

    if existing is not None:
        new_name = desired
        new_province = province_id
        if taken(new_name, new_province):
            # Keep the row that is already on the device rather than colliding.
            new_name = existing.name
            new_province = existing.province_id
        if new_name != existing.name or new_province != existing.province_id:
            existing.name = new_name
            existing.province_id = new_province
            existing.save(update_fields=["name", "province_id"])
        stats["districts"] += 1
        return existing.pk

    create_name = desired if not taken(desired) else _with_unique_suffix(desired, district_id, 128, taken)
    District.objects.create(
        pk=district_id,
        province_id=province_id,
        name=create_name,
        support_type="",
    )
    stats["districts"] += 1
    return district_id


def _facility_name(facility_id: int, district_id: int, name: str) -> str:
    desired = (str(name).strip() if name else "")[:256] or f"Facility {facility_id}"
    existing = Facility.objects.filter(pk=facility_id).first()

    def taken(candidate: str) -> bool:
        return _name_taken(Facility, {"district_id": district_id}, facility_id, candidate)

    if not taken(desired):
        return desired
    if existing is not None and existing.district_id == district_id and not taken(existing.name):
        return existing.name
    return _with_unique_suffix(desired, facility_id, 256, taken)


@transaction.atomic
def apply_embedded_bootstrap(payload: dict) -> dict:
    """
    payload shape: { "bootstrap": {...}, "profile": {...} } from remote API responses.
    Returns a small stats dict.
    """
    bootstrap = payload.get("bootstrap") if isinstance(payload.get("bootstrap"), dict) else {}
    profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}

    prov_payload = profile.get("province") if isinstance(profile.get("province"), dict) else None
    dist_payload = profile.get("district") if isinstance(profile.get("district"), dict) else None

    stats = {
        "provinces": 0,
        "districts": 0,
        "facilities": 0,
        "labs": 0,
        "bikes": 0,
    }

    if prov_payload:
        pid = prov_payload.get("id")
        pname = prov_payload.get("name")
        if pid is not None and pname:
            Province.objects.update_or_create(
                pk=int(pid),
                defaults={"name": str(pname)[:128], "code": ""},
            )
            stats["provinces"] += 1

    if dist_payload:
        did = dist_payload.get("id")
        dname = dist_payload.get("name")
        prov_id = dist_payload.get("province_id")
        if did is not None and dname and prov_id is not None:
            pname_guess = (
                (prov_payload.get("name") if prov_payload else None) or f"Province {prov_id}"
            )
            Province.objects.update_or_create(
                pk=int(prov_id),
                defaults={"name": str(pname_guess)[:128], "code": ""},
            )
            stats["provinces"] += 1
            _upsert_district(int(did), str(dname), int(prov_id), stats)

    fac_lists = []
    for key in ("facilities_district", "facilities_province", "hubs"):
        v = bootstrap.get(key)
        if isinstance(v, list):
            fac_lists.extend(v)
    facilities_by_id = _dedupe_facilities(fac_lists)

    for row in facilities_by_id.values():
        did = row.get("district_id")
        if did is None:
            continue
        did = int(did)
        if District.objects.filter(pk=did).exists():
            continue
        dname = (row.get("district_name") or f"District {did}")[:128]
        root_pid = row.get("province_id")
        if root_pid is None:
            root_pid = bootstrap.get("province_id")
        if root_pid is None and dist_payload:
            root_pid = dist_payload.get("province_id")
        if root_pid is None:
            root_pid = 1
        root_pid = int(root_pid)
        pname = (row.get("province_name") or f"Province {root_pid}")[:128]
        Province.objects.update_or_create(
            pk=root_pid,
            defaults={"name": pname, "code": ""},
        )
        stats["provinces"] += 1
        _upsert_district(did, dname, root_pid, stats)

    for fid, row in facilities_by_id.items():
        did = row.get("district_id")
        if did is None:
            continue
        name = _facility_name(int(fid), int(did), row.get("name") or f"Facility {fid}")
        kind = row.get("kind") or Facility.Kind.HUB
        if kind not in _KIND_SET:
            kind = Facility.Kind.HUB
        st = row.get("support_type") or ""
        if st and st not in _ST_SET:
            st = ""
        Facility.objects.update_or_create(
            pk=int(fid),
            defaults={
                "district_id": int(did),
                "name": name,
                "kind": kind,
                "support_type": st[:20] if st else "",
                "site_code": "",
            },
        )
        stats["facilities"] += 1

    labs = bootstrap.get("labs")
    if isinstance(labs, list):
        for row in labs:
            if not isinstance(row, dict):
                continue
            lid = row.get("id")
            if lid is None:
                continue
            name = row.get("name") or f"Lab {lid}"
            code = row.get("code") or ""
            Lab.objects.update_or_create(
                pk=int(lid),
                defaults={
                    "name": str(name)[:256],
                    "code": str(code)[:64],
                },
            )
            stats["labs"] += 1

    fallback_district_id = bootstrap.get("district_id")
    if isinstance(fallback_district_id, (int, str)) and str(fallback_district_id).isdigit():
        fallback_district_id = int(fallback_district_id)
    else:
        fallback_district_id = None
    if dist_payload and dist_payload.get("id") is not None:
        fallback_district_id = int(dist_payload["id"])

    bikes = bootstrap.get("bikes")
    if isinstance(bikes, list):
        for row in bikes:
            if not isinstance(row, dict):
                continue
            bid = row.get("id")
            reg = row.get("registration_number") or row.get("code") or ""
            if bid is None or not reg:
                continue
            bike_district_id = _bike_district_id(row, fallback_district_id, stats)
            if bike_district_id is None:
                continue
            Bike.objects.update_or_create(
                pk=int(bid),
                defaults={
                    "code": str(reg)[:64],
                    "district_id": bike_district_id,
                    "active": True,
                },
            )
            stats["bikes"] += 1

    return stats


def _bike_district_id(row: dict, fallback_district_id: int | None, stats: dict) -> int | None:
    """Keep each bike on its own district. Older payloads omit district_id and use the profile district."""
    if "district_id" in row:
        raw = row.get("district_id")
        if raw is None or not str(raw).isdigit():
            return None
        return _ensure_district(
            int(raw),
            row.get("district_name") or "",
            row.get("province_id"),
            row.get("province_name") or "",
            stats,
        )
    if fallback_district_id is not None and District.objects.filter(pk=fallback_district_id).exists():
        return fallback_district_id
    return None


def _ensure_district(
    district_id: int,
    district_name: str,
    province_id,
    province_name: str,
    stats: dict,
) -> int | None:
    if District.objects.filter(pk=district_id).exists():
        return district_id
    if province_id is None or not str(province_id).isdigit():
        return None
    province_id = int(province_id)
    Province.objects.update_or_create(
        pk=province_id,
        defaults={"name": (province_name or f"Province {province_id}")[:128], "code": ""},
    )
    stats["provinces"] += 1
    return _upsert_district(
        district_id,
        district_name or f"District {district_id}",
        province_id,
        stats,
    )
