# 05 - MCP Servers

> 📖 **Book Reference:** Chapter 10, Section 5 (Context Flow with MCP)

---

## Overview

The **Model Context Protocol (MCP)** enables AI assistants to access external tools and data sources at runtime. This transforms AI from a static code generator into a dynamic assistant that can:

- Query your documentation wikis
- Access database schemas
- Call internal APIs
- Read file systems
- Execute approved operations

---

## Contents

| Folder | Description |
|--------|-------------|
| [company-docs-server/](./company-docs-server/) | Complete FastMCP server example (Python) |
| [setup-guides/](./setup-guides/) | Configuration guides for popular MCP servers |

### Company Docs Server
A fully-functional MCP server demonstrating:
- **Resources:** Documentation, ADRs, onboarding guides
- **Tools:** Search docs, get ADRs, service info, naming validation
- **Prompts:** Code review checklist, architecture review

| File | Purpose |
|------|---------|
| [server.py](./company-docs-server/server.py) | Main server implementation (~350 lines) |
| [requirements.txt](./company-docs-server/requirements.txt) | Python dependencies |
| [pyproject.toml](./company-docs-server/pyproject.toml) | Modern Python packaging |
| [config/](./company-docs-server/config/) | Tool configuration examples |
| [README.md](./company-docs-server/README.md) | Installation and usage guide |

### Setup Guides
| Guide | Description |
|-------|-------------|
| [context7-setup.md](./setup-guides/context7-setup.md) | Framework documentation on demand |

---

## Quick Start

### 1. Install the Example Server

```bash
cd company-docs-server
pip install -r requirements.txt
```

### 2. Configure Your AI Tool

**For Claude Desktop:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "company-docs": {
      "command": "python",
      "args": ["/full/path/to/company-docs-server/server.py"]
    }
  }
}
```

**For Cursor:**
Create `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "company-docs": {
      "command": "python",
      "args": ["./05-mcp-servers/company-docs-server/server.py"]
    }
  }
}
```

### 3. Restart Your AI Tool

The MCP server will be available in your next session.

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI Assistant  │────▶│   MCP Server    │────▶│  Data Source    │
│  (Claude/Cursor)│     │  (Python/Node)  │     │ (Wiki/DB/API)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        │   MCP Protocol        │   Your Code
        │   (JSON-RPC)          │   (Any language)
        ▼                       ▼
   Standardized            Custom Logic
   Communication           & Integration
```

---

## MCP Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Resources** | Static data the AI can read | Architecture docs, API schemas |
| **Tools** | Functions the AI can call | Search docs, query database |
| **Prompts** | Pre-defined prompt templates | Code review checklist |

---

## Popular MCP Servers

| Server | Purpose | Setup Guide |
|--------|---------|-------------|
| Context7 | Library documentation | [setup-guides/context7-setup.md](./setup-guides/context7-setup.md) |
| Filesystem | Local file access | Built-in |
| GitHub | Repository operations | Official |
| PostgreSQL | Database queries | Official |

---

## Building Your Own

See [company-docs-server/](./company-docs-server/) for a complete example using FastMCP.

Key components:
1. **Resources** — Define what data is available
2. **Tools** — Define what actions can be performed
3. **Configuration** — JSON config for each AI tool

---

## Tips

1. **Start with official servers** — Use community MCP servers before building custom
2. **Limit scope** — Each server should do one thing well
3. **Add logging** — Debug MCP issues with verbose logging
4. **Test standalone** — Verify server works before connecting to AI
5. **Security first** — Never expose sensitive operations without authentication
