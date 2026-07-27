"""
PATTERN: Hash map lookup — two-sum on an UNSORTED array.
PROMPT (generic DSA fallback): "Given an unsorted array, find two numbers
that sum to a target." Return their indices.

WHY HASH MAP, NOT TWO-POINTER:
Two-pointer requires sorted input to know which direction to move (see
04_two_pointer.py). Sorting first would work but costs O(n log n) and
destroys the original index order (you'd have to carry index-tracking
alongside the sort, adding complexity for no benefit).

A hash map gets you O(n) time in a SINGLE PASS, with indices preserved
for free, because you never reorder the array — you just remember what
you've seen and check whether its complement has already appeared.

CORE IDEA:
  - Walk the array once, left to right.
  - At each element x, compute complement = target - x.
  - If complement is already in the map, we found our pair -> done.
  - Otherwise, record x's own index in the map and keep going.

This works because by the time we reach index i, the map contains every
index j < i. So if a valid pair (i, j) exists with j < i, we will have
already stored j's value by the time we check i's complement.
"""


def two_sum_unsorted(arr: list, target: int):
    """
    Returns (first_index, second_index) of a pair summing to target,
    or None if no such pair exists.

    Time:  O(n)  — single pass
    Space: O(n)  — hash map holds up to n entries
    """
    seen = {}  # maps: value -> index where it was first seen

    for i, x in enumerate(arr):
        complement = target - x

        # Step 1: has the number we NEED already appeared earlier?
        if complement in seen:
            return (seen[complement], i)

        # Step 2: not found yet — remember this value for future lookups.
        # Important: record AFTER checking, so a single element can't
        # pair with itself (e.g. target=6, x=3 — 3 shouldn't match its
        # own complement of 3 unless a DIFFERENT index also holds 3).
        seen[x] = i

    return None  # boundary: no valid pair exists anywhere in the array


# --- self-verification pass (run every boundary before calling it done) ---
if __name__ == "__main__":

    # Boundary 1: straightforward pair, order doesn't matter in the array
    assert two_sum_unsorted([2, 7, 11, 15], 9) == (0, 1)  # 2 + 7

    # Boundary 2: pair appears out of "natural" order
    assert two_sum_unsorted([3, 2, 4], 6) == (1, 2)  # 2 + 4

    # Boundary 3: no valid pair — must return None, not crash or raise
    assert two_sum_unsorted([1, 2, 3], 100) is None

    # Boundary 4: exact duplicate values forming the pair (e.g. 3 + 3 = 6)
    assert two_sum_unsorted([3, 3], 6) == (0, 1)

    # Boundary 5: a single element CANNOT pair with itself
    # (target=6, arr=[3] alone has no partner — must NOT match 3 against
    # its own index before a second 3 has been seen)
    assert two_sum_unsorted([3], 6) is None

    # Boundary 6: negative numbers in the mix (-3 + 4 = 1, found at index 1)
    assert two_sum_unsorted([-3, 4, 1, 90], 1) == (0, 1)  # -3 + 4 = 1

    # Boundary 7: zero as a valid target/value
    assert two_sum_unsorted([0, 4, 3, 0], 0) == (0, 3)  # 0 + 0 = 0

    # Boundary 8: empty array
    assert two_sum_unsorted([], 5) is None

    print("all boundary checks passed")


# INTERVIEW TALKING POINT (state this proactively, don't wait to be asked):
# "I'm using a hash map here because the array is unsorted — sorting first
#  and using two pointers would work too, but costs O(n log n) instead of
#  O(n), and I'd have to track original indices separately since sorting
#  reorders the array. The hash map avoids both problems in one pass."