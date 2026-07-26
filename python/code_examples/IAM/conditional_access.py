"""Conditional access policy example for IAM decision making.

Problem statement:
Implement a conditional access engine that evaluates runtime context against
policy requirements like MFA, network location, device trust, and risk.

This is useful for IAM interviews that cover zero trust, dynamic access
controls, and policy-driven authorization decisions.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ConditionalAccessPolicy:
    requires_mfa: bool = False
    allowed_networks: List[str] = None
    min_device_trust: int = 0
    allowed_locations: List[str] = None

    def matches(self, context: Dict[str, object]) -> bool:
        """Check whether the runtime context meets the policy."""
        if self.requires_mfa and not context.get("mfa_verified", False):
            return False

        if self.allowed_networks is not None:
            if context.get("network_zone") not in self.allowed_networks:
                return False

        if self.allowed_locations is not None:
            if context.get("location") not in self.allowed_locations:
                return False

        if context.get("device_trust_score", 0) < self.min_device_trust:
            return False

        return True


class AccessEnforcer:
    def __init__(self):
        self.policies: Dict[str, ConditionalAccessPolicy] = {}

    def add_policy(self, resource: str, policy: ConditionalAccessPolicy) -> None:
        self.policies[resource] = policy

    def is_access_allowed(self, resource: str, context: Dict[str, object]) -> bool:
        policy = self.policies.get(resource)
        if policy is None:
            return False
        return policy.matches(context)


if __name__ == "__main__":
    enforcer = AccessEnforcer()
    enforcer.add_policy(
        "FinancePortal",
        ConditionalAccessPolicy(
            requires_mfa=True,
            allowed_networks=["CORPORATE_VPN", "OFFICE_LAN"],
            min_device_trust=80,
        ),
    )

    context = {
        "mfa_verified": True,
        "network_zone": "CORPORATE_VPN",
        "device_trust_score": 85,
        "location": "US",
    }

    print("FinancePortal access allowed:", enforcer.is_access_allowed("FinancePortal", context))
