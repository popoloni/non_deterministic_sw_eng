# Exercise 4: Multi-Step Feature Implementation

> **Book Reference:** Chapter 10, Section "Context Flow Control"  
> **Time:** 2 hours  
> **Difficulty:** ⭐⭐⭐ Advanced

## Problem Statement

Implement a complete feature using Plan Mode, Structured Handoffs, and Context Management. This exercise combines multiple techniques for complex feature development.

## Learning Objectives

After completing this exercise, you will:
- Use Plan Mode to design before implementing
- Execute structured handoffs between agents
- Manage context window effectively
- Coordinate background and interactive agents

## Prerequisites

- Completed Exercises 1-3
- Understanding of Plan Mode in your tool
- Custom agents configured (test-writer, implementer)
- A medium-complexity feature to implement (3-5 files)

## Instructions

### Phase 1: Plan Mode (15 minutes)

#### In Claude Code (Shift+Tab twice):

```
Developer: [Shift+Tab twice to enter Plan Mode]
Developer: Add user profile editing with avatar upload

Agent: [Researches codebase, generates plan]
```

#### In VS Code with GitHub Copilot:

```
# Select "Plan" from the agents dropdown, or use @plan
Developer: @plan Add user profile editing with avatar upload

Agent: I'll analyze your codebase and create a plan.
       What questions do you have about the requirements?
       
       1. Max avatar file size?
       2. Supported image formats?
       3. Should we crop to square?

Developer: 5MB max, jpg/png only, crop to square.

Agent: [Generates implementation plan]
```

#### Expected Plan Output:

```markdown
# Implementation Plan: Profile Editing

## Summary
Add profile editing page with avatar upload, 
form validation, and optimistic updates.

## Architecture Decisions
- Store avatars in S3 (existing bucket)
- Use existing image processing service
- Optimistic UI updates with React Query

## Tasks
1. [ ] Create ProfileEditForm component
2. [ ] Add avatar upload with preview
3. [ ] Implement profile update API endpoint
4. [ ] Add form validation (Zod schemas)
5. [ ] Connect to React Query mutations
6. [ ] Write integration tests
```

### Phase 2: Structured Handoffs (30 minutes)

#### In VS Code with Copilot Agents:

```
# After plan approval, use handoff or manually invoke
Developer: @test-writer Write tests for profile editing 
           based on the plan above

# Review tests, then click "Hand off to Implementer" button
Developer: @implementer Implement task 1: ProfileEditForm

# Continue with subsequent tasks
Developer: @implementer Continue with task 2: avatar upload
```

#### In Claude Code:

```
# Hand off using custom commands or direct invocation
Developer: /project:test-writer Write tests for profile editing

# After review
Developer: /project:implementer Make the tests pass

# Use /compact between major phases
Developer: /compact preserve profile editing progress
```

### Phase 3: Context Management (Ongoing)

#### Claude Code (explicit commands):

```
# Monitor context usage
Developer: /context
# Output: 45% of context window used

# Compact after milestones
Developer: /compact Summarize: completed tasks 1-3, 
           avatar upload working, tests passing

# If context exceeds 70%, clear and restart
Developer: /clear
Developer: "Read docs/implementation-notes.md and 
           continue from task 4"
```

#### VS Code with Copilot (Agent Sessions):

1. **Monitor sessions**: Check the sessions list for status
2. **Delegate long tasks**: Use background agents
3. **Isolate parallel work**: Use Git worktree isolation

```
# Start a background agent for a long task
Developer: [In background agent] Implement tasks 4-6 from 
           the profile editing plan. Run tests after each.

# Continue interactive work in main session
Developer: [In local agent] @code-reviewer Review the 
           avatar upload implementation

# Check background agent progress via Agent Sessions list
```

#### Cursor:

```
# Start new Composer session for each major phase
Developer: Continue the profile editing feature. 
           Tasks 1-3 are complete (see src/components/
           ProfileEditForm.tsx). Implement task 4.
```

### Complete Workflow Example (VS Code + Copilot)

```
# Phase 1: Planning (local agent)
Developer: @plan Add user profile editing with avatar upload
[Answer clarifying questions]
[Review and approve plan]

# Phase 2: Test specification (local agent)
Developer: @test-writer Write tests for profile editing
[Review tests, click "Hand off to Implementer"]

# Phase 3: Implementation (background agent with worktree)
[Create background agent session]
[Select "Worktree" isolation]
Developer: Implement ProfileEditForm to pass the tests.

# Phase 4: Review (local agent, while background runs)
Developer: @code-reviewer Review the test specifications

# Phase 5: Merge and verify
[Background agent completes]
[Review worktree changes]
[Merge worktree to main workspace]
Developer: npm test -- --coverage
```

## Success Criteria

- [ ] Feature planned before implementation started
- [ ] Plan approved before coding began
- [ ] Handoffs preserved context between agents
- [ ] Context stayed under 70% throughout
- [ ] Background agent ran without blocking (if used)
- [ ] All tests pass with acceptable coverage

## Suggested Features

| Feature | Complexity | Files |
|---------|------------|-------|
| User profile editing | Medium | 4-5 |
| Comment system | Medium | 3-4 |
| Notification center | Medium-High | 5-6 |
| Search with filters | High | 6-7 |

## Hints

1. **Don't skip planning** — The plan prevents wasted implementation effort
2. **Answer clarifying questions** — Better requirements = better implementation
3. **Monitor context** — Use `/context` or session list regularly
4. **Checkpoint often** — Use `/compact` after each major milestone
5. **Use background agents** — Free your main session for review work

## Next Steps

After completing this exercise:
1. Try [Exercise 5: Subagents](../exercise-5-subagents/) for research delegation
2. Apply this workflow to a real project feature
3. Experiment with parallel background agents

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
