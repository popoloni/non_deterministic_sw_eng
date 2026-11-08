# Reader status key

A label is interpreted with its entity and producer. Review readiness, authority and acceptance are separate decisions.

| Entity / check | Value | Producer | Permitted next action |
|---|---|---|---|
| Application decision | `AUTO_APPROVAL_ELIGIBLE`, `REVIEW_REQUIRED` | Policy.evaluate, for a validated transaction | Persist or return eligibility/review routing. Neither value moves funds. |
| Chapter 4 structural check | `PASS`, `FAIL` | ccs_native_gate.py | PASS permits structural review to proceed; FAIL requires repair. Authority and acceptance remain separate. |
| Chapter 4 authority check | `HUMAN_APPROVAL_UNVERIFIED` | The demonstrator reports the absence of authentication | Obtain a separate authority decision; the script does not verify signatures. |
| Chapter 4 acceptance | `NOT_ACCEPTED` | Accountable human owner, outside this checker | No implementation acceptance or release follows from the structural result. |
| Candidate checked by chapter 7 oracles | `READY_FOR_REVIEW`, `REJECTED` | independent_oracle_lab.py | A passing candidate can be reviewed. Any failing check rejects this candidate. |
| Chapter 7 acceptance | `NOT_AUTHORIZED` | Accountable human owner, outside this script | Passing the oracles does not grant real approval. |
| One chapter 11 proposal evaluation | `READY_FOR_HUMAN_REVIEW`, `REJECTED` | Deterministic gate with current revision and file ownership | READY_FOR_HUMAN_REVIEW admits review at that event. REJECTED requires repair or new evidence. Both leave human_approval_verified false. |
| Publication proposal (paper example) | `READY_FOR_PUBLICATION_REVIEW` | Named human reviewer | Review the proposed publication; a separate owner must authorize release. |

`READY_FOR_PUBLICATION_REVIEW`: paper publication example, outside the executable enums.

Source: `STATE_REGISTRY.json`; `python lab/examples/build_status_key.py`.
