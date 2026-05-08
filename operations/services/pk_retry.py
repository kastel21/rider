"""Retry a write with an increasing integer PK when IntegrityError occurs."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from django.db import IntegrityError, transaction

T = TypeVar("T")


def run_with_incrementing_pk(
    start_pk: int,
    fn: Callable[[int], T],
    *,
    max_attempts: int = 10_000,
) -> tuple[T, int]:
    """
    Call ``fn(pk)`` for ``pk = start_pk, start_pk + 1, ...`` inside ``transaction.atomic()``
    until it returns without raising ``IntegrityError``.

    Returns ``(result, pk_used)``. Raises the last ``IntegrityError`` if all attempts fail.
    """
    last: IntegrityError | None = None
    for offset in range(max_attempts):
        pk = start_pk + offset
        try:
            with transaction.atomic():
                result = fn(pk)
            return result, pk
        except IntegrityError as exc:
            last = exc
            continue
    assert last is not None
    raise last
