def merge_windows(windows: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Boundary decision: [1,5] and [5,9] are treated as OVERLAPPING (touching
    counts as merge) -> use `start <= prev_end`, not `<`. Rationale: if a
    user's access ends at t=5 and a new grant starts at t=5, there's no gap
    in actual access -> merging is the correct real-world semantic. State
    this assumption explicitly; a reasonable interviewer may want the
    opposite and you should be ready to flip one comparison operator.
    """
    if not windows:
        return []

    sorted_windows = sorted(windows, key=lambda w: w[0])
    merged = [sorted_windows[0]]

    for start, end in sorted_windows[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:              # overlap OR touching
            merged[-1] = (prev_start, max(prev_end, end))  # handles containment
        else:
            merged.append((start, end))

    return merged


if __name__ == "__main__":
    assert merge_windows([]) == []
    assert merge_windows([(1, 5)]) == [(1, 5)]
    assert merge_windows([(1, 5), (5, 9)]) == [(1, 9)]        # touching -> merged
    assert merge_windows([(1, 5), (6, 9)]) == [(1, 5), (6, 9)]  # gap -> separate
    assert merge_windows([(1, 10), (2, 5)]) == [(1, 10)]       # full containment
    assert merge_windows([(5, 9), (1, 5)]) == [(1, 9)]         # unsorted input
    assert merge_windows([(1, 5), (1, 5)]) == [(1, 5)]         # exact duplicate