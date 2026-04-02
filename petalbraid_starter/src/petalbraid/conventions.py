from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReductionStrategy(str, Enum):
    """How aggressively to simplify a braid word."""

    FREE = "free"
    # Placeholder for future work:
    BRAID_RELATIONS = "braid_relations"


@dataclass(frozen=True, slots=True)
class ConversionConvention:
    """
    Knobs that control the conversion pipeline.

    Notes
    -----
    This starter scaffold intentionally keeps a few choices explicit instead of
    hard-coding a petal-to-braid convention too early.
    """

    cyclic_input: bool = False
    word_start: int = 0
    include_singleton_pairs: bool = False
    reduction: ReductionStrategy = ReductionStrategy.FREE
