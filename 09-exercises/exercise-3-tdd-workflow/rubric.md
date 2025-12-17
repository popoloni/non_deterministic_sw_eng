# Exercise 3: Evaluation Rubric

## Scoring Guide

### 🥉 Bronze (Basic Completion)
**Score: 60-69%**

- [ ] Both agent files created
- [ ] Agents have name and description
- [ ] Tools array defined
- [ ] Basic TDD cycle attempted

### 🥈 Silver (Meets Expectations)
**Score: 70-89%**

All Bronze criteria, plus:
- [ ] Agent boundaries clearly defined (Always/Never sections)
- [ ] Handoffs configured correctly
- [ ] Test-writer only modified tests/ directory
- [ ] Implementer only modified src/ directory
- [ ] Tests failed before implementation (TDD verified)
- [ ] All tests pass after implementation

### 🥇 Gold (Exceeds Expectations)
**Score: 90-100%**

All Silver criteria, plus:
- [ ] Test structure follows template (TC-XXX identifiers)
- [ ] Self-assessment protocol included in implementer
- [ ] Handoff buttons functioned correctly
- [ ] Multiple TDD cycles completed (edge cases added)
- [ ] Implementation is minimal (no over-engineering)

## Boundary Verification

| Check | Test Writer | Implementer |
|-------|-------------|-------------|
| Files in tests/ | ✅ Should create | ❌ Must not modify |
| Files in src/ | ❌ Must not create | ✅ Should create |
| Run tests | ✅ Yes | ✅ Yes |
| Existing tests | ❌ Must not modify | ❌ Must not modify |

## TDD Cycle Verification

| Step | Expected | Actual |
|------|----------|--------|
| 1. Write tests | Tests exist | ☐ |
| 2. Run tests | Tests fail | ☐ |
| 3. Implement | Code exists | ☐ |
| 4. Run tests | Tests pass | ☐ |
| 5. Refactor | Tests still pass | ☐ |

## Common Deductions

| Issue | Deduction | Notes |
|-------|-----------|-------|
| Missing boundaries section | -20% | Critical for agent isolation |
| No handoffs configured | -15% | Reduces workflow value |
| Implementer modified tests | -25% | Violates TDD principle |
| Tests didn't fail first | -15% | Not true TDD |
| Missing tools array | -10% | Agent may not function |
| No self-assessment protocol | -5% | Gold level only |

## Agent File Checklist

### Test Writer
- [ ] `name: Test Writer`
- [ ] `description` includes TDD context
- [ ] `tools` includes search, read, edit, runCommand
- [ ] `handoffs` to implementer configured
- [ ] Boundaries: Always write to tests/
- [ ] Boundaries: Never modify src/
- [ ] Test structure template included

### Implementer
- [ ] `name: Implementer`
- [ ] `description` includes "make tests pass"
- [ ] `tools` includes search, read, edit, runCommand
- [ ] `handoffs` to test-writer (for more tests)
- [ ] Boundaries: Always run tests
- [ ] Boundaries: Never modify tests/
- [ ] Self-assessment after 3 failures (Gold)

## Feedback Template

```markdown
## Exercise 3 Feedback

**Score:** ___/100
**Level:** 🥉 Bronze / 🥈 Silver / 🥇 Gold

### TDD Cycle
- Tests written first: ☐ Yes / ☐ No
- Tests failed initially: ☐ Yes / ☐ No
- All tests pass now: ☐ Yes / ☐ No

### Boundary Compliance
- Test-writer stayed in tests/: ☐ Yes / ☐ No
- Implementer stayed in src/: ☐ Yes / ☐ No

### Areas for Improvement
- 

### Next Steps
- 
```

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
