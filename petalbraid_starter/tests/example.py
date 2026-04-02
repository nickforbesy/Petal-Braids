from petalbraid.permutation import PetalPermutation
from petalbraid.converters import PetalToBraidConvention, petal_to_unreduced_braid
from petalbraid.braid import BraidWord

def run_example():
    # 1) Pick a petal permutation in 1-based indexing
    #    For 2n+1=7, permute {1..7} in petal-knot form
    raw_perm = (1, 4,7, 3,6,2,5)

    # 2) Build validated object
    petal_perm = PetalPermutation.from_iterable(raw_perm, base=1)
    print("petal permutation (0-based internal):", petal_perm)

    # 3) Convert
    conv = PetalToBraidConvention(
        input_base=1,
        canonicalize_rotation=False,
        target_num_strands=None,
        placeholder_positive=True,
    )
    result = petal_to_unreduced_braid(petal_perm, convention=conv)

    print("permutation:", result.permutation)
    print("crossings:", result.crossings)
    print("braid (unreduced):", result.braid)
    print("braid generator tuple:", result.braid.generators)
    print("braid canonical string:", result.braid.canonical_string())

    # 4) Use BraidWord API
    reduced = result.braid.free_reduce()
    print("braid free reduction:", reduced)

if __name__ == "__main__":
    run_example()