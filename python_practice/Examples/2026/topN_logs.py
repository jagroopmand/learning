"""Compute the top N users by activity count inside a time window.

This script reads log lines in the form "epoch_ts,user,action" and counts
how many entries each user has within a half-open interval [start, end).
It then returns the top N users sorted first by descending count and second
by user ID lexicographically to make ranking deterministic when counts tie.
"""

from collections import Counter
import heapq

def top_n(lines, n, start, end):
    """Return the top N users by event count inside the given time window.

    Args:
        lines: An iterable of log lines, each formatted as 'epoch_ts,user,action'.
        n: Number of top users to return.
        start: Window start timestamp (inclusive).
        end: Window end timestamp (exclusive).
    """
    counts = Counter()
    for line in lines:
        line = line.strip()
        if not line:
            continue                      # skip empty or blank lines
        parts = line.split(",")
        if len(parts) != 3:
            continue                      # skip malformed lines without 3 fields
        try:
            ts = float(parts[0])
        except ValueError:
            continue                      # skip lines with invalid timestamps
        if start <= ts < end:             # half-open window: start inclusive, end exclusiveAjit32!

            # Why use Counter object.
            # __missing__ implementation that returns 0 for absent keys. 
            # That means later code can safely do counts[item] += 1 
            # without first checking whether item already exists.
            counts[parts[1]] += 1         # count one event for this user
    # Deterministic ranking: highest counts first, then user ID ascending
    return heapq.nsmallest(n, counts.items(),
                           # count = kv[1], user = kv[0], reverse
                           # negative value of kv[1] reverse the min heap sort order from smallest to largest
                           key=lambda kv: (-kv[1], kv[0]))


'''
### Boundary tests:
#  ts == start (in), ts == end (out), n larger than distinct users,
   tie between two users, empty input, all-malformed input.

### Seeded-bug drill: 
# Replace the window check with start <= ts <= end — double-counts records landing exactly on a window edge when windows are chained. This is precisely the class of bug the prior screen feedback pointed at.

'''