import time


class _Node:
    __slots__ = ("key", "value", "expiry", "prev", "next")

    def __init__(self, key, value, expiry):
        self.key = key
        self.value = value
        self.expiry = expiry
        self.prev = None
        self.next = None


class LRUCacheWithTTL:
    """
    Primitive implementation: doubly linked list + hashmap, no OrderedDict.

    List orientation:
        head.next  = most recently used
        tail.prev  = least recently used
    Sentinel head/tail nodes avoid null-checks at the boundaries.
    """

    def __init__(self, capacity: int, refresh_ttl_on_update: bool = False):
        self.capacity = capacity
        self.refresh_ttl_on_update = refresh_ttl_on_update
        self.map = {}  # key -> _Node

        # Sentinels
        self.head = _Node(None, None, None)
        self.tail = _Node(None, None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    # ---- internal list operations, all O(1) ----

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node: _Node) -> None:
        # front == most recently used, right after head sentinel
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._insert_at_front(node)

    def _is_expired(self, node: _Node, now: float) -> bool:
        return now >= node.expiry  # exp == now -> expired

    # ---- public API ----

    def get(self, key: str, now: float = None) -> object:
        now = time.monotonic() if now is None else now

        node = self.map.get(key)
        if node is None:
            return None

        if self._is_expired(node, now):
            # Expired -> evict fully, do not touch ordering
            self._remove(node)
            del self.map[key]
            return None

        self._move_to_front(node)
        return node.value

    def put(self, key: str, value: object, ttl_seconds: float, now: float = None) -> None:
        now = time.monotonic() if now is None else now

        if self.capacity == 0:
            return  # structurally no room, no-op

        existing = self.map.get(key)
        if existing is not None:
            existing.value = value
            if self.refresh_ttl_on_update:
                existing.expiry = now + ttl_seconds
            self._move_to_front(existing)
            return

        if len(self.map) >= self.capacity:
            lru_node = self.tail.prev          # least recently used
            self._remove(lru_node)
            del self.map[lru_node.key]

        new_node = _Node(key, value, now + ttl_seconds)
        self.map[key] = new_node
        self._insert_at_front(new_node)