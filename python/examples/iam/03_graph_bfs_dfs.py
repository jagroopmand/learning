"""
GENERIC DSA GAP: plain graph traversal (BFS/DFS) — no domain flavor.
Your drills so far (topo sort, heaps) prove you can handle DAG ordering and
priority structures, but not necessarily "shortest hop count" or "is this
reachable" style questions, which are the most common generic-DSA fallback
if an interviewer abandons domain framing mid-interview.

PROMPT A: "Given a directed graph as an adjacency list, find the shortest
number of hops from node A to node B." (unweighted shortest path -> BFS)

PROMPT B: "Given the same graph, return all nodes reachable from A."
(connected component / reachability -> DFS or BFS, either works)
"""
from collections import deque


def shortest_hops(graph: dict, start, target) -> int:
    """BFS shortest path in an unweighted graph. Returns -1 if unreachable."""
    if start == target:
        return 0  # boundary: trivial self-path

    visited = {start}
    queue = deque([(start, 0)])

    while queue:
        node, dist = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor == target:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1  # boundary: target unreachable


def reachable_from(graph: dict, start) -> set:
    """DFS (iterative, to avoid recursion-depth issues on deep graphs)."""
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue  # boundary: avoid reprocessing / infinite loop on cycles
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                stack.append(neighbor)

    return visited


# --- self-verification pass ---
if __name__ == "__main__":
    g = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": ["E"],
        "E": [],
        "F": ["G"],   # disconnected component
        "G": [],
    }

    # Boundary 1: direct shortest path (multiple routes, same length)
    assert shortest_hops(g, "A", "D") == 2

    # Boundary 2: start == target
    assert shortest_hops(g, "A", "A") == 0

    # Boundary 3: unreachable node (disconnected component)
    assert shortest_hops(g, "A", "F") == -1

    # Boundary 4: node with no outgoing edges (leaf / sink)
    assert shortest_hops(g, "A", "E") == 3

    # Boundary 5: reachability from a node with a cycle (add one)
    g_cycle = {"X": ["Y"], "Y": ["Z"], "Z": ["X"]}  # cycle X->Y->Z->X
    assert reachable_from(g_cycle, "X") == {"X", "Y", "Z"}  # must terminate!

    # Boundary 6: reachability of an isolated node
    g_isolated = {"A": [], "B": ["A"]}
    assert reachable_from(g_isolated, "A") == {"A"}

    print("all boundary checks passed")
