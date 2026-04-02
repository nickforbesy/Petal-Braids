from __future__ import annotations

from .permutation import PetalPermutation


SAMPLE_PETAL_PERMUTATIONS_1_BASED = {
    "3_1": "(1357246)",
    "8_19": "(1473625)",
    "4_1": "(1352746)",
    "5_1": "(1426375)",
    "5_2": "(1462735)",
}


def load_samples() -> dict[str, PetalPermutation]:
    return {
        name: PetalPermutation.from_string(text, base=1)
        for name, text in SAMPLE_PETAL_PERMUTATIONS_1_BASED.items()
    }
