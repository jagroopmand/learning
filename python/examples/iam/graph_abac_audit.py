from collections import deque
import json

class AuditedIAMSystem:
    def __init__(self):
        self._graph = {}
        self._boolean_cache = {} # Only cache the simple boolean results
        
        # Rule Registry matching constraint keys to validation logic
        self._rule_registry = {
            "allowed_ip": lambda rule, ctx: ctx.get("client_ip") == rule,
            "requires_mfa": lambda rule, ctx: not rule or ctx.get("mfa_verified", False),
            "min_trust_score": lambda rule, ctx: ctx.get("trust_score", 0) >= rule
        }

    def add_relationship(self, source: str, destination: str, constraints: dict = None) -> None:
        self._boolean_cache.clear() # Clear cache on mutation
        if source not in self._graph: self._graph[source] = {}
        if destination not in self._graph: self._graph[destination] = {}
        self._graph[source][destination] = constraints or {}

    def evaluate_and_audit(self, user: str, resource: str, context: dict) -> dict:
        """
        Evaluates access and returns a comprehensive structured audit report.
        Tracks failures dynamically across transit and target nodes.
        """
        # Base structural integrity check
        if user not in self._graph or resource not in self._graph:
            return {
                "decision": "DENIED",
                "reason": "Invalid Identities",
                "details": f"Either user '{user}' or resource '{resource}' does not exist in the directory."
            }

        queue = deque([user])
        visited = {user}
        parent_map = {user: None}
        
        # Track the precise location where any path branches died due to constraints
        failed_policies = [] 

        while queue:
            current = queue.popleft()

            for neighbor, constraints in self._graph.get(current, {}).items():
                if neighbor not in visited:
                    
                    # Run dynamic validation loop
                    is_valid_hop = True
                    for rule_key, rule_value in constraints.items():
                        validator = self._rule_registry.get(rule_key)
                        
                        if validator is None or not validator(rule_value, context):
                            is_valid_hop = False
                            # Log metadata concerning the policy violation
                            failed_policies.append({
                                "source_node": current,
                                "blocked_node": neighbor,
                                "failed_rule": rule_key,
                                "required_value": rule_value,
                                "provided_value": context.get(rule_key) if rule_key != "allowed_ip" else context.get("client_ip")
                            })
                            break # Broken link, stop checking other rules for this neighbor
                    
                    if not is_valid_hop:
                        continue # Drop this branch of exploration
                    
                    # Secure Target Check
                    parent_map[neighbor] = current
                    if neighbor == resource:
                        return {
                            "decision": "GRANTED",
                            "reason": "Policy Traversal Successful",
                            "audit_path": self._reconstruct_path(parent_map, resource)
                        }

                    visited.add(neighbor)
                    queue.append(neighbor)

        # If the loop exhausts without hitting the target resource
        return {
            "decision": "DENIED",
            "reason": "Policy Constraint Violations or No Available Path",
            "evaluated_failures": failed_policies
        }

    def _reconstruct_path(self, parent_map: dict, target: str) -> list:
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parent_map[current]
        return path[::-1]


# ==========================================
# INTERVIEW TEST SUITE
# ==========================================
if __name__ == "__main__":
    iam = AuditedIAMSystem()

    # Build standard multi-tiered IAM architecture
    iam.add_relationship("alice@company.com", "Engineering_Group")
    
    # Transit node constraint: Corporate Network required to transition to Admin Role
    iam.add_relationship(
        "Engineering_Group", 
        "Production_Admin_Role", 
        constraints={"allowed_ip": "10.0.0.50"}
    )
    
    # Target node constraint: Terminal resource requires high device trust
    iam.add_relationship(
        "Production_Admin_Role", 
        "Financial_Database", 
        constraints={"min_trust_score": 90}
    )

    # --- Scenario 1: Access Denied at the Transit Layer ---
    outside_context = {
        "client_ip": "192.168.1.1", # Wrong IP address
        "trust_score": 95
    }
    
    print("=== SCENARIO 1: WRONG NETWORK LOCATION ===")
    report_1 = iam.evaluate_and_audit("alice@company.com", "Financial_Database", outside_context)
    print(json.dumps(report_1, indent=2))

    # --- Scenario 2: Access Denied at the Target Layer ---
    untrusted_device_context = {
        "client_ip": "10.0.0.50",  # Right IP address
        "trust_score": 45          # Wrong trust score (compromised laptop)
    }
    
    print("\n=== SCENARIO 2: COMPROMISED DEVICE LAYER ===")
    report_2 = iam.evaluate_and_audit("alice@company.com", "Financial_Database", untrusted_device_context)
    print(json.dumps(report_2, indent=2))

    # --- Scenario 3: Access Granted ---
    compliant_context = {
        "client_ip": "10.0.0.50",
        "trust_score": 98
    }
    
    print("\n=== SCENARIO 3: FULL COMPLIANCE ===")
    report_3 = iam.evaluate_and_audit("alice@company.com", "Financial_Database", compliant_context)
    print(json.dumps(report_3, indent=2))
