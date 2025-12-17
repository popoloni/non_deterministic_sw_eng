# Exercise 4 Solutions

This folder contains examples of complete multi-step feature workflows.

## Workflow Phases

| Phase | Tool | Technique |
|-------|------|-----------|
| 1. Planning | @plan / Plan Mode | Design before coding |
| 2. Test Spec | @test-writer | TDD specification |
| 3. Implementation | @implementer / background | Make tests pass |
| 4. Review | @code-reviewer | Quality verification |
| 5. Merge | Worktree merge | Integrate changes |

## Sample Plan Output

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

## Dependencies
- Existing: S3 bucket, image processing service
- New: None (uses existing infrastructure)

## Risks
- Avatar upload size limits
- Image processing latency
```

## Context Management Examples

### Claude Code

```bash
# Check context usage
/context
# Output: 45% of context window used

# Compact after milestone
/compact Completed: ProfileEditForm component with tests passing

# Clear and resume (if over 70%)
/clear
"Read docs/profile-feature.md and continue from task 4"
```

### VS Code Agent Sessions

```
Agent Sessions
--------------
[Running] Profile Feature (worktree: feature/profile)
          Files: +5 ~2 | Tests: 12 passing
          
[Local] Current workspace session
```

### Cursor

```
# New session for each phase
"Continue profile editing. Tasks 1-3 complete 
 (see src/components/ProfileEditForm.tsx). 
 Implement task 4: form validation."
```

## Verification Checklist

- [ ] Plan was created and approved before coding
- [ ] Clarifying questions were answered
- [ ] Tests were written before implementation
- [ ] Handoffs preserved context
- [ ] Context stayed under 70% of window
- [ ] Background agent (if used) completed successfully
- [ ] All tests pass
- [ ] Code review completed

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
