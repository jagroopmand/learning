# input: [(),()]
from pprint import pprint
from collections import deque

class TopoSort:

    def __init__(self, data:list):
        self.graph = {}
        self.in_degree = {}
        self.initialize(data)

    def initialize(self, data: list) :
        if not data:
            return
        for src, dst in data:
            if src not in self.graph:
                self.graph[src] = []
                self.in_degree[src] = 0
            if dst not in self.graph:
                self.graph[dst] = []
                self.in_degree[dst] = 0

            self.graph[src].append(dst)
            self.in_degree[dst] += 1     

    def sort(self) -> list:
       queue = deque([n for n in self.graph if self.in_degree[n] == 0 ])
       result = []

       while queue:
           node = queue.popleft()
           pprint(node)
           result.append(node)

           for neighbor in self.graph[node]:
               self.in_degree[neighbor] -= 1
               if self.in_degree[neighbor] == 0:
                   queue.append(neighbor)


        # cycle detection
       if len(result) != len(self.graph):
           print("cycle/circular-dependency detected, sort impossible")  
           return []         

       return result


if __name__ == "__main__":
     
     data = [ ("a","b"), ("a","c"), ("a", "e"),("b","d"), ("c","e"), ("e", "f")]

     obj  = TopoSort(data)
     pprint(obj.graph)
     pprint(obj.sort())