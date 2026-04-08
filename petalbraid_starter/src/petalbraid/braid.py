from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def _validate_generator(gen: int, num_strands: int) -> None:
    """Validate that a generator is valid for the given braid group.
    
    Args:
        gen: The generator value. Positive integers represent sigma_i,
             negative integers represent sigma_i^{-1}.
        num_strands: The number of strands in the braid group B_n.
    
    Raises:
        ValueError: If gen is 0, or if the absolute value of gen is not
                   in the valid range [1, num_strands - 1].
    """
    if gen == 0:
        raise ValueError("Generator 0 is invalid. Use +/-i for sigma_i^{+/-1}.")
    idx = abs(gen)
    if not (1 <= idx <= num_strands - 1):
        raise ValueError(
            f"Generator {gen} invalid for B_{num_strands}; expected 1..{num_strands - 1}."
        )


@dataclass(frozen=True)
class BraidWord:
    """A braid word in Artin generators.

    We encode sigma_i as +i and sigma_i^{-1} as -i.
    Example: (1, 2, -1) means sigma_1 sigma_2 sigma_1^{-1}.
    """

    num_strands: int
    generators: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.num_strands < 2:
            raise ValueError("A braid needs at least 2 strands.")
        for gen in self.generators:
            _validate_generator(gen, self.num_strands)

    @classmethod
    def from_iterable(cls, num_strands: int, generators: Iterable[int]) -> "BraidWord":
        return cls(num_strands=num_strands, generators=tuple(int(g) for g in generators))

    def __mul__(self, other: "BraidWord") -> "BraidWord":
        if self.num_strands != other.num_strands:
            raise ValueError("Cannot multiply braid words from different braid groups.")
        return BraidWord(self.num_strands, self.generators + other.generators)

    def inverse(self) -> "BraidWord":
        return BraidWord(self.num_strands, tuple(-g for g in reversed(self.generators)))

    def free_reduce(self) -> "BraidWord":
        stack: list[int] = []
        for gen in self.generators:
            if stack and stack[-1] == -gen:
                stack.pop()
            else:
                stack.append(gen)
        return BraidWord(self.num_strands, tuple(stack))

    def conjugate_by_word(self, conjugator: "BraidWord") -> "BraidWord":
        if self.num_strands != conjugator.num_strands:
            raise ValueError("Conjugator must be in the same braid group.")
        return (conjugator * self * conjugator.inverse()).free_reduce()

    def cyclic_conjugates(self) -> tuple["BraidWord", ...]:
        gens = self.free_reduce().generators
        if not gens:
            return (self.free_reduce(),)
        out = []
        for k in range(len(gens)):
            rotated = gens[k:] + gens[:k]
            out.append(BraidWord(self.num_strands, rotated).free_reduce())
        return tuple(dict.fromkeys(out))

    def stabilize(self, sign: int = 1) -> "BraidWord":
        if sign not in (-1, 1):
            raise ValueError("sign must be +1 or -1")
        new_generator = sign * self.num_strands
        return BraidWord(self.num_strands + 1, self.generators + (new_generator,))

    def can_simple_destabilize(self) -> bool:
        if self.num_strands <= 2 or not self.generators:
            return False
        last = self.generators[-1]
        if abs(last) != self.num_strands - 1:
            return False
        return all(abs(g) <= self.num_strands - 2 for g in self.generators[:-1])

    def simple_destabilize(self) -> "BraidWord":
        if not self.can_simple_destabilize():
            raise ValueError("This word is not in the simple alpha*sigma_n^{+/-1} form.")
        return BraidWord(self.num_strands - 1, self.generators[:-1]).free_reduce()

    def exponent_sum(self) -> int:
        return sum(1 if g > 0 else -1 for g in self.generators)

    def canonical_string(self) -> str:
        if not self.generators:
            return f"B_{self.num_strands}: 1"
        parts = []
        for g in self.generators:
            if g > 0:
                parts.append(f"s{g}")
            else:
                parts.append(f"s{-g}^-1")
        return f"B_{self.num_strands}: " + " ".join(parts)

    def __str__(self) -> str:
        return self.canonical_string()
