from collections import OrderedDict
import time
from pprint import pprint

class LRUCacheTTL:

    def __init__(self):
        self.cache_size = 3
        self.cache = OrderedDict()


    def update(self, key:str, val:str,  ttl:float, now: float=None):
        time_now = time.monotonic() if now is None else now
        new_ttl = time_now + ttl
        if key in self.cache:
            self.cache[key] = (val,  new_ttl)
            self.cache.move_to_end(key)

        else:
            if len(self.cache) >= self.cache_size:
                self.cache.popitem(last=False)

            self.cache[key] = (val, new_ttl) 

                   




    def get_key(self, key: str) -> tuple:
        if key in self.cache:
          return self.cache.get(key)
        else:
            return ()



if __name__ == "__main__":

    obj = LRUCacheTTL()

    #New Key
    obj.update("k1", "v1", 3)
    pprint(obj.cache)
     
    #update existing key 
    obj.update("k1", "v12", 3)
    pprint(obj.cache)

    #New Key
    obj.update("k2", "v2", 3)
    pprint(obj.cache)

    #New Key
    obj.update("k3", "v3", 3)
    pprint(obj.cache)

    #New Key, should pop LRU
    obj.update("k4", "v4", 3)
    pprint(obj.cache)