# IAM Example Scripts

This folder contains Python examples that are useful for IAM tech lead interview preparation.

=======
## OAuth2, Tokens & Provisioning

- [oauth2_authorization_code_pkce.py](oauth2_authorization_code_pkce.py) — OAuth 2.0 Authorization Code flow with PKCE: generates code verifier/challenge, builds the authorization URL, and exchanges the code for tokens.
- [jwt_signature_validation.py](jwt_signature_validation.py) — HS256 JWT validator: checks signature, `exp`/`iat`, issuer, audience, and required scope claims.
- [token_validator.py](token_validator.py) — Lightweight token-claims validator (dict-based, no signature check) that walks through fail-closed boundary decisions for missing/expired/future-dated claims and scopes.
- [token_revocation_blacklist.py](token_revocation_blacklist.py) — In-memory revocation store for logout/session termination; blacklists a token ID until its natural expiry and self-cleans once expired.
- [scim_provisioning.py](scim_provisioning.py) — Simplified SCIM-style provisioner: create users/groups, manage group membership, look up a user's groups.
- [conditional_access.py](conditional_access.py) — Conditional access / zero-trust policy engine: evaluates a runtime context (MFA, network zone, device trust, location) against per-resource policies.
- [compliance_traning_check.py](compliance_traning_check.py) — Determines an employee's training-compliance status (not required / pending / overdue / completed) from start date, completion date, and a compliance window.

## Graph-Based RBAC/ABAC Access Engines

A progressive series exploring the same core problem — "does a path exist from user to resource, subject to constraints?" — with each file adding a capability on top of the last.

- [graph_lib.py](graph_lib.py) — Baseline BFS reachability engine (`IAMSystem`): boolean access check with cache invalidation on graph mutation, plus shortest-path audit trail reconstruction. Heavily instrumented with debug prints for walkthroughs.
- [graph_lib_abac.py](graph_lib_abac.py) — Adds ABAC: `DynamicABAC_IAM` evaluates a dispatch table of edge constraints (IP, MFA, trust score, environment) during traversal, and fails closed on unknown rules.
- [graph_abac_audit.py](graph_abac_audit.py) — Adds structured audit output: `AuditedIAMSystem` returns a full decision report (GRANTED/DENIED, matched path, or every constraint that blocked traversal) instead of a bare boolean.
- [graph_abac_audit_generators.py](graph_abac_audit_generators.py) — Same ABAC model reworked as a generator (`find_all_valid_paths`): lazily yields every valid path via backtracking, so a caller can stop after the first result without exploring the whole graph.
- [graph_abac_audit_with_unittest.py](graph_abac_audit_with_unittest.py) — Consolidated `FinalAuditedIAM` engine (adds a self-access evaluation gate) with a full `unittest` suite covering success, transit/target constraint failures, self-access, and cycle safety.

## Permission Resolution (Non-Graph)

- [user_permissions.py](user_permissions.py) — `PRGraph.build_permissions_set`: resolves a group's effective permissions by walking parent groups and unioning grants, with an explicit deny always overriding an inherited grant.
- [user_resource_permissions.py](user_resource_permissions.py) — Flat `(user, resource) -> permissions` lookup table with a simple `check_permission` membership test; no inheritance.
- [topological_sort_with_cycle_detection.py](topological_sort_with_cycle_detection.py) — Kahn's-algorithm topological sort over a dependency graph (e.g. role/permission dependency ordering) with in-degree tracking and cycle detection.

## Supporting Data Structures & Streaming Patterns

General-purpose interview patterns that show up in IAM system design work (caching decisions, rate limiting, log/audit analytics).

- [lru_cache_with_ttl.py](lru_cache_with_ttl.py) — LRU cache with per-key TTL built on `OrderedDict`; documents boundary decisions (capacity 0, expiry-equals-now, optional TTL refresh on update).
- [lru_cache_with_ttl_primitive.py](lru_cache_with_ttl_primitive.py) — Same LRU+TTL cache reimplemented from scratch with a doubly linked list and hashmap (no `OrderedDict`), for when an interviewer wants the primitive version.
- [sliding_window_rate_limiter.py](sliding_window_rate_limiter.py) — Per-key sliding-window rate limiter using a deque of timestamps; includes a documented seeded-bug drill on the eviction boundary condition.
- [merge_overlapping_access_windows.py](merge_overlapping_access_windows.py) — Merges overlapping (and touching) time-interval access grants into a minimal set of windows.
- [log_streaming.py](log_streaming.py) — Per-key event log with binary-search (`bisect`) lookup of the most recent status and of all statuses recorded since a given timestamp.
- [log_streaming_groupby_with_late_data.py](log_streaming_groupby_with_late_data.py) — Tumbling-window stream aggregator with a watermark-based bounded-lateness policy; documents the tradeoff of dropping vs. reopening already-finalized windows.
- [topN_logs.py](topN_logs.py) — Computes the top-N most active users within a `[start, end)` time window from raw log lines, with deterministic tie-breaking.

## Work in Progress / Scratch

- [fix_it_later.py](fix_it_later.py) — Early draft of a constrained-path `PRGraph`; `check_contraints`/`check_permission` are stubbed to always return `False` and the neighbor-expansion loop is incomplete — kept as a "spot the bug" exercise, not a working example.
- [permission_resolution_DAG_topological.py](permission_resolution_DAG_topological.py) — Scratch notes for a DAG-based permission resolver (target behavior sketched in the docstring/comment); the `PRGraph` body is currently dead code and not wired up.

## How to use

Each file can be run as a standalone script. Most include an `if __name__ == "__main__"` block with example usage and expected behavior.

## Why these topics matter

These examples cover IAM and general system-design patterns that come up often in architecture and technical design interviews:

- Secure OAuth2 public client flows and token validation
- Identity provisioning and group membership management
- Conditional/zero-trust access policy enforcement
- RBAC/ABAC graph traversal, from a baseline reachability check up through cached, audited, and generator-based variants
- Permission inheritance and resolution without a graph
- Caching, rate limiting, and streaming/log analytics patterns used across IAM backends

