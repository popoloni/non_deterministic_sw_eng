# Requirements Analyst Validation Checklist

> **Book Reference:** Appendix C — "Best Practices Checklists"
> 
> **When to Use:** After Requirement Analyst completes, before handing off to Architect

## Purpose

Validate that the Requirements Analyst agent has produced a complete, unambiguous `business-context.md` artifact that can serve as the source of truth for technical design.

---

## Checklist

### 1. Artifact Exists

- [ ] File `docs/planning/business-context.md` exists
- [ ] File is not empty (minimum 50 lines)

```bash
# Verification command
test -f docs/planning/business-context.md && \
  wc -l docs/planning/business-context.md | awk '$1 >= 50'
```

---

### 2. Problem Statement

- [ ] Contains exactly ONE clear problem statement
- [ ] Problem is stated as a user/business need (not a technical solution)
- [ ] Problem statement is < 3 sentences

**Good Example:**
> "Users cannot reset their passwords without calling customer support, leading to 500+ support tickets per month."

**Bad Example:**
> "We need to implement a REST API with JWT tokens for password reset functionality."

---

### 3. User Stories

- [ ] At least 3 user stories present
- [ ] Each story follows format: "As a [role], I want [action], so that [benefit]"
- [ ] Each story has a unique identifier (US-001, US-002, etc.)
- [ ] Stories cover primary actors (not just happy path)

```bash
# Count user stories
grep -c "As a" docs/planning/business-context.md
# Expected: >= 3
```

---

### 4. Acceptance Criteria

- [ ] Every user story has at least 2 acceptance criteria
- [ ] Criteria are measurable and testable
- [ ] Criteria use format: AC-XXX linked to US-XXX
- [ ] No subjective language ("fast", "easy", "nice")

**Good Criteria:**
> - AC-001: Password reset email sent within 5 seconds of request
> - AC-002: Reset token expires after exactly 60 minutes

**Bad Criteria:**
> - System should be fast
> - Password reset should be easy to use

---

### 5. Out of Scope

- [ ] "Out of Scope" section exists
- [ ] At least 3 explicit boundaries defined
- [ ] Boundaries prevent scope creep
- [ ] Related features are explicitly deferred

**Example:**
> - Password complexity rules (covered by existing policy)
> - Multi-factor authentication integration
> - Admin password reset (separate feature)

---

### 6. Dependencies

- [ ] External systems listed with status
- [ ] Third-party services identified
- [ ] Data sources documented
- [ ] Blocking dependencies flagged

**Example:**
> | Dependency | Status | Owner |
> |------------|--------|-------|
> | Email service (SendGrid) | Available | Platform team |
> | User database | Available | Backend team |
> | Rate limiting | Needs configuration | DevOps |

---

### 7. Traceability

- [ ] Original issue/ticket number referenced
- [ ] `trace_id` field present for linking
- [ ] Source of requirements documented (email, meeting, Jira)

```yaml
# Expected metadata
trace_id: ISSUE-1234
source: Product meeting 2025-01-15
requested_by: Product Manager
```

---

### 8. No Technical Solutions

- [ ] Document describes WHAT, not HOW
- [ ] No database schemas proposed
- [ ] No API endpoints designed
- [ ] No technology choices made

**Flag these as violations:**
- "Use JWT tokens for..."
- "Create a REST endpoint..."
- "Store in PostgreSQL..."

---

### 9. Clarity Check

- [ ] No undefined acronyms
- [ ] No ambiguous terms ("the system", "it", "users")
- [ ] Stakeholder-friendly language
- [ ] Could be understood by non-technical reader

---

### 10. Human Validation

- [ ] Requirements reviewed with stakeholder
- [ ] Clarifying questions answered
- [ ] Sign-off obtained (comment or approval)

---

## Summary Score

| Category | Status | Notes |
|----------|--------|-------|
| Artifact exists | ☐ | |
| Problem statement | ☐ | |
| User stories | ☐ | |
| Acceptance criteria | ☐ | |
| Out of scope | ☐ | |
| Dependencies | ☐ | |
| Traceability | ☐ | |
| No tech solutions | ☐ | |
| Clarity | ☐ | |
| Human validation | ☐ | |

**Minimum to proceed:** 8/10 items passed

---

## Actions if Failed

### Missing Artifact
```
Cannot proceed: business-context.md missing or incomplete.
Return to Requirement Analyst with:
- Specific missing sections
- Original input for reference
```

### Ambiguous Requirements
```
Requirements unclear. Before Architect handoff:
1. List specific ambiguities
2. Return to Requirement Analyst
3. Request stakeholder clarification
```

### Technical Solutions Present
```
Technical solutions detected in requirements.
Move technical content to notes file.
Keep business-context.md focused on WHAT, not HOW.
```

---

## Automation Script

```bash
#!/bin/bash
# validate-requirements.sh

FILE="docs/planning/business-context.md"

echo "=== Requirements Checklist Validation ==="

# Check file exists
if [ ! -f "$FILE" ]; then
    echo "❌ FAIL: $FILE does not exist"
    exit 1
fi
echo "✅ File exists"

# Check minimum length
LINES=$(wc -l < "$FILE")
if [ "$LINES" -lt 50 ]; then
    echo "❌ FAIL: File has $LINES lines (minimum 50)"
    exit 1
fi
echo "✅ File has $LINES lines"

# Count user stories
STORIES=$(grep -c "As a" "$FILE" || echo 0)
if [ "$STORIES" -lt 3 ]; then
    echo "⚠️ WARNING: Only $STORIES user stories (minimum 3)"
else
    echo "✅ Found $STORIES user stories"
fi

# Check for technical solutions (warning only)
if grep -qi "REST\|API\|database\|JWT\|endpoint" "$FILE"; then
    echo "⚠️ WARNING: Possible technical solutions detected"
fi

echo "=== Validation Complete ==="
```

---

*Based on "Non-Deterministic Software Engineering" (2025), Appendix C — Requirements Analyst produces the source of truth for all downstream agents.*
