# Exercise 6: Background Agents with Isolation

> **Book Reference:** Chapter 10, Section "Multi-Agent Workflows"  
> **Time:** 1 hour  
> **Difficulty:** ⭐⭐⭐ Advanced

## Problem Statement

Run parallel background agents using Git worktree isolation. This exercise demonstrates executing multiple independent tasks simultaneously without file conflicts.

## Learning Objectives

After completing this exercise, you will:
- Create background agent sessions
- Use Git worktree isolation for parallel work
- Monitor multiple agents simultaneously
- Merge worktree changes cleanly

## Prerequisites

- Completed Exercises 1-5
- VS Code with GitHub Copilot (1.107+)
- Git repository with clean working directory
- Understanding of Git worktrees

## Instructions

### Scenario

You need to implement three independent features in parallel:
- **Feature A:** User notifications
- **Feature B:** Export functionality
- **Feature C:** Dashboard widgets

### Step 1: Identify Parallel Tasks (10 minutes)

Select 2-3 independent features that modify different files:

| Feature | Files Affected | Independent? |
|---------|---------------|--------------|
| Notifications | src/notifications/, tests/notifications/ | ✅ |
| Export | src/export/, tests/export/ | ✅ |
| Dashboard | src/dashboard/, tests/dashboard/ | ✅ |

**Key:** Features should not modify the same files.

### Step 2: Create Background Agent Sessions (15 minutes)

#### Session 1: User Notifications

1. In VS Code, open Chat view
2. Click **New Background Agent** (or Command Palette: `Chat: New Background Agent`)
3. Select isolation mode: **Worktree**
4. Optionally select custom agent: **software-engineer**
5. Enter prompt:

```
Implement user notifications feature:
- Add notification model to database
- Create notification service
- Add API endpoints (GET /notifications, POST /notifications/read)
- Write tests for all components

Run tests after implementation. Create PR when complete.
```

#### Session 2: Export Functionality

Repeat the process with:

```
Implement data export feature:
- Add export service supporting CSV and JSON
- Create /export endpoint with format parameter
- Add rate limiting (max 10 exports per hour)
- Write integration tests

Run tests after implementation.
```

#### Session 3: Dashboard Widgets

Repeat with:

```
Implement dashboard widget system:
- Create WidgetContainer component
- Add drag-and-drop reordering
- Persist widget layout to user preferences
- Write component tests with React Testing Library
```

### Step 3: Monitor Progress (Ongoing)

In the Chat view, the Agent Sessions list shows:

```
Agent Sessions
--------------
[Running] User Notifications (worktree: feature/notifications)
          Files: +5 ~2 | Tests: 12 passing
          
[Running] Export Functionality (worktree: feature/export)  
          Files: +3 ~1 | Tests: 8 passing
          
[Running] Dashboard Widgets (worktree: feature/widgets)
          Files: +4 ~0 | Tests: running...
          
[Local] Current workspace session
```

You can continue interactive work in the main session while background agents run.

### Step 4: Review and Merge (35 minutes)

When a background agent completes:

1. Click on the session in Agent Sessions list
2. Review the changes in the worktree
3. Use Source Control view to see the Git worktree
4. Either:
   - Click **Apply Changes** to merge directly to workspace
   - Create a PR from the worktree branch for team review
5. Delete the worktree after merging

### Handling Conflicts

If two agents need to modify the same file:

```bash
# Check for potential conflicts before merging
git diff feature/notifications feature/export -- src/models/

# If conflicts exist, merge sequentially:
# 1. Merge first worktree
git merge feature/notifications

# 2. Rebase second worktree
git checkout feature/export
git rebase main

# 3. Resolve conflicts and complete merge
```

**Best practice:** Design tasks to modify different files.

### Attaching Context to Background Agents

Background agents support rich context attachment:

```
# Attach a problem from the Problems panel
Developer: Fix this issue [drag problem from Problems panel]

# Attach a symbol definition
Developer: Refactor this function [attach symbol from Outline]

# Attach search results
Developer: Update all files using this pattern 
           [attach search results]

# Attach git commit for reference
Developer: Apply this fix to the other service 
           [attach commit reference]
```

## Verification Checklist

- [ ] Multiple background agents created with Worktree isolation
- [ ] Each worktree contains isolated changes
- [ ] Agents ran simultaneously without blocking each other
- [ ] Progress monitored via Agent Sessions list
- [ ] Changes reviewed before merging
- [ ] All worktree changes merged cleanly
- [ ] All tests pass after merging all features
- [ ] Total time less than sequential execution

## Success Criteria

- [ ] At least 2 background agents ran in parallel
- [ ] Git worktree isolation was used
- [ ] No file conflicts between agents
- [ ] All features implemented and tested
- [ ] Merge completed successfully
- [ ] Time saved compared to sequential work

## Time Comparison

| Approach | Feature A | Feature B | Feature C | Total |
|----------|-----------|-----------|-----------|-------|
| Sequential | 30 min | 30 min | 30 min | 90 min |
| Parallel | 30 min | — | — | ~35 min |

**Expected savings:** 50-60% time reduction.

## Hints

1. **Check file overlap** — Ensure features modify different files
2. **Use worktree mode** — "Local" mode causes conflicts
3. **Review before merge** — Don't auto-merge blindly
4. **Run final tests** — Verify integration after all merges

## Next Steps

After completing this exercise:
1. Apply parallel execution to real project work
2. Experiment with 4+ parallel agents
3. Create templates for common parallel patterns

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
