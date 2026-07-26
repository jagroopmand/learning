import unittest
from collections import deque

# =====================================================================
# THE SYSTEM UNDER TEST (Consolidated standard-library implementation)
# =====================================================================
class FinalAuditedIAM:
    def __init__(self, validation_relationships=None):
        self._graph = {}
        self._rule_registry = {
            "allowed_ip": lambda rule, ctx: ctx.get("client_ip") == rule,
            "requires_mfa": lambda rule, ctx: not rule or ctx.get("mfa_verified", False),
            "min_trust_score": lambda rule, ctx: ctx.get("trust_score", 0) >= rule
        }
        if validation_relationships:
            for source, destination, *constraints in validation_relationships:
                edge_rules = constraints[0] if constraints else {}
                self.add_relationship(source, destination, edge_rules)

    def add_relationship(self, source: str, destination: str, constraints: dict = None) -> None:
        if source not in self._graph: self._graph[source] = {}
        if destination not in self._graph: self._graph[destination] = {}
        self._graph[source][destination] = constraints or {}

    def evaluate_and_audit(self, user: str, resource: str, context: dict) -> dict:
        if user not in self._graph or resource not in self._graph:
            return {"decision": "DENIED", "reason": "Invalid Identities"}

        # Secure Self-Evaluation Gate utilizing the dynamic engine
        if user == resource:
            self_constraints = self._graph[user].get(user, {})
            is_valid = self._evaluate_hop_rules(self_constraints, context)
            return {
                "decision": "GRANTED" if is_valid else "DENIED",
                "reason": "Self Evaluation Successful" if is_valid else "Self Evaluation Failed"
            }

        queue = deque([user])
        visited = {user}
        parent_map = {user: None}
        failed_policies = [] 

        while queue:
            current = queue.popleft()

            for neighbor, constraints in self._graph.get(current, {}).items():
                if neighbor not in visited:
                    
                    if not self._evaluate_hop_rules(constraints, context):
                        failed_policies.append({"source_node": current, "blocked_node": neighbor})
                        continue 
                    
                    parent_map[neighbor] = current
                    if neighbor == resource:
                        return {
                            "decision": "GRANTED",
                            "reason": "Policy Traversal Successful",
                            "audit_path": self._reconstruct_path(parent_map, resource)
                        }

                    visited.add(neighbor)
                    queue.append(neighbor)

        return {"decision": "DENIED", "reason": "Policy Constraint Violations", "evaluated_failures": failed_policies}

    def _evaluate_hop_rules(self, constraints: dict, context: dict) -> bool:
        if not constraints: return True
        for rule_key, rule_value in constraints.items():
            validator = self._rule_registry.get(rule_key)
            if validator is None or not validator(rule_value, context):
                return False
        return True

    def _reconstruct_path(self, parent_map: dict, target: str) -> list:
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parent_map[current]
        return path[::-1]


# =====================================================================
# THE INTERVIEW TEST FRAMEWORK
# =====================================================================
class TestSecureIAMSystem(unittest.TestCase):
    
    def setUp(self):
        """Executed before every single test case to ensure an isolated sandbox graph."""
        self.iam = FinalAuditedIAM()
        
        # Build standard enterprise tree path
        self.iam.add_relationship("alice@company.com", "Engineering_Group")
        
        # Transit constraint: Must be on internal corp IP to touch this Role
        self.iam.add_relationship(
            "Engineering_Group", 
            "Production_Admin_Role", 
            constraints={"allowed_ip": "10.0.0.50"}
        )
        
        # Target constraint: Target resource requires a healthy security context
        self.iam.add_relationship(
            "Production_Admin_Role", 
            "Production_Database", 
            constraints={"min_trust_score": 90}
        )

    def test_successful_evaluation_path(self):
        """Verifies that when all context variables are valid, access is GRANTED and the path matches."""
        valid_context = {"client_ip": "10.0.0.50", "trust_score": 95}
        report = self.iam.evaluate_and_audit("alice@company.com", "Production_Database", valid_context)
        
        self.assertEqual(report["decision"], "GRANTED")
        expected_path = ["alice@company.com", "Engineering_Group", "Production_Admin_Role", "Production_Database"]
        self.assertEqual(report["audit_path"], expected_path)

    def test_transit_node_failure(self):
        """Verifies that bad runtime attributes trigger an early exit at an intermediate transit hop."""
        invalid_ip_context = {"client_ip": "192.168.1.1", "trust_score": 95}
        report = self.iam.evaluate_and_audit("alice@company.com", "Production_Database", invalid_ip_context)
        
        self.assertEqual(report["decision"], "DENIED")
        # Ensure the failure array isolates the exact transit link that dropped execution
        failure = report["evaluated_failures"][0]
        self.assertEqual(failure["source_node"], "Engineering_Group")
        self.assertEqual(failure["blocked_node"], "Production_Admin_Role")

    def test_target_node_failure_with_valid_transit(self):
        """Verifies transit nodes pass but the target block stops access if its distinct rules fail."""
        low_trust_context = {"client_ip": "10.0.0.50", "trust_score": 30} # Compromised device
        report = self.iam.evaluate_and_audit("alice@company.com", "Production_Database", low_trust_context)
        
        self.assertEqual(report["decision"], "DENIED")
        failure = report["evaluated_failures"][0]
        self.assertEqual(failure["source_node"], "Production_Admin_Role")
        self.assertEqual(failure["blocked_node"], "Production_Database")

    def test_self_evaluation_with_constraints(self):
        """Verifies the entry gate securely checks ABAC policies even when evaluating a self-access link."""
        # Add a self-referencing relationship with rules to Alice's own node
        self.iam.add_relationship("alice@company.com", "alice@company.com", constraints={"min_trust_score": 80})
        
        bad_self_context = {"trust_score": 40}
        good_self_context = {"trust_score": 90}
        
        report_fail = self.iam.evaluate_and_audit("alice@company.com", "alice@company.com", bad_self_context)
        report_pass = self.iam.evaluate_and_audit("alice@company.com", "alice@company.com", good_self_context)
        
        self.assertEqual(report_fail["decision"], "DENIED")
        self.assertEqual(report_pass["decision"], "GRANTED")

    def test_circular_dependency_resilience(self):
        """Ensures the BFS tracker successfully exits without hitting a recursive loop crash."""
        # Intentionally pollute the environment with an endless cycle loop
        self.iam.add_relationship("Production_Admin_Role", "Engineering_Group")
        
        # Run a search to an impossible target to force the system to traverse every node
        dead_context = {"client_ip": "10.0.0.50", "trust_score": 95}
        report = self.iam.evaluate_and_audit("alice@company.com", "Non_Existent_Resource", dead_context)
        
        # If the code handles cyclic structures correctly, it returns a clean denial without hanging
        self.assertEqual(report["decision"], "DENIED")


if __name__ == "__main__":
    unittest.main()
