import time
from collections import deque, defaultdict

class RateLimiter:
    """Allow at most `limit` requests per `window_seconds` seconds, per key."""
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window_seconds = window_seconds
        self.hits_by_key = defaultdict(deque)   # key -> deque of timestamps

    def allow(self, key: str, now: float = None) -> bool:
        now = time.monotonic() if now is None else now
        # If this key has never been seen before, allow the first request
        # and record its timestamp.
        if key not in self.hits_by_key:
            timestamps = self.hits_by_key[key]
            timestamps.append(now)
            return True
        timestamps = self.hits_by_key[key]
        # Evict timestamps OUTSIDE the window.
        # Boundary decision: a hit at exactly (now - window_seconds) is
        # OUT of the window -> use <= for eviction.
        while timestamps and timestamps[0] <= now - self.window_seconds:
            timestamps.popleft()
        # If the number of hits still inside the sliding window is below the
        # configured limit, record the current hit and allow the request.
        # Otherwise the request is rejected because the caller has exceeded
        # the allowed request rate for this key.
        if len(timestamps) < self.limit:
            timestamps.append(now)
            return True
        return False


'''
### Boundary tests to run aloud:
(1) limit-th request in window → allowed;
(2) (limit+1)-th → denied;
(3) request at exactly now = first_hit + window_seconds → first hit evicted, request allowed;
(4) two keys do not interfere;
(5) limit=0.

### Seeded-bug drill:
# change eviction to timestamps[0] < now - self.window_seconds. Effect: a hit exactly at the window edge is retained
  one call too long → the limiter denies a request it should allow.
# Practice spotting this in under 2 minutes.
'''
