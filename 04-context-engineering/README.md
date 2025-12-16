# 04 - Context Engineering

> 📖 **Book Reference:** Chapter 10, Sections 3-4 (Static & Dynamic Context)

---

## Overview

Context Engineering is the practice of providing AI coding assistants with the right information at the right time. This is **the highest-leverage activity** for improving AI-assisted development outcomes.

Two types of context:
- **Static Context** — Project-level instructions that rarely change (AGENTS.md, rules files)
- **Dynamic Context** — Runtime information fetched on demand (MCP servers, tool integrations)

---

## Contents

| Folder | Description | Tool |
|--------|-------------|------|
| [agents-md/](./agents-md/) | AGENTS.md templates | Cross-platform |
| [cursor-rules/](./cursor-rules/) | Cursor .mdc rule files | Cursor |
| [copilot-instructions/](./copilot-instructions/) | GitHub Copilot instructions | GitHub Copilot |
| [claude/](./claude/) | CLAUDE.md templates | Claude Code |

---

## Quick Start

### Universal (All Tools)
Copy `agents-md/minimal.md` to your project root as `AGENTS.md`:
```bash
cp agents-md/minimal.md YOUR_PROJECT/AGENTS.md
```

### Cursor
Copy the `.cursor` folder:
```bash
cp -r cursor-rules/.cursor YOUR_PROJECT/
```

### GitHub Copilot
Copy the instructions structure:
```bash
cp -r copilot-instructions/.github YOUR_PROJECT/
```

### Claude Code
Copy the CLAUDE.md file:
```bash
cp claude/CLAUDE.md YOUR_PROJECT/
```

---

## File Hierarchy

```
your-project/
├── AGENTS.md                          # Universal, read by most tools
├── CLAUDE.md                          # Claude Code specific
├── .cursor/
│   └── rules/
│       ├── api-validation.mdc         # Cursor rules (MDC format)
│       ├── testing.mdc
│       └── security.mdc
└── .github/
    ├── copilot-instructions.md        # GitHub Copilot global
    └── instructions/
        ├── api.instructions.md        # Copilot path-specific
        └── tests.instructions.md
```

---

## What to Include

### Essential (40 lines)
- Project overview (tech stack, architecture)
- Key commands (build, test, run)
- Code standards (formatting, naming)
- Critical patterns (error handling, API calls)

### Recommended (100-200 lines)
- All of the above, plus:
- Directory structure explanation
- Testing requirements
- Security requirements
- Common pitfalls to avoid

### Comprehensive (300+ lines)
- All of the above, plus:
- Detailed architecture decisions
- Integration patterns
- Performance considerations
- Team conventions

---

## Tips

1. **Start minimal** — 40 lines is better than no context file
2. **Update regularly** — Context files should evolve with the project
3. **Be specific** — "Use zod for validation" beats "validate inputs"
4. **Include examples** — Show, don't just tell
5. **Layer your context** — Global rules + path-specific rules
