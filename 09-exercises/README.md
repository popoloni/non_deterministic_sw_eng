# 09 - Exercises

> 📖 **Book Reference:** Appendix C (Exercise Solutions)

---

## Overview

This folder contains hands-on exercises from the book, each with problem statements, starter files, sample solutions, and evaluation rubrics.

## Exercise Index

| Exercise | Difficulty | Time | Skills Practiced |
|----------|------------|------|------------------|
| [Exercise 1: Static Context Setup](./exercise-1-static-context/) | ⭐ Beginner | 30 min | Instruction files, project conventions |
| [Exercise 2: MCP Integration](./exercise-2-mcp-integration/) | ⭐⭐ Intermediate | 1 hour | Dynamic context, MCP servers |
| [Exercise 3: TDD Workflow](./exercise-3-tdd-workflow/) | ⭐⭐ Intermediate | 1 hour | Multi-agent, test-first development |
| [Exercise 4: Multi-Step Feature](./exercise-4-multi-step-feature/) | ⭐⭐⭐ Advanced | 2 hours | Plan mode, handoffs, context management |
| [Exercise 5: Subagents](./exercise-5-subagents/) | ⭐⭐⭐ Advanced | 1 hour | Subagent delegation, research isolation |
| [Exercise 6: Background Agents](./exercise-6-background-agents/) | ⭐⭐⭐ Advanced | 1 hour | Parallel execution, Git worktree isolation |

## Recommended Learning Path

```
┌─────────────────────────────────────────────────────────────────┐
│                      BEGINNER PATH                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Exercise 1  │ →  │ Exercise 2  │ →  │ Exercise 3  │         │
│  │   Static    │    │     MCP     │    │     TDD     │         │
│  │  Context    │    │ Integration │    │  Workflow   │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│        30 min            1 hour            1 hour               │
│                                                                 │
│                        Total: 2.5 hours                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ADVANCED PATH                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Exercise 4  │ →  │ Exercise 5  │ →  │ Exercise 6  │         │
│  │ Multi-Step  │    │  Subagents  │    │ Background  │         │
│  │  Feature    │    │             │    │   Agents    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│        2 hours           1 hour            1 hour               │
│                                                                 │
│                        Total: 4 hours                           │
└─────────────────────────────────────────────────────────────────┘
```

## Exercise Structure

Each exercise folder contains:

```
exercise-N-name/
├── README.md           # Problem statement and instructions
├── starter/            # Starting files for the exercise
│   └── ...
├── solution/           # Reference solution
│   └── ...
└── rubric.md           # Evaluation criteria
```

## Prerequisites

Before starting exercises:

1. **Development Environment**
   - VS Code or Cursor installed
   - GitHub Copilot, Claude Code, or Cursor AI configured
   - Git repository initialized

2. **Book Context**
   - Read Chapter 10 (Tools and Practices)
   - Understand the 70% rule (Pattern 8)
   - Familiar with context engineering concepts

3. **Tool Access**
   - At least one AI coding assistant active
   - MCP server capability (for Exercise 2+)
   - Custom agent support (for Exercise 3+)

## Success Criteria

Each exercise has specific success criteria, but general principles:

| Criteria | What It Means |
|----------|---------------|
| ✅ AI followed conventions | Instruction files were effective |
| ✅ No hallucinated APIs | Dynamic context worked correctly |
| ✅ Agents stayed in boundaries | Multi-agent isolation succeeded |
| ✅ Context stayed under 70% | Context management applied |
| ✅ Human checkpoints honored | Validation gates respected |

## Evaluation Rubrics

Each exercise includes a rubric with three levels:

| Level | Description |
|-------|-------------|
| 🥉 Bronze | Completed the exercise, basic functionality |
| 🥈 Silver | Met all success criteria, clean implementation |
| 🥇 Gold | Extended solution, added improvements |

## Tips for Success

1. **Read the problem statement completely** before starting
2. **Set up instruction files first** — they're foundational
3. **Validate incrementally** — don't wait until the end
4. **Use the rubric** to self-assess before checking solutions
5. **Compare with solutions** to learn alternative approaches

## Related Resources

- [Context Engineering](../04-context-engineering/) — AGENTS.md templates
- [MCP Servers](../05-mcp-servers/) — Server examples for Exercise 2
- [Custom Agents](../06-custom-agents/) — Agent templates for Exercise 3+
- [Enterprise Workflow](../07-enterprise-workflow/) — Checklists and handoffs
- [Maturity Model](../10-reference/maturity-model.md) — Track your progression

---

*Based on practical exercises from "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
