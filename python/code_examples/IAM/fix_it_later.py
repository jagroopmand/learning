from typing_extensions import runtime_checkable
from collections import deque 
import json


class PRGraph:
    def __init__(self, relationships ={}):
        self._graph = {}
        self.initialize(relationships)
        

    def initialize(self, relationships: dict):
        for data in relationships:
            # print("data:: ", data)
            src = data["relationship"][0]
            # print("src:: " + src)

            dst = data["relationship"][1]
            # print("dst:: " + dst)

            constraints =  data["constraints"] if "constraints" in data else {}
            # print("constraints:: " + str(len(constraints)))

            permissions =  data["permissions"] if "permissions" in data else {}
            # print("permissions:: " + str(len(permissions)))

            self.add(src, dst, constraints, permissions)

    def add(self, src: str, dst: str, permissions: dict = {}, constraints: dict = {}) -> None:
        if src not in self._graph: self._graph[src] = {}
        if dst not in self._graph: self._graph[dst] = {}
        # print("graph: " , self._graph)
        self._graph[src][dst] = {}
        self._graph[src][dst]["constraints"] = constraints
        self._graph[src][dst]["permissions"] = permissions
        # print("graph: " , self._graph)

        


    def remove(self, node: str):
        if node in self._graph: del self._graph[node]
        

    def check_access(self, src: str, dst: str, context: dict = {}, requested_permissoins: dict={} ) -> bool:
        visited = {src}
        iteration_queue = deque([src])
        access_granted = False

        while iteration_queue: 
            current_node = iteration_queue.popleft()
            
            if current_node == dst:
                if self.check_contraints(context) and self.check_permission(requested_permissoins):
                    access_granted = True
                

            for neighbor in iteration_queue: 
                if neighbor not in visited:
                    visited.add(neighbor)

        return access_granted             

    
    def check_contraints(self, context: dict ={}) -> bool:
        return False           
        
    def check_permission(self, requested_permissoins: dict={}) -> bool:
        return False

    

if __name__ == "__main__":
    iam_graph_data = [
        {"relationship" : ("tech", "junior_engineer")},
        {"relationship" : ("tech", "senior_engineer")},
        {"relationship" : ("tech", "architect")},
        {"relationship" : ("senior_engineer", "engineer")},
        {"relationship" : ("engineer", "contractor")},
        {"relationship" : ("engineer", "contractor")},
        {"relationship" : ( "engineer", "resourceA"), "constraints" : { "min_trust_score": 85,"requires_mfa": True}, "permissions" : ("R")},
        {"relationship" : ("engineer", "resourceB"), "constraints" : { "min_trust_score": 85,"requires_mfa": True}, "permissions" : ("R", "W")}
    ]
    

    graph_obj = PRGraph(iam_graph_data)
    print("======================")
    print(graph_obj._graph)
    print("======================")

    allowed = graph_obj.check_access("a", "b", {}, {})
    print(f"allowed: ",  allowed)