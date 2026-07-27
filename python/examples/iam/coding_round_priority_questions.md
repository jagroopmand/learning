# Coding Round Priority Guide

Companion to `README.md` (script index). This file ranks the same scripts
by likelihood of relevance in a generic Senior/Staff-level Python coding
interview — ranked by **algorithmic transferability**, not by domain label.
A coding round tests the underlying skill (state management, complexity
tradeoffs, boundary handling); the domain wrapper on top (IAM, e-commerce,
logistics, whatever) is cosmetic and doesn't change what's being evaluated.

Domain-specific depth (OAuth2/PKCE, JWT, SCIM, etc.) is high-value —
just more likely to surface in a system design or architecture discussion
round than in a pure coding round.

## Tier 1 — Canonical CS patterns (highest coding-round likelihood, company-agnostic)

Real signal regardless of wrapper: state management, complexity tradeoffs,
boundary handling.

1. [sliding_window_rate_limiter.py](sliding_window_rate_limiter.py) — deque-based sliding window
2. [lru_cache_with_ttl.py](lru_cache_with_ttl.py) / [lru_cache_with_ttl_primitive.py](lru_cache_with_ttl_primitive.py) — cache eviction + expiry (OrderedDict version and hand-rolled doubly-linked-list version — have both ready)
3. [merge_overlapping_access_windows.py](merge_overlapping_access_windows.py) — classic interval-merge
4. [topological_sort_with_cycle_detection.py](topological_sort_with_cycle_detection.py) — Kahn's algorithm, cycle detection
5. [topN_logs.py](topN_logs.py) — log parsing + windowed aggregation
6. [log_streaming_groupby_with_late_data.py](log_streaming_groupby_with_late_data.py) — watermark/late-data tradeoffs
7. [log_streaming.py](log_streaming.py) — `bisect`/binary-search lookup pattern
8. [graph_lib.py](graph_lib.py) — baseline BFS reachability + path reconstruction (strip the domain label mentally — it's graph traversal + caching)

## Tier 2 — Strong generic value, more structural complexity

The constrained-traversal series is a genuinely valuable graph-traversal
progression (constraint dispatch tables, generators/backtracking, audit-report
structuring) independent of its domain framing.

9. [graph_lib_abac.py](graph_lib_abac.py) — constrained traversal via dispatch table
10. [graph_abac_audit_generators.py](graph_abac_audit_generators.py) — lazy path enumeration via generators/backtracking — **least common pattern in this set, easiest to go blank on under pressure, worth a specific pre-interview look**
11. [graph_abac_audit.py](graph_abac_audit.py) — structured decision reporting vs. bare boolean
12. [user_permissions.py](user_permissions.py) — inheritance/grant-union walk (hashmap + light graph)
13. [graph_abac_audit_with_unittest.py](graph_abac_audit_with_unittest.py) — same engine, consolidated + test-covered; lower priority as a *fresh* coding problem, useful as a "how I'd structure tests" answer if asked
14. [user_resource_permissions.py](user_resource_permissions.py) — flat lookup, no inheritance; good warmup baseline

## Tier 3 — Domain-specific (save for system design / architecture discussion)

Correct, deep domain knowledge — higher-value as spoken architecture
discussion than as a coding-round answer.

15. [oauth2_authorization_code_pkce.py](oauth2_authorization_code_pkce.py)
16. [jwt_signature_validation.py](jwt_signature_validation.py)
17. [token_validator.py](token_validator.py)
18. [token_revocation_blacklist.py](token_revocation_blacklist.py)
19. [scim_provisioning.py](scim_provisioning.py)
20. [conditional_access.py](conditional_access.py)
21. [compliance_traning_check.py](compliance_traning_check.py) — lowest DSA content of the set, mostly date-window business logic

## Tier 4 — Debugging drills, not solved examples

Useful specifically for "spot the bug live" practice, not standalone review.

22. [fix_it_later.py](fix_it_later.py) — stubbed methods, incomplete loop
23. [permission_resolution_DAG_topological.py](permission_resolution_DAG_topological.py) — dead code, scratch

## If short on time

Focus review on Tier 1 in full, plus Tier 2 item #10 (generator/backtracking)
specifically — it's the pattern most likely to be forgotten under pressure
and least likely to come up unless deliberately refreshed.
