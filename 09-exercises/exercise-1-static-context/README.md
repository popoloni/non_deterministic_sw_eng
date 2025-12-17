# Exercise 1: Create Your First Instruction File

> **Book Reference:** Chapter 10, Section "Static Context"  
> **Time:** 30 minutes  
> **Difficulty:** ⭐ Beginner

## Problem Statement

Create your first AI instruction file in 30 minutes. This foundational exercise establishes the static context that guides AI behavior in your project.

## Learning Objectives

After completing this exercise, you will:
- Understand instruction file formats for different tools
- Know where to place instruction files
- Create a minimal but effective instruction file
- Validate that AI follows your project conventions

## Prerequisites

- One of: GitHub Copilot, Claude Code, or Cursor
- A project repository (can use starter files provided)
- Basic understanding of your project's tech stack

## Instructions

### Step 1: Choose Your Tool's Instruction File Format (5 min)

| Tool | File Location |
|------|---------------|
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Code | `CLAUDE.md` (project root) |
| Cursor | `.cursor/rules/*.mdc` or `.cursorrules` |

### Step 2: Copy the Minimal Template (5 min)

Use one of the templates in the [solution/](./solution/) folder as a starting point.

### Step 3: Customize for Your Project (15 min)

Update these sections:
- **Technology stack** — Your actual frameworks and versions
- **Commands** — Your actual build/test/lint commands
- **Conventions** — 3-5 key coding standards
- **Reference patterns** — Point to one good example in your codebase

### Step 4: Commit and Test (5 min)

1. Commit the instruction file to your repository
2. Ask the AI to implement a small feature
3. Check if it follows your conventions

## Validation Steps

Ask the AI to perform these tasks and verify behavior:

| Test | Expected Behavior |
|------|-------------------|
| Create a new component | Uses your component pattern |
| Add an API call | Uses your API client pattern |
| Write a test | Uses your testing library |

If any behavior is wrong, add more explicit guidance to your instruction file.

## Success Criteria

- [ ] Instruction file committed to repository
- [ ] AI generates code using your tech stack (not generic defaults)
- [ ] AI follows at least 3 of your stated conventions
- [ ] You identified at least 1 area to improve in future iterations

## Hints

1. **Start minimal** — A 20-line file that works beats a 200-line file that's ignored
2. **Be specific** — "Use React Query" is better than "use appropriate state management"
3. **Reference examples** — "See src/components/UserCard/" is more effective than lengthy descriptions
4. **Iterate** — Add rules when you see AI make mistakes

## Next Steps

After completing this exercise:
1. Try [Exercise 2: MCP Integration](../exercise-2-mcp-integration/) to add dynamic context
2. Add more rules as you observe AI mistakes
3. Share your instruction file with your team

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
