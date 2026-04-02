# petalbraid

A starter Python package for experiments with petal permutations, braid words,
and Markov-equivalence-aware design.

This scaffold is intentionally split into three layers:

1. `permutation.py`
   - parse and validate petal permutations
   - support both 1-based and 0-based input conventions
   - normalize cyclic rotations when you decide on a canonical representative

2. `braid.py`
   - represent braid words in Artin generators
   - word-level operations: inversion, free reduction, conjugation,
     stabilization and simple destabilization checks

3. `markov.py`
   - Markov-move layer on top of braid words
   - bounded search utilities for experimentation
   - API surface where a later complete equivalence engine can live

4. `converters.py`
   - where your actual petal-permutation-to-braid algorithm should go
   - currently a clean placeholder with typed hooks

## Quick start

```bash
cd petalbraid_starter
python -m pytest
```

## Notes on scope

This starter does **not** claim to solve the full Markov-equivalence problem by
local simplification alone. Instead, it gives you a clean package shape that
keeps these concerns separate:

- deterministic conversion from a chosen petal convention to an unreduced braid
- algebraic word simplification inside a fixed braid group
- Markov-level moves between different braid groups

That separation matters because "reduced braid word" and "same closed braid"
are different problems.
