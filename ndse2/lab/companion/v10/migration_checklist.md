# Bounded schema-view migration
1. Map adapter -> Policy.evaluate -> ApprovalService store and historical replay.
2. Freeze canonical v1/v2 fixtures and retain their hashes.
3. Translate only the view schema; reject ambiguous fields, duplicate departments and non-integer units.
4. Compare complete Decision records across the boundary/risk/cross-border cases.
5. Reopen the same decision store under v2; replay the original key/payload unchanged.
6. Review uncovered consumers; this finite fixture set is not a completeness proof.
7. Roll back the view reader if interpretation differs. Never rewrite decision history.
This is synthetic offline testing, not measured operational migration or performance.
