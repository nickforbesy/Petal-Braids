from petalbraid import PetalPermutation, build_standard_stem, petal_to_crossings


def test_validate_permutation() -> None:
    pi = PetalPermutation((3, 1, 4, 2, 0))
    assert pi.n == 2
    assert pi.petal_number == 5


def test_cyclic_shift() -> None:
    pi = PetalPermutation((3, 1, 4, 2, 0))
    assert pi.cyclic_shift(1).values == (1, 4, 2, 0, 3)


def test_build_standard_stem() -> None:
    pi = PetalPermutation((3, 1, 4, 2, 0))
    stem = build_standard_stem(pi)
    assert stem.left_pairs[0].is_singleton
    assert stem.right_pairs[-1].is_singleton
    assert [pair.endpoints for pair in stem.ordinary_left_pairs] == [(1, 4), (0, 2)]
    assert [pair.endpoints for pair in stem.ordinary_right_pairs] == [(1, 3), (2, 4)]


def test_crossings_are_list() -> None:
    crossings = petal_to_crossings((3, 1, 4, 2, 0))
    assert isinstance(crossings, list)
