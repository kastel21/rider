"""Best-effort parse and merge of trip ``*_other_specify`` free text for M&E export.

Riders enter counts per category as free text (e.g. ``8 CD4, 10 FBC``). When multiple
trip rows or weekly reports are aggregated, matching categories (case-insensitive) have
their counts summed for display only — stored trip text is not modified.

Limitations: typos and inconsistent spelling will not merge; parsing is heuristic.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

_SEGMENT_SPLIT = re.compile(r"[,;]+")

# Leading integer, optional space, then label (hyphens allowed, e.g. COVID-19).
_COUNT_LABEL = re.compile(r"^(\d+)\s+(.+)$", re.DOTALL)

# Count glued directly to label (e.g. 10fbc).
_COUNT_GLUED = re.compile(r"^(\d+)([A-Za-z].+)$")


@dataclass(frozen=True)
class _ParsedSegment:
    kind: Literal["counted", "opaque"]
    count: int
    label: str
    raw: str


def _normalize_label_key(label: str) -> str:
    return " ".join(label.split()).casefold()


def _parse_segment(segment: str) -> _ParsedSegment:
    raw = segment.strip()
    if not raw:
        return _ParsedSegment(kind="opaque", count=0, label="", raw="")

    m = _COUNT_LABEL.match(raw)
    if m:
        return _ParsedSegment(
            kind="counted",
            count=int(m.group(1)),
            label=m.group(2).strip(),
            raw=raw,
        )

    m = _COUNT_GLUED.match(raw)
    if m:
        return _ParsedSegment(
            kind="counted",
            count=int(m.group(1)),
            label=m.group(2).strip(),
            raw=raw,
        )

    # No leading count — opaque segment (deduped by exact text, not merged by label).
    return _ParsedSegment(kind="opaque", count=1, label=raw, raw=raw)


def parse_other_specify(text: str) -> list[tuple[int, str]]:
    """Parse one field value into ``(count, label)`` pairs for counted segments only."""
    out: list[tuple[int, str]] = []
    for part in _SEGMENT_SPLIT.split(text or ""):
        seg = _parse_segment(part)
        if seg.kind == "counted" and seg.label:
            out.append((seg.count, seg.label))
    return out


def aggregate_other_specify_texts(texts: list[str]) -> str:
    """
    Merge multiple ``*_other_specify`` strings: sum counts for the same category label.

    Category order follows first appearance across all input strings. Display casing
    is taken from the first occurrence of each category. Unparseable segments are
    appended unchanged (exact-text dedupe).
    """
    counts: dict[str, int] = {}
    display_labels: dict[str, str] = {}
    order: list[str] = []
    opaque_seen: list[str] = []
    opaque_set: set[str] = set()

    for text in texts:
        if not (text or "").strip():
            continue
        for part in _SEGMENT_SPLIT.split(text):
            seg = _parse_segment(part)
            if not seg.raw:
                continue
            if seg.kind == "counted" and seg.label:
                key = _normalize_label_key(seg.label)
                if key not in counts:
                    counts[key] = 0
                    display_labels[key] = seg.label
                    order.append(key)
                counts[key] += seg.count
            else:
                t = seg.raw
                if t not in opaque_set:
                    opaque_set.add(t)
                    opaque_seen.append(t)

    parts: list[str] = []
    for key in order:
        parts.append(f"{counts[key]} {display_labels[key]}")
    parts.extend(opaque_seen)
    return ", ".join(parts)
