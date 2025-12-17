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
│   ├── templates/                          # NEW (Task 6.2)
│   │   ├── wiki-mcp-template/
│   │   ├── database-schema-mcp/
│   │   ├── api-docs-mcp/
│   │   └── observability-mcp/
│   └── setup-guides/
│       └── context7-setup.md
│
├── 06-custom-agents/
│   ├── README.md
│   ├── AGENT_DESIGN_GUIDE.md               # NEW (Task 6.4)
│   ├── github-agents/
│   │   ├── test-agent.md
│   │   ├── docs-agent.md
│   │   ├── security-agent.md
│   │   └── refactor-agent.md
│   ├── claude-agents/
│   │   ├── planning-agent.md
│   │   ├── implementation-agent.md
│   │   └── review-agent.md
│   ├── tdd-workflow/                       # NEW (Task 5.2)
│   │   ├── README.md
│   │   ├── tdd-red.md
│   │   ├── tdd-green.md
│   │   └── tdd-refactor.md
│   └── starter-agents/                     # NEW (Task 5.3)
│       ├── README.md
│       ├── documentation-agent.md
│       ├── test-coverage-agent.md
│       ├── security-scanner-agent.md
│       └── refactoring-agent.md
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
│   ├── checklists/                         # NEW (Task 5.5)
│   │   ├── README.md
│   │   ├── requirements-checklist.md
│   │   ├── architecture-checklist.md
│   │   └── handoff-checklist.md
│   ├── schemas/                            # NEW (Task 8.3)
│   │   ├── handoff-schema.json
│   │   ├── handoff-validator.py
│   │   └── handoff-examples/
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
├── 09-exercises/                           # NEW (Task 6.1)
│   ├── README.md
│   ├── exercise-1-payment-processor/
│   ├── exercise-2-api-migration/
│   ├── exercise-3-security-audit/
│   ├── exercise-4-legacy-refactor/
│   ├── exercise-5-test-generation/
│   └── exercise-6-documentation/
│
├── 10-reference/
│   ├── README.md
│   ├── 70-percent-checklist.md
│   ├── vibe-vs-engineering.md
│   ├── skill-transformation.md
│   ├── maturity-model.md                   # NEW (Task 5.4)
│   ├── cross-tool-compatibility.md         # NEW (Task 8.1)
│   ├── context-commands.md                 # NEW (Task 8.2)
│   └── measurements/                       # NEW (Task 6.3)
│       ├── time-savings-calculator.py
│       ├── quality-metrics-tracker.md
│       ├── adoption-dashboard.md
│       └── roi-calculator.md
│
└── 11-antipatterns/                        # NEW (Tasks 7.1, 7.2, 7.3)
    ├── README.md
    ├── ANTIPATTERNS_INDEX.md
    ├── chapter7-antipatterns/
    │   ├── README.md
    │   ├── 01-insufficient-context.md
    │   ├── 02-vague-instructions.md
    │   ├── 03-blind-trust.md
    │   ├── 04-inefficient-iteration.md
    │   ├── 05-ignoring-limitations.md
    │   ├── 06-over-engineering.md
    │   ├── 07-context-pollution.md
    │   └── 08-security-negligence.md
    └── chapter10-pitfalls/
        ├── README.md
        ├── 01-tool-hopping.md
        ├── 02-over-automation.md
        ├── 03-context-window-abuse.md
        ├── 04-prompt-hoarding.md
        └── 05-metric-theater.md
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


### Phase 5: Deep Scan & Critical Additions (Priority: High)

**Task 5.1:** ✅ COMPLETED - Comprehensive Book Scan
- Scanned entire book for missing examples
- Results documented in `TASK_5_1_SCAN_RESULTS.md` with 3 addendums
- Commits: 3d030b5, 97fe3a9, 498df72, 7f982d8

**Task 5.2:** Add TDD Workflow Agent Chain
- **Source:** `chapter10/07_dev_practices.tex` (lines 20-90), `appendix_c_v4.tex` (TDD pattern)
- **Output:** `/06-custom-agents/tdd-workflow/`
- **Deliverables:**
  - `tdd-red.md` — Write failing tests first, with AI assistance
  - `tdd-green.md` — Minimal implementation to pass tests
  - `tdd-refactor.md` — Clean up while keeping tests green
  - `README.md` — Workflow orchestration guide

**Task 5.3:** Create Starter Agents Collection
- **Source:** `chapter10/06_multi_agent.tex` (lines 100-200)
- **Output:** `/06-custom-agents/starter-agents/`
- **Deliverables:**
  - `documentation-agent.md` — Auto-generate and update docs
  - `test-coverage-agent.md` — Identify untested paths
  - `security-scanner-agent.md` — OWASP-aligned security review
  - `refactoring-agent.md` — Identify code smells and suggest improvements
  - `README.md` — When to use each agent

**Task 5.4:** Add Context Engineering Maturity Model
- **Source:** `chapter10/01_maturity_levels.tex` (complete file)
- **Output:** `/10-reference/maturity-model.md`
- **Deliverables:**
  - 5-level maturity progression (Reactive → Predictive)
  - Self-assessment checklist for each level
  - Progression roadmap with recommended actions
  - Tool recommendations by maturity level

**Task 5.5:** Build Enterprise Workflow Checklists
- **Source:** `appendix_c_v4.tex` (lines 200-400, 1400-1500)
- **Output:** `/07-enterprise-workflow/checklists/`
- **Deliverables:**
  - `requirements-checklist.md` — Requirements Analyst validation (10 items)
  - `architecture-checklist.md` — Architect validation (10 items)
  - `handoff-checklist.md` — Phase transition validation (8 items)
  - `README.md` — How to use checklists in workflow

---

### Phase 6: Extended Content & Exercises (Priority: Medium)

**Task 6.1:** Create Exercise Solutions Folder
- **Source:** `appendix_c_v4.tex` (Exercise sections)
- **Output:** `/09-exercises/`
- **Deliverables:**
  - `exercise-1-payment-processor/` — Multi-agent payment system
  - `exercise-2-api-migration/` — REST to GraphQL migration
  - `exercise-3-security-audit/` — Security agent workflow
  - `exercise-4-legacy-refactor/` — COBOL to Python patterns
  - `exercise-5-test-generation/` — AI-assisted test suite
  - `exercise-6-documentation/` — Living documentation system
  - Each folder: problem statement, sample solution, evaluation rubric

**Task 6.2:** Add MCP Server Templates
- **Source:** `chapter10/05_context_flow.tex`, `appendix_b1.tex`
- **Output:** `/05-mcp-servers/templates/`
- **Deliverables:**
  - `wiki-mcp-template/` — Internal wiki integration pattern
  - `database-schema-mcp/` — Schema discovery and documentation
  - `api-docs-mcp/` — OpenAPI/Swagger integration
  - `observability-mcp/` — Metrics and logging integration
  - Each template: base code, configuration, README

**Task 6.3:** Create Measurement Scripts
- **Source:** `chapter10/10_measurement.tex`
- **Output:** `/10-reference/measurements/`
- **Deliverables:**
  - `time-savings-calculator.py` — Calculate AI-assisted time savings
  - `quality-metrics-tracker.md` — Bug rate, code review metrics
  - `adoption-dashboard.md` — Team adoption tracking template
  - `roi-calculator.md` — Business case template

**Task 6.4:** Write Agent Design Guide
- **Source:** `chapter10/06_multi_agent.tex` (agent design principles)
- **Output:** `/06-custom-agents/AGENT_DESIGN_GUIDE.md`
- **Deliverables:**
  - Agent anatomy: description, tools, boundaries, handoff
  - When to split vs combine agents
  - Testing and validation strategies
  - Common pitfalls and solutions

---

### Phase 7: Antipatterns & Pitfalls Collection (Priority: Medium)

**Task 7.1:** Implement Chapter 7 Antipatterns
- **Source:** `chapter07/chapter07_antipatterns.tex`
- **Output:** `/11-antipatterns/chapter7-antipatterns/`
- **Deliverables:** (8 timeless antipatterns)
  - `01-insufficient-context.md` — Problem, example, MCP solution
  - `02-vague-instructions.md` — Problem, example, specification pattern
  - `03-blind-trust.md` — Problem, example, verification workflow
  - `04-inefficient-iteration.md` — Problem, example, batch approach
  - `05-ignoring-limitations.md` — Problem, example, hybrid approach
  - `06-over-engineering.md` — Problem, example, iterative design
  - `07-context-pollution.md` — Problem, example, session management
  - `08-security-negligence.md` — Problem, example, security agent
  - `README.md` — Antipattern index with quick diagnosis guide

**Task 7.2:** Implement Chapter 10 Pitfalls (2025-Specific)
- **Source:** `chapter10/11_pitfalls.tex`
- **Output:** `/11-antipatterns/chapter10-pitfalls/`
- **Deliverables:** (5 contemporary pitfalls)
  - `01-tool-hopping.md` — Switching tools without mastery
  - `02-over-automation.md` — Automating everything prematurely
  - `03-context-window-abuse.md` — Dumping entire codebases
  - `04-prompt-hoarding.md` — Over-collecting without curation
  - `05-metric-theater.md` — Gaming productivity metrics
  - `README.md` — Pitfall recognition and remediation guide

**Task 7.3:** Create Antipatterns Cross-Reference
- **Output:** `/11-antipatterns/ANTIPATTERNS_INDEX.md`
- **Deliverables:**
  - Complete index of all 13 antipatterns/pitfalls
  - Symptom-to-antipattern diagnostic table
  - Link to relevant solutions in other folders
  - Team discussion templates

---

### Phase 8: Advanced Content & Community Setup (Priority: Lower)

**Task 8.1:** Cross-Tool Compatibility Guide
- **Source:** `chapter10/02_choosing_tools.tex`
- **Output:** `/10-reference/cross-tool-compatibility.md`
- **Deliverables:**
  - Feature matrix: Copilot vs Cursor vs Claude Code
  - Configuration translation guide
  - Migration paths between tools
  - Interoperability patterns

**Task 8.2:** Context Commands Reference
- **Source:** `chapter10/03_static_context.tex`, `chapter10/04_dynamic_context.tex`
- **Output:** `/10-reference/context-commands.md`
- **Deliverables:**
  - Complete command reference by tool
  - Dynamic context patterns
  - Advanced context composition
  - Troubleshooting common context issues

**Task 8.3:** Handoff Schema Definition
- **Source:** `appendix_c_v4.tex` (handoff sections)
- **Output:** `/07-enterprise-workflow/schemas/`
- **Deliverables:**
  - `handoff-schema.json` — JSON Schema for handoff documents
  - `handoff-validator.py` — Validation script
  - `handoff-examples/` — Real-world examples
  - `README.md` — Schema documentation

**Task 8.4:** Create Community Contribution Issues
- **Output:** GitHub Issues with "help wanted" label
- **Deliverables:**
  - Issue: TypeScript variants for Python examples
  - Issue: Additional MCP server implementations
  - Issue: Real-world case studies
  - Issue: Video tutorial scripts
  - Issue: Multi-language specification templates

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
| 05-mcp-servers | chapter10/05_context_flow.tex, appendix_b1.tex |
| 05-mcp-servers/templates | chapter10/05_context_flow.tex (wiki, schema, API patterns) |
| 06-custom-agents | chapter10/06_multi_agent.tex |
| 06-custom-agents/tdd-workflow | chapter10/07_dev_practices.tex, appendix_c_v4.tex |
| 06-custom-agents/starter-agents | chapter10/06_multi_agent.tex |
| 07-enterprise-workflow | appendix_c_v4.tex |
| 07-enterprise-workflow/checklists | appendix_c_v4.tex (validation sections) |
| 08-security | chapter07_part2.tex |
| 09-exercises | appendix_c_v4.tex (exercises section) |
| 10-reference | appendix_a.tex |
| 10-reference/maturity-model | chapter10/01_maturity_levels.tex |
| 10-reference/measurements | chapter10/10_measurement.tex |
| 10-reference/cross-tool | chapter10/02_choosing_tools.tex |
| 11-antipatterns/chapter7 | chapter07/chapter07_antipatterns.tex |
| 11-antipatterns/chapter10 | chapter10/11_pitfalls.tex |

---

## Success Criteria

### Phase 1-4 (Original)
- [x] All 10 base folders created with README.md files
- [x] MCP server runs successfully with `python server.py`
- [ ] All YAML/JSON files pass validation
- [x] Every example links back to book chapter
- [ ] GitHub Actions pass on main branch
- [ ] At least 3 "help wanted" issues created for community expansion

### Phase 5 (Critical Additions)
- [ ] TDD workflow agents created (3 files)
- [ ] Starter agents collection complete (4 agents)
- [ ] Context Engineering Maturity Model documented
- [ ] Enterprise workflow checklists created (3 checklists, 28 items)

### Phase 6 (Extended Content)
- [ ] Exercise solutions folder with 6 exercises
- [ ] MCP server templates (4 templates)
- [ ] Measurement scripts and dashboards
- [ ] Agent Design Guide complete

### Phase 7 (Antipatterns)
- [ ] Chapter 7 antipatterns folder (8 antipatterns)
- [ ] Chapter 10 pitfalls folder (5 pitfalls)
- [ ] Master antipatterns index with diagnostics

### Phase 8 (Advanced/Community)
- [ ] Cross-tool compatibility guide
- [ ] Context commands reference
- [ ] Handoff schema with validator
- [ ] Community contribution issues created

---

## Implementation Summary

| Phase | Tasks | Priority | Status |
|-------|-------|----------|--------|
| Phase 1 | 1.1, 1.2, 1.3 | Critical | ✅ Complete |
| Phase 2 | 2.1, 2.2 | High | ✅ Complete |
| Phase 3 | 3.1, 3.2, 3.3 | Medium | ✅ Complete |
| Phase 4 | 4.1, 4.2, 4.3, 4.4 | Standard | ⏳ Pending |
| Phase 5 | 5.1, 5.2, 5.3, 5.4, 5.5 | High | 5.1 ✅ / 5.2-5.5 ⏳ |
| Phase 6 | 6.1, 6.2, 6.3, 6.4 | Medium | ⏳ Pending |
| Phase 7 | 7.1, 7.2, 7.3 | Medium | ⏳ Pending |
| Phase 8 | 8.1, 8.2, 8.3, 8.4 | Lower | ⏳ Pending |

**Total Tasks:** 24  
**Completed:** 8  
**Remaining:** 16

---

## Recommended Implementation Order

For maximum value with minimal effort, implement in this order:

1. **Task 5.2** - TDD Workflow (high impact, clear source)
2. **Task 5.3** - Starter Agents (extends existing agents folder)
3. **Task 5.4** - Maturity Model (single file, high reference value)
4. **Task 5.5** - Enterprise Checklists (complements existing workflow)
5. **Task 7.1** - Chapter 7 Antipatterns (timeless content)
6. **Task 7.2** - Chapter 10 Pitfalls (contemporary relevance)
7. **Task 6.1** - Exercises (reader engagement)
8. **Task 4.1-4.4** - Automation & Polish (GitHub readiness)
9. **Tasks 6.2-6.4** - Extended content
10. **Tasks 8.1-8.4** - Advanced content & community
