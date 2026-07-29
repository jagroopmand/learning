import time
from collections import deque, defaultdict

class RateLimiter:

    def __init__(self, window_size: int=5, rate_limit: int = 2):
        self.rate_limit=rate_limit
        self.window_size= window_size
        self.hits_count_client = defaultdict(deque)


    def get_hits(self, clientid:str) -> deque:
        return self.hits_count_client[clientid]
    
    def allow(self, clientid: int, now: float = None) -> bool:
        now = time.monotonic() if now is None else now  

        timestamps = self.hits_count_client[clientid]

        while timestamps and timestamps[0] <= now - self.window_size:
            timestamps.popleft()
        
        if len(timestamps) < self.rate_limit:
            timestamps.append(now)
            return True
        
        return False
    



if __name__ == "__main__":
    obj = RateLimiter(4, 3)

    assert obj.allow("a", 4) is True
    assert obj.allow("a", 3) is True
    assert obj.allow("a", 2) is True
    for hit in obj.get_hits("a"):
        print("hit1: " , hit)    
    
    assert obj.allow("a", 6) is False
    for hit in obj.get_hits("a"):
        print("hit2: " , hit)    


    assert obj.allow("a", 11) is True
    for hit in obj.get_hits("a"):
        print("hit3: " , hit)   