# IAM Interview Example Scripts

This folder contains Python examples that are useful for IAM tech lead interview preparation.

## New IAM-focused examples

- `oauth2_authorization_code_pkce.py`
  - Demonstrates the OAuth 2.0 Authorization Code flow with PKCE.
  - Shows how to generate a code verifier/challenge, build an authorization URL, and exchange an auth code for tokens.

- `jwt_signature_validation.py`
  - Implements JWT validation with HS256 signature verification.
  - Covers claim checks for `exp`, `iat`, `iss`, `aud`, and required scopes.

- `scim_provisioning.py`
  - Implements a simplified SCIM-style provisioning model.
  - Contains user/group creation, membership management, and directory lookup logic.

- `conditional_access.py`
  - Demonstrates conditional access policy evaluation.
  - Covers runtime context checks for MFA, network location, device trust, and risk-based access.

- `token_revocation_blacklist.py`
  - Shows token revocation and blacklist handling.
  - Useful for illustrating logout, session invalidation, and immediate revocation semantics.

## How to use

Each file can be run as a standalone script. They include an `if __name__ == "__main__"` block with example usage and expected behavior.

## Why these topics matter

These examples were added to cover IAM patterns that are often discussed in architecture and technical design interviews:

- Secure OAuth2 public client flows
- Token validation and claim verification
- Identity provisioning and group membership management
- Conditional/zero-trust access policy enforcement
- Token revocation and session termination
