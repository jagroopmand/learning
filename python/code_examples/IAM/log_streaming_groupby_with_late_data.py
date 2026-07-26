class WindowedAggregator:
    """
    60-second tumbling windows, keyed by group_id, with bounded lateness.

    Design:
    - watermark = latest timestamp seen so far, minus max_lateness.
      Any window whose end <= watermark is safe to finalize -- no more
      records can legally arrive for it.
    - A record arriving for an ALREADY-finalized window is dropped
      (documented choice -- alternative is "reopen and re-emit",
      which is more correct but far more complex; state the tradeoff).
    """

    def __init__(self, window_size: int = 60, max_lateness: int = 5):
        self.window_size = window_size
        self.max_lateness = max_lateness
        self.sums = {}          # (window_start, group_id) -> running sum
        self.latest_ts_seen = float("-inf")
        self.finalized_windows = set()   # window_start values already emitted
        self.emitted = []       # (window_start, group_id, sum) for finalized windows

    def _window_start(self, ts: float) -> int:
        return int(ts // self.window_size) * self.window_size

    def _watermark(self) -> float:
        return self.latest_ts_seen - self.max_lateness

    def add_record(self, timestamp: float, group_id: str, value: float) -> None:
        self.latest_ts_seen = max(self.latest_ts_seen, timestamp)
        w_start = self._window_start(timestamp)

        # Boundary: a record for a window that's ALREADY finalized -> drop it.
        # (window is finalized once window_end <= watermark at time of check)
        if w_start in self.finalized_windows:
            return  # dropped late-arriving-after-finalization record

        key = (w_start, group_id)
        self.sums[key] = self.sums.get(key, 0) + value
        self._finalize_ready_windows()

    def _finalize_ready_windows(self) -> None:
        watermark = self._watermark()
        ready = {w_start for (w_start, _gid) in self.sums
                 if w_start + self.window_size <= watermark
                 and w_start not in self.finalized_windows}

        for w_start in sorted(ready):
            for (ws, gid), total in list(self.sums.items()):
                if ws == w_start:
                    self.emitted.append((ws, gid, total))
                    del self.sums[(ws, gid)]
            self.finalized_windows.add(w_start)

if __name__ == "__main__":
    agg = WindowedAggregator(window_size=60, max_lateness=5)

    agg.add_record(10, "g1", 5)      # window [0,60), sum=5
    agg.add_record(30, "g1", 3)      # same window, sum=8
    agg.add_record(65, "g1", 1)      # new window [60,120); watermark=65-5=60
                                    # window [0,60) ends at 60 <= watermark(60) -> finalize!
    assert (0, "g1", 8) in agg.emitted

    agg.add_record(59, "g1", 100)    # LATE for window [0,60) -> already finalized -> dropped
    assert not any(w == 0 for (w, _, _) in agg.emitted[1:])  # no re-emission

    # exactly-at-lateness-boundary record: should still count if window not yet finalized
    agg2 = WindowedAggregator(window_size=60, max_lateness=5)
    agg2.add_record(58, "g1", 1)
    agg2.add_record(62, "g1", 1)      # watermark = 62-5=57, window [0,60) end=60 > 57, NOT finalized yet
    agg2.add_record(59, "g1", 2)      # still accepted, window not finalized            