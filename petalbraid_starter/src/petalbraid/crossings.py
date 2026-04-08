from __future__ import annotations

from dataclasses import dataclass

from .stem import Side, StemDiagram, StemPair


@dataclass(frozen=True, slots=True)
class CrossingRecord:
    """
    A purely combinatorial crossing record.

    Notes
    -----
    This object deliberately stops short of claiming an Artin generator index or
    a sign. Those depend on the exact braidification/sign conventions you adopt.
    """

    side: Side
    first: StemPair
    second: StemPair
    order_key: tuple[int, int, int, int]


def intervals_interleave(a: StemPair, b: StemPair) -> bool:
    if a.is_singleton or b.is_singleton:
        return False

    x1, x2 = a.endpoints
    y1, y2 = b.endpoints
    return (x1 < y1 < x2 < y2) or (y1 < x1 < y2 < x2)


def crossing_order_key(a: StemPair, b: StemPair) -> tuple[int, int, int, int]:
    """
    A deterministic sort key for crossings.

    This is just a stable placeholder. You may later replace it with the exact
    geometric order in which your chosen sweep/braidification encounters the
    crossings.
    """
    return (*a.endpoints, *b.endpoints)


def enumerate_side_crossings(pairs: tuple[StemPair, ...], side: Side) -> list[CrossingRecord]:
    """
    Enumerate all crossings between stem pairs on a given side.

    Parameters
    ----------
    pairs : tuple[StemPair, ...]
        A tuple of stem pairs to check for crossings.
    side : Side
        The side (LEFT or RIGHT) these pairs belong to.

    Returns
    -------
    list[CrossingRecord]
        A sorted list of crossing records for all pairs that interleave,
        ordered by their crossing order key.

    Notes
    -----
    Only pairs with interleaving intervals are included as crossings.
    Singleton pairs are automatically excluded by the interleaving check.
    """
    out: list[CrossingRecord] = []
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            a = pairs[i]
            b = pairs[j]
            if intervals_interleave(a, b):
                out.append(
                    CrossingRecord(
                        side=side,
                        first=a,
                        second=b,
                        order_key=crossing_order_key(a, b),
                    )
                )
    out.sort(key=lambda c: c.order_key)
    return out


def enumerate_stem_crossings(stem: StemDiagram) -> list[CrossingRecord]:
    left = enumerate_side_crossings(stem.ordinary_left_pairs, Side.LEFT)
    right = enumerate_side_crossings(stem.ordinary_right_pairs, Side.RIGHT)
    all_crossings = left + right
    all_crossings.sort(key=lambda c: c.order_key)
    return all_crossings
