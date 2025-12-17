# Exercise 1: Evaluation Rubric

## Scoring Guide

### 🥉 Bronze (Basic Completion)
**Score: 60-69%**

- [ ] Instruction file exists in correct location
- [ ] Contains project technology stack
- [ ] Contains at least 2 commands
- [ ] AI generates code (may not follow all conventions)

### 🥈 Silver (Meets Expectations)
**Score: 70-89%**

All Bronze criteria, plus:
- [ ] Contains 3+ coding conventions
- [ ] References at least 1 example file in codebase
- [ ] AI follows stated tech stack
- [ ] AI uses correct testing library
- [ ] File is under 50 lines (concise)

### 🥇 Gold (Exceeds Expectations)
**Score: 90-100%**

All Silver criteria, plus:
- [ ] Tool-specific format used correctly (MDC for Cursor, etc.)
- [ ] AI follows all stated conventions in test scenarios
- [ ] Identified and documented at least 1 iteration improvement
- [ ] Instructions are clear enough for team adoption

## Validation Checklist

### File Location
| Tool | Expected Location | Found |
|------|-------------------|-------|
| GitHub Copilot | `.github/copilot-instructions.md` | ☐ |
| Claude Code | `CLAUDE.md` | ☐ |
| Cursor | `.cursor/rules/*.mdc` | ☐ |

### Content Checklist
- [ ] Technology stack clearly stated
- [ ] Build/test/lint commands listed
- [ ] Key conventions documented
- [ ] Reference patterns with file paths
- [ ] No contradictory instructions

### Behavioral Tests
| Test Prompt | Convention Expected | AI Followed? |
|-------------|---------------------|--------------|
| "Create a component" | Functional, not class | ☐ |
| "Add API call" | Uses apiClient pattern | ☐ |
| "Write a test" | Uses specified library | ☐ |

## Common Deductions

| Issue | Deduction | Notes |
|-------|-----------|-------|
| Wrong file location | -20% | AI may not find the file |
| No commands listed | -10% | AI can't run builds/tests |
| No reference patterns | -10% | AI guesses conventions |
| Over 100 lines | -5% | May be ignored or skimmed |
| Contradictory rules | -15% | Causes inconsistent behavior |

## Feedback Template

```markdown
## Exercise 1 Feedback

**Score:** ___/100
**Level:** 🥉 Bronze / 🥈 Silver / 🥇 Gold

### Strengths
- 

### Areas for Improvement
- 

### Next Steps
- 
```

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
