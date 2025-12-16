# 03 - Migrations

> 📖 **Book Reference:** Chapter 7, Pattern 12 (Migration as Learning)

---

## Overview

AI excels at code migrations — converting codebases from one pattern, framework, or language to another. This pattern leverages AI's ability to:

- Recognize patterns across large codebases
- Apply consistent transformations
- Handle boilerplate conversion automatically
- Identify edge cases that need human attention

---

## Contents

| Folder | Description |
|--------|-------------|
| [react-class-to-hooks/](./react-class-to-hooks/) | Complete React class → hooks migration example |

---

## Migration Strategy

### Phase 1: Analysis
Ask AI to analyze the codebase and identify:
- Components/modules to migrate
- Dependencies between them
- Risk assessment for each

### Phase 2: Pilot Migration
- Select a simple, isolated component
- Perform full migration with AI assistance
- Validate thoroughly
- Document lessons learned

### Phase 3: Systematic Migration
- Migrate in dependency order (leaves first)
- Run full test suite after each migration
- Keep old and new code in parallel during transition

### Phase 4: Cleanup
- Remove deprecated code
- Update documentation
- Archive migration prompts for future reference

---

## Example: React Class to Hooks

See [react-class-to-hooks/](./react-class-to-hooks/) for a complete before/after example.

### Prompt Template

```
Migrate the following React class component to a functional component with hooks:

[Paste class component]

Requirements:
- Use useState for all state variables
- Use useEffect for lifecycle methods
- Use useCallback for methods passed as props
- Preserve all existing functionality
- Maintain the same prop interface
- Add TypeScript types if not present
```

---

## Common Migrations

| From | To | AI Capability |
|------|-----|---------------|
| React Class → Hooks | ⭐⭐⭐⭐⭐ | Excellent |
| JavaScript → TypeScript | ⭐⭐⭐⭐⭐ | Excellent |
| REST → GraphQL | ⭐⭐⭐⭐ | Very Good |
| Callbacks → Async/Await | ⭐⭐⭐⭐⭐ | Excellent |
| SQL → ORM | ⭐⭐⭐ | Good |
| Monolith → Microservices | ⭐⭐ | Needs guidance |

---

## Tips

1. **Migrate tests first** — Having passing tests makes code migration safer
2. **Small batches** — Migrate one component at a time
3. **Preserve behavior** — Focus on transformation, not improvement
4. **Document decisions** — Record why certain approaches were chosen
