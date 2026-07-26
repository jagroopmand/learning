"""Token revocation and blacklist example for session invalidation.

Problem statement:
Implement a revocation store that can mark token IDs as revoked and ensure
subsequent access checks fail even if the token is otherwise valid.

This is useful for IAM interviews that cover logout, token revocation, and
immediate session termination.
"""

import time
from typing import Dict


class TokenRevocationStore:
    def __init__(self):
        self._revoked: Dict[str, float] = {}  # token_id -> expiration timestamp

    def revoke(self, token_id: str, expires_at: float) -> None:
        """Mark a token as revoked until its natural expiry."""
        self._revoked[token_id] = expires_at

    def is_revoked(self, token_id: str, now: float = None) -> bool:
        """Return True if the token is revoked or has not yet been cleaned up."""
        now = time.time() if now is None else now
        expiry = self._revoked.get(token_id)
        if expiry is None:
            return False
        if now >= expiry:
            # Once the token is expired naturally, we can remove it from the blacklist.
            del self._revoked[token_id]
            return False
        return True

    def cleanup(self, now: float = None) -> None:
        """Remove revoked entries that are already expired."""
        now = time.time() if now is None else now
        expired_keys = [token_id for token_id, expiry in self._revoked.items() if expiry <= now]
        for token_id in expired_keys:
            del self._revoked[token_id]


def validate_access_token(token_id: str, token_payload: dict, revocation_store: TokenRevocationStore, now: float = None) -> bool:
    """Validate a token against expiry and the revocation blacklist."""
    now = time.time() if now is None else now
    if token_payload.get("exp") is None or now >= token_payload["exp"]:
        return False
    if revocation_store.is_revoked(token_id, now=now):
        return False
    return True


if __name__ == "__main__":
    now = time.time()
    store = TokenRevocationStore()
    token_id = "token-abc-123"
    payload = {"sub": "alice", "exp": now + 300}

    print("Valid before revoke:", validate_access_token(token_id, payload, store, now=now))
    store.revoke(token_id, expires_at=payload["exp"])
    print("Valid after revoke:", validate_access_token(token_id, payload, store, now=now))
    print("Revocation state:", store.is_revoked(token_id, now=now))
