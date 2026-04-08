from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .braid import BraidWord
from .crossings import CrossingRecord, enumerate_stem_crossings
from .permutation import PetalPermutation
from .stem import build_standard_stem


@dataclass(frozen=True)
class PetalToBraidConvention:
    input_base: int = 0
    canonicalize_rotation: bool = False
    target_num_strands: int | None = None
    placeholder_positive: bool = True
    placeholder_strategy: str = "wave"  # "wave" or "increasing"


@dataclass(frozen=True)
class ConversionResult:
    permutation: PetalPermutation
    crossings: tuple[CrossingRecord, ...]
    braid: BraidWord


def _coerce_permutation(
    data: PetalPermutation | Iterable[int] | str,
    *,
    convention: PetalToBraidConvention,
) -> PetalPermutation:
    if isinstance(data, PetalPermutation):
        perm = data
    elif isinstance(data, str):
        perm = PetalPermutation.from_string(data, base=convention.input_base)
    else:
        perm = PetalPermutation.from_iterable(data, base=convention.input_base)

    if convention.canonicalize_rotation:
        perm = perm.canonical_lex_rotation()
    return perm


def _default_num_strands(perm: PetalPermutation) -> int:
    return max(1, (len(perm) - 1) // 2)


def _wave_indices(num_crossings: int, num_strands: int) -> tuple[int, ...]:
    """Return indices like 1,2,...,m,m-1,...,1,2,... with m=num_strands-1."""
    max_gen = num_strands - 1
    if max_gen <= 0 or num_crossings <= 0:
        return ()

    if max_gen == 1:
        return (1,) * num_crossings

    one_period = tuple(range(1, max_gen + 1)) + tuple(range(max_gen - 1, 0, -1))
    out: list[int] = []
    while len(out) < num_crossings:
        out.extend(one_period)
    return tuple(out[:num_crossings])


def _increasing_indices(num_crossings: int, num_strands: int) -> tuple[int, ...]:
    """Return indices cycling upward: 1,2,...,m,1,2,..."""
    max_gen = num_strands - 1
    if max_gen <= 0 or num_crossings <= 0:
        return ()

    return tuple(((k % max_gen) + 1) for k in range(num_crossings))


def _placeholder_generators(
    *,
    num_crossings: int,
    num_strands: int,
    positive: bool,
    strategy: str,
) -> tuple[int, ...]:
    if strategy == "wave":
        base = _wave_indices(num_crossings, num_strands)
    elif strategy == "increasing":
        base = _increasing_indices(num_crossings, num_strands)
    else:
        raise ValueError(f"Unknown placeholder strategy: {strategy!r}")

    sign = 1 if positive else -1
    return tuple(sign * g for g in base)


def petal_to_crossings(
    data: PetalPermutation | Iterable[int] | str,
    *,
    convention: PetalToBraidConvention | None = None,
) -> list[CrossingRecord]:
    conv = convention or PetalToBraidConvention()
    perm = _coerce_permutation(data, convention=conv)
    stem = build_standard_stem(perm)
    return enumerate_stem_crossings(stem)


def petal_to_unreduced_braid(
    data: PetalPermutation | Iterable[int] | str,
    *,
    convention: PetalToBraidConvention | None = None,
) -> ConversionResult:
    conv = convention or PetalToBraidConvention()
    perm = _coerce_permutation(data, convention=conv)
    crossings = tuple(petal_to_crossings(perm, convention=conv))

    if conv.target_num_strands is None:
        num_strands = _default_num_strands(perm)
    else:
        num_strands = conv.target_num_strands

    generators = _placeholder_generators(
        num_crossings=len(crossings),
        num_strands=num_strands,
        positive=conv.placeholder_positive,
        strategy=conv.placeholder_strategy,
    )
    braid = BraidWord(num_strands=num_strands, generators=generators)

    return ConversionResult(permutation=perm, crossings=crossings, braid=braid)
