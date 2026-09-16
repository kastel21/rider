"""Merge duplicate districts created by shorthand vs official names (e.g. UMP)."""

from __future__ import annotations

from collections import defaultdict

from django.db import models
from django.db.models import UniqueConstraint

from operations.geo_names import canon_district_name, district_alias_keys

_KIND_RANK = {"hub": 3, "lab": 2, "clinic": 1}


def _app_models(apps=None):
    if apps is None:
        from django.apps import apps as django_apps

        models = django_apps.get_models()
    else:
        models = apps.get_models()
    return [m for m in models if m._meta.app_label == "operations"]


def _model(apps, app_label: str, name: str):
    if apps is None:
        from django.apps import apps as django_apps

        return django_apps.get_model(app_label, name)
    return apps.get_model(app_label, name)


def get_or_create_district(province, raw_name: str, *, defaults=None, apps=None):
    """
    Resolve a district by canonical name, reusing an alias row (e.g. UMP) instead of
    creating a second district. Renames the alias row when the canonical name is free.
    """
    District = _model(apps, "operations", "District")
    canonical = canon_district_name(raw_name)
    if not canonical:
        raise ValueError("District name is empty")

    qs = District.objects.filter(province=province)
    existing = qs.filter(name__iexact=canonical).first()
    if existing is None:
        keys = district_alias_keys(canonical)
        for key in keys:
            existing = qs.filter(name__iexact=key).first()
            if existing is not None:
                break
    if existing is not None:
        if existing.name != canonical and not qs.filter(name__iexact=canonical).exclude(pk=existing.pk).exists():
            existing.name = canonical
            existing.save(update_fields=["name"])
        if defaults:
            changed = []
            for field, value in defaults.items():
                if value and not getattr(existing, field, ""):
                    setattr(existing, field, value)
                    changed.append(field)
            if changed:
                existing.save(update_fields=changed)
        return existing, False

    kwargs = dict(defaults or {})
    district = District.objects.create(province=province, name=canonical, **kwargs)
    return district, True


def _unique_field_sets(model, field_name: str) -> list[tuple[str, ...]]:
    found: list[tuple[str, ...]] = []
    for ut in model._meta.unique_together:
        if field_name in ut:
            found.append(tuple(ut))
    for constraint in getattr(model._meta, "constraints", ()):
        if isinstance(constraint, UniqueConstraint) and field_name in constraint.fields:
            found.append(tuple(constraint.fields))
    return found


def _merge_numeric_row(keep, absorb) -> None:
    changed: list[str] = []
    for field in absorb._meta.fields:
        if field.primary_key or field.name in {"created_at", "updated_at"}:
            continue
        if isinstance(field, (models.IntegerField, models.DecimalField)) and not field.is_relation:
            keep_val = getattr(keep, field.name) or 0
            absorb_val = getattr(absorb, field.name) or 0
            total = keep_val + absorb_val
            if total != keep_val:
                setattr(keep, field.name, total)
                changed.append(field.name)
        elif isinstance(field, models.TextField):
            keep_val = (getattr(keep, field.name) or "").strip()
            absorb_val = (getattr(absorb, field.name) or "").strip()
            if absorb_val and absorb_val not in keep_val:
                setattr(keep, field.name, f"{keep_val}\n{absorb_val}".strip() if keep_val else absorb_val)
                changed.append(field.name)
    if changed:
        keep.save(update_fields=changed)


def _repoint_fk_and_m2m(from_obj, to_obj, *, apps=None, skip_models=frozenset()) -> None:
    from_label = from_obj._meta.label
    for model in _app_models(apps):
        if model._meta.label in skip_models:
            continue
        for field in model._meta.get_fields():
            related = getattr(field, "related_model", None)
            if related is None or getattr(related, "_meta", None) is None:
                continue
            if related._meta.label != from_label:
                continue
            if field.many_to_many and not field.auto_created:
                for obj in model.objects.filter(**{field.name: from_obj}):
                    rel = getattr(obj, field.name)
                    rel.remove(from_obj)
                    rel.add(to_obj)
                continue
            if not field.many_to_one or field.auto_created:
                continue
            field_name = field.name
            unique_sets = _unique_field_sets(model, field_name)
            qs = model.objects.filter(**{field_name: from_obj})
            if not unique_sets:
                qs.update(**{field_name: to_obj})
                continue
            for row in list(qs):
                conflict = None
                for fields in unique_sets:
                    lookup = {}
                    for fname in fields:
                        lookup[fname] = to_obj if fname == field_name else getattr(row, fname)
                    conflict = model.objects.filter(**lookup).exclude(pk=row.pk).first()
                    if conflict:
                        break
                if conflict:
                    _merge_numeric_row(conflict, row)
                    row.delete()
                else:
                    setattr(row, field_name, to_obj)
                    row.save(update_fields=[field_name])


def merge_facility(keep, absorb, *, apps=None) -> None:
    """Keep ``keep``'s PK; copy better kind/codes from ``absorb``, then delete ``absorb``."""
    if keep.pk == absorb.pk:
        return
    changed: list[str] = []
    if _KIND_RANK.get((absorb.kind or "").lower(), 0) > _KIND_RANK.get((keep.kind or "").lower(), 0):
        keep.kind = absorb.kind
        changed.append("kind")
    if not (keep.site_code or "").strip() and (absorb.site_code or "").strip():
        keep.site_code = absorb.site_code
        changed.append("site_code")
    if not (keep.support_type or "").strip() and (absorb.support_type or "").strip():
        keep.support_type = absorb.support_type
        changed.append("support_type")
    if changed:
        keep.save(update_fields=changed)

    _repoint_fk_and_m2m(absorb, keep, apps=apps)
    absorb.delete()


def merge_district(keep, absorb, *, apps=None) -> None:
    if keep.pk == absorb.pk:
        return
    Facility = _model(apps, "operations", "Facility")
    for fac in list(Facility.objects.filter(district=absorb)):
        existing = (
            Facility.objects.filter(district=keep, name__iexact=fac.name).exclude(pk=fac.pk).first()
        )
        if existing:
            merge_facility(existing, fac, apps=apps)
        else:
            fac.district = keep
            fac.save(update_fields=["district"])

    if not (keep.support_type or "").strip() and (absorb.support_type or "").strip():
        keep.support_type = absorb.support_type
        keep.save(update_fields=["support_type"])

    _repoint_fk_and_m2m(
        absorb,
        keep,
        apps=apps,
        skip_models=frozenset({"operations.Facility"}),
    )
    absorb.delete()


def _pick_keep(districts, *, apps=None):
    """Keep the oldest row so existing rider ``district_id`` values stay stable."""
    return min(districts, key=lambda d: d.pk)


def merge_aliased_districts(*, apps=None) -> list[dict]:
    """
    For each province, fold alias district rows into one canonical district.

    Prefers the row that already has rider profiles so mobile ``district_id`` stays stable.
    """
    District = _model(apps, "operations", "District")
    Province = _model(apps, "operations", "Province")
    results: list[dict] = []

    for province in Province.objects.all().order_by("id"):
        buckets: dict[str, list] = defaultdict(list)
        for district in District.objects.filter(province=province).order_by("id"):
            buckets[canon_district_name(district.name)].append(district)

        for canonical, districts in buckets.items():
            if not canonical:
                continue
            if len(districts) == 1:
                only = districts[0]
                if only.name != canonical:
                    only.name = canonical
                    only.save(update_fields=["name"])
                    results.append(
                        {
                            "province": province.name,
                            "kept_id": only.pk,
                            "renamed_to": canonical,
                            "absorbed_ids": [],
                        }
                    )
                continue

            keep = _pick_keep(districts, apps=apps)
            absorbed_ids = []
            for absorb in districts:
                if absorb.pk == keep.pk:
                    continue
                absorbed_ids.append(absorb.pk)
                merge_district(keep, absorb, apps=apps)
            keep.refresh_from_db()
            if keep.name != canonical:
                keep.name = canonical
                keep.save(update_fields=["name"])
            results.append(
                {
                    "province": province.name,
                    "kept_id": keep.pk,
                    "renamed_to": canonical,
                    "absorbed_ids": absorbed_ids,
                }
            )
    return results
