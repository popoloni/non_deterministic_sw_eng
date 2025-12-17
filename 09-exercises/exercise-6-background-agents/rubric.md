# Exercise 6: Evaluation Rubric

## Scoring Guide

### 🥉 Bronze (Basic Completion)
**Score: 60-69%**

- [ ] At least 2 background agents created
- [ ] Agents used worktree isolation
- [ ] Agents completed their tasks

### 🥈 Silver (Meets Expectations)
**Score: 70-89%**

All Bronze criteria, plus:
- [ ] 3+ background agents ran in parallel
- [ ] No file conflicts between agents
- [ ] Progress monitored via Agent Sessions
- [ ] All changes merged successfully
- [ ] All tests pass after merge

### 🥇 Gold (Exceeds Expectations)
**Score: 90-100%**

All Silver criteria, plus:
- [ ] Time savings measured and significant (>40%)
- [ ] Code review completed on worktree changes
- [ ] Conflict resolution demonstrated (if applicable)
- [ ] Interactive work continued during background execution
- [ ] Documentation of parallel strategy

## Parallel Execution Verification

| Agent | Started | Completed | Duration | Files | Conflicts |
|-------|---------|-----------|----------|-------|-----------|
| Agent 1 | ☐ | ☐ | ___ min | ___ | ☐ None |
| Agent 2 | ☐ | ☐ | ___ min | ___ | ☐ None |
| Agent 3 | ☐ | ☐ | ___ min | ___ | ☐ None |

**Total parallel time:** ___ min
**Sequential estimate:** ___ min
**Time savings:** ___% 

## Worktree Verification

| Check | Agent 1 | Agent 2 | Agent 3 |
|-------|---------|---------|---------|
| Worktree created | ☐ | ☐ | ☐ |
| Separate branch | ☐ | ☐ | ☐ |
| Files isolated | ☐ | ☐ | ☐ |
| Tests in worktree pass | ☐ | ☐ | ☐ |

## Merge Verification

| Step | Completed |
|------|-----------|
| Changes reviewed | ☐ |
| PR created (if applicable) | ☐ |
| Worktree merged | ☐ |
| Conflicts resolved (if any) | ☐ |
| Integration tests pass | ☐ |
| Worktree deleted | ☐ |

## Common Deductions

| Issue | Deduction | Notes |
|-------|-----------|-------|
| Used Local mode instead of Worktree | -25% | Likely file conflicts |
| File conflicts between agents | -20% | Poor task partitioning |
| Didn't monitor progress | -10% | May miss issues |
| Blind merge without review | -15% | Quality risk |
| Tests fail after merge | -20% | Integration issues |
| No time savings measured | -5% | Gold requirement |

## Task Independence Checklist

Before starting, verify:
- [ ] Feature A files don't overlap with Feature B
- [ ] Feature B files don't overlap with Feature C
- [ ] Feature A files don't overlap with Feature C
- [ ] Shared utilities (if any) are read-only

## Feedback Template

```markdown
## Exercise 6 Feedback

**Score:** ___/100
**Level:** 🥉 Bronze / 🥈 Silver / 🥇 Gold

### Parallel Execution
- Agents created: ___ 
- Isolation mode: ☐ Worktree / ☐ Local
- Ran simultaneously: ☐ Yes / ☐ No

### Time Performance
- Sequential estimate: ___ min
- Actual parallel time: ___ min
- Savings: ___%

### Merge Status
- All merged: ☐ Yes / ☐ No
- Conflicts: ☐ None / ☐ Resolved / ☐ Unresolved
- Tests pass: ☐ Yes / ☐ No

### Notes
- 
```

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
