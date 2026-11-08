# Verifier contract and acceptance separation

The *maker* may edit the implementation, tests proposed by the maker, and design note. The *checker* runs independent test cases derived from `01_intent_contract.json`, including risk and cross-border cases absent from the legacy code. A passing maker loop is **READY FOR REVIEW, NOT ACCEPTED**. A separate accountable reviewer checks the intended external behavior, version provenance, CLI safety, negative cases, and relevant evidence.

## Independent oracles

- AC-001 and AC-002: boundary tests for Treasury EUR 3,000 / EUR 4,000 under v1/v2.
- AC-003 and AC-004: ensure no high-risk or cross-border request is eligible, even at one minor unit.
- AC-005: identical request and key yield exactly one decision and audit event across replay; old version preserved on replay after late clarification.
- AC-006: changed payload or transaction ID duplicated under another key fails with a conflict.
- Additional invariants: reject zero/negative amounts, booleans/floats as money, unknown risk, non-EUR currency, unsafe policy contents, and detect simple audit corruption.

## Acceptance record template

| Gate | Proposed input | Reviewer evidence | Status at baseline |
|---|---|---|---|
| Intent | INT-001 + INT-002 | Example owner approval only, not real | Illustrative |
| Local tests | `python -m unittest discover -s tests -v` | Captured in release log | Passing |
| Change verification | v1 vs v2 and historical replay | Deterministic output | Passing |
| Security | STRIDE-style review | Open production omissions | Not production-acceptable |
| Independent review | Reviewer not responsible for patch | Named approval record | Not performed |
| Production | Deployment and rollback evidence | Not implemented | Out of scope |

If an orchestrator rejects the same passing loop twice without a citeable policy hook or failing oracle, stop automatic retries, preserve artifacts and escalate to a named human. Never let the orchestrator silently invent new requirements.
