# NDSE companion laboratory

This laboratory makes the Treasury case reproducible. Start with the same EUR 4,000 request under two policy versions, then inspect historical replay, conflicts and the controls used in the later chapters. The data and actors are synthetic; the programs run locally and require no credentials.

## Start here

Extract the companion archive supplied with this edition. Open a terminal in the directory containing `lab/`, `scripts/` and `series/`. This is the **companion root**. All commands below start there unless another working directory is stated.

The code requires Python **3.10 or later** and uses only its standard library. The current verification was performed on Linux with **Python 3.12.14**. The file-broker tests need a filesystem that permits symbolic links. These setup commands use a POSIX shell; no package installation through pip is needed.

```sh
python3 --version
python3 -m venv --without-pip .venv
. .venv/bin/activate
python lab/examples/policy_boundary.py
```

The first example should print:

```text
approval-eur-v1: AUTO_APPROVAL_ELIGIBLE
approval-eur-v2: REVIEW_REQUIRED
```

`amount_minor=400000` means EUR 4,000, expressed as integer cents. The request has low risk, belongs to Treasury and is not cross-border. The v1 ceiling is EUR 5,000; the v2 ceiling is EUR 3,000. The program reads the supplied policy files and calls the recovered `Policy.evaluate` method.

Run the complete local path:

```sh
python scripts/run_lab_checks.py
```

Success is reported as `"passed": true` with `"phases_passed": 3` and `"phases_total": 3`. The detailed report is `audit/current_run/LAB_CHECK_SUMMARY.json`. The three phases run the companion checks, the first example and the explicit case trace. A nonzero exit means that a phase failed; its log is named in the report.

## Results to inspect

| Result | Expected value | Where to inspect it |
|---|---:|---|
| Companion execution gates | 20/20 | `audit/v10/companion_runs/RUN_SUMMARY.json` |
| Service regressions | 19 tests | `audit/v10/companion_runs/service_regression_19.log` |
| Chapter 7 behavioral records | 21/21 | `audit/v10/companion_runs/ch07.json` |
| Real isolated mutation campaign | 12 killed, 0 survived, 0 infrastructure errors | `audit/v10/companion_runs/ch07_mutations.json` |
| Metamorphic samples | 2,184/2,184 amount pairs | `audit/v10/companion_runs/ch07_relations.json` |
| Differential samples | 168/168 cases | Same report; status comparisons only |
| Separate relation identity controls | 3/3 | Same report; replay and fresh identities |
| Additional v10 regressions | 47 tests | `audit/v10/companion_runs/v10_composed_regressions.log` |
| Historical proposal evaluations | 3 ready, 4 rejected | `audit/v10/companion_runs/ch11.json` |
| Explicit recheck under the final intention | 2 ready, 5 rejected | `audit/case_trace/CH11_CASE_TIMELINE.json` |
| Historical replay and both identity conflicts | Original v1 response preserved; two audit events | `audit/case_trace/CANONICAL_CASE_TRACE.json` |

The 19 service regressions and 21 independent behavioral records are different suites. The 47 additional tests exercise the later controller examples. Do not add these counts and call them independent research trials. The chapter 9 comparison is a small authored fixture: nine questions concern source retrieval and T10 concerns programmed abstention. Its current per-task records are in `audit/v10/companion_runs/retrieval/`.

The seven chapter 11 evaluations are historical events. A1 was ready before INT-002 arrived. The second result explicitly runs the gate again at the final revision: only B2 and E2 are then ready for human review. This recheck does not imply that a human has accepted or released the software.

## Run a chapter route

Every command in this section starts at the companion root. The scripts for Chapters 3, 4, 5 and 7 accept `--help`; a missing or invalid required argument prints usage and exits with code 2.

### Chapters 3–5: permissions, intention and architecture

```sh
python lab/companion/ch03/permission_bounded_surrogate.py lab/case_study audit/reader/ch03/trace.jsonl
python lab/companion/ch04/ccs_native_gate.py lab/case_study
python lab/companion/ch05/architecture_fitness_v2.py lab/case_study
```

Chapter 3 creates missing output directories and records four events, including two denials. `request_network` checks an empty allowlist of exact URLs. Its network event records `performed: false`; the program sends no request. Chapter 4 reports eight structural checks with `structural_status: PASS`, `authority_status: HUMAN_APPROVAL_UNVERIFIED` and `acceptance_status: NOT_ACCEPTED`. Chapter 5 reports 19/19 fitness records, including detection of the deliberately stale adapter as a negative control.

### Chapter 7: independent expectations and real mutations

```sh
python lab/companion/ch07/independent_oracle_lab.py lab/case_study
python lab/companion/ch07/mutation_runner.py lab/case_study
python lab/companion/ch07/relation_examples.py lab/case_study
```

The oracle reports 21 behavioral records. The campaign establishes a passing baseline and changes one named fault in each of 12 isolated copies. Its JSON retains the exact patch, source digests, failed behavioral record names and outcome. All 12 are killed in the reference run. Syntax/import failures, timeouts, malformed results and a failing baseline are infrastructure errors and cannot count as kills. Temporary mutated copies are removed after the run; the source case is unchanged. For one fault, append `--mutant M12_replay_appends_valid_chain_row`.

The relation example keeps currency, department, risk, cross-border flag, requester and policy fixed while increasing a valid positive integer amount. None of its 2,184 sampled pairs changes `REVIEW_REQUIRED` into `AUTO_APPROVAL_ELIGIBLE`. Its 168 differential cases compare **status only**: v1/v2 differ exactly for LOW-risk domestic Treasury amounts from 300,001 through 500,000 cents inclusive. The output includes the four interval boundaries and the HIGH-risk, cross-border, OPS and unknown-department countercontexts. These are finite samples. Whole decisions also carry policy-version metadata. Pure `Policy.evaluate` avoids replay state; service experiments require fresh transaction IDs **and** fresh keys. Three separate identity controls demonstrate why historical replay has its own contract.

### Chapters 9 and 11: retrieval, history and coordination

```sh
python lab/companion/ch09/retrieval_handoff_agent.py lab/case_study lab/companion/ch09/holdout_questions.json audit/reader/retrieval
python lab/companion/ch11/multi_agent_governance.py
python scripts/build_case_trace.py
```

The authored Chapter 9 fixture reports 6/10 baseline and 8/10 memory-mode combined successes; each total includes the programmed abstention case T10. Inspect `trial_results.csv` and `agent_traces.json` rather than treating the totals as comprehension measures. Chapter 11 prints the historical 3-ready/4-rejected result. The trace command separately records the final-revision 2-ready/5-rejected recheck.

The separate [proposed comprehension follow-up](companion/ch09/FOLLOWUP_DESIGN_EN.md) specifies new tasks and independent scoring. It has not been executed; its human and model cohorts do not appear in the fixture results.

A **lease** is a temporary target assignment with an owner, expiry and generation. The sequential coordinator checks it when admitting an item to its review queue. Its outputs now use `HOLD_WRONG_LEASE` and `HOLD_EXPIRED_LEASE` consistently. `series/PUBLIC_PROJECTION.json` documents this schema rename in the unpublished candidate. Queue admission does not grant release authority.

### Service and controller tests

Run all 47 later controller tests from the root:

```sh
python -m unittest discover -s lab/companion/v10 -v
```

For the original 19 service regressions, change directory explicitly:

```sh
cd lab/case_study
python -m unittest discover -s tests -q
cd ../..
```

For one named controller module, use its own working directory:

```sh
cd lab/companion/v10
python -m unittest test_control_state -v
python -m unittest test_measurement -v
python -m unittest test_coordination -v
cd ../../..
```

### Actual artifacts printed in the book

```sh
python lab/examples/build_reader_artifacts.py
```

The command runs the checks and writes seven files under `audit/reader_artifacts/`. Reference copies are in `lab/reader_artifacts/`: the intention bundle, permission envelope and trace, fitness excerpt, evidence record, environment profile and versioned memory cards. The evidence record names actual source digests and the executed command; authentication and execution attestation remain false. The architecture decision is `lab/case_study/docs/03_architecture_decisions.md`. The versioned threshold cards use the `memory_scope.py` schema; the retrieval agent's broader card remains `docs/06_case_memory_card.json` inside the case.

## What each part supplies

| Chapter | Material | Activity |
|---|---|---|
| 1 | `lab/case_study/docs/01_intent_contract.json` | Read the declared requirements and identify questions for the owner. |
| 2 | `lab/companion/v10/measurement.py` | Check measurement definitions against a synthetic event ledger. |
| 3 | `lab/companion/ch03/` and `lab/companion/v10/control_state.py` | Inspect permission decisions; exercise limits, restart, revocation and stale-intention checks. |
| 4 | `lab/companion/ch04/ccs_native_gate.py` | Inspect structural checks and distinguish them from authority and acceptance. |
| 5 | `lab/companion/ch05/` and `lab/companion/v10/schema_view.py` | Check architectural fitness; change a derived representation while preserving policy behavior and replay. |
| 6 | `lab/companion/v10/file_broker.py` | Test allowed and denied local file operations. |
| 7 | `lab/companion/ch07/independent_oracle_lab.py` | Derive expected behavior from the contract and expose deliberate defects. |
| 8 | `lab/companion/v10/review_findings.json` | Classify review findings and write a reasoned human verdict. |
| 9 | `lab/companion/ch09/` and `lab/companion/v10/memory_scope.py` | Inspect retrieval and test a versioned memory card. |
| 10 | `lab/companion/ch10/` | Test protocol software; the participant study itself is a proposed activity. |
| 11 | `lab/companion/ch11/` and `lab/companion/v10/coordination.py` | Inspect proposal events and local sequential coordination. |
| 12 | `lab/companion/v10/whole_change_cost_worksheet.csv` | Calculate illustrative costs and decide which real measurements would be needed. |
| 13 | The exercise and solution in the book | Review a bounded documentation change; no publication is performed by this laboratory. |

The detailed classification is `lab/companion/v10/SCOPE_MATRIX.json`. Empty production-pilot and participant-rating templates are deliberately rejected by their analysis programs. Software tests do not turn those templates into observed field or learning results. The lost-response extension in Appendix A is design pseudocode.

## The shared case and its versions

`series/CASE_LEDGER.json` records the common rules, units and identities. Both it and `series/STATE_REGISTRY.json` are reader projections: editorial production history is held outside this distribution. The registry contains 20 operational families. `series/READER_STATUS_KEY_EN.md` is the compact key generated from that registry; the publication example is a prose label, not an executable enum. `series/STATE_REGISTRY.json` distinguishes application decisions, controller results, reasons, authority declarations and memory validity. `series/SCENARIO_ID_MAP.json` separates SCN-DATE, SCN-COORD and SCN-EVIDENCE from canonical INT-001/INT-002.

The distributed INT-001 document is a consolidated teaching contract: AC-002 already compares v1 and v2. Read it together with the INT-002 delta. Policy amounts are integer EUR cents. Repeating the same key and request returns the stored original response; a new request uses the active policy. Reusing an identity inconsistently raises a conflict.

## If a result differs

Keep the archive filename and its SHA-256, the output of `python --version`, your operating system, the exact command and working directory, and the failing log under `audit/`. Include these details in a [repository issue](https://github.com/popoloni/non_deterministic_sw_eng/issues). The edition's release record identifies the distributed code; older provenance logs are not a substitute for the results of your own run.

The Python socket guard used by the test runner is a local testing aid. The broker and coordinator illustrate specific checks in one process; they do not implement operating-system isolation, authenticated approvals or a distributed production service.

## Source checks behind the book

The [source-claim register](../evidence/REGISTER_EN.md) identifies the chapters, source IDs and exact primary versions consulted. The public register contains documentary provenance; the book text and the complete editorial change register remain in the production package.
