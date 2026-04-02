from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .braid import BraidWord


@dataclass(frozen=True)
class MarkovConfig:
    max_depth: int = 4
    allow_stabilization: bool = True
    allow_destabilization: bool = True
    allow_cyclic_conjugation: bool = True


def markov_neighbors(word: BraidWord, config: MarkovConfig | None = None) -> tuple[BraidWord, ...]:
    cfg = config or MarkovConfig()
    out: list[BraidWord] = []

    if cfg.allow_cyclic_conjugation:
        out.extend(word.cyclic_conjugates())

    if cfg.allow_stabilization:
        out.append(word.stabilize(+1).free_reduce())
        out.append(word.stabilize(-1).free_reduce())

    if cfg.allow_destabilization and word.can_simple_destabilize():
        out.append(word.simple_destabilize())

    dedup = dict.fromkeys(w.free_reduce() for w in out)
    return tuple(dedup)


def bounded_markov_equivalent(
    left: BraidWord,
    right: BraidWord,
    config: MarkovConfig | None = None,
) -> bool:
    """Experimental bounded search for Markov equivalence.

    This is useful for small examples and debugging your conversion routine,
    but it is not a complete decision procedure at finite depth.
    """

    cfg = config or MarkovConfig()
    left0 = left.free_reduce()
    right0 = right.free_reduce()
    if left0 == right0:
        return True

    q = deque([(left0, 0)])
    seen = {left0}

    while q:
        current, depth = q.popleft()
        if depth >= cfg.max_depth:
            continue
        for nxt in markov_neighbors(current, cfg):
            if nxt == right0:
                return True
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, depth + 1))

    return False
