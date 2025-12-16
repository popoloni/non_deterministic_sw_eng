# Companion Repository Implementation Guide
## "Non-Deterministic Software Engineering" by Enrico Papalini

---

## Repository Overview

**Repository Name:** `ai-assisted-engineering-examples`  
**Purpose:** Hands-on code examples, configuration templates, and practical materials for readers  
**Primary Languages:** TypeScript/JavaScript, Python, Markdown, YAML  

---

## Directory Structure

```
ai-assisted-engineering-examples/
├── README.md
├── LICENSE (MIT)
├── CONTRIBUTING.md
├── .github/
│   ├── workflows/
│   │   ├── validate-configs.yml
│   │   └── test-mcp-server.yml
│   └── ISSUE_TEMPLATE/
│       ├── outdated-example.md
│       └── missing-pattern.md
│
├── 01-fundamentals/
│   └── README.md
│
├── 02-specifications/
│   ├── README.md
│   ├── auth-middleware-spec.md
│   ├── api-endpoint-spec.md
│   └── feature-spec-template.md
│
├── 03-migrations/
│   ├── README.md
│   └── react-class-to-hooks/
│       ├── before/
│       └── after/
│
├── 04-context-engineering/
│   ├── README.md
│   ├── agents-md/
│   │   ├── minimal.md
│   │   ├── full-stack-project.md
│   │   └── monorepo.md
│   ├── cursor-rules/
│   │   ├── api-validation.mdc
│   │   ├── testing.mdc
│   │   └── security.mdc
│   ├── copilot-instructions/
│   │   └── .github/
│   │       ├── copilot-instructions.md
│   │       └── instructions/
│   └── claude/
│       └── CLAUDE.md
│
├── 05-mcp-servers/
│   ├── README.md
│   ├── company-docs-server/
│   │   ├── server.py
│   │   ├── requirements.txt
│   │   ├── pyproject.toml
│   │   └── config/
│   │       ├── claude_desktop_config.json
│   │       └── cursor_mcp.json
│   └── setup-guides/
│       └── context7-setup.md
│
├── 06-custom-agents/
│   ├── README.md
│   ├── github-agents/
│   │   ├── test-agent.md
│   │   ├── docs-agent.md
│   │   ├── security-agent.md
│   │   └── refactor-agent.md
│   └── claude-agents/
│       ├── planning-agent.md
│       ├── implementation-agent.md
│       └── review-agent.md
│
├── 07-enterprise-workflow/
│   ├── README.md
│   ├── planning-phase/
│   │   ├── requirements-analyst.md
│   │   ├── architect-agent.md
│   │   ├── api-champion.md
│   │   └── messaging-champion.md
│   ├── execution-phase/
│   │   ├── test-explorer.md
│   │   ├── test-engineer.md
│   │   └── software-engineer.md
│   ├── artifacts/
│   │   ├── business-context-template.md
│   │   ├── solution-design-template.md
│   │   ├── api-definitions-template.md
│   │   └── test-cases-template.md
│   └── handoffs/
│       └── workflow-config.yaml
│
├── 08-security/
│   ├── README.md
│   └── checklists/
│       ├── auth-review.md
│       ├── input-validation.md
│       └── data-protection.md
│
├── 09-testing/
│   ├── README.md
│   └── examples/
│       └── table-driven-tests.ts
│
└── 10-reference/
    ├── README.md
    ├── 70-percent-checklist.md
    ├── vibe-vs-engineering.md
    └── skill-transformation.md
```

---

## Implementation Phases

### Phase 1: Foundation (Priority: Critical)

**Task 1.1:** Create repository with base structure
- Initialize Git repository
- Add MIT LICENSE
- Create root README.md with book overview, navigation table, and quick-start

**Task 1.2:** Extract Context Engineering examples
- **Source:** `chapters_verbose/chapter10/03_static_context.tex`, `04_dynamic_context.tex`
- **Output:** `/04-context-engineering/`
- **Deliverables:**
  - 3 AGENTS.md variants (minimal 40-line, full-stack, monorepo)
  - 3 Cursor .mdc rule files (api-validation, testing, security)
  - Complete .github/copilot-instructions.md structure
  - CLAUDE.md template

**Task 1.3:** Build MCP Server project
- **Source:** `chapters_verbose/chapter10/05_context_flow.tex`
- **Output:** `/05-mcp-servers/company-docs-server/`
- **Deliverables:**
  - Fully working FastMCP Python server (not just snippet)
  - requirements.txt with pinned versions
  - pyproject.toml for modern Python packaging
  - Configuration files for Claude Desktop and Cursor
  - README with installation and testing instructions

---

### Phase 2: Agents & Workflows (Priority: High)

**Task 2.1:** Create Custom Agents collection
- **Source:** `chapters_verbose/chapter10/06_multi_agent.tex`
- **Output:** `/06-custom-agents/`
- **Deliverables:**
  - GitHub Copilot agent definitions (test, docs, security, refactor)
  - Claude Code agent definitions (planning, implementation, review)
  - Each agent includes: description, tools, capabilities, boundaries

**Task 2.2:** Build Enterprise Workflow suite
- **Source:** `appendices/appendix_c_v4.tex`
- **Output:** `/07-enterprise-workflow/`
- **Deliverables:**
  - Complete planning-phase agents (requirements-analyst, architect, api-champion, messaging-champion)
  - Complete execution-phase agents (test-explorer, test-engineer, software-engineer)
  - Artifact templates for each workflow stage
  - Handoff configuration with YAML frontmatter

---

### Phase 3: Patterns & Examples (Priority: Medium)

**Task 3.1:** Add Specification templates
- **Source:** `chapters_verbose/chapter07/chapter07_part1.tex`
- **Output:** `/02-specifications/`
- **Deliverables:**
  - JWT Authentication Middleware specification (complete)
  - API endpoint specification template
  - Generic feature specification template

**Task 3.2:** Create Migration examples
- **Source:** `chapters_verbose/chapter07/chapter07_part3.tex`
- **Output:** `/03-migrations/react-class-to-hooks/`
- **Deliverables:**
  - Complete React class component (before/)
  - Complete hooks-based equivalent (after/)
  - Migration prompt template

**Task 3.3:** Add Security checklists
- **Source:** `chapters_verbose/chapter07/chapter07_part2.tex`
- **Output:** `/08-security/checklists/`
- **Deliverables:**
  - Authentication review checklist
  - Input validation checklist
  - Data protection checklist

---

### Phase 4: Automation & Polish (Priority: Standard)

**Task 4.1:** Configure GitHub Actions
- **validate-configs.yml:** Lint all YAML/JSON files, validate Markdown structure
- **test-mcp-server.yml:** Install Python dependencies, run MCP server smoke test

**Task 4.2:** Create issue templates
- **outdated-example.md:** For reporting configs that no longer work with tool updates
- **missing-pattern.md:** For requesting new patterns from the book

**Task 4.3:** Write CONTRIBUTING.md
- Guidelines for expanding snippets to full examples
- Style guide for documentation
- Instructions for adding multi-language variants

**Task 4.4:** Add reference materials
- **Source:** `appendices/appendix_a.tex`
- **Output:** `/10-reference/`
- **Deliverables:**
  - 70% Rule checklist
  - Vibe Coding vs Engineering comparison
  - Skill transformation guide
  - clickable set of link to navigate the reference matherials

---

## Metadata Standards

Every configuration file includes YAML frontmatter:

```yaml
---
tool: cursor | copilot | claude | generic
tool_version: "1.0"
last_verified: 2025-12-16
book_chapter: 10
book_section: "Static Context"
---
```

---

## Content Guidelines

1. **Expand key examples** (MCP server, enterprise agents) into fully working projects
2. **Keep templates minimal** with clear "customize for your project" markers
3. **Include version metadata** on all tool-specific configurations
4. **Mark community contribution opportunities** as GitHub issues labeled "help wanted"
5. **Cross-reference book chapters** in every README
6. **Primary language first** — mark "Python variant wanted" or "TypeScript variant wanted" for community

---

## Source File Mapping

| Repository Folder | LaTeX Source Files |
|-------------------|-------------------|
| 02-specifications | chapter07_part1.tex |
| 03-migrations | chapter07_part3.tex |
| 04-context-engineering | chapter10/03_static_context.tex, 04_dynamic_context.tex |
| 05-mcp-servers | chapter10/05_context_flow.tex |
| 06-custom-agents | chapter10/06_multi_agent.tex |
| 07-enterprise-workflow | appendix_c_v4.tex |
| 08-security | chapter07_part2.tex |
| 10-reference | appendix_a.tex |

---

## Success Criteria

- [ ] All 10 folders created with README.md files
- [ ] MCP server runs successfully with `python server.py`
- [ ] All YAML/JSON files pass validation
- [ ] Every example links back to book chapter
- [ ] GitHub Actions pass on main branch
- [ ] At least 3 "help wanted" issues created for community expansion
