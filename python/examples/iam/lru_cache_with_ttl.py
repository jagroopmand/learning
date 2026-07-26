from collections import OrderedDict
import time


class LRUCacheWithTTL:
    """
    LRU cache with per-key TTL.

    Design decisions (state these out loud in an interview):
    - capacity == 0 -> every put is a no-op, nothing is ever stored.
    - A `get` on an expired key evicts it and returns None; does NOT
      count as a "use" for LRU ordering (nothing to move).
    - refresh_ttl_on_update controls whether `put` on an existing key
      resets its TTL clock. Configurable rather than hardcoded, since
      it's a genuine tradeoff (audit-stability vs. staleness risk).
    """

    def __init__(self, capacity: int, refresh_ttl_on_update: bool = False):
        self.capacity = capacity
        self.refresh_ttl_on_update = refresh_ttl_on_update
        # OrderedDict preserves insertion order; we move_to_end() on
        # access to keep "most recently used" at the end.
        self.cache: OrderedDict[str, tuple] = OrderedDict()  # key -> (value, expiry_time)

    def _is_expired(self, expiry_time: float, now: float) -> bool:
        # Boundary decision: exp == now is EXPIRED (>=), not valid.
        # State this explicitly if asked.
        return now >= expiry_time

    def get(self, key: str, now: float = None) -> object:
        now = time.monotonic() if now is None else now

        if key not in self.cache:
            return None

        value, expiry_time = self.cache[key]

        if self._is_expired(expiry_time, now):
            # Expired -> evict, do NOT touch LRU order (nothing to promote)
            del self.cache[key]
            return None

        # Valid hit -> this key becomes most recently used
        self.cache.move_to_end(key)
        return value

    def put(self, key: str, value: object, ttl_seconds: float, now: float = None) -> None:
        now = time.monotonic() if now is None else now

        # Boundary: capacity 0 -> structurally no room, no-op.
        if self.capacity == 0:
            return

        if key in self.cache:
            _, old_expiry = self.cache[key]
            new_expiry = (now + ttl_seconds) if self.refresh_ttl_on_update else old_expiry
            self.cache[key] = (value, new_expiry)
             # new key always gets added at the end which is most recently used(MRU) item 
            self.cache.move_to_end(key)
            return

        # New key: evict LRU if at capacity BEFORE inserting
        if len(self.cache) >= self.capacity:
            # pop oldest from front i.e. least recently used(LRU)
            self.cache.popitem(last=False)  

        self.cache[key] = (value, now + ttl_seconds)




if __name__ == "__main__":
    c = LRUCacheWithTTL(capacity=2)

    c.put("a", 1, ttl_seconds=10, now=0)
    c.put("b", 2, ttl_seconds=10, now=1)
    assert c.get("a", now=2) == 1          # "a" is now MRU
    c.put("c", 3, ttl_seconds=10, now=3)   # over capacity -> evict LRU
    assert c.get("b", now=4) is None       # "b" was evicted, not "a"
    assert c.get("a", now=4) == 1
    assert c.get("c", now=4) == 3

    # expiry boundary: exp == now
    c.put("d", 4, ttl_seconds=5, now=0)
    assert c.get("d", now=5) is None       # expired exactly at now == exp
    print("dsdsdsdsdsds>>>>>:",  c.get("d", now=4.999))
    assert c.get("d", now=4.999) == 4      # one tick before, still valid

    # capacity 0
    zero = LRUCacheWithTTL(capacity=0)
    zero.put("x", 1, ttl_seconds=10, now=0)
    assert zero.get("x", now=0) is None    # never stored        