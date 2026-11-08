# V10 companion: one synthetic change, separate claims

Run `python scripts/run_companion_checks_v10.py` from the editable project's root. The runner preserves earlier logs and writes current evidence under `audit/v10/companion_runs/`. A test-only Python network guard is checked during the run; it is not an operating-system isolation boundary.

The reference approval service keeps Treasury at 500000 minor units in v1 and 300000 in v2. A new 400000-minor-unit request requires review in v2, while replay under the original key and canonical payload preserves the stored v1 response. SCN-COORD is an isolated coordination-test token; SCN-EVIDENCE is an isolated stale-evidence-test token. The book uses SCN-DATE for a separate hypothetical effective-date exercise. None is a third canonical policy. The schema-view migration changes representation, not authorized behavior.

The additional tests cover measurement accounting, loop budgets surviving restart, scoped file operations, stale or altered evidence, a deliberately circular oracle, memory validity, representation migration and sequential coordination. Statuses such as `ACTION_ADMITTED_NOT_ACCEPTED` and `READY_FOR_HUMAN_REVIEW_AUTHORITY_UNVERIFIED` do not authorize acceptance or release. Missing or stale evidence remains a hold.

`SCOPE_MATRIX.json` separates executable modules and tests, synthetic fixtures, design pseudocode and unexecuted empirical protocols. The lost-response discussion remains pseudocode. The learning protocol and production pilot remain unexecuted; software tests of their tools cannot supply participant results or establish operational effectiveness.

`adoption_memo.json` is a decision template, not a production authorization. No script calls a model provider, trains a model, accesses production, or requires a secret.
