# Exercise 5: Evaluation Rubric

## Scoring Guide

### 🥉 Bronze (Basic Completion)
**Score: 60-69%**

- [ ] Researcher agent file created
- [ ] Main agent file exists with tools array
- [ ] Subagent invocation attempted

### 🥈 Silver (Meets Expectations)
**Score: 70-89%**

All Bronze criteria, plus:
- [ ] Researcher has `infer: true` in frontmatter
- [ ] Main agent has `runSubagent` in tools
- [ ] Subagent successfully completed research
- [ ] Summary returned to main context
- [ ] Implementation used research findings

### 🥇 Gold (Exceeds Expectations)
**Score: 90-100%**

All Silver criteria, plus:
- [ ] Research summary is concise (under 500 words)
- [ ] Main context not polluted with raw research
- [ ] Multiple subagent calls used effectively
- [ ] Sensitive agents protected with `infer: false`
- [ ] Subagent output format followed

## Configuration Verification

### Researcher Agent
| Setting | Required Value | Actual |
|---------|----------------|--------|
| `infer` | `true` | ☐ |
| `tools` | includes 'search', 'read' | ☐ |
| Output format | Structured summary | ☐ |

### Main Agent
| Setting | Required | Actual |
|---------|----------|--------|
| `tools` includes `runSubagent` | ✅ | ☐ |
| Can list available subagents | ✅ | ☐ |
| Can invoke researcher | ✅ | ☐ |

## Subagent Behavior Verification

| Test | Expected | Pass? |
|------|----------|-------|
| Ask "What subagents can you use?" | Lists researcher | ☐ |
| Invoke researcher | Returns summary | ☐ |
| Check main context | No raw research data | ☐ |
| Check research summary | Under 500 words | ☐ |

## Common Deductions

| Issue | Deduction | Notes |
|-------|-----------|-------|
| Missing `infer: true` | -25% | Subagent won't be available |
| Missing `runSubagent` tool | -25% | Can't invoke subagents |
| Raw data in main context | -15% | Summary not returned |
| Summary too long | -10% | Pollutes main context |
| No structured output | -10% | Hard to use findings |

## Context Pollution Check

After subagent returns:
- [ ] Main context contains only summary
- [ ] No file contents from research
- [ ] No intermediate analysis steps
- [ ] Context window increased by < 1000 tokens

## Feedback Template

```markdown
## Exercise 5 Feedback

**Score:** ___/100
**Level:** 🥉 Bronze / 🥈 Silver / 🥇 Gold

### Agent Configuration
- Researcher `infer: true`: ☐ Yes / ☐ No
- Main agent `runSubagent`: ☐ Yes / ☐ No

### Subagent Execution
- Subagent invoked: ☐ Yes / ☐ No
- Summary returned: ☐ Yes / ☐ No
- Context clean: ☐ Yes / ☐ No

### Research Quality
- Summary concise: ☐ Yes / ☐ No
- Findings actionable: ☐ Yes / ☐ No
- Used in implementation: ☐ Yes / ☐ No

### Notes
- 
```

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
