"""
Apply remote rider bootstrap + profile JSON into the local SQLite DB (embedded Android).

Service-account sync scopes reference data to the remote rider's district/province; it does not
create end-user passwords. Local /login/ still requires User rows from seed or provisioning.
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
            District.objects.update_or_create(
                pk=int(did),
                defaults={
                    "province_id": int(prov_id),
                    "name": str(dname)[:128],
                    "support_type": "",
                },
            )
            stats["districts"] += 1

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
        root_pid = bootstrap.get("province_id")
        if root_pid is None and dist_payload:
            root_pid = dist_payload.get("province_id")
        if root_pid is None:
            root_pid = 1
        root_pid = int(root_pid)
        Province.objects.update_or_create(
            pk=root_pid,
            defaults={"name": f"Province {root_pid}", "code": ""},
        )
        stats["provinces"] += 1
        District.objects.update_or_create(
            pk=did,
            defaults={
                "province_id": root_pid,
                "name": dname,
                "support_type": "",
            },
        )
        stats["districts"] += 1

    for fid, row in facilities_by_id.items():
        did = row.get("district_id")
        if did is None:
            continue
        name = row.get("name") or f"Facility {fid}"
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
                "name": str(name)[:256],
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

    district_id = bootstrap.get("district_id")
    if isinstance(district_id, (int, str)) and str(district_id).isdigit():
        district_id = int(district_id)
    else:
        district_id = None
    if dist_payload and dist_payload.get("id") is not None:
        district_id = int(dist_payload["id"])

    bikes = bootstrap.get("bikes")
    if isinstance(bikes, list) and district_id is not None:
        for row in bikes:
            if not isinstance(row, dict):
                continue
            bid = row.get("id")
            reg = row.get("registration_number") or row.get("code") or ""
            if bid is None or not reg:
                continue
            Bike.objects.update_or_create(
                pk=int(bid),
                defaults={
                    "code": str(reg)[:64],
                    "district_id": district_id,
                    "active": True,
                },
            )
            stats["bikes"] += 1

    return stats
