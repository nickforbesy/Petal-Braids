from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .permutation import PetalPermutation


class Side(str, Enum):
    LEFT = "L"
    RIGHT = "R"


@dataclass(frozen=True, slots=True)
class StemPair:
    """
    One left- or right-side pair in a stem-style representation.

    For now, a pair is either:
    - an interval `(low, high)` with low < high, or
    - a singleton `(k,)` representing one of the special/basepoint strands.
    """

    side: Side
    endpoints: tuple[int, ...]
    index: int

    def __post_init__(self) -> None:
        if len(self.endpoints) not in (1, 2):
            raise ValueError("StemPair endpoints must have length 1 or 2")
        if len(self.endpoints) == 2 and self.endpoints[0] >= self.endpoints[1]:
            raise ValueError("StemPair interval endpoints must satisfy low < high")

    @property
    def is_singleton(self) -> bool:
        return len(self.endpoints) == 1

    @property
    def low(self) -> int:
        if self.is_singleton:
            raise ValueError("singleton StemPair has no interval low endpoint")
        return self.endpoints[0]

    @property
    def high(self) -> int:
        if self.is_singleton:
            raise ValueError("singleton StemPair has no interval high endpoint")
        return self.endpoints[1]


@dataclass(frozen=True, slots=True)
class StemDiagram:
    word: PetalPermutation
    left_pairs: tuple[StemPair, ...]
    right_pairs: tuple[StemPair, ...]

    @property
    def ordinary_left_pairs(self) -> tuple[StemPair, ...]:
        return tuple(pair for pair in self.left_pairs if not pair.is_singleton)

    @property
    def ordinary_right_pairs(self) -> tuple[StemPair, ...]:
        return tuple(pair for pair in self.right_pairs if not pair.is_singleton)


def build_standard_stem(word: PetalPermutation) -> StemDiagram:
    """
    Build the standard left/right pairing associated to a chosen word
    W = (p0, ..., p_{2n}).

    Left side:
        (p0), (p1, p2), (p3, p4), ..., (p_{2n-1}, p_{2n})

    Right side:
        (p0, p1), (p2, p3), ..., (p_{2n-2}, p_{2n-1}), (p_{2n})
    """
    p = word.values

    left_pairs: list[StemPair] = [StemPair(Side.LEFT, (p[0],), 0)]
    left_index = 1
    for i in range(1, len(p), 2):
        a, b = sorted((p[i], p[i + 1]))
        left_pairs.append(StemPair(Side.LEFT, (a, b), left_index))
        left_index += 1

    right_pairs: list[StemPair] = []
    right_index = 0
    for i in range(0, len(p) - 1, 2):
        a, b = sorted((p[i], p[i + 1]))
        right_pairs.append(StemPair(Side.RIGHT, (a, b), right_index))
        right_index += 1
    right_pairs.append(StemPair(Side.RIGHT, (p[-1],), right_index))

    return StemDiagram(
        word=word,
        left_pairs=tuple(left_pairs),
        right_pairs=tuple(right_pairs),
    )
