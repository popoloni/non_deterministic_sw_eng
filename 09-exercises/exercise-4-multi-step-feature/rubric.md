# Exercise 4: Evaluation Rubric

## Scoring Guide

### 🥉 Bronze (Basic Completion)
**Score: 60-69%**

- [ ] Plan was created before implementation
- [ ] At least one handoff occurred
- [ ] Feature was implemented
- [ ] Tests exist

### 🥈 Silver (Meets Expectations)
**Score: 70-89%**

All Bronze criteria, plus:
- [ ] Plan was reviewed and approved before coding
- [ ] Clarifying questions were answered
- [ ] TDD cycle was followed (tests first)
- [ ] Multiple handoffs preserved context
- [ ] Context management was attempted
- [ ] All tests pass

### 🥇 Gold (Exceeds Expectations)
**Score: 90-100%**

All Silver criteria, plus:
- [ ] Context stayed under 70% throughout
- [ ] Background agent used for long tasks
- [ ] Worktree isolation used (if parallel work)
- [ ] Code review completed before merge
- [ ] Documentation updated
- [ ] Feature is production-ready

## Phase Verification

### Phase 1: Planning
| Criteria | Points | Achieved |
|----------|--------|----------|
| Plan exists | 10 | ☐ |
| Contains task list | 5 | ☐ |
| Architecture decisions documented | 5 | ☐ |
| Clarifying questions answered | 5 | ☐ |
| Plan approved before coding | 5 | ☐ |

### Phase 2: Test Specification
| Criteria | Points | Achieved |
|----------|--------|----------|
| Tests written first | 10 | ☐ |
| Tests cover happy path | 5 | ☐ |
| Tests cover edge cases | 5 | ☐ |
| Tests failed initially | 5 | ☐ |

### Phase 3: Implementation
| Criteria | Points | Achieved |
|----------|--------|----------|
| Implementation follows plan | 10 | ☐ |
| Tests pass | 10 | ☐ |
| Minimal implementation (no over-engineering) | 5 | ☐ |

### Phase 4: Context & Review
| Criteria | Points | Achieved |
|----------|--------|----------|
| Context monitored | 5 | ☐ |
| Context stayed under 70% | 5 | ☐ |
| Code review completed | 5 | ☐ |

**Total: 100 points**

## Context Management Verification

| Checkpoint | Context Level | Pass/Fail |
|------------|---------------|-----------|
| After planning | < 30% | ☐ |
| After test spec | < 50% | ☐ |
| After task 3 | < 70% | ☐ |
| After completion | < 80% | ☐ |

## Common Deductions

| Issue | Deduction | Notes |
|-------|-----------|-------|
| No plan created | -25% | Critical planning phase |
| Skipped clarifying questions | -10% | Requirements incomplete |
| Tests after implementation | -15% | Not TDD |
| Context exceeded 70% | -10% | Should have compacted |
| No code review | -10% | Gold level requirement |
| Handoffs lost context | -15% | Need better prompts |

## Feedback Template

```markdown
## Exercise 4 Feedback

**Score:** ___/100
**Level:** 🥉 Bronze / 🥈 Silver / 🥇 Gold

### Phase Completion
- Planning: ☐ Complete / ☐ Partial / ☐ Skipped
- Test Spec: ☐ Complete / ☐ Partial / ☐ Skipped
- Implementation: ☐ Complete / ☐ Partial / ☐ Skipped
- Review: ☐ Complete / ☐ Partial / ☐ Skipped

### Context Management
- Max context level reached: ___%
- Compaction used: ☐ Yes / ☐ No
- Background agents used: ☐ Yes / ☐ No

### Feature Status
- Tests passing: ☐ Yes / ☐ No
- Production ready: ☐ Yes / ☐ No

### Notes
- 
```

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
