# Exercise 2: Add MCP to Your Workflow

> **Book Reference:** Chapter 10, Section "Dynamic Context"  
> **Time:** 1 hour  
> **Difficulty:** ⭐⭐ Intermediate

## Problem Statement

Add Model Context Protocol (MCP) servers to your workflow in 1 hour. This exercise establishes dynamic context that provides real-time information to AI assistants.

## Learning Objectives

After completing this exercise, you will:
- Configure MCP servers for your AI tool
- Use Context7 for framework documentation
- Set up auto-invoke rules for MCP tools
- Verify AI can access current documentation

## Prerequisites

- Completed [Exercise 1: Static Context](../exercise-1-static-context/)
- Node.js 18+ installed (for npx)
- One of: GitHub Copilot, Claude Code, or Cursor

## Instructions

### Phase 1: Start with Context7 (15 minutes)

Context7 provides up-to-date framework documentation to AI assistants.

#### For Claude Code

```bash
# Add Context7 via Claude Code's mcp add command
claude mcp add context7 -- npx -y @upstash/context7-mcp

# Or add to .mcp.json in project root:
```

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

#### For Cursor

Add to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

#### For GitHub Copilot

1. Navigate to your repository on GitHub
2. Go to **Settings** > **Copilot** > **Coding agent**
3. In the MCP configuration section, add JSON:

```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

4. Click **Save** to validate the configuration
5. For secrets, add them with names prefixed `COPILOT_MCP_`

### Phase 2: Add Filesystem MCP (15 minutes)

Add access to your project documentation:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "project-docs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "--root", "./docs"]
    }
  }
}
```

### Phase 3: Test the Configuration (15 minutes)

Ask the AI:

```
"What's new in Next.js 15 App Router? use context7"
```

**Expected:** Current documentation from source, not stale training data.

```
"What is our API authentication approach? Check project docs."
```

**Expected:** Information from your `./docs` folder.

### Phase 4: Set Up Auto-Invoke Rules (15 minutes)

#### For Claude Code (add to `CLAUDE.md`):

```markdown
Always use context7 when I need code generation, 
setup or configuration steps, or library/API documentation.
```

#### For Cursor (add to `.cursor/rules/mcp.mdc`):

```markdown
---
description: MCP usage rules
alwaysApply: true
---
Use context7 MCP automatically for framework documentation.
```

#### For GitHub Copilot (add to `.github/copilot-instructions.md`):

```markdown
When generating code that uses external libraries, 
use the context7 MCP tool to fetch current documentation
before writing implementation code.
```

## Success Criteria

- [ ] MCP configuration file exists and is valid JSON
- [ ] Context7 server responds to queries
- [ ] AI can answer questions about current framework versions
- [ ] AI doesn't hallucinate outdated APIs
- [ ] Auto-invoke rules are configured

## Validation Tests

| Test | Expected Result |
|------|-----------------|
| Ask about Next.js 15 features | Current docs, not 2023 info |
| Ask about your project architecture | Reads from ./docs |
| Generate React code | Uses current React patterns |
| Ask about deprecated API | Warns about deprecation |

## Hints

1. **Restart your AI tool** after changing MCP configuration
2. **Check the MCP server logs** if queries fail
3. **Start with one server** — Context7 alone provides huge value
4. **Test incrementally** — Verify each server before adding more

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP server not found | Ensure Node.js 18+ installed |
| Server doesn't respond | Check JSON syntax in config file |
| Wrong documentation returned | Verify framework name spelling |
| Filesystem access denied | Check `--root` path is correct |

## Next Steps

After completing this exercise:
1. Try [Exercise 3: TDD Workflow](../exercise-3-tdd-workflow/) to use multi-agent patterns
2. Explore [MCP Server Templates](../../05-mcp-servers/templates/) for custom servers
3. Build a custom MCP server for your company's internal docs

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
