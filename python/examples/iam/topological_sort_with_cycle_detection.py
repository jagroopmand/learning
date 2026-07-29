from collections import deque
import logging
from pprint import pprint

#Dependency tree

class TopologicalSort:
    def __init__(self, data: list = None):
        self.logger = logging.getLogger(__name__)
        self._graph = {}
        self._in_degree = {}
        self._initialize(data)

    def _initialize(self, data: list):
        if not data:
            self.logger.warning("data is empty")
            return

        for src, dst in data:
            # Initialize nodes
            if src not in self._graph:
                self._graph[src] = []
                self._in_degree[src] = 0
            if dst not in self._graph:
                self._graph[dst] = []
                self._in_degree[dst] = 0

            self._graph[src].append(dst)
            self._in_degree[dst] += 1  # dst has one more dependency

    def get_sequence(self) -> list:
        # Seed queue with all zero in-degree nodes
        '''
        This creates a new deque object containing all nodes n from self._graph 
        whose in-degree is zero.
         
        The list comprehension 
        [[n for n in self._graph if self._in_degree[n] == 0]]
        iterates over every node in the graph and selects only
        those with no incoming edges.

        Using deque instead of a plain list makes the collection
        efficient for popping nodes from the left, which is a common
        operation in Kahn’s topological sort. queue therefore starts 
        as the initial frontier of nodes ready to be processed
          in the topological ordering.
        '''
        queue = deque([n for n in self._graph if self._in_degree[n] == 0])
        result = []

        while queue:
            node = queue.popleft()
            pprint(node)
            result.append(node)

            for neighbor in self._graph[node]:
                self._in_degree[neighbor] -= 1        # dependency satisfied
                if self._in_degree[neighbor] == 0:    # all deps met
                    queue.append(neighbor)

        # Cycle detection
        if len(result) != len(self._graph):
            self.logger.error("Cycle detected — topological sort impossible")
            return []

        return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    input_data = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("C", "D"),
        ("A", "E"),
        ("E", "F")
    ]

    sorter = TopologicalSort(input_data)
    pprint(sorter._graph)
    result = sorter.get_sequence()
    print("Topological order:", result)
    # Valid output: ['A', 'B', 'C', 'E', 'D', 'F'] or similar


'''
Boundary tests: empty graph, single node no edges, 
disconnected components, self-loop (cycle), duplicate edge.
'''    