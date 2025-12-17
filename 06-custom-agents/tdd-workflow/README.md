# TDD Workflow Agent Chain

> 📖 **Book Reference:** Chapter 10, Section 7 - Development Practices Enhanced by AI
> 
> 📖 **Exercise:** Appendix C - Your First Multi-Agent Workflow

---

## Overview

This folder contains a complete TDD (Test-Driven Development) workflow using specialized AI agents. The workflow follows Kent Beck's Red-Green-Refactor cycle, enhanced with AI assistance.

### The Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     TDD + AI WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                        │
│   │   RED   │───▶│  GREEN  │───▶│REFACTOR │───┐                    │
│   │         │    │         │    │         │   │                    │
│   │tdd-red  │    │tdd-green│    │tdd-refac│   │                    │
│   └─────────┘    └─────────┘    └─────────┘   │                    │
│        ▲                                      │                    │
│        └──────────────────────────────────────┘                    │
│                    (repeat for each feature)                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Why TDD + AI?

From the book (Kent Beck interview):

> "I have this sense of tension and release. Once the tension of a red test is released and you have green, now I'm free to think all those thoughts of, like, yeah, but this isn't going to work for these test cases..."

### Key Benefits

1. **Tests Provide Constraints for AI** — Prevents hallucination of requirements
2. **TDD Catches AI Mistakes Fast** — Failed tests surface errors in seconds
3. **TDD Structures the AI Workflow** — Natural stopping points for human review

---

## Agents in This Workflow

| Agent | Role | Phase |
|-------|------|-------|
| [tdd-red.md](./tdd-red.md) | Write failing tests as specifications | RED |
| [tdd-green.md](./tdd-green.md) | Implement minimal code to pass tests | GREEN |
| [tdd-refactor.md](./tdd-refactor.md) | Improve code structure, keep tests green | REFACTOR |

---

## How to Use

### Option A: VS Code with GitHub Copilot

1. Copy agents to `.github/agents/` in your project
2. Open Chat view (`Ctrl+Alt+I`)
3. Select **tdd-red** from agents dropdown
4. Describe your requirements
5. After tests are written, click **Hand off to Implementer**
6. Review implementation
7. Click **Hand off to Refactor** when tests pass

### Option B: Copilot CLI

```bash
# Step 1: Write failing tests
copilot --agent=tdd-red --prompt "Write tests for user password reset:
- Request reset with email
- Token expires after 1 hour  
- Set new password with valid token"

# Step 2: Implement to make tests pass
copilot --agent=tdd-green --prompt "Make the password reset tests pass"

# Step 3: Refactor when green
copilot --agent=tdd-refactor --prompt "Clean up the implementation"
```

### Option C: Claude Code

1. Add agents to your CLAUDE.md as sub-agents
2. Use slash commands to invoke: `/test-first`, `/implement`, `/refactor`

---

## The "Immutable Test" Problem

Kent Beck identified a critical issue with AI agents:

> "I really want an immutable annotation that says, no, no, this is correct. And if you ever change this, I'm going to unplug you."

All agents in this workflow include the **Test Modification Policy** to prevent AI from modifying tests to make them pass:

```markdown
### Test Modification Policy
**CRITICAL RULE:** Tests are the source of truth.
- NEVER modify an existing test to make it pass
- NEVER remove assertions to fix failures
- NEVER change expected values to match actual output
- If a test appears wrong, ASK the human before changing it
```

---

## Practical Example

```typescript
// Step 1: tdd-red writes failing test
describe('UserAuthentication', () => {
  it('should return JWT token when credentials are valid', () => {
    const result = authenticateUser('user@example.com', 'password123');
    expect(result).toHaveProperty('token');
    expect(result.token).toMatch(/^eyJ/); // JWT format
  });
});

// Step 2: tdd-green implements minimal code
// FAIL: authenticateUser is not defined → implements function

// Step 3: tdd-refactor cleans up
// Extract generateToken() for reusability
// Add error handling constants
```

---

## Verification Checklist

After completing a TDD cycle:

- [ ] Tests were written BEFORE implementation
- [ ] Tests initially failed (TDD verification)
- [ ] tdd-red only created files in `tests/`
- [ ] tdd-green only created files in `src/`
- [ ] No test files were modified by tdd-green
- [ ] All tests pass after implementation
- [ ] Refactoring kept all tests green

---

## Research Findings

From Thoughtworks and industry practitioners:

- **15-50% time savings** on test generation and boilerplate
- **10-40% savings** on business logic (depends on context)
- **TDD + pair programming** identified as best mitigations against "AI smells"

> "TDD with Copilot requires a lot of discipline, as it is easy to generate more than necessary for the next step." — Thoughtworks

---

## Files

| File | Description |
|------|-------------|
| [tdd-red.md](./tdd-red.md) | Test Writer agent - RED phase |
| [tdd-green.md](./tdd-green.md) | Implementer agent - GREEN phase |
| [tdd-refactor.md](./tdd-refactor.md) | Refactoring agent - REFACTOR phase |

---

## Related Resources

- [Custom Agents Guide](../README.md)
- [Test Agent (GitHub)](../github-agents/test-agent.md)
- [Security Checklists](../../08-security/checklists/)
