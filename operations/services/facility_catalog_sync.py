"""Match CSV clinic/hub rows to existing non-lab facilities within a district.

Dry-run helper for replacing the site list without changing facility PKs.
VL labs (kind=lab) are never rename targets.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

from operations.geo_names import canon_district_name, canon_province_name, norm_text
from operations.models import Facility, Province
from operations.services.district_merge import get_or_create_district

ORG_PREFIX_RE = re.compile(r"^[a-z]{2}\s+", re.I)
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_CLINIC_SUFFIXES = (
    "rural health centres",
    "rural health centers",
    "rural health centre",
    "rural health center",
    "health centres",
    "health centers",
    "health centre",
    "health center",
    "satellite clinics",
    "satellite clinic",
    "poly clinics",
    "poly clinic",
    "polyclinics",
    "polyclinic",
    "clinics",
    "clinic",
    "rhc",
    "poly",
)
_HOSPITAL_SUFFIXES = ("hospitals", "hospital")
_TYPE_SUFFIX_GROUPS = (_CLINIC_SUFFIXES, _HOSPITAL_SUFFIXES)

REVIEW_RATIO = 0.86


@dataclass(frozen=True)
class ExistingFacility:
    province: str
    district: str
    name: str
    kind: str = Facility.Kind.CLINIC
    support_type: str = ""
    pk: int | None = None


@dataclass(frozen=True)
class CsvSite:
    line_no: int
    province: str
    district: str
    name: str
    raw_province: str
    raw_district: str
    raw_name: str


@dataclass
class MatchRow:
    action: str
    csv: CsvSite
    existing: ExistingFacility | None = None
    rule: str = ""
    ratio: float | None = None
    note: str = ""


@dataclass
class CatalogPlan:
    unchanged: list[MatchRow] = field(default_factory=list)
    rename: list[MatchRow] = field(default_factory=list)
    create: list[MatchRow] = field(default_factory=list)
    review: list[MatchRow] = field(default_factory=list)
    unmatched_existing: list[ExistingFacility] = field(default_factory=list)
    skipped_csv: list[tuple[int, str]] = field(default_factory=list)
    source: str = ""

    def counts(self) -> dict[str, int]:
        return {
            "csv_rows": (
                len(self.unchanged)
                + len(self.rename)
                + len(self.create)
                + len(self.review)
                + len(self.skipped_csv)
            ),
            "unchanged": len(self.unchanged),
            "rename": len(self.rename),
            "create": len(self.create),
            "review": len(self.review),
            "unmatched_existing": len(self.unmatched_existing),
            "skipped_csv": len(self.skipped_csv),
        }


def strip_org_prefix(raw: str) -> str:
    """Remove DHIS2-style ``bu Bulawayo`` prefixes; leave the rest of the name."""
    s = norm_text(raw)
    nxt = ORG_PREFIX_RE.sub("", s, count=1).strip()
    return nxt or s


def _strip_type_suffix(punct: str, suffixes: tuple[str, ...]) -> str:
    for suffix in suffixes:
        token = f" {suffix}"
        if punct.endswith(token):
            return punct[: -len(token)].strip()
    return punct


def name_keys(name: str) -> tuple[str, str, str]:
    exact = norm_text(name).lower()
    punct = " ".join(NON_ALNUM_RE.sub(" ", exact).split())
    while True:
        collapsed = re.sub(r"\b([a-z0-9])\s+(?=[a-z0-9]\b)", r"\1", punct)
        if collapsed == punct:
            break
        punct = collapsed
    family, core = _type_family_and_core(punct)
    return exact, punct, core


def _type_family_and_core(punct: str) -> tuple[int | None, str]:
    for i, group in enumerate(_TYPE_SUFFIX_GROUPS):
        nxt = _strip_type_suffix(punct, group)
        if nxt != punct:
            return i, nxt or punct
    return None, punct


def _index_unique(items: list[ExistingFacility], key_fn) -> dict[tuple, ExistingFacility]:
    buckets: dict[tuple, list[ExistingFacility]] = defaultdict(list)
    for fac in items:
        key = key_fn(fac)
        if key is None:
            continue
        buckets[key].append(fac)
    return {k: v[0] for k, v in buckets.items() if len(v) == 1}


def parse_sites_csv(path: Path) -> tuple[list[CsvSite], list[tuple[int, str]]]:
    sites: list[CsvSite] = []
    skipped: list[tuple[int, str]] = []
    raw = path.read_text(encoding="utf-8-sig")
    reader = csv.DictReader(raw.splitlines())
    if not reader.fieldnames:
        raise ValueError(f"CSV has no header: {path}")
    fields = {h.strip().lower(): h for h in reader.fieldnames if h}
    try:
        p_col, d_col, s_col = fields["province"], fields["district"], fields["site"]
    except KeyError as exc:
        raise ValueError("CSV must have Province, District, Site columns") from exc

    for line_no, row in enumerate(reader, start=2):
        raw_p = row.get(p_col) or ""
        raw_d = row.get(d_col) or ""
        raw_s = row.get(s_col) or ""
        province = canon_province_name(strip_org_prefix(raw_p))
        district = canon_district_name(strip_org_prefix(raw_d))
        name = strip_org_prefix(raw_s)
        if not province or not district or not name:
            skipped.append((line_no, "blank province, district, or site"))
            continue
        sites.append(
            CsvSite(
                line_no=line_no,
                province=province,
                district=district,
                name=name,
                raw_province=raw_p,
                raw_district=raw_d,
                raw_name=raw_s,
            )
        )
    return sites, skipped


def _load_tsv(path: Path, *, default_kind: str, support_type: str) -> list[ExistingFacility]:
    out: list[ExistingFacility] = []
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        province = canon_province_name(parts[0].strip())
        district = canon_district_name(parts[1].strip())
        name = "\t".join(parts[2:]).strip()
        if not province or not district or not name:
            continue
        out.append(
            ExistingFacility(
                province=province,
                district=district,
                name=name,
                kind=default_kind,
                support_type=support_type,
            )
        )
    return out


def load_fixture_facilities(fixtures_dir: Path | None = None) -> list[ExistingFacility]:
    root = fixtures_dir or Path(__file__).resolve().parent.parent / "fixtures"
    by_key: dict[tuple[str, str, str], ExistingFacility] = {}

    def add_all(rows: list[ExistingFacility], *, prefer_kind: str | None = None) -> None:
        for fac in rows:
            key = (fac.province.casefold(), fac.district.casefold(), fac.name.casefold())
            existing = by_key.get(key)
            if existing is None:
                by_key[key] = fac
                continue
            if prefer_kind and fac.kind == prefer_kind and existing.kind != prefer_kind:
                by_key[key] = fac

    add_all(_load_tsv(root / "facilities_dsd.tsv", default_kind=Facility.Kind.CLINIC, support_type="DSD"))
    add_all(_load_tsv(root / "facilities_ta_sdi.tsv", default_kind=Facility.Kind.CLINIC, support_type="TA-SDI"))
    add_all(
        _load_tsv(root / "hubs_ta_sdi.tsv", default_kind=Facility.Kind.HUB, support_type="TA-SDI"),
        prefer_kind=Facility.Kind.HUB,
    )
    add_all(_load_tsv(root / "facility_labs.tsv", default_kind=Facility.Kind.LAB, support_type=""))
    return list(by_key.values())


def load_db_facilities() -> list[ExistingFacility]:
    rows = Facility.objects.select_related("district", "district__province").order_by("id")
    return [
        ExistingFacility(
            province=fac.district.province.name,
            district=fac.district.name,
            name=fac.name,
            kind=fac.kind,
            support_type=fac.support_type or "",
            pk=fac.pk,
        )
        for fac in rows
    ]


def plan_catalog(csv_sites: list[CsvSite], existing: list[ExistingFacility], *, source: str) -> CatalogPlan:
    plan = CatalogPlan(source=source)
    labs = [f for f in existing if f.kind == Facility.Kind.LAB]
    targets = [f for f in existing if f.kind != Facility.Kind.LAB]

    exact_ix = _index_unique(
        targets, lambda f: (f.district.casefold(), name_keys(f.name)[0])
    )
    punct_ix = _index_unique(
        targets, lambda f: (f.district.casefold(), name_keys(f.name)[1])
    )

    def typed_key(fac: ExistingFacility):
        punct = name_keys(fac.name)[1]
        family, core = _type_family_and_core(punct)
        if family is None or len(core.split()) < 2:
            return None
        return fac.district.casefold(), family, core

    strip_ix = _index_unique(targets, typed_key)
    lab_punct = {(f.district.casefold(), name_keys(f.name)[1]) for f in labs}

    by_district: dict[str, list[ExistingFacility]] = defaultdict(list)
    for fac in targets:
        by_district[fac.district.casefold()].append(fac)

    claimed: set[tuple[str, str]] = set()

    def claim_key(fac: ExistingFacility) -> tuple[str, str]:
        return fac.district.casefold(), fac.name.casefold()

    def find_close(site: CsvSite) -> tuple[ExistingFacility | None, float]:
        punct = name_keys(site.name)[1]
        best: ExistingFacility | None = None
        best_ratio = 0.0
        second = 0.0
        for fac in by_district.get(site.district.casefold(), []):
            if claim_key(fac) in claimed:
                continue
            r = SequenceMatcher(None, punct, name_keys(fac.name)[1]).ratio()
            if r > best_ratio:
                second = best_ratio
                best_ratio = r
                best = fac
            elif r > second:
                second = r
        if best is None or best_ratio < REVIEW_RATIO:
            return None, 0.0
        if second and (best_ratio - second) < 0.06:
            return None, best_ratio
        return best, best_ratio

    for site in csv_sites:
        dkey = site.district.casefold()
        exact, punct, _ = name_keys(site.name)

        hit = exact_ix.get((dkey, exact))
        if hit and claim_key(hit) not in claimed:
            claimed.add(claim_key(hit))
            plan.unchanged.append(MatchRow("unchanged", site, hit, "exact"))
            continue

        if (dkey, punct) in lab_punct:
            plan.review.append(
                MatchRow("review", site, None, "matches_lab", note="Name collides with a VL lab in this district")
            )
            continue

        hit = punct_ix.get((dkey, punct))
        if hit and claim_key(hit) not in claimed:
            claimed.add(claim_key(hit))
            plan.rename.append(MatchRow("rename", site, hit, "punctuation"))
            continue

        family, core = _type_family_and_core(punct)
        if family is not None and len(core.split()) >= 2:
            hit = strip_ix.get((dkey, family, core))
            if hit and claim_key(hit) not in claimed and core != punct:
                claimed.add(claim_key(hit))
                plan.rename.append(MatchRow("rename", site, hit, "trailing_type"))
                continue

        close, ratio = find_close(site)
        if close is not None:
            plan.review.append(
                MatchRow(
                    "review",
                    site,
                    close,
                    "similar",
                    ratio=round(ratio, 3),
                    note="Possible same site; not unique enough to auto-rename",
                )
            )
            continue

        plan.create.append(MatchRow("create", site, None, "no_match"))

    matched_keys = claimed
    plan.unmatched_existing = [
        fac for fac in targets if claim_key(fac) not in matched_keys
    ]
    plan.unmatched_existing.sort(key=lambda f: (f.province, f.district, f.name.lower()))
    return plan


def write_plan_csvs(plan: CatalogPlan, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def dump(name: str, headers: list[str], rows: list[list[str]]) -> Path:
        path = out_dir / name
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(headers)
            w.writerows(rows)
        written.append(path)
        return path

    dump(
        "rename.csv",
        ["province", "district", "old_name", "new_name", "rule", "kind", "support_type", "pk"],
        [
            [
                r.csv.province,
                r.csv.district,
                r.existing.name if r.existing else "",
                r.csv.name,
                r.rule,
                r.existing.kind if r.existing else "",
                r.existing.support_type if r.existing else "",
                "" if not r.existing or r.existing.pk is None else str(r.existing.pk),
            ]
            for r in plan.rename
        ],
    )
    dump(
        "create.csv",
        ["csv_line", "province", "district", "name"],
        [[str(r.csv.line_no), r.csv.province, r.csv.district, r.csv.name] for r in plan.create],
    )
    dump(
        "review.csv",
        ["csv_line", "province", "district", "csv_name", "candidate_name", "rule", "ratio", "note"],
        [
            [
                str(r.csv.line_no),
                r.csv.province,
                r.csv.district,
                r.csv.name,
                r.existing.name if r.existing else "",
                r.rule,
                "" if r.ratio is None else str(r.ratio),
                r.note,
            ]
            for r in plan.review
        ],
    )
    dump(
        "unchanged_sample.csv",
        ["province", "district", "name"],
        [[r.csv.province, r.csv.district, r.csv.name] for r in plan.unchanged],
    )
    dump(
        "unmatched_existing.csv",
        ["province", "district", "name", "kind", "support_type", "pk"],
        [
            [
                f.province,
                f.district,
                f.name,
                f.kind,
                f.support_type,
                "" if f.pk is None else str(f.pk),
            ]
            for f in plan.unmatched_existing
        ],
    )
    return written


def _support_for_district(district) -> str:
    if district.support_type:
        return district.support_type
    from django.db.models import Count

    top = (
        Facility.objects.filter(district=district)
        .exclude(kind=Facility.Kind.LAB)
        .exclude(support_type="")
        .values("support_type")
        .annotate(n=Count("id"))
        .order_by("-n")
        .first()
    )
    return (top["support_type"] if top else "") or "DSD"


def apply_catalog_plan(plan: CatalogPlan) -> dict[str, int]:
    """Rename safe matches and create unmatched CSV sites. Does not delete or touch labs/review."""
    stats = {
        "renamed": 0,
        "created": 0,
        "rename_skipped": 0,
        "create_skipped": 0,
        "review_left": len(plan.review),
        "unmatched_kept": len(plan.unmatched_existing),
    }

    for row in plan.rename:
        fac = None
        if row.existing and row.existing.pk:
            fac = Facility.objects.filter(pk=row.existing.pk).exclude(kind=Facility.Kind.LAB).first()
        if fac is None and row.existing:
            fac = (
                Facility.objects.filter(
                    district__name__iexact=row.existing.district,
                    district__province__name__iexact=row.existing.province,
                    name__iexact=row.existing.name,
                )
                .exclude(kind=Facility.Kind.LAB)
                .first()
            )
        if fac is None:
            stats["rename_skipped"] += 1
            continue
        new_name = row.csv.name
        if fac.name == new_name:
            continue
        clash = (
            Facility.objects.filter(district_id=fac.district_id, name__iexact=new_name)
            .exclude(pk=fac.pk)
            .exists()
        )
        if clash:
            stats["rename_skipped"] += 1
            continue
        fac.name = new_name
        fac.save(update_fields=["name"])
        stats["renamed"] += 1

    province_cache: dict[str, object] = {}
    district_cache: dict[tuple[int, str], object] = {}
    support_cache: dict[int, str] = {}
    existing_names = {
        (did, nam.casefold())
        for did, nam in Facility.objects.values_list("district_id", "name")
    }
    pending: list[Facility] = []
    pending_keys: set[tuple[int, str]] = set()

    for row in plan.create:
        pname = row.csv.province
        if pname not in province_cache:
            province_cache[pname], _ = Province.objects.get_or_create(name=pname)
        province = province_cache[pname]
        dkey = (province.pk, row.csv.district.casefold())
        if dkey not in district_cache:
            district_cache[dkey], _ = get_or_create_district(province, row.csv.district)
        district = district_cache[dkey]
        name_key = (district.pk, row.csv.name.casefold())
        if name_key in existing_names or name_key in pending_keys:
            stats["create_skipped"] += 1
            continue
        if district.pk not in support_cache:
            support_cache[district.pk] = _support_for_district(district)
        pending.append(
            Facility(
                district=district,
                name=row.csv.name,
                kind=Facility.Kind.CLINIC,
                support_type=support_cache[district.pk],
            )
        )
        pending_keys.add(name_key)

    if pending:
        Facility.objects.bulk_create(pending, batch_size=100)
        stats["created"] = len(pending)

    return stats


def apply_plan_to_fixtures(plan: CatalogPlan, fixtures_dir: Path) -> dict[str, int]:
    """Rewrite clinic/hub TSVs: rename in place, append creates. Labs file is left untouched."""
    stats = {"renamed": 0, "created": 0, "rename_skipped": 0}
    rename_map: dict[tuple[str, str], str] = {}
    for row in plan.rename:
        if not row.existing:
            continue
        rename_map[(row.existing.district.casefold(), row.existing.name.casefold())] = row.csv.name

    data_files = ("facilities_dsd.tsv", "facilities_ta_sdi.tsv", "hubs_ta_sdi.tsv")
    district_file_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for fname in data_files:
        path = fixtures_dir / fname
        if not path.is_file():
            continue
        out_lines: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = line
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                out_lines.append(raw)
                continue
            parts = stripped.split("\t")
            if len(parts) < 3:
                out_lines.append(raw)
                continue
            district = canon_district_name(parts[1].strip())
            name = "\t".join(parts[2:]).strip()
            key = (district.casefold(), name.casefold())
            new_name = rename_map.get(key)
            if new_name and new_name != name:
                parts = [parts[0], parts[1], new_name]
                out_lines.append("\t".join(parts))
                stats["renamed"] += 1
                name = new_name
            else:
                out_lines.append(raw)
            if fname != "hubs_ta_sdi.tsv":
                district_file_counts[district.casefold()][fname] += 1
        path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

    existing_keys = {
        (f.district.casefold(), f.name.casefold())
        for f in load_fixture_facilities(fixtures_dir)
        if f.kind != Facility.Kind.LAB
    }
    dsd_path = fixtures_dir / "facilities_dsd.tsv"
    ta_path = fixtures_dir / "facilities_ta_sdi.tsv"
    buckets: dict[str, list[str]] = {"facilities_dsd.tsv": [], "facilities_ta_sdi.tsv": []}
    for row in plan.create:
        key = (row.csv.district.casefold(), row.csv.name.casefold())
        if key in existing_keys:
            continue
        counts = district_file_counts.get(row.csv.district.casefold(), {})
        target = "facilities_ta_sdi.tsv" if counts.get("facilities_ta_sdi.tsv", 0) > counts.get(
            "facilities_dsd.tsv", 0
        ) else "facilities_dsd.tsv"
        buckets[target].append(f"{row.csv.province}\t{row.csv.district}\t{row.csv.name}")
        existing_keys.add(key)
        stats["created"] += 1

    for fname, extra in buckets.items():
        if not extra:
            continue
        path = dsd_path if fname.startswith("facilities_dsd") else ta_path
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if text and not text.endswith("\n"):
            text += "\n"
        path.write_text(text + "\n".join(extra) + "\n", encoding="utf-8")

    return stats
