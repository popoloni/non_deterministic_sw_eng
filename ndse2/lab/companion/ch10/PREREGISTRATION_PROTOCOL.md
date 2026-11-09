# Chapter 10 — Preregisterable delayed-retention and transfer evaluation

**Status:** Prepared, not executed. No participants enrolled, no follow-up data collected, no observed treatment effect. This is a methodological proposal, not a clinical or psychometric validation.

## Research question and design
Among software developers unfamiliar with the synthetic approval service, does an **expert-curated AI code tour with prediction and explanation checkpoints** improve unaided transfer performance 14 days later, compared with **unrestricted AI assistance**? Both conditions receive identical repository snapshots, task time, test access, and the same coding model/version if deployed. The experimental manipulation is the structure of assistance; do not attribute a difference solely to model quality.

Randomize *participants* 1:1 after a baseline test, stratified by experience band and baseline score if enough participants. Generate assignments with `randomize.py` from anonymized participant IDs, an optional predeclared `stratum` field, and an archived private seed. For small strata, balance is only within one participant; this is not a power calculation. Do not expose assignments, the seed, or participant linkage to raters. This is a **between-subject** design to avoid learning carryover; use Form A at baseline and an unseen Form B at delayed transfer. The earlier allocation script counterbalanced these forms even though the assisted Treasury task also rehearses Form A, making that form unsuitable as an unseen delayed endpoint. The corrected default therefore fixes A/B order. Any future counterbalanced design needs genuinely matched, unpracticed forms and separate preregistration. The assignment file is not part of the blinded rating packet.

## Study sessions
- **Day 0, before treatment (15–20 min):** consent, prior experience, baseline Form A, unaided prediction and explanation; no AI.
- **Day 0, assisted change (35–45 min):** task in the approval service. Treatment receives an expert-curated tour, AI hints and required prediction/explanation checkpoints. Control receives unrestricted AI assistance and identical project files and independent tests. Record prompts, source accesses, elapsed time, test outcomes and reviewer interventions.
- **Day 0, immediately after (15–20 min):** unaided explanation, source citations, negative-test reasoning, and change-impact exercise; model and tour disabled.
- **Day 14 ±2 days (25–35 min):** previously unseen parallel form, unaided; include novel jurisdiction rule, unchanged historical replay and unsafe proposed patch. Record whether participants accessed prohibited assistance and apply preregistered exclusion rules.

## Endpoints
**Primary:** participant-level delayed-transfer total (five dimensions scored 0–2; 0–10). Do not choose the best-performing question post hoc. **Secondary:** immediate score, baseline-adjusted change, critical unsafe-assumption rate, time, correct citations, number of independent negative cases and subjective workload. Missing Day-14 scores must be reported; primary analysis should not assume missingness at random without sensitivity analysis.

## Sampling and power
A convenience pilot of 12–20 participants can assess feasibility and scoring reliability, **not** establish a well-powered effect. Estimate outcome variance and attrition in the pilot, then preregister a separate confirmatory sample size for a specified minimally important difference, alpha and desired power. Avoid interpreting the pilot's p-value as definitive.

## Blind scoring and rubric
Two independent raters score pseudonymous answer packets without condition, participant linkage or session metadata. Use `BLIND_RATINGS_TEMPLATE.csv`, not the private key. Form content can still reveal session or task type; assess this blinding limitation in the feasibility pilot rather than claim perfect time-point blinding. See `RUBRIC.md`. Adjudicate disagreements only after saving raw independent ratings. After both independent ratings are locked, an analyst joins `RATING_KEY_TEMPLATE.csv` and reports exact agreement and quadratic-weighted Cohen's kappa per dimension where estimable; if prevalence is degenerate, report kappa as undefined rather than zero. Examine task-form difficulty, ceiling/floor effects and inter-item correlations; do not infer reliability from one small synthetic exercise.

## Analysis plan
For a sufficiently powered randomized study, estimate treatment effect on Day-14 score using baseline score and predeclared experience strata as covariates. Report coefficient, 95% confidence interval, group sample sizes, missingness and a sensitivity analysis. Use participant as unit; do not treat five rubric dimensions as five independent subjects. Use a stratified randomization check and a blind scoring reliability audit before unblinding.

## Data governance
Use participant pseudonyms, separate consent and identity data from scores, document model/tool versions, and avoid uploading real proprietary repositories or personal information to third-party AI tools. Follow applicable institutional ethics and privacy review.

## No-results rule
Do not populate outcome tables with fabricated participant data. The included scorer refuses an empty dataset. Test fixtures, if used to test the code, must be labeled **synthetic software tests** and excluded from the study results.

## Operational preparation before recruitment
Validate task-form difficulty and author non-overlapping immediate-assessment prompts; the supplied five-item forms are prototypes, not a complete calibrated test bank. Preserve Form B from baseline/treatment exposure. The allocator and scorer validate software inputs only. Their unit tests use artificial vectors labelled software tests, never participant evidence.

## V10 alignment of practice and transfer
The fixed baseline-A / delayed-B allocation remains unchanged. The session list formerly said “A or B”; it now agrees with the fixed order and prevents inadvertent exposure of Form B.
The optional schema-view practice rehearses responsibility boundaries, invariant preservation and authority recognition. It is not an extra arm. Any use during assisted work must be identical in available task material across conditions, with only the already declared assistance structure differing.
Before recruitment, review both forms for comparable difficulty, independence from the practiced example and coverage of those competencies. Inspect critical unsafe answers separately from total score; report independent rater agreement and floor/ceiling behavior. No criterion-validity or reliability claim is made here.
All added practice/transfer descriptions are protocol refinements, not participant outcomes.
