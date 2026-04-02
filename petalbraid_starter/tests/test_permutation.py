from petalbraid.permutation import PetalPermutation
from petalbraid.samples import load_samples


def test_parse_one_based_compact_cycle():
    p = PetalPermutation.from_string("(1357246)", base=1)
    assert p.values == (0, 2, 4, 6, 1, 3, 5)
    assert p.n == 3


def test_rotation_count_matches_size():
    p = PetalPermutation.from_iterable([0, 2, 4, 6, 1, 3, 5])
    assert len(p.all_rotations()) == p.size


def test_abs_differences_for_trefoil_sample():
    p = PetalPermutation.from_string("(1357246)", base=1)
    assert p.abs_differences_cyclic() == (2, 2, 2, 2, 2, 2, 2)


def test_load_user_samples():
    samples = load_samples()
    assert set(samples) == {"3_1", "8_19", "4_1", "5_1", "5_2"}
