from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PetalPermutation:
    """A validated petal permutation.

    Internally this is always stored in 0-based form on {0, ..., 2n}.
    Example:
        input '(1357246)' with base=1 -> values=(0, 2, 4, 6, 1, 3, 5)
    """

    values: tuple[int, ...]

    def __post_init__(self) -> None:
        vals = self.values
        if len(vals) % 2 == 0:
            raise ValueError("Petal permutations must have odd length 2n+1.")
        expected = tuple(range(len(vals)))
        if tuple(sorted(vals)) != expected:
            raise ValueError(
                f"Expected a permutation of {expected}, got {vals}."
            )

    @classmethod
    def from_iterable(cls, values: Iterable[int], *, base: int = 0) -> "PetalPermutation":
        vals = tuple(int(v) - base for v in values)
        return cls(vals)

    @classmethod
    def from_string(cls, text: str, *, base: int = 0) -> "PetalPermutation":
        digits = _parse_cycle_text(text)
        return cls.from_iterable(digits, base=base)

    @property
    def size(self) -> int:
        return len(self.values)

    @property
    def petal_number(self) -> int:
        return len(self.values)

    @property
    def n(self) -> int:
        return (len(self.values) - 1) // 2

    def to_base(self, base: int = 0) -> tuple[int, ...]:
        return tuple(v + base for v in self.values)

    def rotate(self, shift: int) -> "PetalPermutation":
        k = shift % self.size
        return PetalPermutation(self.values[k:] + self.values[:k])

    def all_rotations(self) -> tuple["PetalPermutation", ...]:
        return tuple(self.rotate(k) for k in range(self.size))

    def cyclic_shift(self, shift: int) -> "PetalPermutation":
        return self.rotate(shift)

    def all_cyclic_shifts(self) -> tuple["PetalPermutation", ...]:
        return self.all_rotations()

    def canonical_shift_by_minimum(self) -> "PetalPermutation":
        idx = self.values.index(0)
        return self.rotate(idx)

    def canonical_lex_rotation(self) -> "PetalPermutation":
        return min(self.all_rotations(), key=lambda p: p.values)

    def abs_differences_cyclic(self) -> tuple[int, ...]:
        """Cyclic distances between consecutive entries modulo the permutation size.

        For size m, the distance between a and b is min(|a-b|, m-|a-b|).
        This matches the common knot-table summary format for petal permutations.
        """
        vals = self.values
        m = self.size
        out = []
        for i in range(m):
            diff = abs(vals[(i + 1) % m] - vals[i])
            out.append(min(diff, m - diff))
        return tuple(out)

    def __str__(self) -> str:
        return f"PetalPermutation{self.values}"


def _parse_cycle_text(text: str) -> tuple[int, ...]:
    cleaned = text.strip()
    for ch in "()[]{} ,":
        cleaned = cleaned.replace(ch, "")
    if not cleaned:
        raise ValueError("Empty permutation string.")

    if "," in text or " " in text:
        tokens = text.replace("(", " ").replace(")", " ")
        tokens = tokens.replace("[", " ").replace("]", " ")
        tokens = tokens.replace("{", " ").replace("}", " ")
        tokens = tokens.replace(",", " ").split()
        if not tokens:
            raise ValueError("Could not parse permutation tokens.")
        return tuple(int(tok) for tok in tokens)

    if not cleaned.isdigit():
        raise ValueError(
            "Compact cycle notation currently supports only single-digit entries. "
            "Use a spaced or comma-separated form for multi-digit entries."
        )
    return tuple(int(ch) for ch in cleaned)
