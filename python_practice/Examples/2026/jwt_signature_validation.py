"""JWT validation with signature verification and claim checks.

Problem statement:
Implement a simple JSON Web Token validator that verifies the token's
signature, expiration, issuer, audience, and optional scope claim.

This is useful for IAM interviews describing how to validate bearer tokens
and why signature + claim checks are essential for secure authorization.
"""

import base64
import hashlib
import hmac
import json
from typing import Optional, Tuple


def base64url_decode(value: str) -> bytes:
    """Decode a base64-url string, adding padding if necessary."""
    value = value.encode("ascii")
    padding = b"=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def verify_hs256_signature(token: str, secret: str) -> bool:
    """Verify an HS256 JWT signature using a shared secret."""
    header_b64, payload_b64, signature_b64 = token.split(".")
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_signature = hmac.new(
        secret.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    try:
        actual_signature = base64url_decode(signature_b64)
    except (ValueError, binascii.Error):
        return False
    return hmac.compare_digest(expected_signature, actual_signature)


def parse_jwt(token: str) -> Tuple[dict, dict]:
    """Parse a JWT and return decoded header and payload as dicts."""
    header_b64, payload_b64, _ = token.split(".")
    header = json.loads(base64url_decode(header_b64))
    payload = json.loads(base64url_decode(payload_b64))
    return header, payload


def validate_jwt(
    token: str,
    secret: str,
    now: float,
    issuer: Optional[str] = None,
    audience: Optional[str] = None,
    required_scope: Optional[str] = None,
) -> Tuple[bool, str]:
    """Validate the JWT signature and standard claims."""
    try:
        header, payload = parse_jwt(token)
    except Exception as exc:
        return False, f"invalid token format: {exc}"

    if header.get("alg") != "HS256":
        return False, "unsupported algorithm"

    if not verify_hs256_signature(token, secret):
        return False, "invalid signature"

    if "exp" not in payload:
        return False, "missing exp claim"
    if now >= payload["exp"]:
        return False, "token expired"

    if "iat" in payload and payload["iat"] > now:
        return False, "token issued in the future"

    if issuer is not None and payload.get("iss") != issuer:
        return False, "issuer mismatch"

    if audience is not None:
        aud = payload.get("aud")
        if aud != audience and (not isinstance(aud, list) or audience not in aud):
            return False, "audience mismatch"

    if required_scope is not None:
        scopes = payload.get("scope") or payload.get("scopes")
        if scopes is None:
            return False, "missing scope claim"
        if isinstance(scopes, str):
            scopes = scopes.split()
        if required_scope not in scopes:
            return False, "required scope not present"

    return True, "valid"


if __name__ == "__main__":
    # Example secret-based JWT for HS256 validation.
    example_secret = "super-secret-key"
    example_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJ1c2VyMSIsImV4cCI6MjUwMDAwMDAwLCJpc3MiOiJodHRwczovL2F1dGguZXhhbXBsZS5jb20iLCJhdWQiOiJhcGkiLCJzY29wZSI6InJlYWQgd3JpdGUiLCJpYXQiOjE2MDAwMDAwMDB9."
        "F8xvD6QsYuC2xPQcK2QGNuUnE_XCbA7mA32wgcJCdSw"
    )
    is_valid_token, reason = validate_jwt(
        example_token,
        secret=example_secret,
        now=1700000000,
        issuer="https://auth.example.com",
        audience="api",
        required_scope="read",
    )
    print(is_valid_token, reason)
