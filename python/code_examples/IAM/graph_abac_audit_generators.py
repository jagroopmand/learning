class StreamingIAMSystem:
    def __init__(self):
        # Nested dictionary adjacency list: { source: { destination: constraints } }
        self._graph = {}
        
        # Rule registry matching constraint keys to validation logic
        self._rule_registry = {
            "allowed_ip": lambda rule, ctx: ctx.get("client_ip") == rule,
            "requires_mfa": lambda rule, ctx: not rule or ctx.get("mfa_verified", False),
            "min_trust_score": lambda rule, ctx: ctx.get("trust_score", 0) >= rule
        }

    def add_relationship(self, source: str, destination: str, constraints: dict = None) -> None:
        """Adds a directional permission link. O(1) time."""
        if source not in self._graph: self._graph[source] = {}
        if destination not in self._graph: self._graph[destination] = {}
        self._graph[source][destination] = constraints or {}

    def find_all_valid_paths(self, current_node: str, target: str, context: dict, visited=None, path=None):
        """
        A recursive generator that yields valid audit paths one by one.
        Uses a backtracking approach combined with strict ABAC rule evaluation.
        """
        # Initialize mutable tracking containers on the initial outer entry frame
        if visited is None: visited = set()
        if path is None: path = []

        # 1. Base Boundary Check
        if current_node not in self._graph:
            return

        # Append the current node to the tracking states
        path.append(current_node)
        visited.add(current_node)

        # 2. Base Target Case: If we reached the target resource, stream the path out!
        if current_node == target:
            yield list(path) # Yield a flat snapshot copy of the current successful path array
        else:
            # 3. Recursive Branch Explorations
            for neighbor, constraints in self._graph.get(current_node, {}).items():
                if neighbor not in visited:
                    
                    # --- DYNAMIC ABAC VERIFICATION ---
                    # Evaluate conditions BEFORE stepping into the next recursive frame
                    if not self._evaluate_constraints(constraints, context):
                        continue # Constraint failed! Skip this whole path branch entirely.

                    # Delegate stream handling to sub-generator frames via 'yield from'
                    yield from self.find_all_valid_paths(neighbor, target, context, visited, path)

        # 4. BACKTRACKING CLEANUP: Unwind the state tracking vectors as we pull out of the frame
        path.pop()
        visited.remove(current_node)

    def _evaluate_constraints(self, constraints: dict, context: dict) -> bool:
        if not constraints:
            return True
        for rule_key, rule_value in constraints.items():
            validator = self._rule_registry.get(rule_key)
            if validator is None or not validator(rule_value, context):
                return False
        return True


# ==========================================
# INTERVIEW TEST & SHOWCASE SUITE
# ==========================================
if __name__ == "__main__":
    iam = StreamingIAMSystem()

    # Scenario setup: Alice has multiple structural routes to reach the database
    # ROUTE 1: via Engineering Group -> Production Admin Role
    iam.add_relationship("alice@company.com", "Engineering_Group")
    iam.add_relationship("Engineering_Group", "Production_Admin_Role")
    iam.add_relationship("Production_Admin_Role", "Secure_Database", {"min_trust_score": 80})

    # ROUTE 2: via Backup Dev Group -> Emergency Read-Only Role
    iam.add_relationship("alice@company.com", "Backup_Dev_Group")
    iam.add_relationship("Backup_Dev_Group", "Emergency_Role")
    iam.add_relationship("Emergency_Role", "Secure_Database", {"min_trust_score": 80})
    
    # ROUTE 3: Malicious path blocked by network constraints
    iam.add_relationship("alice@company.com", "Hacked_Transit_Node")
    iam.add_relationship("Hacked_Transit_Node", "Secure_Database", {"allowed_ip": "10.0.0.1"})

    # Active Request Context (Valid trust score, but wrong IP for Route 3)
    runtime_context = {
        "client_ip": "192.168.1.10",
        "trust_score": 95
    }

    print("--- Case A: Streaming EVERY Valid Path to the Resource ---")
    path_generator = iam.find_all_valid_paths("alice@company.com", "Secure_Database", runtime_context)
    
    # The graph evaluates lazily as we loop over the generator object
    for index, verified_path in enumerate(path_generator, start=1):
        print(f"Path Option #{index}: {' -> '.join(verified_path)}")


    print("\n--- Case B: Short-Circuit Optimization (Get ONLY the first path) ---")
    another_generator = iam.find_all_valid_paths("alice@company.com", "Secure_Database", runtime_context)
    
    try:
        # Python's built-in next() function grabs the very first stream entry
        first_path = next(another_generator)
        print(f"First available authorization trail found:\n{' -> '.join(first_path)}")
        # Because we stop here, the rest of the graph is NEVER traversed or computed!
    except StopIteration:
        print("No valid paths exist for this authorization configuration.")
