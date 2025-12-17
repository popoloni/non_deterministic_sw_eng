# Agent Handoff Validation Checklist

> **Book Reference:** Appendix C — "Best Practices Checklists" & "Handoff Payload Schema"
> 
> **When to Use:** At EVERY agent transition in the enterprise workflow

## Purpose

Validate that handoff between agents is complete, traceable, and ready for the receiving agent to continue work without ambiguity.

---

## Checklist

### 1. Artifact Produced

- [ ] Required output artifact exists
- [ ] Artifact is in expected location
- [ ] Artifact is not empty

| Agent | Required Artifact |
|-------|-------------------|
| Requirement Analyst | `docs/planning/business-context.md` |
| Architect | `docs/planning/solution-design.md` |
| API Champion | `docs/planning/api-definitions.yaml` |
| Messaging Champion | `docs/planning/messaging-definitions.yaml` |
| Test Explorer | `docs/execution/test-cases.md` |
| Test Engineer | `tests/**/*.test.ts` |
| Software Engineer | `src/**/*.ts` |

```bash
# Example verification
test -s docs/planning/business-context.md && echo "✅ Artifact exists"
```

---

### 2. Required Sections Complete

- [ ] All mandatory sections present
- [ ] No placeholder text remaining
- [ ] No TODO markers left
- [ ] No "TBD" or "[FILL IN]" text

```bash
# Check for incomplete markers
grep -i "TODO\|TBD\|FIXME\|\[FILL" docs/planning/*.md
# Expected: No matches
```

---

### 3. Validation Passed

- [ ] Lint/validation command ran successfully
- [ ] No errors in output
- [ ] Warnings addressed or documented

| Artifact | Validation Command |
|----------|-------------------|
| Markdown files | `npx markdownlint docs/**/*.md` |
| OpenAPI spec | `npx @redocly/cli lint docs/planning/api-definitions.yaml` |
| AsyncAPI spec | `npx @asyncapi/cli validate docs/planning/messaging-definitions.yaml` |
| TypeScript | `npm run typecheck` |
| Tests | `npm test` |

---

### 4. Trace ID Present

- [ ] `trace_id` field exists in artifact or commit
- [ ] Trace ID links to original issue/epic
- [ ] All artifacts share the same trace ID

```yaml
# Expected in artifact header or commit message
trace_id: ISSUE-1234
```

---

### 5. Context Summary Provided

- [ ] Brief summary of work completed
- [ ] Key decisions documented
- [ ] Relevant constraints noted

**Example handoff summary:**
```markdown
## Handoff Summary

**From:** Requirement Analyst
**To:** Architect
**Trace ID:** ISSUE-1234

**Completed:**
- 5 user stories defined (US-001 through US-005)
- 12 acceptance criteria documented
- Scope boundaries established

**Key Decisions:**
- Password reset limited to email-verified users
- Token expiration set to 60 minutes (per security policy)

**Notes for Architect:**
- Email service rate limits: 100/minute
- Existing user table schema in docs/db-schema.md
```

---

### 6. Open Questions Resolved

- [ ] No blocking questions remain
- [ ] Questions for receiving agent clearly marked
- [ ] Assumptions documented if questions couldn't be answered

**If questions remain:**
```markdown
## Open Questions (for Architect)

1. Should token be single-use or time-based only?
   - **Assumption:** Single-use AND time-based (most secure)
   - **Needs confirmation:** Yes

2. Maximum concurrent reset requests per user?
   - **Assumption:** 3 per hour
   - **Needs confirmation:** No (following existing rate limit pattern)
```

---

### 7. Receiving Agent Can Start

- [ ] Receiving agent's input requirements satisfied
- [ ] No missing dependencies
- [ ] Clear starting point defined

**Verification by receiving agent:**
```markdown
# As Architect, verify before starting:
- [x] docs/planning/business-context.md exists
- [x] Problem statement is clear
- [x] User stories are complete
- [x] Acceptance criteria are measurable
```

---

### 8. Human Checkpoint Passed

- [ ] Human reviewer approved the artifact
- [ ] Comments/feedback addressed
- [ ] Sign-off recorded (GitHub approval, comment, or commit)

**For merge request gates:**
- [ ] PR created with artifact changes
- [ ] At least one approval received
- [ ] CI checks passing
- [ ] Merge completed

---

## Handoff Payload Template

When automating handoffs, use this payload structure:

```json
{
  "schema_version": "1.0",
  "trace_id": "ISSUE-1234",
  "timestamp": "2025-01-15T10:30:00Z",
  "from_agent": "requirement-analyst",
  "to_agent": "architect",
  "artifacts": [
    {
      "path": "docs/planning/business-context.md",
      "checksum": "sha256:abc123...",
      "sections_completed": [
        "problem_statement",
        "user_stories",
        "acceptance_criteria",
        "out_of_scope",
        "dependencies"
      ]
    }
  ],
  "context_summary": "5 user stories defined for password reset feature",
  "open_questions": [],
  "validation_status": {
    "artifact_exists": true,
    "required_sections_present": true,
    "lint_passed": true,
    "human_approved": true
  }
}
```

---

## Summary Score

| Category | Status | Notes |
|----------|--------|-------|
| Artifact produced | ☐ | |
| Required sections complete | ☐ | |
| Validation passed | ☐ | |
| Trace ID present | ☐ | |
| Context summary provided | ☐ | |
| Open questions resolved | ☐ | |
| Receiving agent can start | ☐ | |
| Human checkpoint passed | ☐ | |

**Minimum to proceed:** ALL 8 items passed (handoffs are critical)

---

## Actions if Failed

### Artifact Missing
```
HANDOFF BLOCKED: Required artifact not found.

Expected: [artifact path]
Status: File does not exist

Action: Return to [from_agent] to complete artifact.
```

### Validation Failed
```
HANDOFF BLOCKED: Validation errors found.

Command: [validation command]
Errors: [error list]

Action: Fix validation errors before handoff.
```

### Missing Human Approval
```
HANDOFF BLOCKED: Human checkpoint required.

Artifact: [path]
Status: Awaiting human review

Action: Request review and obtain approval.
```

---

## Automation Script

```bash
#!/bin/bash
# validate-handoff.sh

FROM_AGENT=$1
TO_AGENT=$2
TRACE_ID=$3

echo "=== Handoff Validation: $FROM_AGENT → $TO_AGENT ==="
echo "Trace ID: $TRACE_ID"
echo ""

ERRORS=0

# Define expected artifacts by agent
case $FROM_AGENT in
    "requirement-analyst")
        ARTIFACT="docs/planning/business-context.md"
        VALIDATOR="markdownlint"
        ;;
    "architect")
        ARTIFACT="docs/planning/solution-design.md"
        VALIDATOR="markdownlint"
        ;;
    "api-champion")
        ARTIFACT="docs/planning/api-definitions.yaml"
        VALIDATOR="redocly lint"
        ;;
    "messaging-champion")
        ARTIFACT="docs/planning/messaging-definitions.yaml"
        VALIDATOR="asyncapi validate"
        ;;
    *)
        echo "Unknown agent: $FROM_AGENT"
        exit 1
        ;;
esac

# Check 1: Artifact exists
if [ -s "$ARTIFACT" ]; then
    echo "✅ Artifact exists: $ARTIFACT"
else
    echo "❌ Artifact missing: $ARTIFACT"
    ERRORS=$((ERRORS + 1))
fi

# Check 2: No incomplete markers
if grep -qi "TODO\|TBD\|FIXME" "$ARTIFACT" 2>/dev/null; then
    echo "⚠️ WARNING: Incomplete markers found"
    grep -i "TODO\|TBD\|FIXME" "$ARTIFACT"
fi

# Check 3: Trace ID present
if grep -q "$TRACE_ID" "$ARTIFACT" 2>/dev/null; then
    echo "✅ Trace ID found"
else
    echo "⚠️ WARNING: Trace ID not found in artifact"
fi

# Summary
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "=== HANDOFF APPROVED ==="
else
    echo "=== HANDOFF BLOCKED: $ERRORS errors ==="
    exit 1
fi
```

---

## Quick Reference: Agent Transitions

| From | To | Gate |
|------|-----|------|
| Requirement Analyst | Architect | business-context.md complete |
| Architect | API Champion | solution-design.md complete |
| API Champion | Messaging Champion | api-definitions.yaml valid |
| Messaging Champion | Test Explorer | **MERGE REQUEST GATE** |
| Test Explorer | Test Engineer | test-cases.md complete |
| Test Explorer | Software Engineer | test-cases.md complete |
| Test Engineer | (parallel) | Tests written (should fail) |
| Software Engineer | QA Review | Tests pass, code complete |
| All Execution | Complete | **MERGE REQUEST GATE** |

---

*Based on "Non-Deterministic Software Engineering" (2025), Appendix C — "In effective multi-agent workflows, no changes are made without developer validation."*
