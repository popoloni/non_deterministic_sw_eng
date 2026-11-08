# Synthetic architecture comparison
Status: author-designed decision exercise, not an agent benchmark.
One authorized intention: preserve policy-versioned routing, risk safeguards and historical replay.
One base revision per comparison; separate worktrees for A and B.

| Option | Design | Discriminant | Decision |
|---|---|---|---|
| A | Copy threshold into handler | Needs another rule owner and a synchronized edit for next threshold delta | Reject for this exercise |
| B | Delegate routing to existing policy module | Keeps a single rule owner and existing replay boundary | Select for this exercise |

Record test commands/results, rejected reasoning, unresolved dependencies and actual reviewer before using this design in a project.
Model convergence is discussion, not an acceptance oracle.
