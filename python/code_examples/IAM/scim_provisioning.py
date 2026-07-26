"""SCIM-like provisioning example for users and groups.

Problem statement:
Implement a simplified SCIM-style provisioning service that can create users,
create groups, manage group membership, and perform schema mapping. This
illustrates IAM directory provisioning and identity sync behavior.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SCIMUser:
    id: str
    user_name: str
    display_name: str
    emails: List[str] = field(default_factory=list)
    external_id: Optional[str] = None


@dataclass
class SCIMGroup:
    id: str
    display_name: str
    members: List[str] = field(default_factory=list)


class SCIMProvisioner:
    def __init__(self):
        self.users: Dict[str, SCIMUser] = {}
        self.groups: Dict[str, SCIMGroup] = {}

    def create_user(self, user_name: str, display_name: str, emails: List[str], external_id: Optional[str] = None) -> SCIMUser:
        """Create a new SCIM user record."""
        user_id = f"user-{len(self.users) + 1}"
        user = SCIMUser(id=user_id, user_name=user_name, display_name=display_name, emails=emails, external_id=external_id)
        self.users[user_id] = user
        return user

    def create_group(self, display_name: str) -> SCIMGroup:
        """Create a new SCIM group record."""
        group_id = f"group-{len(self.groups) + 1}"
        group = SCIMGroup(id=group_id, display_name=display_name)
        self.groups[group_id] = group
        return group

    def add_user_to_group(self, user_id: str, group_id: str) -> bool:
        """Add a user to a group if both exist."""
        if user_id not in self.users or group_id not in self.groups:
            return False
        group = self.groups[group_id]
        if user_id not in group.members:
            group.members.append(user_id)
        return True

    def get_user(self, user_id: str) -> Optional[SCIMUser]:
        """Return a user by ID."""
        return self.users.get(user_id)

    def list_groups_for_user(self, user_id: str) -> List[SCIMGroup]:
        """Return groups that the user belongs to."""
        return [group for group in self.groups.values() if user_id in group.members]


if __name__ == "__main__":
    provisioner = SCIMProvisioner()
    alice = provisioner.create_user(
        user_name="alice",
        display_name="Alice Johnson",
        emails=["alice@example.com"],
        external_id="ext-123",
    )
    dev_group = provisioner.create_group("Developers")
    provisioner.add_user_to_group(alice.id, dev_group.id)

    print("Created user:", alice)
    print("Created group:", dev_group)
    print("Groups for Alice:", [g.display_name for g in provisioner.list_groups_for_user(alice.id)])
