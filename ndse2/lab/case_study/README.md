# Running case study — an approval-routing change in a brownfield transaction service

**Release:** Pre-Writing Baseline v1.0, 9 October 2026. **Runtime:** Python 3.10+ and SQLite, standard library only. **All input data are synthetic.** This laboratory *does not* approve or settle real transactions and must never receive real credentials, payment data, or customer information.

## What the reader inherits

A pre-existing routing function (`approval_lab/legacy.py`) treats any amount up to EUR 10,000 as automatically eligible for approval. It ignores risk, business department, and whether a transaction is cross-border. That is the deliberate defect, not an acceptable product design. Run `python -m approval_lab legacy-demo` to reveal it before viewing the corrected implementation. The new `approval_lab.policy.Policy` and `approval_lab.service.ApprovalService` represent a fully testable reference design, not a claim that an AI agent generated correct software.

The stakeholder then asks for configurable approval rules, but the initial request leaves several things unclear: which department owns each threshold, whether high-risk and cross-border transactions can be auto-eligible, how repeat requests should behave, whether a previous decision should be recomputed when rules change, and what kind of audit trail is sufficient. These questions are resolved in a versioned intent contract before designing the implementation.

## Run it, completely offline

```bash
cd case_study
python -m approval_lab demo
python -m approval_lab legacy-demo
python -m unittest discover -s tests -v
```

The `demo` command evaluates a synthetic **EUR 4,000 Treasury transaction**. Policy **v1** has a EUR 5,000 Treasury threshold and finds it eligible. After an explicitly authorized late clarification, policy **v2** lowers that threshold to EUR 3,000, requiring human review. No actual approval action is performed.

To create a persistent synthetic decision ledger:

```bash
python -m approval_lab evaluate --db demo.sqlite --policy v1 \
  --transaction-id DEMO-001 --idempotency-key KEY-001 \
  --amount-minor 400000 --department TREASURY --risk LOW
python -m approval_lab audit-check --db demo.sqlite
```

The response distinguishes `AUTO_APPROVAL_ELIGIBLE` (a *recommendation*) from `REVIEW_REQUIRED`; neither means money was moved or an approval completed. An identical idempotency key replays its previous decision, including the version of the policy originally applied. Conflicting payloads are rejected. See tests for boundary and failure cases.

## What this implementation intentionally does **not** provide

Authentication, real authorization, segregation-of-duties enforcement, database migrations, high availability, durable signatures, key custody, secure clock attestations, SAST results, full concurrency load testing, disaster recovery, jurisdictional compliance, and actual transaction settlement are outside the lab. The SHA-256 audit chain only detects simple accidental edits; it does not prevent a privileged attacker from rewriting the database and chain. `sqlite3` transactions make local demonstration repeatable but are not a validated distributed ledger. Any production adaptation would require a new threat model and entirely new verification.

## How this case maps to the manual

Chapters 1–2 define the work unit and measurement baseline; Chapter 3 bounds agent permissions; Chapter 4 captures intent and the late delta; Chapters 5–6 design and secure the change; Chapters 7–8 independently verify and review it; Chapter 9 stores provenance-aware knowledge; Chapter 10 defines a comprehension exercise; Chapter 11 names owners and change authority; Chapter 12 evaluates cost per accepted change under uncertainty. The documents in `docs/` are synthetic example artifacts, not empirical research findings.
