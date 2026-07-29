from collections import OrderedDict
import time
class LRUCache:

    def __init__(self,cache_size: int=3):
        self.cache_size = cache_size
        self.lru_cache= OrderedDict()


    def put(self, key:str, val: str, ttl: float, now: float):
        now = time.monotonic() if now is None else now


        #case 1: key exists, update key ttl
        if key in self.lru_cache:
            _, expiry_time = self.lru_cache[key]
            new_expiry = now + ttl
            self.lru_cache[key] = (val, new_expiry)
            self.lru_cache.move_to_end(key)

        #case 2: new key, check cache size and evict LRU if cache full
        if len(self.lru_cache) >= self.cache_size:
            # evict LRU
            self.lru_cache.popitem(last=False)
        
        self.lru_cache[key] = (val,now+ttl)

           