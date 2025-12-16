# React Class to Hooks Migration Example

> 📖 **Book Reference:** Chapter 7, Pattern 12 - Migration as Learning

---

## Overview

This folder contains a complete before/after example of migrating React class components to functional components with hooks. This is a practical demonstration of the **Migration as Learning** pattern.

---

## The Migration as Learning Process

From the book:

> "Migrations are not just chores to delegate—they're learning opportunities to understand your system deeply. The pattern is: Learn manually → Teach AI → Scale with AI → Continue learning from edge cases."

### Step 1: Establish the Pattern (Manual Learning)

**Don't start by telling AI to migrate everything.**

Instead:
1. Pick ONE representative file
2. Manually migrate it yourself (this is the learning)
3. Document what changed
4. This becomes your example AND your understanding

### Step 2: Document Your Learning

See [MIGRATION_PATTERN.md](./MIGRATION_PATTERN.md) for the documented transformation rules.

### Step 3: Create the AI Prompt Template

See [MIGRATION_PROMPT.md](./MIGRATION_PROMPT.md) for the reusable prompt.

### Step 4: Verify

Apply prompt to ONE more file and verify:
- [ ] Code compiles
- [ ] Tests pass
- [ ] Behavior unchanged
- [ ] No regressions
- [ ] AI followed the pattern correctly

---

## Files

> **Note:** These files use `// @ts-nocheck` since they're demonstration code without `node_modules` installed. 
> To enable full type checking, run `npm install` in this folder.

### Before (Class Components)

| File | Description |
|------|-------------|
| [before/UserProfile.tsx](./before/UserProfile.tsx) | User profile with data fetching |
| [before/SearchForm.tsx](./before/SearchForm.tsx) | Search form with controlled inputs |
| [before/DataTable.tsx](./before/DataTable.tsx) | Complex table with sorting, pagination |

### After (Hooks-Based)

| File | Description |
|------|-------------|
| [after/UserProfile.tsx](./after/UserProfile.tsx) | User profile with useState, useEffect |
| [after/SearchForm.tsx](./after/SearchForm.tsx) | Search form with controlled hooks |
| [after/DataTable.tsx](./after/DataTable.tsx) | Table with custom hooks |

### Templates

| File | Description |
|------|-------------|
| [MIGRATION_PATTERN.md](./MIGRATION_PATTERN.md) | Documented transformation rules |
| [MIGRATION_PROMPT.md](./MIGRATION_PROMPT.md) | Reusable AI prompt template |

---

## Key Transformations

| Class Pattern | Hooks Equivalent |
|---------------|------------------|
| `state = { ... }` | `useState()` for each variable |
| `componentDidMount` | `useEffect(() => {}, [])` |
| `componentDidUpdate` | `useEffect(() => {}, [deps])` |
| `componentWillUnmount` | `useEffect(() => { return cleanup }, [])` |
| `this.setState()` | `setStateVar()` |
| Class methods | `useCallback()` or regular functions |
| `this.props` | Destructured props |

---

## Learning Outcomes

After completing this migration manually, you will understand:

1. **Why hooks are better** for this use case
2. **The transformation pattern** for systematic conversion
3. **Edge cases** (cleanup, dependencies, stale closures)
4. **Common mistakes** to avoid

---

## Time Savings

From the book's case study:

| Approach | Time | Learning |
|----------|------|----------|
| Fully Manual | 6 weeks | High |
| Fully AI (no learning) | 2 weeks | None |
| **Migration as Learning** | **3 weeks** | **High** |

The Migration as Learning approach saves ~50% time while preserving all learning.

---

## Related Patterns

- **Pattern 11** (Legacy Code Navigation): Understand before migrating
- **Pattern 4** (Small Verifiable Chunks): Migrate in small batches
- **Pattern 2** (Test-Driven AI Development): Tests verify correctness
- **Pattern 8** (Learning Loop Preservation): The core principle
