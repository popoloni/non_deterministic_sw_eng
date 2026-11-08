# Real-pilot data contract

One row per **assigned task** (not per model attempt). The required CSV columns are:

`task_id,mode,assigned_at,accepted,released,developer_minutes,reviewer_minutes,verification_minutes,model_cost_eur,compute_cost_eur,followup_minutes,incident_loss_eur,deployment_outcome,observation_days,risk_class`

- `mode`: human_led / pair_assisted / bounded_agent / agent_independent_checker (or exact locally registered labels).
- `accepted` and `released`: 0 or 1, with `released <= accepted`.
- Times: active minutes attributable to the task; include rejected attempts in their assigned task's totals.
- `model_cost_eur`, `compute_cost_eur`: actual billed or allocated amounts.
- `followup_minutes`: observed corrective work in a common post-merge window.
- `incident_loss_eur`: observed loss if defensibly attributed; otherwise zero with a separately maintained unmeasured-risk flag.
- `deployment_outcome`: not_deployed / success / rollback / incident / unknown.
- `observation_days`: actual available follow-up window.
- `risk_class`: preregistered risk stratum.

The calibration script validates the input and produces **descriptive** cost per assigned/accepted/released task. It does not infer causal uplift from observational assignments or estimate rare losses from zero observed incidents.

For a causal pilot, additionally retain randomization assignment, compliance, task family, baseline complexity, reviewer ID, versioned tool configuration, CI status, timestamps for stage transitions, deployment identifier, and reasons for exclusion. Store those securely and de-identify before sharing.
