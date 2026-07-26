import bisect
from collections import defaultdict

class StreamingLogger:
    def __init__(self):
        # test_id → list of (timestamp, status) tuples
        self.logs = defaultdict(list)

    def log(self, test_id: str, timestamp: int, status: str) -> None:
        self.logs[test_id].append((timestamp, status))

    def get_most_recent(self, test_id: str) -> str:
        entries = self.logs.get(test_id)
        if not entries:
            return None
        return entries[-1][1]

    def get_status_since(self, test_id: str, timestamp: int) -> list:
        entries = self.logs.get(test_id)
        if not entries:
            return []
        
        # Extract timestamps for binary search
        timestamps = [e[0] for e in entries]
        
        # Find first index strictly after given timestamp
        index = bisect.bisect_right(timestamps, timestamp)
        
        # Return statuses from that index onward
        return [e[1] for e in entries[index:]]


# ==========================================
# TEST
# ==========================================
if __name__ == "__main__":
    logger = StreamingLogger()

    logger.log("test_1", 1, "pass")
    logger.log("test_2", 2, "fail")
    logger.log("test_1", 3, "pass")
    logger.log("test_1", 4, "fail")

    print(logger.get_most_recent("test_1"))        # fail
    print(logger.get_most_recent("test_2"))        # fail
    print(logger.get_most_recent("test_99"))       # None

    print(logger.get_status_since("test_1", 2))   # ['pass', 'fail']
    print(logger.get_status_since("test_1", 0))   # ['pass', 'pass', 'fail']
    print(logger.get_status_since("test_1", 4))   # []
    print(logger.get_status_since("test_99", 1))  # []