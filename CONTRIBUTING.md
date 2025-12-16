# Contributing to AI-Assisted Engineering Examples

Thank you for your interest in contributing! This repository serves as the companion to "Non-Deterministic Software Engineering" and we welcome community improvements.

---

## 📋 Types of Contributions

### 1. Report Outdated Examples
AI tool configurations change frequently. If you find an example that no longer works:
- Open an issue using the "Outdated Example" template
- Include the tool name, version, and error message
- Suggest the fix if you know it

### 2. Add Language Variants
Many examples are in one language but could benefit from alternatives:
- TypeScript ↔ JavaScript
- Python ↔ TypeScript
- Add the variant in the same folder with a clear suffix (e.g., `server.py` → `server.ts`)

### 3. Expand Snippets to Complete Projects
Some examples are minimal templates. To expand them:
- Keep the original minimal version
- Create a `/complete` subfolder with the expanded version
- Include all necessary files (package.json, tsconfig.json, etc.)
- Add a README explaining how to run it

### 4. Improve Documentation
- Fix typos or unclear explanations
- Add more context linking to book chapters
- Improve code comments

---

## 📝 Style Guide

### File Metadata
Every configuration file must include YAML frontmatter:

```yaml
---
tool: cursor | copilot | claude | generic
tool_version: "1.0"
last_verified: 2025-12-16
book_chapter: 10
book_section: "Section Name"
---
```

### Code Style
- **Python:** Follow PEP 8, use type hints
- **TypeScript:** Use strict mode, explicit return types
- **Markdown:** Use ATX headers (`#`), fenced code blocks with language tags

### Commit Messages
Use conventional commits:
```
feat(mcp): add PostgreSQL server example
fix(cursor): update rules for v1.2 format
docs(readme): clarify installation steps
```

---

## 🔄 Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your changes (`git checkout -b feat/my-improvement`)
3. **Make your changes** following the style guide
4. **Test your changes** (run any applicable tests)
5. **Update metadata** (bump `last_verified` date if updating existing files)
6. **Submit a PR** with a clear description

### PR Checklist
- [ ] Follows the style guide
- [ ] Includes/updates YAML frontmatter metadata
- [ ] Links to relevant book chapter in README
- [ ] Tests pass (if applicable)
- [ ] No sensitive data or API keys included

---

## 🏷️ Issue Labels

| Label | Description |
|-------|-------------|
| `outdated` | Example no longer works with current tool version |
| `help wanted` | Looking for community contribution |
| `good first issue` | Simple fix, good for newcomers |
| `enhancement` | New feature or expansion |
| `documentation` | Documentation improvement |
| `python-variant` | Needs Python version |
| `typescript-variant` | Needs TypeScript version |

---

## 📞 Questions?

If you're unsure about anything, open an issue with the "Question" label. We're happy to help!

---

## 🙏 Thank You

Every contribution helps readers learn AI-assisted engineering more effectively. We appreciate your time and effort!
