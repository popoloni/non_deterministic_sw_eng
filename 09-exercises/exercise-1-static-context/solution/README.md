# Exercise 1 Solutions

This folder contains sample instruction files for different AI coding tools.

## Files

| File | Tool | Description |
|------|------|-------------|
| [copilot-instructions.md](./copilot-instructions.md) | GitHub Copilot | Full-featured example |
| [CLAUDE.md](./CLAUDE.md) | Claude Code | Concise format example |
| [project.mdc](./project.mdc) | Cursor | MDC format with globs |

## Example Project Context

These solutions assume a **Customer Portal** project with:
- **Frontend:** React 18 with TypeScript
- **Backend:** Node.js 20 / Express
- **Database:** PostgreSQL
- **Testing:** Jest + React Testing Library

Customize these templates for your actual project.

## Validation Commands

After setting up your instruction file, test with:

```
# Ask AI to create a component
"Create a UserProfile component that displays user avatar and name"

# Check:
# ✅ Uses functional component (not class)
# ✅ Uses TypeScript with proper types
# ✅ Follows your naming conventions

# Ask AI to add an API call
"Add a function to fetch user profile from /api/users/:id"

# Check:
# ✅ Uses your apiClient pattern (if specified)
# ✅ Handles errors appropriately
# ✅ Uses TypeScript types

# Ask AI to write a test
"Write tests for the UserProfile component"

# Check:
# ✅ Uses React Testing Library (not Enzyme)
# ✅ Follows your test structure conventions
# ✅ Tests meaningful behavior
```

## Common Issues

| Issue | Solution |
|-------|----------|
| AI ignores instruction file | Check file location is correct for your tool |
| AI uses wrong testing library | Add explicit "Use X, not Y" statements |
| AI doesn't follow patterns | Add "See: src/path/example.ts" references |
| Instructions too verbose | AI may skip long files; keep under 100 lines |

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
