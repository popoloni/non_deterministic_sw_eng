# Exercise 2: Evaluation Rubric

## Scoring Guide

### 🥉 Bronze (Basic Completion)
**Score: 60-69%**

- [ ] MCP configuration file exists
- [ ] At least one MCP server configured
- [ ] Configuration JSON is valid
- [ ] Server responds to explicit invocation

### 🥈 Silver (Meets Expectations)
**Score: 70-89%**

All Bronze criteria, plus:
- [ ] Context7 configured and working
- [ ] Filesystem MCP configured for docs
- [ ] AI returns current framework docs (not stale)
- [ ] AI can read project documentation
- [ ] Config placed in correct location for tool

### 🥇 Gold (Exceeds Expectations)
**Score: 90-100%**

All Silver criteria, plus:
- [ ] Auto-invoke rules configured
- [ ] AI uses MCP automatically (without explicit mention)
- [ ] Multiple MCP servers configured and working
- [ ] Documented which servers are used when

## Validation Checklist

### Configuration File
- [ ] File exists in correct location
- [ ] JSON syntax is valid
- [ ] Server command is correct (`npx -y`)
- [ ] Arguments are properly formatted

### Server Functionality
| Server | Test Query | Expected Result | Pass? |
|--------|------------|-----------------|-------|
| Context7 | "React 19 features" | Current docs | ☐ |
| Filesystem | "Our API standards" | Project docs | ☐ |

### Auto-Invoke (Gold level)
- [ ] Rule added to instruction file
- [ ] AI uses MCP without explicit request
- [ ] Framework code uses current patterns

## Common Deductions

| Issue | Deduction | Notes |
|-------|-----------|-------|
| Invalid JSON | -25% | Server won't start |
| Wrong file location | -20% | Tool won't find config |
| No Context7 | -15% | Missing key capability |
| Server errors on start | -15% | Check npx command |
| Stale docs returned | -10% | MCP may not be invoked |
| No auto-invoke rules | -5% | Only affects Gold level |

## Troubleshooting Guide

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| "Server not found" | Node.js < 18 | Upgrade Node.js |
| "Invalid JSON" | Syntax error | Validate with jsonlint |
| "Permission denied" | Wrong root path | Use relative path |
| "Timeout" | Network issue | Check internet connection |
| "Stale results" | Caching | Restart AI tool |

## Feedback Template

```markdown
## Exercise 2 Feedback

**Score:** ___/100
**Level:** 🥉 Bronze / 🥈 Silver / 🥇 Gold

### Servers Configured
- [ ] Context7
- [ ] Filesystem (docs)
- [ ] Other: ___

### Test Results
| Test | Result |
|------|--------|
| Current framework docs | ☐ Pass / ☐ Fail |
| Project documentation | ☐ Pass / ☐ Fail |
| Auto-invoke | ☐ Pass / ☐ Fail / ☐ N/A |

### Notes
- 
```

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
