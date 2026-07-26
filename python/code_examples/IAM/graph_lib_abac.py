from collections import deque
import rich

class DynamicABAC_IAM:
    def __init__(self, validation_relationships=None):
        self._graph = {}
        self._cache = {}
        
        # --- THE DYNAMIC DISPATCHER MAP ---
        # Maps a constraint token to a validation function.
        # Each function takes (constraint_value, runtime_context) and returns a boolean.
        self._rule_registry = {
            "allowed_ip": lambda rule_val, ctx: ctx.get("client_ip") == rule_val,
            "requires_mfa": lambda rule_val, ctx: not rule_val or ctx.get("mfa_verified", False),
            "required_env": lambda rule_val, ctx: ctx.get("environment") == rule_val,
            "min_trust_score": lambda rule_val, ctx: ctx.get("device_trust_score", 0) >= rule_val
        }
        
        if validation_relationships:
            for source, destination, *constraints in validation_relationships:
                edge_rules = constraints if constraints else {}
                self.add_relationship(source, destination, edge_rules)

    def _invalidate_cache(self):
        self._cache.clear()

    def add_relationship(self, source: str, destination: str, constraints: dict = None) -> None:
        self._invalidate_cache()
        if source not in self._graph: self._graph[source] = {}
        if destination not in self._graph: self._graph[destination] = {}
        self._graph[source][destination] = constraints or {}
        rich.print(f"✅ Added relationship: {source} -> {destination} with constraints: {constraints or 'None'}")
        rich.print(f"Current Graph State: {self._graph}")

    def check_access(self, user: str, resource: str, context: dict) -> bool:
        cache_key = (user, resource)
        if cache_key in self._cache:
            return self._cache[cache_key]

        if user not in self._graph or resource not in self._graph:
            return False

        # Secure Self-Evaluation Gate utilizing the dynamic engine
        if user == resource:
            self_constraints = self._graph[user].get(user, {})
            return self._evaluate_constraints(self_constraints, context)

        queue = deque([user])
        visited = {user}
        has_any_constraints_checked = False

        while queue:
            current = queue.popleft()

            for neighbor, constraints in self._graph.get(current, {}).items():
                if neighbor not in visited:
                    
                    if constraints:
                        has_any_constraints_checked = True
                    
                    # Run dynamic multi-rule validation
                    if not self._evaluate_constraints(constraints, context):
                        continue 
                    
                    if neighbor == resource:
                        if not has_any_constraints_checked:
                            self._cache[cache_key] = True
                        return True
                        
                    visited.add(neighbor)
                    queue.append(neighbor)

        if not has_any_constraints_checked:
            self._cache[cache_key] = False
        return False

    # ==========================================
    # DECOUPLED DYNAMIC CONSTRAINT ENGINE
    # ==========================================
    def _evaluate_constraints(self, constraints: dict, context: dict) -> bool:
        """
        Dynamically loops over all rules assigned to an edge.
        Fails closed (returns False) if any rule is unsupported or unfulfilled.
        """
        # Open by default if no policy constraints exist on this link
        if not constraints:
            return True

        # Loop over every policy rule attached to the edge link
        for rule_key, rule_value in constraints.items():
            
            # Fetch the matching evaluation logic from our registry
            validator = self._rule_registry.get(rule_key)
            
            # Security Hardening: Fail-Closed if an admin configures an unknown rule key
            if validator is None:
                print(f"⚠️ SECURITY ALERT: Unknown constraint rule '{rule_key}'. Blocking path.")
                return False
                
            # Execute the registry lambda against the current active context
            if not validator(rule_value, context):
                return False # Single rule failure breaks the whole loop (AND logic)

        return True # All registered rules successfully passed evaluation


# ==========================================
# INTERVIEW TEST SUITE
# ==========================================
if __name__ == "__main__":
    iam = DynamicABAC_IAM()

    # Define a complex edge with multiple, disparate dynamic rules
    # It must match the client IP AND ensure device trust score is high enough
    strict_rules = {
        "allowed_ip": "10.0.0.99",
        "min_trust_score": 85,
        "requires_mfa": True
    }
    
    iam.add_relationship("alice@company.com", "Secure_Shell_Access", strict_rules)

    # Context A: Passes IP and MFA, but device is unpatched/untrusted
    compromised_context = {
        "client_ip": "10.0.0.99",
        "mfa_verified": True,
        "device_trust_score": 40 # Too low!
    }
    
    print("Test 1 (Low Trust Score):", iam.check_access("alice@company.com", "Secure_Shell_Access", compromised_context))
    # Expected: False

    # Context B: All values successfully map and evaluate
    perfect_context = {
        "client_ip": "10.0.0.99",
        "mfa_verified": True,
        "device_trust_score": 95 # Secure!
    }
    
    print("Test 2 (Full Compliance):", iam.check_access("alice@company.com", "Secure_Shell_Access", perfect_context))
    # Expected: True
