from collections import deque
import rich

class IAMSystem:
    def __init__(self, validation_relationships=None):
        """
        Initializes a sparse IAM graph using an adjacency list.
         Accepts an optional list of (source, destination) tuples to batch initialize data.
        """
        self._graph = {}

        # Cache for fast access lookups: Map of (user, resource) -> bool
        self._access_cache = {}
        
        if validation_relationships:
            for source, destination in validation_relationships:
                self.add_relationship(source, destination)

     # ==========================================
    # INTERNAL CACHE MANAGEMENT UTILITIES
    # ==========================================
    
    def _invalidate_cache(self) -> None:
        """
        Clears the authorization cache completely when the graph mutates.
        Essential for security compliance to prevent stale access permissions.
        """
        self._access_cache.clear()

    # ==========================================
    # 1. GRAPH INITIALIZATION & MUTATION UTILITIES
    # ==========================================

    def add_relationship(self, source: str, destination: str, constraints: dict = None) -> None:
        """Adds a directional permission or assignment link. O(1) time."""

        """Adds a directional permission link. Triggers cache invalidation. O(1)."""
        self._invalidate_cache() # Evict cache instantly on change

        if source not in self._graph:
            self._graph[source] = set()
        if destination not in self._graph:
            self._graph[destination] = set()
        self._graph[source].add(destination)

    def remove_identity(self, target_node: str) -> None:
        """
        Completely purges a user, group, or resource from the IAM system.
        Ensures no orphaned references or security leaks remain. O(V + E) time.
        """

        self._invalidate_cache() # Evict cache instantly on revocation

        # Remove the node and all its outgoing connections
        if target_node in self._graph:
            del self._graph[target_node]
            
        # Clean up all incoming connections pointing to this node
        for source_node, connections in self._graph.items():
            connections.discard(target_node)

    # ==========================================
    # 2. AUDIT & ACCESS EVALUATION UTILITIES
    # ==========================================

    def check_access(self, user: str, resource: str) -> bool:
        """
        High-performance Boolean check for fast real-time authorization.
        Terminates the moment a valid path is found. O(V + E) time.
        """
        """
        Boolean check for fast real-time authorization.
        O(1) on a cache hit; O(V + E) on a cache miss.
        """

        # 1. Check the cache first
        cache_key = (user, resource)
        if cache_key in self._access_cache:
            print(f"⚡ >>>>>>>>>>> [CACHE HIT] Evaluated access for {user} -> {resource}")
            return self._access_cache[cache_key]

        print(f"🔍 >>>>>>>>>>> [CACHE MISS] Computing graph path for {user} -> {resource}")
        
        # 2. Graph Boundary Check
        if user not in self._graph or resource not in self._graph:
            self._access_cache[cache_key] = False
            return False

        if user not in self._graph or resource not in self._graph:
            return False
            
        queue = deque([user])
        rich.print ("queue: ", queue)
        visited = {user}
        print ("visited: ", visited)

        while queue:
            print ("============== node ===================================")
            rich.print ("graph node iteration - queue before pop: ", queue)
            current = queue.popleft()
            print ("current graph node: ", current)
            
            # Early evaluation optimization
            if current == resource:
                print ("Found resource: ", current)
                print ("Path exists from user to resource.")
                print ("visited: ", visited)
                access_granted = True
                self._access_cache[(user, resource)] = True
                return True
                
            for neighbor in self._graph.get(current, []):
                print("------------------ neighbor -------------------------------")
                print ("neighbor: ", neighbor)
                if neighbor not in visited:
                    print ("adding neighbor to visited: ", neighbor)
                    visited.add(neighbor)
                    # print ("visited: ", visited)
                    # print ("appending neighbor to queue of nodes to iterate over: ", neighbor)
                    # rich.print ("queue before append: ", queue)
                    queue.append(neighbor)
                    rich.print ("queue after append: ", queue)
                else:
                    print ("neighbor already visited: ", neighbor)  
        print ("No path found from user to resource.")            
        self._access_cache[(user, resource)] = False
        return False

    def find_shortest_audit_path(self, user: str, resource: str) -> list:
        """
        Traces and returns the exact shortest chain of assignment for compliance auditing.
        Returns a list of strings representing the path, or None if no access exists.
        """
        if user not in self._graph or resource not in self._graph:
            return None

        queue = deque([user])
        visited = {user}
        parent_map = {user: None} # Tracks back links cleanly without slicing lists

        while queue:
            current = queue.popleft()

            if current == resource:
                return self._reconstruct_path(parent_map, resource)

            for neighbor in self._graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent_map[neighbor] = current
                    queue.append(neighbor)
        return None

    def _reconstruct_path(self, parent_map: dict, target: str) -> list:
        """Helper to trace backwards from target to source. O(V) time."""
        path = []
        current = target
        print ("parent_map: ", parent_map)
        print ("current/target: ", current)

        while current is not None:
            print("==================================================")
            print ("current node: ", current)
            path.append(current)
            print ("path: ", path)
            current = parent_map[current]
        print ("Final path before reverse: ", path)
        return path[::-1] # Reverse path to get correct User -> Resource order


# ==========================================
# INTERVIEW TEST SUITE
# ==========================================
if __name__ == "__main__":
    # Input data mimicking a database payload or config file
    enterprise_iam_data = [
        # Route A: Long inheritance path
        ("alice@company.com", "General_Staff_Group"),
        ("General_Staff_Group", "IT_Support_Group"),
        ("IT_Support_Group", "Emergency_Admin_Role"),
        ("Emergency_Admin_Role", "Production_Database"),
        
        # Route B: Shorter path to the same resource
        ("alice@company.com", "BreakGlass_Admin_Role"),
        ("BreakGlass_Admin_Role", "Production_Database"),
        
        # Unrelated route
        ("bob@company.com", "Finance_Group"),
        ("Finance_Group", "Stripe_Dashboard"),
        
        # Circular Loop to test algorithm safety
        ("IT_Support_Group", "General_Staff_Group")
    ]

    rich.print("--- Step 1: Initializing Graph from Batch Data ---")
    iam = IAMSystem(validation_relationships=enterprise_iam_data)
    # rich.print("Graph initialized with nodes:", list(iam._graph.keys()))
    rich.print ("Graph structure:" , iam._graph)
    # for node, edges in iam._graph.items():
    #     print(f"  {node} -> {edges}")

    print("\n--- Step 2: Testing Real-time Authorization Checks ---")
    # check from graph
    print(f"Alice access to DB?   -> {iam.check_access('alice@company.com', 'Production_Database')}") # True
    # check from cache
    print(f"Alice access to DB?   -> {iam.check_access('alice@company.com', 'Production_Database')}") # True
    # print(f"Alice access to Stripe? -> {iam.check_access('alice@company.com', 'Stripe_Dashboard')}")     # False

    print("\n--- Step 3: Testing Audit Shortest Path (BFS Proof) ---")
    # This must skip the 4-step route and find the 2-step route via BreakGlass
    audit_trail = iam.find_shortest_audit_path("alice@company.com", "Production_Database")
    print(f"Shortest Audit Trail:\n{' -> '.join(audit_trail)}")

    print("\n--- Step 4: Testing Identity Revocation Utility ---")
    # Revoking the role that granted the short path
    # print("Revoking 'BreakGlass_Admin_Role' from system...")
    # iam.remove_identity("BreakGlass_Admin_Role")

    print("\n--- Step 5: Re-Evaluating Post-Revocation ---")
    # Alice should still have access, but her shortest path must dynamically switch to Route A
    # print(f"Alice access to DB still valid? -> {iam.check_access('alice@company.com', 'Production_Database')}")
    
    # new_audit_trail = iam.find_shortest_audit_path("alice@company.com", "Production_Database")
    # print(f"New Shortest Audit Trail:\n{' -> '.join(new_audit_trail)}")
