# Auto-Invoke Rules

Add these rules to your instruction files to automatically invoke MCP tools.

## Claude Code

Add to `CLAUDE.md`:

```markdown
Always use context7 when I need code generation, 
setup or configuration steps, or library/API documentation.
```

## Cursor

Create `.cursor/rules/mcp.mdc`:

```markdown
---
description: MCP usage rules
alwaysApply: true
---
Use context7 MCP automatically for framework documentation.
```

## GitHub Copilot

Add to `.github/copilot-instructions.md`:

```markdown
When generating code that uses external libraries, 
use the context7 MCP tool to fetch current documentation
before writing implementation code.
```

## Verification

Test that auto-invoke is working:

```
# Don't mention MCP explicitly:
"Generate a React Server Component for user profiles"

# AI should automatically use context7 to fetch
# current RSC documentation before generating code
```
