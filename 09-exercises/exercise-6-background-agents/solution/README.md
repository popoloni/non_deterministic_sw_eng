# Exercise 6 Solutions

This folder contains examples and guidance for parallel background agent execution.

## Scenario Overview

Three independent features implemented in parallel:

| Feature | Branch | Files | Status |
|---------|--------|-------|--------|
| Notifications | feature/notifications | src/notifications/ | Complete |
| Export | feature/export | src/export/ | Complete |
| Dashboard | feature/widgets | src/dashboard/ | Complete |

## Background Agent Setup

### Session 1: Notifications

```
Agent: software-engineer
Isolation: Worktree
Branch: feature/notifications

Prompt:
Implement user notifications feature:
- Add notification model to database
- Create notification service
- Add API endpoints (GET /notifications, POST /notifications/read)
- Write tests for all components
Run tests after implementation.
```

### Session 2: Export

```
Agent: software-engineer
Isolation: Worktree
Branch: feature/export

Prompt:
Implement data export feature:
- Add export service supporting CSV and JSON
- Create /export endpoint with format parameter
- Add rate limiting (max 10 exports per hour)
- Write integration tests
```

### Session 3: Dashboard

```
Agent: software-engineer
Isolation: Worktree
Branch: feature/widgets

Prompt:
Implement dashboard widget system:
- Create WidgetContainer component
- Add drag-and-drop reordering
- Persist widget layout to user preferences
- Write component tests
```

## Monitoring Progress

Agent Sessions view shows:

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

## Merge Process

### Option A: Apply Changes (Quick)

1. Click session in Agent Sessions list
2. Click "Apply Changes"
3. Changes merged to main workspace
4. Delete worktree

### Option B: Create PR (Team Review)

1. Click session in Agent Sessions list
2. Click "Create PR"
3. PR created from worktree branch
4. Team reviews
5. Merge PR on GitHub
6. Pull changes locally

## Conflict Resolution

```bash
# Check for conflicts before merging
git diff feature/notifications feature/export -- src/

# Sequential merge if conflicts
git merge feature/notifications
git checkout feature/export
git rebase main
# Resolve conflicts
git rebase --continue
git merge feature/export
```

## Time Savings

| Metric | Sequential | Parallel | Savings |
|--------|------------|----------|---------|
| Total time | 90 min | 35 min | 61% |
| Developer attention | 90 min | 20 min | 78% |

## Verification Checklist

- [ ] All three agents created with Worktree isolation
- [ ] Agents ran simultaneously
- [ ] No file conflicts
- [ ] All tests pass
- [ ] Time < sequential time

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
