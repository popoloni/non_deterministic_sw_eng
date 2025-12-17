# Exercise 3: TDD Workflow with Two Agents

> **Book Reference:** Chapter 10, Section "Multi-Agent Workflows"  
> **Time:** 1 hour  
> **Difficulty:** ⭐⭐ Intermediate

## Problem Statement

Implement a TDD (Test-Driven Development) workflow using two specialized agents: a Test Writer and an Implementer. This exercise demonstrates multi-agent coordination with clear boundaries.

## Learning Objectives

After completing this exercise, you will:
- Create custom agent definitions with boundaries
- Configure agent handoffs
- Execute a complete TDD cycle with AI assistance
- Verify agents stay within their designated areas

## Prerequisites

- Completed [Exercise 1](../exercise-1-static-context/) and [Exercise 2](../exercise-2-mcp-integration/)
- GitHub Copilot with custom agents, or Claude Code, or Cursor
- A project with a test framework configured (Jest, pytest, etc.)

## Instructions

### Step 1: Create Test Writer Agent (15 minutes)

Create `.github/agents/test-writer.md`:

```markdown
---
name: Test Writer
description: Writes failing tests as specifications before 
             implementation. First step in TDD workflow.
tools: ['search', 'read', 'edit', 'runCommand']
handoffs:
  - label: Hand off to Implementer
    agent: implementer
    prompt: |
      Make these tests pass. Tests are in tests/ directory.
      Start with the first failing test.
    send: false
---

# Test Writer Agent

You write tests BEFORE implementation exists.

## Your Role
- Translate requirements into executable test specifications
- Focus on behavior, not implementation details
- Write tests that will fail (code does not exist yet)

## Output Location
Write all tests to the `tests/` directory only.

## Boundaries

### Always Do
- Write tests to tests/ directory only
- Include edge cases and error conditions
- Use descriptive test names
- Run tests to confirm they fail

### Never Do
- Modify files in src/
- Write implementation code
- Remove or modify existing tests
```

### Step 2: Create Implementer Agent (15 minutes)

Create `.github/agents/implementer.md`:

```markdown
---
name: Implementer
description: Implements minimal code to make tests pass.
             Second step in TDD workflow.
tools: ['search', 'read', 'edit', 'runCommand']
handoffs:
  - label: Add More Tests
    agent: test-writer
    prompt: |
      Add tests for edge cases and error handling.
      Current tests are passing.
    send: false
---

# Implementer Agent

You implement ONLY what is needed to pass existing tests.

## Your Role
- Read failing tests to understand requirements
- Write minimal code to make tests pass
- Run tests after each change

## Workflow
1. Read the failing test(s)
2. Write minimal implementation
3. Run tests
4. If tests pass, stop - do not add more

## Boundaries

### Always Do
- Run tests after each change
- Follow existing code patterns
- Keep changes minimal

### Never Do
- Modify files in tests/
- Add features not covered by tests
- Delete tests to make them pass
```

### Step 3: Execute TDD Workflow (30 minutes)

#### Option A: VS Code with GitHub Copilot

1. Open Chat view (Ctrl+Alt+I)
2. Select **test-writer** from agents dropdown
3. Enter requirements:
   ```
   Write failing tests for user password reset:
   - User requests reset with email
   - System sends email with token
   - Token expires after 1 hour
   - User can set new password with valid token
   ```
4. Review generated tests
5. Click **Hand off to Implementer** button
6. Review implementation
7. Click **Add More Tests** as needed

#### Option B: Claude Code

```bash
# Start with test-writer
/project:test-writer Write failing tests for password reset

# After reviewing tests
/project:implementer Make the tests pass
```

#### Option C: Command Line

```bash
# Start with test-writer agent
copilot --agent=test-writer --prompt "Write failing tests for 
user password reset: request with email, token expiry 1hr, 
set new password with valid token"

# After reviewing tests, invoke implementer
copilot --agent=implementer --prompt "Make the password reset 
tests pass. Start with the request endpoint."
```

## Verification Checklist

- [ ] Test-writer only created files in `tests/`
- [ ] Tests initially failed (TDD verification)
- [ ] Implementer only created files in `src/`
- [ ] All tests now pass
- [ ] No test files were modified by implementer
- [ ] Handoff buttons appeared and functioned correctly

## Success Criteria

- [ ] Both agent files created with correct format
- [ ] Agent boundaries are clearly defined
- [ ] Complete feature implemented using TDD cycle
- [ ] Each agent stayed within its boundaries
- [ ] Natural review points between agents

## Sample Feature Ideas

If you don't have a specific feature, try one of these:

| Feature | Test Cases |
|---------|------------|
| Email validation | Valid format, invalid format, edge cases |
| Shopping cart | Add item, remove item, calculate total |
| Rate limiter | Under limit, at limit, over limit |
| Date formatter | Various formats, timezones, edge cases |

## Hints

1. **Start small** — Use a simple feature for your first TDD cycle
2. **Review tests** — Don't hand off until tests are good specifications
3. **Check boundaries** — Verify agents don't cross into forbidden directories
4. **Run tests often** — Both agents should run tests to verify state

## Next Steps

After completing this exercise:
1. Try [Exercise 4: Multi-Step Feature](../exercise-4-multi-step-feature/) for planning + TDD
2. Add a third agent (code-reviewer) to your workflow
3. Apply this pattern to a real project feature

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
