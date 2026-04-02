from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .braid import BraidWord
from .crossings import CrossingRecord, enumerate_stem_crossings
from .permutation import PetalPermutation
from .stem import build_standard_stem


@dataclass(frozen=True)
class PetalToBraidConvention:
    """Configuration for your eventual petal -> braid algorithm.

    The scaffold is intentionally explicit about these choices because they
    affect the braid word you get from a petal permutation.
    """

    input_base: int = 0
    canonicalize_rotation: bool = False
    target_num_strands: int | None = None
    placeholder_positive: bool = True


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


def petal_to_crossings(
    data: PetalPermutation | Iterable[int] | str,
    *,
    convention: PetalToBraidConvention | None = None,
) -> list[CrossingRecord]:
    """Convert a petal permutation into a crossing list via a stem intermediate.

    This is a solid first milestone because it gives you a deterministic,
    inspectable combinatorial object before you commit to a braid convention.
    """

    conv = convention or PetalToBraidConvention()
    perm = _coerce_permutation(data, convention=conv)
    stem = build_standard_stem(perm)
    return enumerate_stem_crossings(stem)


def petal_to_unreduced_braid(
    data: PetalPermutation | Iterable[int] | str,
    *,
    convention: PetalToBraidConvention | None = None,
) -> ConversionResult:
    """Starter placeholder from petal permutation to braid word.

    The current generator assignment is intentionally simple and deterministic:
    the k-th crossing becomes sigma_k (or sigma_k^-1 if you flip the placeholder
    sign). This is *not* the final knot-theoretic map. It is here so the
    package is runnable while we develop the real generator/sign assignment.
    """

    conv = convention or PetalToBraidConvention()
    perm = _coerce_permutation(data, convention=conv)
    crossings = tuple(petal_to_crossings(perm, convention=conv))

    if conv.target_num_strands is None:
        num_strands = max(2, len(crossings) + 1)
    else:
        num_strands = conv.target_num_strands

    sign = 1 if conv.placeholder_positive else -1
    generators = tuple(sign * max(1, idx) for idx, _ in enumerate(crossings, start=1))
    braid = BraidWord(num_strands=num_strands, generators=generators)

    return ConversionResult(permutation=perm, crossings=crossings, braid=braid)
