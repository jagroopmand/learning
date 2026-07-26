def is_valid(token: dict, now: float, required_scope: str = None) -> tuple[bool, str]:
    """
    token: {"sub": str, "exp": float, "iat": float (optional), "scopes": [str]}
    Returns (is_valid, reason).

    Boundary decisions (state these aloud):
    - Missing 'exp' -> treat as invalid (fail-closed, not fail-open).
    - exp == now -> EXPIRED (>= check), consistent with the cache TTL logic.
    - iat in the future (now < iat) -> invalid; likely clock skew or a
      forged/future-dated token. Fail-closed here too.
    - Missing 'scopes' key vs empty list are different: missing -> malformed
      token (invalid structurally); empty list -> valid token, just has
      no scopes, so any required_scope check fails.
    """
    if "sub" not in token or not token["sub"]:
        return False, "missing subject"

    if "exp" not in token:
        return False, "missing expiry"

    exp = token["exp"]
    if now >= exp:
        return False, "expired"

    if "iat" in token and token["iat"] > now:
        return False, "issued in the future (clock skew or forged token)"

    if required_scope is not None:
        if "scopes" not in token:
            return False, "malformed token: no scopes field"
        if required_scope not in token["scopes"]:
            return False, f"missing required scope: {required_scope}"

    return True, "valid"


if __name__ == "__main__":
    base = {"sub": "user1", "exp": 100, "iat": 0, "scopes": ["read"]}

    assert is_valid(base, now=99)  == (True, "valid")
    assert is_valid(base, now=100) == (False, "expired")          # exp == now
    assert is_valid({**base, "exp": 100}, now=100.0001)[0] is False

    assert is_valid({"sub": "u", "iat": 0}, now=5) == (False, "missing expiry")
    assert is_valid({"exp": 100}, now=5) == (False, "missing subject")

    skewed = {"sub": "u", "exp": 100, "iat": 50}
    assert is_valid(skewed, now=10) == (False, "issued in the future (clock skew or forged token)")

    no_scopes_field = {"sub": "u", "exp": 100}
    assert is_valid(no_scopes_field, now=0, required_scope="admin")[0] is False

    empty_scopes = {"sub": "u", "exp": 100, "scopes": []}
    assert is_valid(empty_scopes, now=0, required_scope="admin") == (False, "missing required scope: admin")
    assert is_valid(empty_scopes, now=0) == (True, "valid")  # no scope required -> fine