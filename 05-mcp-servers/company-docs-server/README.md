# Company Docs MCP Server

> 📖 **Book Reference:** Chapter 10, Section 4 (Dynamic Context Engineering)

A complete Model Context Protocol (MCP) server example that provides AI assistants with access to company documentation, architecture decisions, and searchable knowledge base.

## Features

### Resources (Read-only data)
| URI | Description |
|-----|-------------|
| `docs://architecture` | System architecture overview |
| `docs://api-standards` | API design conventions |
| `docs://coding-standards` | Coding standards and best practices |
| `docs://onboarding` | Developer onboarding guide |
| `adr://list` | List of Architecture Decision Records |

### Tools (Executable functions)
| Tool | Description |
|------|-------------|
| `search_docs(query)` | Search all documentation |
| `get_adr(adr_id)` | Retrieve specific ADR |
| `get_service_info(service_name)` | Get service details |
| `check_naming_convention(name, context)` | Validate naming standards |

### Prompts (Reusable templates)
| Prompt | Description |
|--------|-------------|
| `code_review_checklist` | Standard code review checklist |
| `architecture_review` | Architecture review prompts |

## Quick Start

### 1. Install Dependencies

```bash
cd company-docs-server
pip install -r requirements.txt
```

Or with pip editable install:
```bash
pip install -e .
```

### 2. Test the Server

```bash
python server.py
```

You should see:
```
Starting Company Docs MCP Server...
Available resources:
  - docs://architecture
  - docs://api-standards
  ...
Server running. Press Ctrl+C to stop.
```

### 3. Configure Your AI Tool

#### For Claude Desktop

Copy the config to your Claude configuration:

**macOS:**
```bash
cp config/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
copy config\claude_desktop_config.json "$env:APPDATA\Claude\claude_desktop_config.json"
```

Edit the file to set the correct path to `server.py`.

#### For Cursor

Copy to your project:
```bash
mkdir -p .cursor
cp config/cursor_mcp.json .cursor/mcp.json
```

### 4. Restart Your AI Tool

The MCP server will be available in your next session.

## Customization

### Adding Your Own Documentation

Replace the `DOCS_STORE` dictionary in `server.py` with your actual documentation:

```python
DOCS_STORE = {
    "architecture": load_from_file("docs/architecture.md"),
    "api-standards": fetch_from_wiki("https://wiki.company.com/api"),
    # ... add more sources
}
```

### Adding Database Integration

```python
from sqlalchemy import create_engine

engine = create_engine(os.environ["DATABASE_URL"])

@mcp.tool()
def get_schema(table_name: str) -> str:
    """Returns the schema for a database table."""
    # Query information_schema
    ...
```

### Adding External API Integration

```python
import httpx

@mcp.tool()
def search_confluence(query: str) -> str:
    """Searches Confluence for documentation."""
    client = httpx.Client(
        base_url="https://company.atlassian.net/wiki/rest/api",
        headers={"Authorization": f"Bearer {os.environ['CONFLUENCE_TOKEN']}"}
    )
    response = client.get("/content/search", params={"cql": f"text ~ '{query}'"})
    # Format and return results
    ...
```

## Production Considerations

### Security
- Run MCP servers locally via stdio transport when possible
- Use environment variables for secrets
- Implement rate limiting for external API calls
- Audit tool outputs before acting on them

### Performance
- Cache frequently accessed documentation
- Use vector embeddings for semantic search
- Implement pagination for large result sets

### Monitoring
- Add structured logging
- Track tool invocation metrics
- Monitor context window usage

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI Assistant  │────▶│   MCP Server    │────▶│  Data Sources   │
│  (Claude/Cursor)│     │   (server.py)   │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │   stdio transport     │   Your integrations   │
        │                       │                       │
        ▼                       ▼                       ▼
   Chat requests          FastMCP framework       - Files
   Tool calls             - Resources             - Databases
   Resource reads         - Tools                 - APIs
                          - Prompts               - Wikis
```

## Related Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Server Registry](https://mcpregistry.io)
- [Context7 Setup](../setup-guides/context7-setup.md)
