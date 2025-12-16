---
tool: context7
tool_version: "1.0"
last_verified: 2025-12-16
book_chapter: 10
book_section: "Dynamic Context Engineering"
---

# Context7 Setup Guide

> 📖 **Book Reference:** Chapter 10, Section 4 (Dynamic Context Engineering)

Context7 is an MCP server that fetches current, version-specific documentation from source repositories and injects it into your LLM's context window.

## Problem It Solves

AI assistants rely on potentially stale training data for frameworks and libraries, leading to:
- Hallucinated APIs that don't exist
- Deprecated methods that no longer work
- Missing features added after training cutoff

## Installation

### Via npx (Recommended)

No installation required—runs directly:

```bash
npx @anthropic/context7-mcp
```

### Via npm (Global)

```bash
npm install -g @anthropic/context7-mcp
```

## Configuration

### For Claude Desktop

Add to your Claude Desktop configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["@anthropic/context7-mcp"]
    }
  }
}
```

### For Cursor

Create `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["@anthropic/context7-mcp"]
    }
  }
}
```

## Usage

### Method 1: Explicit Invocation

Add "use context7" to your prompts:

```
Create a Next.js middleware that checks for a valid JWT 
in cookies and redirects unauthenticated users to /login.
use context7
```

### Method 2: Auto-Invocation via Rules

Create a Cursor rule (`.cursor/rules/context7.mdc`):

```yaml
---
description: Auto-invoke Context7 for framework questions
globs: "**/*.{ts,tsx,js,jsx}"
alwaysApply: false
---
# Framework Documentation

When generating code that uses external frameworks or libraries,
automatically fetch current documentation using context7.

Especially important for:
- Next.js (App Router vs Pages Router differences)
- React (Server Components, new hooks)
- Vue 3 (Composition API)
- Astro
- Any rapidly-evolving framework
```

## Supported Libraries

Context7 supports thousands of libraries. Some popular ones:

| Library | ID | Notes |
|---------|-----|-------|
| Next.js | `nextjs` | App Router, Server Components |
| React | `react` | Hooks, Server Components |
| Vue | `vue` | Composition API |
| Astro | `astro` | Content Collections |
| TailwindCSS | `tailwindcss` | v3/v4 differences |
| Prisma | `prisma` | Schema, Client |
| tRPC | `trpc` | v10/v11 differences |

## Example Workflow

### Without Context7
```
Developer: "Create a Next.js 15 server action"
AI: [Uses training data from Next.js 13]
AI: Creates outdated code pattern
Result: Code doesn't work with current Next.js
```

### With Context7
```
Developer: "Create a Next.js 15 server action. use context7"
AI: [Context7 fetches Next.js 15 docs]
AI: Creates code using current patterns
Result: Code works correctly
```

## Real-World Impact

From ThoughtWorks teams:
> "Context7 has greatly reduced code hallucinations and reliance on stale training data."

Most valuable with rapidly-evolving frameworks where training data goes stale quickly.

## Troubleshooting

### "Library not found"
- Check the library ID on [context7.com](https://context7.com)
- Some libraries use different IDs than package names

### Slow responses
- Context7 fetches docs in real-time
- First request for a library may be slower
- Subsequent requests are cached

### Missing API
- Context7 pulls from official documentation
- If API is undocumented upstream, it won't appear
- File an issue with Context7 or the library maintainers

## Related Resources

- [Context7 Website](https://context7.com)
- [MCP Specification](https://modelcontextprotocol.io)
- [Company Docs Server](../company-docs-server/) - Custom MCP example
