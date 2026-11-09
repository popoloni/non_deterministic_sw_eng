# Design record — ADR-001: a bounded policy evaluator

**Context.** A legacy function maps a number to an approval recommendation. The human-defined intention introduces department rules, mandatory review for high risk and cross-border, and idempotent evidence. A non-deterministic agent may propose implementations, but this reference solution is deterministic so test oracles can be independent of a model's explanations.

**Decision.** Maintain a strict `Transaction` boundary, a versioned `Policy` with per-department integer-minor thresholds, and a SQLite-based `ApprovalService` with atomic idempotency and local evidence. Human review remains a distinct status; this demonstration never executes an actual approval. The intent contract is normative; this ADR is a replaceable design choice. Reject strings that are not in the domain enum and reject floating money values. Policy files cannot silently introduce unknown fields. Treat historical replays as immutable regardless of the current policy version.

**Alternatives.** A rules engine is unnecessary for two departments; it would add dependency and maintenance costs before the mechanism is justified. A remote API and blockchain ledger would compromise reproducibility and produce a misleading impression of production readiness. A plain JSON log would make idempotency and atomicity too easy to violate.

**Consequences.** The implementation is explainable and testable. SQLite is fit only for the local demonstration and has no authorization, HA, or protected audit custody. Audit hash chaining is a tamper-detection exercise, not cryptographic assurance. Do not infer that all architectural choices are empirically justified by a particular AI/SWE study.

**Tests and reversibility.** Both v1 and v2 policies are retained; the codebase exercises both versions. Late changes invalidate policy-dependent tests, not historical outputs. The owner can revert to v1 in new synthetic evaluations without modifying previous records. The explicit reviewer gate remains necessary before a deployable decision.
