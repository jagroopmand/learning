"""
GENERIC DSA GAP: two-pointer technique — not touched in any drill so far.
Common fallback pattern for array/string problems when the interviewer wants
to see you avoid an O(n^2) brute force.

PROMPT (Jatin-style, could map to "merge two sorted audit-log streams by
timestamp"): "Given two sorted arrays, merge them into one sorted array."

PROMPT variant (classic, likely if they go generic): "Given a sorted array,
find two numbers that sum to a target." (two-sum on sorted input)
"""


def merge_sorted(a: list, b: list) -> list:
    """Merge two sorted lists in O(n+m), O(n+m) space. Stable on ties (a first)."""
    i, j = 0, 0
    result = []

    while i < len(a) and j < len(b):
        # tie-break: a first, to keep merge stable if these were, say,
        # two sorted log streams and a's source should win ties
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    # boundary: drain whichever list still has leftovers
    result.extend(a[i:])
    result.extend(b[j:])
    return result


def two_sum_sorted(arr: list, target: int):
    """Two-pointer two-sum on a SORTED array. O(n) time, O(1) space.
    Returns (i, j) indices or None if no pair sums to target."""
    lo, hi = 0, len(arr) - 1

    while lo < hi:
        total = arr[lo] + arr[hi]
        if total == target:
            return (lo, hi)
        elif total < target:
            lo += 1
        else:
            hi -= 1

    return None  # boundary: no valid pair


# --- self-verification pass ---
if __name__ == "__main__":
    # merge_sorted boundaries
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([], [1, 2]) == [1, 2]            # one list empty
    assert merge_sorted([1, 2], []) == [1, 2]            # other list empty
    assert merge_sorted([], []) == []                     # both empty
    assert merge_sorted([1, 1, 1], [1, 1]) == [1, 1, 1, 1, 1]  # all duplicates
    assert merge_sorted([5], [1]) == [1, 5]              # single elements, b < a

    # two_sum_sorted boundaries
    assert two_sum_sorted([1, 2, 3, 4, 6], 6) == (1, 3)  # 2+4
    assert two_sum_sorted([1, 2, 3], 100) is None        # no pair exists
    assert two_sum_sorted([3, 3], 6) == (0, 1)           # exact duplicate pair
    assert two_sum_sorted([1], 1) is None                # single element, can't pair with self
    assert two_sum_sorted([-3, -1, 0, 2, 5], 4) == (1, 4)  # negative numbers: -1+5

    print("all boundary checks passed")
