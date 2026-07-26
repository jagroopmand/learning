"""
PATTERN: Streaming aggregation — running percentile (p95/p99) with bounded memory
PROMPT: "You're monitoring PDP (policy decision point) latency.
Track p95 over the last N requests with O(1) memory-ish, no full history scan."

APPROACH: Fixed-size sliding window + sorted insertion (bisect).
This is the pragmatic interview-friendly version: O(window) space (bounded,
not "everything"), O(log w) insert via bisect, O(1) percentile read.
Distinguish this out loud from RunningMedian above: here we deliberately
DROP old data (sliding window over last N), trading exactness-over-all-time
for bounded memory — which is usually what a latency dashboard actually wants
anyway (you care about "recent" p95, not all-time p95).
"""
import bisect
from collections import deque


class RunningPercentile:
    def __init__(self, window_size: int, percentile: float = 0.95):
        if window_size <= 0:
            raise ValueError("window_size must be positive")  # boundary
        if not (0 < percentile < 1):
            raise ValueError("percentile must be in (0, 1)")  # boundary
        self.window_size = window_size
        self.percentile = percentile
        self.order = deque()      # insertion order, for eviction
        self.sorted_vals = []     # kept sorted for O(log w) percentile lookup

    def add(self, latency_ms: float) -> None:
        self.order.append(latency_ms)
        bisect.insort(self.sorted_vals, latency_ms)

        if len(self.order) > self.window_size:
            oldest = self.order.popleft()
            # remove exactly one occurrence of `oldest` from sorted_vals
            idx = bisect.bisect_left(self.sorted_vals, oldest)
            # defensive check: with float latencies duplicates are common,
            # bisect_left gives the FIRST matching index, which is correct
            # for removing "the" oldest value's slot (still O(log w) find,
            # O(w) removal due to list shift — acceptable at interview scale;
            # flag that a real prod version would use a Fenwick tree / skip
            # list / sorted balanced structure for O(log w) removal too).
            assert self.sorted_vals[idx] == oldest  # self-check: found it
            self.sorted_vals.pop(idx)

    def get_percentile(self) -> float:
        if not self.sorted_vals:
            raise ValueError("no data yet")  # boundary: empty window
        idx = int(self.percentile * (len(self.sorted_vals) - 1))
        return self.sorted_vals[idx]


# --- self-verification pass ---
if __name__ == "__main__":
    rp = RunningPercentile(window_size=5, percentile=0.95)

    # Boundary 1: window not yet full (n=2 -> idx = int(0.95*(2-1)) = 0 -> arr[0])
    rp.add(10)
    rp.add(20)
    assert rp.get_percentile() == 10  # low-biased for tiny n, worth flagging aloud

    # Boundary 2: window exactly full
    for v in [30, 40, 50]:
        rp.add(v)
    assert rp.sorted_vals == [10, 20, 30, 40, 50]

    # Boundary 3: eviction on overflow — oldest (10) should drop
    rp.add(60)
    assert 10 not in rp.sorted_vals
    assert rp.sorted_vals == [20, 30, 40, 50, 60]

    # Boundary 4: duplicate values (must evict the correct instance, not both)
    rp2 = RunningPercentile(window_size=3, percentile=0.95)
    rp2.add(5)
    rp2.add(5)
    rp2.add(5)
    rp2.add(9)  # evicts one of the three 5s
    assert rp2.sorted_vals == [5, 5, 9], rp2.sorted_vals

    # Boundary 5: invalid construction args should raise immediately
    for bad_kwargs in [dict(window_size=0), dict(window_size=5, percentile=1.0)]:
        try:
            RunningPercentile(**bad_kwargs)
            assert False, f"expected ValueError for {bad_kwargs}"
        except ValueError:
            pass

    print("all boundary checks passed")
