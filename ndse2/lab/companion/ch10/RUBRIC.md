# Capability rubric v0.2 — unvalidated instrument

Five dimensions scored 0–2 on each parallel form. Total 0–10. Raters must quote the participant's relevant evidence; correct file names without correct reasoning do not earn full credit.

| Dimension | 0 — incorrect/missing | 1 — partial | 2 — supported and accurate |
|---|---|---|---|
| Authority | Treats observed code or example signature as production authorization | Names an authority but misses its scope | Distinguishes approved intent, design, and illustrative authority; identifies decision owner |
| Behavior prediction | Wrong policy decision or no version distinction | Correct one version only or incomplete boundary reasoning | Correct predictions for both versions/novel rule, with boundary and risk precedence |
| Causal explanation | Restates code without rationale | Identifies one relevant dependency | Explains policy evaluation, idempotent persistence and why replay is historical |
| Negative verification | Cannot find or construct failing counterexample | Gives relevant test but weak oracle | Constructs independent contract-derived negative case and identifies failing invariant |
| Change impact | Claims all evidence remains valid or must be deleted | Finds one affected artifact | Distinguishes stale boundary evidence from unchanged risk/replay invariants and names review owner |

**Unsafe-assumption flag:** yes/no, separately coded if the answer (a) treats example authority as real production sign-off, (b) reevaluates historical decisions on replay, or (c) automatically approves HIGH/cross-border transactions. This is a safety screening signal, not a validated certification rule. Do not compute a weighted total with invented weights.

**Validation requirements:** content review by two independent senior engineers and one domain owner; pilot cognitive interviews for ambiguity; blinded inter-rater agreement; item discrimination and ceiling effects; alternate-form equivalence; delayed test–retest stability; construct/criterion validity against an external maintenance task. None are established by writing this rubric.
