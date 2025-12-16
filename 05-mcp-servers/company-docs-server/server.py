"""
Company Documentation MCP Server

A Model Context Protocol (MCP) server that provides AI assistants
with access to internal documentation, architecture decisions,
and searchable knowledge base.

Book Reference: Chapter 10, Section 4 (Dynamic Context Engineering)

Usage:
    python server.py

Configuration:
    See config/ folder for Claude Desktop and Cursor setup.
"""

from fastmcp import FastMCP
from pathlib import Path
import json
import re
from typing import Optional

# Initialize the MCP server
mcp = FastMCP(
    "company-docs",
    description="Access company documentation, architecture decisions, and internal knowledge base"
)

# =============================================================================
# SAMPLE DATA (Replace with your actual data sources)
# =============================================================================

# Simulated documentation store
DOCS_STORE = {
    "architecture": """
# System Architecture

## Overview
Our system follows a microservices architecture with the following components:

- **API Gateway**: Kong-based gateway handling routing and rate limiting
- **User Service**: Manages authentication and user profiles (Node.js)
- **Order Service**: Handles order processing and payments (Node.js)
- **Notification Service**: Email, SMS, and push notifications (Python)
- **Analytics Service**: Event processing and reporting (Python)

## Communication Patterns
- Synchronous: REST APIs between services
- Asynchronous: RabbitMQ for event-driven communication

## Database Strategy
- PostgreSQL for transactional data
- Redis for caching and sessions
- Elasticsearch for search functionality

## Deployment
- Kubernetes on AWS EKS
- GitOps with ArgoCD
- Prometheus + Grafana for observability
""",
    
    "api-standards": """
# API Standards

## RESTful Conventions
- Use plural nouns for resources: `/users`, `/orders`
- Use HTTP methods correctly: GET, POST, PUT, PATCH, DELETE
- Return appropriate status codes

## Request/Response Format
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "totalPages": 10,
    "totalItems": 100
  }
}
```

## Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": { "field": "email" }
  }
}
```

## Authentication
- Bearer tokens in Authorization header
- JWT with 24-hour expiry
- Refresh token rotation enabled
""",

    "coding-standards": """
# Coding Standards

## TypeScript
- Strict mode enabled
- No `any` types
- Explicit return types on all functions
- Use interfaces for object shapes

## Naming Conventions
- camelCase for variables and functions
- PascalCase for classes and interfaces
- UPPER_SNAKE_CASE for constants

## Testing Requirements
- Minimum 80% coverage
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows

## Code Review Checklist
- [ ] Types are explicit, no `any`
- [ ] Error handling is complete
- [ ] Tests cover happy path and edge cases
- [ ] No hardcoded secrets
- [ ] Logging includes correlation IDs
""",

    "onboarding": """
# Developer Onboarding

## Getting Started
1. Clone the monorepo: `git clone git@github.com:company/platform.git`
2. Install dependencies: `pnpm install`
3. Copy environment: `cp .env.example .env`
4. Start services: `pnpm dev`

## Key Contacts
- Architecture questions: #architecture-team on Slack
- DevOps support: #platform-team on Slack
- Security reviews: security@company.com

## Required Reading
- [Architecture Overview](docs://architecture)
- [API Standards](docs://api-standards)
- [Coding Standards](docs://coding-standards)

## Development Environment
- Node.js 20+
- Python 3.11+
- Docker Desktop
- pnpm (not npm or yarn)
"""
}

# Simulated ADR (Architecture Decision Records) store
ADR_STORE = {
    "ADR-001": {
        "title": "Adopt Monorepo Structure",
        "status": "accepted",
        "date": "2024-01-15",
        "context": "We need to share code between multiple services while maintaining separate deployments.",
        "decision": "Use Turborepo with pnpm workspaces for monorepo management.",
        "consequences": "Enables code sharing, requires learning Turborepo, CI/CD needs adjustment."
    },
    "ADR-002": {
        "title": "Use PostgreSQL as Primary Database",
        "status": "accepted",
        "date": "2024-01-20",
        "context": "We need a reliable, scalable relational database for transactional data.",
        "decision": "PostgreSQL 16 with Prisma ORM for type-safe database access.",
        "consequences": "Strong typing, good tooling, team familiarity. Lock-in to relational model."
    },
    "ADR-003": {
        "title": "Event-Driven Communication Between Services",
        "status": "accepted",
        "date": "2024-02-01",
        "context": "Services need to communicate without tight coupling.",
        "decision": "Use RabbitMQ for async messaging with JSON schemas for events.",
        "consequences": "Loose coupling, eventual consistency, need for idempotent consumers."
    },
    "ADR-004": {
        "title": "JWT-Based Authentication",
        "status": "accepted",
        "date": "2024-02-10",
        "context": "We need stateless authentication across microservices.",
        "decision": "JWT tokens with 24h expiry, refresh token rotation, stored in HTTP-only cookies.",
        "consequences": "Stateless verification, need for token revocation strategy."
    }
}


# =============================================================================
# RESOURCES - Read-only data exposed via URIs
# =============================================================================

@mcp.resource("docs://architecture")
def get_architecture_docs() -> str:
    """Returns the system architecture documentation."""
    return DOCS_STORE["architecture"]


@mcp.resource("docs://api-standards")
def get_api_standards() -> str:
    """Returns API design standards and conventions."""
    return DOCS_STORE["api-standards"]


@mcp.resource("docs://coding-standards")
def get_coding_standards() -> str:
    """Returns coding standards and best practices."""
    return DOCS_STORE["coding-standards"]


@mcp.resource("docs://onboarding")
def get_onboarding_docs() -> str:
    """Returns developer onboarding guide."""
    return DOCS_STORE["onboarding"]


@mcp.resource("adr://list")
def list_adrs() -> str:
    """Returns a list of all Architecture Decision Records."""
    result = "# Architecture Decision Records\n\n"
    for adr_id, adr in ADR_STORE.items():
        result += f"- **{adr_id}**: {adr['title']} ({adr['status']})\n"
    return result


# =============================================================================
# TOOLS - Executable functions the AI can call
# =============================================================================

@mcp.tool()
def search_docs(query: str) -> str:
    """
    Searches all documentation for relevant information.
    
    Args:
        query: The search query (keywords or natural language)
    
    Returns:
        Matching documentation sections with relevance context
    """
    query_lower = query.lower()
    results = []
    
    for doc_name, doc_content in DOCS_STORE.items():
        # Simple keyword matching (replace with vector search in production)
        if query_lower in doc_content.lower():
            # Extract relevant section
            lines = doc_content.split('\n')
            matching_lines = []
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # Include surrounding context
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = '\n'.join(lines[start:end])
                    matching_lines.append(context)
            
            if matching_lines:
                results.append(f"## From {doc_name}:\n" + '\n...\n'.join(matching_lines[:3]))
    
    if results:
        return "# Search Results\n\n" + '\n\n'.join(results)
    else:
        return f"No documentation found matching '{query}'. Try different keywords."


@mcp.tool()
def get_adr(adr_id: str) -> str:
    """
    Retrieves a specific Architecture Decision Record.
    
    Args:
        adr_id: The ADR identifier (e.g., "ADR-001")
    
    Returns:
        The full ADR document or error message
    """
    adr_id_upper = adr_id.upper()
    
    if adr_id_upper not in ADR_STORE:
        available = ", ".join(ADR_STORE.keys())
        return f"ADR '{adr_id}' not found. Available ADRs: {available}"
    
    adr = ADR_STORE[adr_id_upper]
    return f"""# {adr_id_upper}: {adr['title']}

**Status:** {adr['status']}
**Date:** {adr['date']}

## Context
{adr['context']}

## Decision
{adr['decision']}

## Consequences
{adr['consequences']}
"""


@mcp.tool()
def get_service_info(service_name: str) -> str:
    """
    Returns information about a specific service in our architecture.
    
    Args:
        service_name: Name of the service (e.g., "user-service", "order-service")
    
    Returns:
        Service details including tech stack, responsibilities, and API endpoints
    """
    services = {
        "user-service": {
            "tech": "Node.js 20, Express, TypeScript, Prisma",
            "database": "PostgreSQL (users, profiles, sessions)",
            "responsibilities": [
                "User registration and authentication",
                "Profile management",
                "Session handling with JWT",
                "OAuth2 provider integration"
            ],
            "endpoints": [
                "POST /auth/login",
                "POST /auth/register",
                "POST /auth/refresh",
                "GET /users/:id",
                "PATCH /users/:id"
            ],
            "owner": "Platform Team"
        },
        "order-service": {
            "tech": "Node.js 20, Express, TypeScript, Prisma",
            "database": "PostgreSQL (orders, order_items, payments)",
            "responsibilities": [
                "Order creation and management",
                "Payment processing",
                "Order status tracking",
                "Inventory coordination"
            ],
            "endpoints": [
                "POST /orders",
                "GET /orders/:id",
                "PATCH /orders/:id/status",
                "POST /orders/:id/payment"
            ],
            "owner": "Commerce Team"
        },
        "notification-service": {
            "tech": "Python 3.11, FastAPI, Celery",
            "database": "PostgreSQL (notifications, templates)",
            "responsibilities": [
                "Email notifications",
                "SMS notifications",
                "Push notifications",
                "Template management"
            ],
            "endpoints": [
                "POST /notifications/send",
                "GET /notifications/:id",
                "POST /templates"
            ],
            "owner": "Platform Team"
        }
    }
    
    service_key = service_name.lower().replace(" ", "-")
    
    if service_key not in services:
        available = ", ".join(services.keys())
        return f"Service '{service_name}' not found. Available services: {available}"
    
    svc = services[service_key]
    endpoints_list = "\n".join(f"  - {ep}" for ep in svc["endpoints"])
    responsibilities_list = "\n".join(f"  - {r}" for r in svc["responsibilities"])
    
    return f"""# {service_name}

**Tech Stack:** {svc['tech']}
**Database:** {svc['database']}
**Owner:** {svc['owner']}

## Responsibilities
{responsibilities_list}

## API Endpoints
{endpoints_list}
"""


@mcp.tool()
def check_naming_convention(name: str, context: str = "variable") -> str:
    """
    Validates a name against our coding standards.
    
    Args:
        name: The name to validate
        context: The naming context - "variable", "function", "class", "constant", or "file"
    
    Returns:
        Validation result with suggestions if needed
    """
    context = context.lower()
    
    conventions = {
        "variable": ("camelCase", r'^[a-z][a-zA-Z0-9]*$'),
        "function": ("camelCase", r'^[a-z][a-zA-Z0-9]*$'),
        "class": ("PascalCase", r'^[A-Z][a-zA-Z0-9]*$'),
        "interface": ("PascalCase", r'^[A-Z][a-zA-Z0-9]*$'),
        "constant": ("UPPER_SNAKE_CASE", r'^[A-Z][A-Z0-9_]*$'),
        "file": ("kebab-case", r'^[a-z][a-z0-9-]*$'),
    }
    
    if context not in conventions:
        return f"Unknown context '{context}'. Use: {', '.join(conventions.keys())}"
    
    expected_style, pattern = conventions[context]
    
    if re.match(pattern, name):
        return f"✅ '{name}' follows {expected_style} convention for {context}s."
    else:
        return f"❌ '{name}' does not follow {expected_style} convention for {context}s.\n\nExpected format: {expected_style}"


# =============================================================================
# PROMPTS - Reusable prompt templates
# =============================================================================

@mcp.prompt()
def code_review_checklist() -> str:
    """Returns a standard code review checklist."""
    return """Please review the code using this checklist:

## Code Quality
- [ ] Types are explicit, no `any` types
- [ ] Functions have single responsibility
- [ ] Error handling is complete
- [ ] No commented-out code

## Testing
- [ ] Unit tests cover business logic
- [ ] Edge cases are tested
- [ ] Test descriptions are clear

## Security
- [ ] Input validation is present
- [ ] No hardcoded secrets
- [ ] SQL queries are parameterized
- [ ] Authentication/authorization checked

## Documentation
- [ ] Public functions have JSDoc comments
- [ ] Complex logic has explanatory comments
- [ ] README updated if needed

Please identify any issues and suggest improvements."""


@mcp.prompt()
def architecture_review() -> str:
    """Returns prompts for architecture review."""
    return """Please review this code/design against our architecture standards:

1. **Service Boundaries**: Does this respect service ownership?
2. **Communication**: Is sync/async communication used appropriately?
3. **Data Ownership**: Does this query only data it owns?
4. **Error Handling**: Are failures handled gracefully?
5. **Observability**: Is logging/tracing adequate?

Reference our Architecture ADRs for decisions:
- ADR-001: Monorepo Structure
- ADR-002: PostgreSQL Database
- ADR-003: Event-Driven Communication
- ADR-004: JWT Authentication

Identify any violations and suggest corrections."""


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("Starting Company Docs MCP Server...")
    print("Available resources:")
    print("  - docs://architecture")
    print("  - docs://api-standards")
    print("  - docs://coding-standards")
    print("  - docs://onboarding")
    print("  - adr://list")
    print("\nAvailable tools:")
    print("  - search_docs(query)")
    print("  - get_adr(adr_id)")
    print("  - get_service_info(service_name)")
    print("  - check_naming_convention(name, context)")
    print("\nAvailable prompts:")
    print("  - code_review_checklist")
    print("  - architecture_review")
    print("\nServer running. Press Ctrl+C to stop.")
    mcp.run()
