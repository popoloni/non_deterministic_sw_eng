# 10 - Reference

> 📖 **Book Reference:** Appendix A (Quick Reference Guides)

---

## Overview

Quick reference materials for daily use. Print these, bookmark them, or keep them open while working with AI assistants.

---

## Contents

| File | Description |
|------|-------------|
| [70-percent-checklist.md](./70-percent-checklist.md) | The 30% that AI misses — what to always verify |
| [vibe-vs-engineering.md](./vibe-vs-engineering.md) | Quick comparison: when each approach is appropriate |
| [skill-transformation.md](./skill-transformation.md) | How engineering skills evolve with AI |
| [maturity-model.md](./maturity-model.md) | **Context Engineering Maturity Model** — 5-level progression + tool maturity rings |

---

## Quick Reference: The 70% Rule

AI typically gets you 70% of the way. **Always verify:**

### ✅ Security
- [ ] Input validation complete?
- [ ] Auth checks on all endpoints?
- [ ] No hardcoded secrets?
- [ ] SQL injection protected?
- [ ] XSS sanitization applied?

### ✅ Error Handling
- [ ] All error paths handled?
- [ ] Errors don't leak information?
- [ ] Graceful degradation?
- [ ] Retry logic where needed?

### ✅ Edge Cases
- [ ] Empty inputs handled?
- [ ] Null/undefined checked?
- [ ] Boundary conditions tested?
- [ ] Concurrent access safe?

### ✅ Performance
- [ ] N+1 queries avoided?
- [ ] Pagination implemented?
- [ ] Caching where appropriate?
- [ ] Memory leaks prevented?

### ✅ Integration
- [ ] Works with existing code?
- [ ] Follows project conventions?
- [ ] Documentation updated?
- [ ] Tests comprehensive?

---

## Quick Reference: Vibe vs. Engineering

| Aspect | Vibe Coding | Professional Engineering |
|--------|-------------|-------------------------|
| **Goal** | "Make it work" | "Make it right" |
| **Verification** | Manual testing | Automated tests |
| **Security** | "Probably fine" | Verified secure |
| **Documentation** | None | Complete |
| **Appropriate for** | Prototypes, learning | Production, teams |

---

## Quick Reference: Skill Evolution

| Traditional Skill | AI-Era Evolution |
|-------------------|------------------|
| Writing code | Reviewing/guiding AI code |
| Memorizing syntax | Understanding concepts |
| Solo debugging | Collaborative debugging with AI |
| Reading docs | Teaching AI to read docs (MCP) |
| Code review | AI-assisted review + human judgment |

---

## Using These References

1. **During development** — Check the 70% list after AI generates code
2. **During review** — Use vibe vs. engineering to assess code quality
3. **During planning** — Consider skill evolution when designing workflows
