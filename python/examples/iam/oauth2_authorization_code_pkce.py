"""OAuth 2.0 Authorization Code flow with PKCE.

Problem statement:
Implement the client-side parts of a secure OAuth2 authorization code flow
that uses Proof Key for Code Exchange (PKCE). This example generates the code
verifier and challenge, builds the authorization URL, and exchanges an auth code
for tokens.

This is useful for IAM interviews when discussing secure public-client flows
and why PKCE is required for browser/native/mobile apps.
"""

import base64
import hashlib
import os
import urllib.parse


def generate_code_verifier(length: int = 64) -> str:
    """Generate a high-entropy PKCE code verifier."""
    return base64.urlsafe_b64encode(os.urandom(length)).rstrip(b"=").decode("ascii")


def generate_code_challenge(code_verifier: str) -> str:
    """Derive the PKCE code challenge from the code verifier."""
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_authorization_url(
    auth_endpoint: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    code_challenge: str,
    code_challenge_method: str = "S256",
) -> str:
    """Build the OAuth2 authorization URL for the user-agent redirect."""
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
    }
    return f"{auth_endpoint}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(
    token_endpoint: str,
    code: str,
    redirect_uri: str,
    client_id: str,
    code_verifier: str,
    http_post,
) -> dict:
    """Exchange the authorization code for tokens using the PKCE verifier.

    The `http_post` parameter is a callable that performs an HTTP POST and
    returns a JSON-decoded dict. This keeps the example framework-independent.
    """
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": code_verifier,
    }
    return http_post(token_endpoint, data=body)


if __name__ == "__main__":
    # Example usage for a public OAuth2 client.
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    auth_url = build_authorization_url(
        auth_endpoint="https://auth.example.com/oauth2/authorize",
        client_id="my-client-id",
        redirect_uri="https://app.example.com/callback",
        scope="openid profile email",
        state="random-state-123",
        code_challenge=challenge,
    )

    print("Authorization URL:")
    print(auth_url)
    print()
    print("Code verifier (store this securely until the callback):")
    print(verifier)
    print("Code challenge (sent in the auth request):")
    print(challenge)

    # In a real app, the browser is redirected to auth_url, the user consents,
    # and the authorization server redirects back with ?code=...&state=... .
    # After that, exchange_code_for_token() is called with the original verifier.
