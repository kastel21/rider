"""Canonical province/district names so CSV/TSV shorthand cannot create duplicates."""

PROVINCE_ALIASES = {
    "mat north": "Matabeleland North",
    "mat south": "Matabeleland South",
    "mash east": "Mashonaland East",
    "mash west": "Mashonaland West",
    "mash central": "Mashonaland Central",
}

# Shorthand / alternate spelling → name used on rider profiles (case-insensitive keys).
DISTRICT_ALIASES = {
    "ump": "Uzumba Maramba Pfungwe",
    "murehwa": "Murewa",
    "mt. darwin": "Mount Darwin",
    "mt darwin": "Mount Darwin",
    "kadoma": "Kadoma Sanyati",
}


def norm_text(v: str) -> str:
    return " ".join((v or "").strip().split())


def canon_province_name(name: str) -> str:
    n = norm_text(name)
    return PROVINCE_ALIASES.get(n.lower(), n)


def canon_district_name(name: str) -> str:
    n = norm_text(name)
    if not n:
        return n
    return DISTRICT_ALIASES.get(n.lower(), n)


def district_alias_keys(canonical: str) -> tuple[str, ...]:
    """Names (including aliases) that mean ``canonical``, for DB lookups."""
    target = norm_text(canonical)
    names = [target]
    for alias, dest in DISTRICT_ALIASES.items():
        if dest.casefold() == target.casefold():
            names.append(alias)
            names.append(alias.upper())
            names.append(alias.title())
    seen: set[str] = set()
    out: list[str] = []
    for n in names:
        key = n.casefold()
        if n and key not in seen:
            seen.add(key)
            out.append(n)
    return tuple(out)
