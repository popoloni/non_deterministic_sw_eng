# Starter Agents Collection

> **Book Reference:** Chapter 10, Section 6 — "Custom Agent Personas"

This folder contains production-ready agent templates for the four most valuable starter agents identified in *Non-Deterministic Software Engineering*. These are the agents GitHub recommends starting with after analyzing 2,500+ repositories.

## Quick Reference

| Agent | Primary Use | Best For |
|-------|------------|----------|
| [Documentation Agent](./documentation-agent.md) | Generate docs from code | API docs, README updates, architecture docs |
| [Test Coverage Agent](./test-coverage-agent.md) | Find untested code paths | Coverage gaps, edge cases, regression tests |
| [Security Scanner Agent](./security-scanner-agent.md) | OWASP security review | Vulnerability scan, dependency audit, secrets detection |
| [Refactoring Agent](./refactoring-agent.md) | Improve code quality | Code smells, complexity reduction, pattern consistency |

## Installation

Copy the `.md` files to your repository:

```bash
# For GitHub Copilot agents
mkdir -p .github/agents
cp documentation-agent.md .github/agents/
cp test-coverage-agent.md .github/agents/
cp security-scanner-agent.md .github/agents/
cp refactoring-agent.md .github/agents/
```

## When to Use Each Agent

### 📚 Documentation Agent (`@docs`)

**Use when:**
- New feature shipped without docs
- API endpoints lack examples  
- README is outdated
- Architecture decisions need recording

**Trigger phrases:**
```
@docs Document the UserService API
@docs Update README with new installation steps
@docs Create ADR for switching to PostgreSQL
```

### 🧪 Test Coverage Agent (`@test-coverage`)

**Use when:**
- Coverage report shows gaps
- New code lacks tests
- Edge cases need identification
- Regression tests needed after bug fix

**Trigger phrases:**
```
@test-coverage Find untested paths in OrderService
@test-coverage Generate edge case tests for validateEmail
@test-coverage What scenarios are missing for the payment flow?
```

### 🔒 Security Scanner Agent (`@security`)

**Use when:**
- Before PR merge to main
- After adding new dependencies
- When handling user input
- During compliance reviews

**Trigger phrases:**
```
@security Review authentication flow for vulnerabilities
@security Check dependencies for CVEs
@security Audit input validation in API endpoints
```

### ♻️ Refactoring Agent (`@refactor`)

**Use when:**
- Function exceeds 50 lines
- Cyclomatic complexity > 10
- Duplicate code detected
- Code review flags quality issues

**Trigger phrases:**
```
@refactor Simplify the OrderProcessor class
@refactor Extract common patterns from these handlers
@refactor Reduce complexity in calculateDiscount
```

## Selection Flowchart

```
What's your immediate need?
│
├── 📝 "Code exists but docs don't"
│   └── Use @docs agent
│
├── 🧪 "Code exists but tests don't"
│   └── Use @test-coverage agent
│
├── 🔒 "Need security review before merge"
│   └── Use @security agent
│
├── 🔧 "Code works but it's messy"
│   └── Use @refactor agent
│
└── 🆕 "Building new feature"
    └── Use @test-coverage first (TDD)
```

## Agent Interaction Patterns

### Sequential Workflow (Recommended for new features)

```
1. @test-coverage → Write failing tests
2. (You implement) → Make tests pass
3. @refactor → Clean up implementation
4. @docs → Document the feature
5. @security → Final security review
```

### Parallel Workflow (For existing codebases)

Run these simultaneously on different files:
- `@docs` on `/src/services/`
- `@test-coverage` on `/src/utils/`
- `@security` on `/src/auth/`

## Key Insight from GitHub's Analysis

> "Most agent files fail because they're too vague. 'You are a helpful coding assistant' doesn't work. 'You are a test engineer who writes tests for React components, follows these examples, and never modifies source code' does."
> 
> — GitHub analysis of 2,500+ repositories with custom agents

These starter agents embody this principle: each has a **specific role**, **clear boundaries**, and **executable commands**.

## Customization Guide

### Adapt to Your Stack

Replace the example commands with your project's actual commands:

```yaml
# Before (generic)
tools: ['npm test']

# After (your project)
tools: ['pytest --cov=src', 'python -m pytest tests/']
```

### Add Project-Specific Context

Reference your project files:

```markdown
## Project Standards

Follow patterns in:
- [src/services/UserService.ts](../src/services/UserService.ts) - service structure
- [tests/unit/example.test.ts](../tests/unit/example.test.ts) - test format
```

### Extend Boundaries

Add domain-specific rules:

```markdown
### ❌ Never Do
- Modify files in `/core/` (legacy system, frozen)
- Generate docs for internal-only APIs
- Run tests against production database
```

## Related Resources

- [TDD Workflow Agents](../tdd-workflow/) — Red-Green-Refactor cycle
- [Enterprise Workflow](../../07-enterprise-workflow/) — Full team orchestration
- [GitHub Agents](../github-agents/) — Alternative implementations

---

*These agent templates are based on patterns from "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
