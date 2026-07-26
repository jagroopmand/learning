"""
PATTERN: Streaming aggregation — maintain a running stat without storing everything
PROMPT : "Given a stream of numbers (e.g. request latencies), support
add(x) and get_median() in O(log n) per add, without re-scanning full history."

APPROACH: Two heaps.
  - max_heap (as negated min-heap) holds the SMALLER half
  - min_heap holds the LARGER half
  - Invariant: len(max_heap) == len(min_heap) or len(max_heap) == len(min_heap) + 1
  - Median = top of max_heap (odd count) or avg of both tops (even count)

Space: O(n) for the heaps themselves — but this is unavoidable if you need the
EXACT median. The "don't store everything" win here is architectural (no re-sort
of the full array on every insert, no O(n log n) per query) — flag this
explicitly in the interview: exact median of a stream fundamentally requires
retaining the values in some ordered structure. If the interviewer pushes for
O(1) space, pivot to approximate methods (t-digest, P² algorithm) — see note
at bottom.
"""
import heapq


class RunningMedian:
    def __init__(self):
        self.small = []  # max-heap (store negatives), holds smaller half
        self.large = []  # min-heap, holds larger half

    def add(self, x: float) -> None:
        # Step 1: always push to small first, then rebalance across
        heapq.heappush(self.small, -x)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # Step 2: maintain size invariant (small can have at most 1 extra)
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def get_median(self) -> float:
        if not self.small:
            raise ValueError("no data yet")  # boundary: empty stream
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0


# --- self-verification pass (do this out loud in the real interview) ---
if __name__ == "__main__":
    rm = RunningMedian()

    # Boundary 1: single element
    rm.add(5)
    assert rm.get_median() == 5

    # Boundary 2: two elements (even count -> average)
    rm.add(10)
    assert rm.get_median() == 7.5

    # Boundary 3: negative numbers
    rm.add(-100)
    assert rm.get_median() == 5  # sorted: -100, 5, 10 -> median 5

    # Boundary 4: duplicates
    rm2 = RunningMedian()
    for v in [3, 3, 3, 3]:
        rm2.add(v)
    assert rm2.get_median() == 3

    # Boundary 5: get_median on empty stream should raise, not crash silently
    try:
        RunningMedian().get_median()
        assert False, "expected ValueError"
    except ValueError:
        pass

    # Boundary 6: descending insertion order (stress the rebalance logic)
    rm3 = RunningMedian()
    for v in [9, 8, 7, 6, 5]:
        rm3.add(v)
    assert rm3.get_median() == 7

    print("all boundary checks passed")

# NOTE on approximation (only if interviewer asks for O(1)/sub-linear space):
#   - P^2 algorithm: maintains 5 markers, updates positions with parabolic
#     interpolation, O(1) space, approximate but converges well for streams.
#   - t-digest: clusters of (mean, count), merges neighboring clusters when
#     over a size budget — standard in monitoring systems (this is likely
#     closest to what Tetra's own p95/p99 latency dashboards use internally).
#   - Reservoir sampling + exact median on the sample: O(k) space, tunable
#     accuracy vs. k.
