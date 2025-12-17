# Exercise 2 Solutions

This folder contains MCP configuration files for different AI coding tools.

## Files

| File | Tool | Description |
|------|------|-------------|
| [claude-mcp.json](./claude-mcp.json) | Claude Code | .mcp.json for project root |
| [cursor-mcp.json](./cursor-mcp.json) | Cursor | .cursor/mcp.json format |
| [copilot-mcp.json](./copilot-mcp.json) | GitHub Copilot | Repository settings format |
| [auto-invoke-rules/](./auto-invoke-rules/) | All tools | Rules for automatic MCP usage |

## Configuration Placement

| Tool | Config Location | Scope |
|------|-----------------|-------|
| Claude Code | `.mcp.json` (project root) | Project |
| Claude Code | `~/.claude/mcp.json` | Global |
| Cursor | `.cursor/mcp.json` | Project |
| Cursor | `~/.cursor/mcp.json` | Global |
| GitHub Copilot | Repository Settings > Copilot | Repository |

## Verification Commands

### Test Context7

```
# In any AI tool:
"What's new in React 19? use context7"

# Expected: Current React 19 documentation
# Not expected: Outdated React 18 info
```

### Test Filesystem MCP

```
# In any AI tool:
"Summarize our API design principles from the docs folder"

# Expected: Content from your ./docs directory
# Not expected: Generic API principles
```

### Test Auto-Invoke

```
# Without explicitly mentioning MCP:
"Generate a Next.js App Router page component"

# Expected: Uses current App Router patterns
# With auto-invoke, AI should use context7 automatically
```

## Common Configurations

### Minimal (Context7 only)

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

### Standard (Context7 + Docs)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "docs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", 
               "--root", "./docs"]
    }
  }
}
```

### Extended (Multiple Sources)

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "docs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "--root", "./docs"]
    },
    "examples": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "--root", "./examples"]
    }
  }
}
```

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
