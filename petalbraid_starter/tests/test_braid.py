from petalbraid.braid import BraidWord
from petalbraid.markov import MarkovConfig, bounded_markov_equivalent


def test_free_reduction():
    word = BraidWord(3, (1, -1, 2, -2, 1))
    assert word.free_reduce().generators == (1,)


def test_stabilization_changes_braid_group():
    word = BraidWord(3, (1, 2))
    stab = word.stabilize(+1)
    assert stab.num_strands == 4
    assert stab.generators == (1, 2, 3)


def test_simple_destabilization_round_trip():
    word = BraidWord(3, (1,))
    stab = word.stabilize(-1)
    assert stab.can_simple_destabilize()
    assert stab.simple_destabilize() == word


def test_bounded_markov_equivalence_catches_simple_stabilization():
    left = BraidWord(3, (1, 2))
    right = left.stabilize(+1)
    cfg = MarkovConfig(max_depth=2)
    assert bounded_markov_equivalent(left, right, cfg)
