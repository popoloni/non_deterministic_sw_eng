# Enterprise Workflow Checklists

> **Book Reference:** Appendix C — "Best Practices Checklists"

This folder contains validation checklists for the enterprise multi-agent workflow. Use these at human checkpoint gates between phases.

## Checklist Index

| Checklist | When to Use | Items |
|-----------|-------------|-------|
| [Requirements Checklist](./requirements-checklist.md) | After Requirement Analyst → Before Architect | 10 |
| [Architecture Checklist](./architecture-checklist.md) | After Architect → Before API Champion | 10 |
| [Handoff Checklist](./handoff-checklist.md) | At every agent transition | 8 |

## Workflow Overview

```
┌────────────────── PLANNING PHASE ──────────────────┐
│                                                     │
│  Requirement    →   Architect   →   API Champion   │
│   Analyst           Agent           Agent          │
│      │                │                │           │
│      ▼                ▼                ▼           │
│  ┌───────┐        ┌───────┐        ┌───────┐      │
│  │ REQ   │        │ ARCH  │        │ API   │      │
│  │ CHECK │        │ CHECK │        │ CHECK │      │
│  └───────┘        └───────┘        └───────┘      │
│                                                    │
│            ═══════════════════════════             │
│                 MERGE REQUEST GATE                 │
│            ═══════════════════════════             │
│                                                    │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────── EXECUTION PHASE ─────────────────┐
│                                                     │
│     Test Explorer  →  Test Engineer                │
│          │               ↕ parallel                │
│          │          Software Engineer              │
│          ▼                │                        │
│     ┌───────┐        ┌───────┐                    │
│     │ TEST  │        │HANDOFF│                    │
│     │ CHECK │        │ CHECK │                    │
│     └───────┘        └───────┘                    │
│                                                    │
│            ═══════════════════════════             │
│                 MERGE REQUEST GATE                 │
│            ═══════════════════════════             │
│                                                    │
└────────────────────────────────────────────────────┘
```

## Usage Instructions

### At Phase Gates

1. **Stop** before approving any handoff
2. **Open** the relevant checklist
3. **Verify** each item is complete
4. **Document** any deviations or approvals
5. **Proceed** only when all required items pass

### For Merge Requests

Before approving any merge request:

1. Run the [Handoff Checklist](./handoff-checklist.md)
2. Run the phase-specific checklist:
   - Planning → Execution: [Architecture Checklist](./architecture-checklist.md)
   - Execution → Complete: Test coverage verification

### Automation

These checklists can be automated via:
- GitHub Actions (PR template with checklist)
- VS Code tasks (validation scripts)
- CI/CD gates (artifact validation)

## Checklist Status Legend

| Symbol | Meaning |
|--------|---------|
| ☐ | Not started |
| ☑ | Complete |
| ⚠️ | Partial / Needs attention |
| ❌ | Failed / Blocked |

## Related Resources

- [Planning Phase Agents](../planning-phase/) — Agent configurations
- [Execution Phase Agents](../execution-phase/) — Agent configurations
- [Handoff Configuration](../handoffs/) — YAML configuration
- [Artifact Templates](../artifacts/) — Required artifact formats

---

*Based on best practices from "Non-Deterministic Software Engineering" (2025), Appendix C — Human checkpoints prevent automation failures.*
