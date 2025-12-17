# Task 5.1: Book Scan Results - Missing Examples and Additions

> 📖 **Task Reference:** Phase 5 - Double Check  
> **Status:** Pending Validation  
> **Date:** 2025-12-16

---

## Executive Summary

After scanning all book chapters and comparing with current repository contents, I've identified several missing examples that would enhance the companion repository's completeness.

---

## 1. ANTIPATTERNS EXAMPLES (HIGH VALUE)

### Source: `chapter07/chapter07_antipatterns.tex`

The book documents 8 antipatterns with detailed "what it looks like," "warning signs," and "prevention" sections. These should have dedicated examples.

**Proposed Addition: `/11-antipatterns/`**

| Antipattern | Detection Example | Prevention Example |
|-------------|-------------------|-------------------|
| 1. Blind Acceptance | PR review checklist | Explainability test template |
| 2. The 70% Trap | Code smell detector | TDD completion checklist |
| 3. Vibe Production Deployment | Prototype boundary markers | Production graduation checklist |
| 4. Context-Free Generation | Convention violation detector | Context engineering templates (✓ exists) |
| 5. Batch Size Explosion | PR size analyzer config | Chunking guidelines |
| 6. Security as Afterthought | Security scan configs | Security-first checklists (✓ exists) |
| 7. Learning Loop Destruction | Skill assessment template | Learning objectives template |
| 8. Measurement Theater | Anti-metric examples | Balanced metrics dashboard |

**Deliverables:**
- `antipattern-detection-checklist.md` — Warning signs for each antipattern
- `prevention-strategies.md` — Detailed prevention for each
- `pr-size-analyzer/` — GitHub Action to detect batch size explosion
- `prototype-markers/` — Templates for marking prototype vs production code

---

## 2. TDD + AI TESTING EXAMPLES (HIGH VALUE)

### Source: `chapter07_part1.tex` (Pattern 2) + `appendix_b1.tex` (Kent Beck insights)

The book has excellent `parseUserInput` test examples but the `09-testing/examples/` folder is empty.

**Proposed Addition: `/09-testing/examples/`**

| File | Description | Book Reference |
|------|-------------|----------------|
| `tdd-workflow-example/` | Complete TDD workflow with AI | Pattern 2 |
| `immutable-tests.test.ts` | Tests marked as "DO NOT MODIFY" | Kent Beck quote |
| `table-driven-tests.test.ts` | Table-driven test pattern | Pattern 2 |
| `parseUserInput.test.ts` | Complete example from book | Pattern 2 |
| `parseUserInput.ts` | Implementation passing all tests | Pattern 2 |

**Kent Beck's Immutable Test Pattern:**
```typescript
// AI: DO NOT MODIFY THIS TEST - This defines correct behavior
// @immutable
test('critical business rule', () => {
  expect(calculateTax(100, 'CA')).toBe(7.25);
});
```

---

## 3. TRIO PROGRAMMING TEMPLATES (MEDIUM VALUE)

### Source: `chapter07_part3.tex` (Pattern 13)

The book describes Trio Programming (Junior + Senior + AI) but no templates exist.

**Proposed Addition: `/06-custom-agents/trio-programming/`**

| File | Description |
|------|-------------|
| `session-template.md` | Template for trio session planning |
| `senior-guide.md` | Guide for senior role in trio |
| `junior-checklist.md` | Checklist for junior's learning objectives |
| `debrief-template.md` | Post-session learning capture |

---

## 4. COST MANAGEMENT EXAMPLES (MEDIUM VALUE)

### Source: `chapter07_part4.tex` (Pattern 18) + `appendix_b1.tex` (Farhan Thawar)

The book has strong guidance on cost management but no practical templates.

**Proposed Addition: `/10-reference/cost-management/`**

| File | Description |
|------|-------------|
| `token-budget-calculator.md` | Spreadsheet/formula for token budgets |
| `roi-calculation-template.md` | Template for calculating AI ROI |
| `value-tracking-dashboard.md` | Metrics to track (per Farhan's advice) |

**Key Quote to Implement:**
> "If I could give you a tool that could make your engineering team more productive by even 10%, would you pay for it?" — Farhan Thawar

---

## 5. STRUCTURED ENABLEMENT MATERIALS (MEDIUM VALUE)

### Source: `chapter07_part4.tex` (Pattern 15)

The book details a complete enablement program structure.

**Proposed Addition: `/10-reference/enablement/`**

| File | Description |
|------|-------------|
| `training-session-1.md` | Fundamentals (90 min) agenda |
| `training-session-2.md` | Hands-on workshop (2 hr) agenda |
| `certification-checklist.md` | Requirements for tool access |
| `office-hours-guide.md` | Running effective office hours |
| `weekly-digest-template.md` | Template for learning digest |

---

## 6. QUICK REFERENCE CARDS (LOW VALUE - NICE TO HAVE)

### Source: `appendix_a.tex`

The book has extensive quick reference content that could be formatted as printable cards.

**Proposed Addition: `/10-reference/printable/`**

| File | Description |
|------|-------------|
| `70-percent-card.pdf` | One-page printable reference |
| `warning-signs-poster.pdf` | Team room poster |
| `pattern-selection-flowchart.pdf` | Decision tree for pattern selection |

---

## 7. EXPERT QUOTES COLLECTION (LOW VALUE - NICE TO HAVE)

### Source: `appendix_b1.tex`

Actionable quotes from Kent Beck, Martin Fowler, Farhan Thawar, Laura Tacho.

**Proposed Addition: `/10-reference/expert-insights.md`**

Curated collection with practical applications for each quote.

---

## Priority Recommendation

| Priority | Addition | Effort | Value |
|----------|----------|--------|-------|
| **1** | Antipatterns folder with detection/prevention | High | Very High |
| **2** | TDD + AI testing examples | Medium | High |
| **3** | Trio programming templates | Low | Medium |
| **4** | Cost management examples | Low | Medium |
| **5** | Structured enablement materials | Medium | Medium |
| **6** | Quick reference cards | Low | Low |
| **7** | Expert quotes collection | Low | Low |

---

## Recommended Implementation Order

### Immediate (Task 5.2 - If approved):
1. **Antipatterns detection/prevention** — This fills a significant gap and provides immediate value

### Phase 4 (After current work):
2. **TDD testing examples** — Complete the 09-testing folder
3. **Trio programming templates** — Small addition to agents

### Future (Community contributions):
4-7. Lower priority items can be marked as "help wanted" issues

---

## Validation Requested

Please review and approve:

- [ ] Create `/11-antipatterns/` folder with detection and prevention materials
- [ ] Populate `/09-testing/examples/` with TDD + AI examples from book
- [ ] Add trio programming templates to `/06-custom-agents/`
- [ ] Add cost management templates to `/10-reference/`
- [ ] Add enablement materials to `/10-reference/`
- [ ] Mark remaining items as GitHub issues for community

---

## Notes

1. The MCP server alternative mentioned in the task hint refers to using MCP to provide real-time context to prevent antipatterns. This is partially covered by the existing MCP server but could be enhanced.

2. Many antipatterns reference existing patterns as prevention (e.g., Pattern 6 prevents Antipattern 1). Cross-references should be maintained.

3. Kent Beck's "immutable tests" concept is particularly valuable and should be prominently featured.

---
---

# ADDENDUM: Deep Scan of Chapter 10 and Appendix C

> **Scan Date:** 2025-12-16  
> **Focus Areas:** `chapters_verbose/chapter10/` and `appendices/appendix_c_v4.tex`  
> **Purpose:** Identify code examples, configurations, and templates with high implementation value

---

## CHAPTER 10 SCAN: Tools and Practices

### 10.1 Static Context Engineering (`03_static_context.tex`)

**Existing Coverage:** Most examples already implemented in `/04-context-engineering/`

**Additional Examples Found:**

| Example | Lines | Status | Action |
|---------|-------|--------|--------|
| 40-line minimal AGENTS.md | 75-105 | ✅ Covered | Already in `agents-md/minimal.md` |
| GitHub Copilot `applyTo` pattern | 134-145 | ✅ Covered | In copilot-instructions |
| Cursor MDC file format | 168-185 | ✅ Covered | In cursor-rules |
| Claude Code CLAUDE.md | 255-280 | ✅ Covered | In claude folder |
| Cross-tool compatibility table | 295-320 | ⚠️ Partial | Add comparison README |
| Supporting documentation pattern | 345-360 | ❌ Missing | Add ARCHITECTURE.md template |

**NEW Proposed Addition: `/04-context-engineering/cross-tool/`**

```
cross-tool/
├── README.md                    # Cross-tool compatibility guide
├── ARCHITECTURE.md.template     # Referenced supporting doc
├── PRODUCT.md.template          # Product vision template
└── sync-instructions.sh         # Script to sync canonical AGENTS.md to tool-specific files
```

---

### 10.2 Dynamic Context Engineering (`04_dynamic_context.tex`)

**Existing Coverage:** MCP server exists but missing additional configurations

**Additional Examples Found:**

| Example | Lines | Status | Action |
|---------|-------|--------|--------|
| FastMCP basic server | 135-148 | ✅ Covered | In company-docs-server |
| Claude Desktop config | 155-162 | ✅ Covered | Exists |
| Cursor MCP config | 165-172 | ✅ Covered | Exists |
| MCP Security mitigations | 95-115 | ❌ Missing | Add security config guide |
| Context7 setup | 190-210 | ⚠️ Partial | Expand setup guide |
| Shopify Wiki MCP example | 220-235 | ❌ Missing | Add wiki-server variant |
| Custom MCP implementation patterns | 255-280 | ❌ Missing | Add template patterns |

**NEW Proposed Addition: `/05-mcp-servers/templates/`**

```
templates/
├── wiki-server/                 # Internal wiki MCP pattern (Shopify style)
│   ├── server.py
│   ├── README.md
│   └── requirements.txt
├── database-schema-server/      # Schema introspection MCP
│   ├── server.py
│   └── config.example.json
├── api-contract-server/         # OpenAPI spec serving MCP
│   └── server.py
├── observability-server/        # Logs/metrics MCP pattern
│   └── server.py
└── MCP_SECURITY.md              # Security hardening guide
```

---

### 10.3 Context Flow Control (`05_context_flow.tex`)

**High-Value Examples Not Yet Implemented:**

| Example | Lines | Value | Description |
|---------|-------|-------|-------------|
| TDD handoff workflow | 80-120 | HIGH | `tdd-red.agent.md` → `tdd-green.agent.md` → `tdd-refactor.agent.md` |
| Subagent research pattern | 145-175 | HIGH | Research delegation with summary return |
| Context compaction strategy | 200-235 | MEDIUM | Manual compact commands and timing |
| Todo list for complex tasks | 245-275 | LOW | Built-in VS Code feature |
| Essential commands reference table | 280-295 | MEDIUM | Quick reference for context commands |

**NEW Proposed Addition: `/06-custom-agents/tdd-workflow/`**

```
tdd-workflow/
├── README.md                    # TDD workflow overview
├── tdd-red.agent.md             # Write failing tests agent
├── tdd-green.agent.md           # Make tests pass agent
├── tdd-refactor.agent.md        # Code improvement agent
└── workflow-diagram.md          # Visual workflow guide
```

**NEW Proposed Addition: `/10-reference/context-commands.md`**

Essential commands reference table with:
- `/init`, `/clear`, `/compact`, `/context`, `/config`
- `/resume`, `/continue`, `Shift+Tab (2x)`
- When to use each command

---

### 10.4 Multi-Agent Workflows (`06_multi_agent.tex`)

**Critical Examples with High Implementation Value:**

| Example | Lines | Value | Status |
|---------|-------|-------|--------|
| test-agent persona | 55-85 | HIGH | ❌ Missing (add to custom-agents) |
| Orchestrator-Worker diagram | 110-145 | MEDIUM | ❌ Missing |
| Custom agent patterns table | 155-170 | MEDIUM | Partial |
| Teams of Coding Agents tools comparison | 200-280 | HIGH | ❌ Missing |
| Context Engineering Maturity Model | 425-480 | HIGH | ❌ Missing |

**NEW Proposed Addition: `/06-custom-agents/starter-agents/`**

```
starter-agents/
├── docs-agent.agent.md          # Documentation writer
├── test-agent.agent.md          # QA engineer persona
├── security-agent.agent.md      # Security reviewer
├── refactor-agent.agent.md      # Code improvement
└── README.md                    # When to use each
```

**NEW Proposed Addition: `/10-reference/maturity-model.md`**

The book defines a 5-level Context Engineering Maturity Model:
- Level 0: No Context Engineering
- Level 1: Basic Static Context
- Level 2: Managed Context
- Level 3: Advanced Multi-Agent
- Level 4: Autonomous Context (Experimental)

Each level has checklist items that should be extracted.

---

### 10.5 Development Practices (`07_dev_practices.tex`)

**TDD + AI Examples (HIGH VALUE):**

| Example | Lines | Description |
|---------|-------|-------------|
| Traditional TDD cycle diagram | 50-75 | Red-Green-Refactor visual |
| TDD + AI cycle 7-step workflow | 80-130 | Extended workflow with AI |
| TDD + AI workflow comparison | 155-180 | Side-by-side comparison |
| Human review checklist | 100-115 | 5-point review checklist |

**NEW Proposed Addition: `/09-testing/tdd-ai-workflow/`**

```
tdd-ai-workflow/
├── README.md                    # TDD + AI methodology
├── workflow-steps.md            # 7-step workflow from book
├── human-review-checklist.md    # Required review points
├── example-session/             # Complete TDD session transcript
│   ├── 01-write-failing-test.md
│   ├── 02-prompt-ai.md
│   ├── 03-review-code.md
│   └── 04-refactor.md
└── COMPARISON.md                # Traditional vs AI-assisted TDD
```

---

### 10.6 Measurement & Observability (`10_measurement.tex`)

**Practical Examples Found:**

| Example | Lines | Value | Description |
|---------|-------|-------|-------------|
| PR Size analysis script | 45-52 | HIGH | Git one-liner for analysis |
| Code churn rate script | 70-78 | HIGH | Git command for churn |
| Test coverage dashboard | 105-115 | MEDIUM | ASCII dashboard example |
| Static analysis dashboard | 125-135 | MEDIUM | ASCII dashboard example |
| Refactoring activity tracker | 145-155 | MEDIUM | Git grep command |

**NEW Proposed Addition: `/10-reference/measurement/`**

```
measurement/
├── README.md                    # Overview of AI measurement
├── git-analysis-scripts.sh      # All git one-liners from book
├── pr-size-monitor/             # GitHub Action for PR size alerts
│   ├── action.yml
│   └── README.md
├── dashboards/                  # ASCII dashboard templates
│   ├── coverage-trend.md
│   └── static-analysis.md
└── metrics-checklist.md         # What to measure post-AI adoption
```

---

## APPENDIX C SCAN: Implementation Guide and Solutions

### C.1 Agent Types and Concepts (Lines 1-200)

**Conceptual Content (Not Code):**
- Local Agents characteristics
- Background Agents with Git Worktree isolation
- Cloud Agents (Copilot Coding Agent)
- Third-Party Agents (OpenAI Codex)
- Subagents: How they work

**Already well covered in existing agents. No action needed.**

---

### C.2 Creating Custom Agents (Lines 200-400)

**HIGH VALUE Examples:**

| Example | Lines | Status | Priority |
|---------|-------|--------|----------|
| Complete Planner Agent | 235-285 | ❌ Missing | HIGH |
| Built-in tools table | 290-320 | ❌ Missing | MEDIUM |
| Effective instructions guide | 325-360 | ❌ Missing | HIGH |
| MCP server configuration | 365-395 | ✅ Covered | - |

**NEW Proposed Addition: `/06-custom-agents/how-to-write/`**

```
how-to-write/
├── README.md                    # How to write effective agents
├── agent-structure.md           # YAML frontmatter + body format
├── tools-reference.md           # Built-in tools table
├── six-core-areas.md            # Commands, testing, project, style, git, boundaries
├── examples/
│   ├── good-agent.agent.md      # Well-structured example
│   └── bad-agent.agent.md       # Common mistakes to avoid
└── CHECKLIST.md                 # Agent configuration checklist
```

---

### C.3 Enterprise Workflow Agent Profiles (Lines 400-850)

**COMPLETE AGENT IMPLEMENTATIONS (HIGH VALUE):**

These are production-ready agent files ready for extraction:

| Agent | Lines | File Location | Key Features |
|-------|-------|---------------|--------------|
| Requirement Analyst | 430-510 | `requirement-analyst.md` | Commands, boundaries, handoffs |
| Architect | 515-585 | `architect.md` | Mermaid diagrams, validation |
| API Champion | 590-665 | `api-champion.md` | OpenAPI, Redocly lint |
| Messaging Champion | 670-745 | `messaging-champion.md` | AsyncAPI, DLQ patterns |
| Test Explorer | 750-835 | `test-explorer.md` | Test case templates, traceability |
| Test Engineer | 840-920 | `test-engineer.md` | Jest/Vitest, self-assessment |
| Software Engineer | 925-1020 | `software-engineer.md` | 70% threshold, Zod patterns |

**Status:** ✅ Already extracted in `/07-enterprise-workflow/`

**ENHANCEMENT NEEDED:**
The current extraction may be missing the complete files. Need to verify completeness.

---

### C.4 Handoff Payload Schema (Lines 1025-1095)

**JSON Schema for Handoff Validation:**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Handoff Payload",
  "type": "object",
  "required": ["schema_version", "trace_id", "from_agent", "to_agent", 
               "artifacts", "validation_status"]
  // ... complete schema in book
}
```

**NEW Proposed Addition: `/07-enterprise-workflow/handoffs/handoff-schema.json`**

Complete JSON Schema for programmatic validation of handoffs.

---

### C.5 Best Practices Checklists (Lines 1095-1180)

**THREE CRITICAL CHECKLISTS:**

| Checklist | Lines | Items | Status |
|-----------|-------|-------|--------|
| Agent Configuration | 1100-1130 | 13 items | ❌ Missing |
| Multi-Agent Workflow | 1135-1155 | 9 items | ❌ Missing |
| Background Agent Best Practices | 1160-1180 | 6 items | ❌ Missing |

**NEW Proposed Addition: `/07-enterprise-workflow/checklists/`**

```
checklists/
├── agent-configuration.md       # 13-item checklist
├── multi-agent-workflow.md      # 9-item checklist
├── background-agents.md         # 6-item checklist
└── README.md                    # When to use each
```

---

### C.6 Exercise Solutions (Lines 1200-2199)

**COMPLETE SOLUTIONS FOR BOOK EXERCISES:**

| Exercise | Lines | Tool Coverage | Status |
|----------|-------|---------------|--------|
| Create First Instruction File | 1220-1330 | All 3 tools | ⚠️ Partial |
| Add MCP to Workflow | 1335-1445 | All 3 tools | ⚠️ Partial |
| First Multi-Agent Workflow (TDD) | 1450-1600 | GitHub Copilot | ❌ Missing |
| Multi-Step Feature Implementation | 1605-1780 | All 3 tools | ❌ Missing |
| Subagents for Complex Tasks | 1785-1880 | VS Code | ❌ Missing |
| Background Agents with Isolation | 1900-2100 | VS Code | ❌ Missing |

**NEW Proposed Addition: `/10-reference/exercise-solutions/`**

```
exercise-solutions/
├── README.md                    # Index of exercises
├── 01-first-instruction-file/
│   ├── copilot-instructions.md
│   ├── CLAUDE.md
│   └── cursor-project.mdc
├── 02-mcp-workflow/
│   ├── claude-config.json
│   ├── cursor-config.json
│   └── copilot-setup.md
├── 03-tdd-workflow/
│   ├── test-writer.agent.md
│   └── implementer.agent.md
├── 04-multi-step-feature/
│   └── workflow-transcript.md
├── 05-subagents/
│   ├── researcher.agent.md
│   └── usage-guide.md
└── 06-background-agents/
    └── parallel-workflow.md
```

---

## UPDATED PRIORITY RECOMMENDATIONS

### Priority 1 - CRITICAL (New from deep scan)

| Addition | Source | Effort | Value |
|----------|--------|--------|-------|
| TDD Workflow agents (`tdd-red`, `tdd-green`, `tdd-refactor`) | Ch10 §3 | Medium | Very High |
| Starter agents (docs, test, security, refactor) | Ch10 §4 | Medium | Very High |
| Context Engineering Maturity Model | Ch10 §4 | Low | High |
| Enterprise workflow checklists (3 checklists) | App C | Low | High |

### Priority 2 - HIGH (New from deep scan)

| Addition | Source | Effort | Value |
|----------|--------|--------|-------|
| Exercise solutions folder (6 exercises) | App C | High | High |
| MCP server templates (wiki, schema, API, observability) | Ch10 §2 | High | High |
| Measurement scripts and dashboards | Ch10 §6 | Medium | Medium |
| Agent writing guide | App C | Medium | High |

### Priority 3 - MEDIUM (New from deep scan)

| Addition | Source | Effort | Value |
|----------|--------|--------|-------|
| Cross-tool compatibility guide | Ch10 §1 | Low | Medium |
| Context commands reference | Ch10 §3 | Low | Medium |
| Handoff JSON schema | App C | Low | Medium |
| TDD + AI workflow documentation | Ch10 §5 | Medium | Medium |

---

## CONSOLIDATED IMPLEMENTATION PLAN

### Immediate High Value (Recommend for Task 5.2):

1. **`/06-custom-agents/tdd-workflow/`** — Complete TDD agent chain from Chapter 10
2. **`/06-custom-agents/starter-agents/`** — 4 essential starter agents
3. **`/07-enterprise-workflow/checklists/`** — 3 critical checklists
4. **`/10-reference/maturity-model.md`** — Context Engineering Maturity Model

### Phase 4 Additions:

5. **`/10-reference/exercise-solutions/`** — All 6 exercise solutions from Appendix C
6. **`/05-mcp-servers/templates/`** — Additional MCP patterns
7. **`/10-reference/measurement/`** — Git scripts and dashboards

### GitHub Issues for Community:

8. Cross-tool sync script
9. Printable reference cards
10. Additional MCP server variants

---

## Validation Requested (Updated)

Please review and approve these additions from the deep scan:

**Critical:**
- [ ] Create `/06-custom-agents/tdd-workflow/` with TDD agent chain
- [ ] Create `/06-custom-agents/starter-agents/` with 4 essential agents
- [ ] Create `/07-enterprise-workflow/checklists/` with 3 checklists
- [ ] Create `/10-reference/maturity-model.md`

**High Priority:**
- [ ] Create `/10-reference/exercise-solutions/` with Appendix C solutions
- [ ] Create `/05-mcp-servers/templates/` with MCP patterns
- [ ] Create `/10-reference/measurement/` with git scripts

**Medium Priority:**
- [ ] Add cross-tool compatibility README
- [ ] Add context commands quick reference
- [ ] Add handoff JSON schema

---

## Cross-Reference: Overlap with Existing Plan

| COMPANION_REPO_PLAN Task | Deep Scan Finding | Status |
|--------------------------|-------------------|--------|
| Task 1.2: Context Engineering | Chapter 10 §1 examples | ✅ Complete |
| Task 1.3: MCP Server | Chapter 10 §2 patterns | ⚠️ Expand with templates |
| Task 2.1: Custom Agents | Chapter 10 §4 + App C | ⚠️ Add starter agents |
| Task 2.2: Enterprise Workflow | App C §3 | ⚠️ Add checklists |
| Task 4.4: Reference Materials | Chapter 10 §5-6 + App C §6 | ❌ Add measurement + exercises |

---
---

# ADDENDUM 2: Chapter 10 Pitfalls Section Analysis

> **Scan Date:** 2025-12-16  
> **Source:** `chapters_verbose/chapter10/11_pitfalls.tex`  
> **Purpose:** Identify additional content for antipatterns folder

---

## KEY FINDING: Two Distinct Sets of Antipatterns

The book explicitly distinguishes between:

1. **Chapter 7 Antipatterns (8 total)** — "Timeless failure modes of AI-assisted development"
2. **Chapter 10 Pitfalls (5 total)** — "2025-specific organizational and tool landscape pitfalls"

> *"Unlike the timeless antipatterns in Chapter 7, these five pitfalls arise from specific characteristics of the 2025 AI landscape"*

**All 5 pitfalls are marked `Status: HOLD` in ThoughtWorks Radar** — meaning "Proceed with extreme caution or avoid entirely."

---

## THE 5 CHAPTER 10 PITFALLS

### Pitfall 1: AI-Accelerated Shadow IT

**Definition:** Employees using AI tools to build business-critical applications outside IT governance.

**Key Content to Extract:**

| Content Type | Description | Lines |
|--------------|-------------|-------|
| Comparison table | Traditional vs AI-Accelerated Shadow IT | 65-80 |
| Warning signs checklist | 7 organizational warning signs | 95-105 |
| Risk categories | Data breach, Continuity, Compliance | 110-120 |
| Governance flowchart | Fast-lane governance diagram | 130-180 |
| Policy template | AI Development Tools Policy (Markdown) | 240-260 |
| Incident response | Adopt/Replace/Sunset pathways | 195-230 |

**Proposed Files:**
```
/11-antipatterns/pitfalls/
├── shadow-it/
│   ├── README.md                    # Overview and risks
│   ├── warning-signs-checklist.md   # 7 organizational symptoms
│   ├── governance-fast-lane.md      # Risk-based triage process
│   ├── ai-tools-policy.md           # Template policy document
│   └── incident-response.md         # Adopt/Replace/Sunset guide
```

---

### Pitfall 2: Text-to-SQL

**Definition:** Allowing AI to convert natural language directly into SQL without human review.

**Key Content to Extract:**

| Content Type | Description | Lines |
|--------------|-------------|-------|
| Problem examples | 4 core problems with code samples | 290-380 |
| Alternatives table | What to use instead | 385-400 |
| Semantic layer example | YAML definition for dbt/Cube | 410-450 |
| GraphQL pattern | Schema example for LLM data access | 455-485 |
| Query templates | Validated query library pattern | 490-520 |
| Acceptable conditions | 6 conditions checklist | 525-535 |

**Proposed Files:**
```
/11-antipatterns/pitfalls/
├── text-to-sql/
│   ├── README.md                    # Why it fails
│   ├── problems-examples.md         # 4 problems with code
│   ├── semantic-layer-example.yaml  # dbt/Cube pattern
│   ├── graphql-alternative.md       # GraphQL as safer option
│   ├── query-templates.py           # Validated query pattern
│   └── acceptable-conditions.md     # When it might be OK
```

---

### Pitfall 3: Capacity-Driven Development

**Definition:** Assigning developers to features outside their primary stream because "they have capacity."

**Key Content to Extract:**

| Content Type | Description | Lines |
|--------------|-------------|-------|
| Congestion collapse example | Week-by-week velocity decline | 590-620 |
| Better alternatives | 5 alternatives to context switching | 640-720 |
| WIP limits policy | Cross-stream work policy template | 725-745 |
| Dynamic reteaming | Permanent vs temporary assignment | 750-780 |
| Decision framework | DO/DON'T table by situation | 785-800 |
| Warning signs | 8 organizational symptoms | 810-825 |

**Proposed Files:**
```
/11-antipatterns/pitfalls/
├── capacity-driven/
│   ├── README.md                    # The antipattern explained
│   ├── congestion-collapse.md       # Example scenario
│   ├── better-alternatives.md       # 5 alternatives
│   ├── wip-limits-policy.md         # Policy template
│   ├── reteaming-guide.md           # Dynamic reteaming vs temp assignment
│   └── warning-signs.md             # 8 symptoms checklist
```

---

### Pitfall 4: Standalone Data Engineering Teams

**Definition:** Dedicated data team separate from product teams, creating domain knowledge gaps.

**Key Content to Extract:**

| Content Type | Description | Lines |
|--------------|-------------|-------|
| Domain knowledge gap example | CLV calculation scenario | 865-900 |
| Data Mesh structure | Team topology diagram | 945-970 |
| Transition phases | 4-phase migration guide | 980-1020 |
| Concerns/responses | FAQ addressing objections | 1025-1055 |
| Decision framework | Recommendations by org size | 1060-1075 |

**Proposed Files:**
```
/11-antipatterns/pitfalls/
├── standalone-data-teams/
│   ├── README.md                    # Why it's an antipattern
│   ├── domain-gap-example.md        # CLV scenario
│   ├── data-mesh-topology.md        # Alternative structure
│   ├── transition-guide.md          # 4-phase migration
│   └── objections-faq.md            # Common concerns addressed
```

---

### Pitfall 5: Unoptimized MCP Token Usage (HIGH VALUE)

**Definition:** Loading all MCP tool definitions into context upfront, causing token bloat.

**Key Content to Extract:**

| Content Type | Description | Lines |
|--------------|-------------|-------|
| Scale example | Token overhead by server count | 1115-1135 |
| Data round-tripping | Before/after code examples | 1140-1180 |
| Pattern comparison table | Default vs Code execution | 1215-1230 |
| Progressive discovery | Filesystem structure for tools | 1245-1280 |
| Data filtering example | Before/after code (99% reduction) | 1285-1340 |
| Privacy-preserving pattern | Tokenization example | 1345-1395 |
| Skills/state persistence | Reusable code pattern | 1400-1430 |
| Decision framework | When to use each pattern | 1475-1500 |
| Migration strategy | 4-phase optimization plan | 1515-1555 |
| Warning signs | 7 symptoms of token bloat | 1560-1575 |

**Proposed Files:**
```
/11-antipatterns/pitfalls/
├── mcp-token-bloat/
│   ├── README.md                    # The problem explained
│   ├── scale-calculations.md        # Token overhead examples
│   ├── optimization-patterns/
│   │   ├── progressive-discovery.ts # On-demand tool loading
│   │   ├── data-filtering.ts        # Sandbox processing
│   │   ├── privacy-preserving.ts    # PII tokenization
│   │   └── skills-persistence.ts    # Reusable code
│   ├── pattern-comparison.md        # Default vs Code execution
│   ├── decision-framework.md        # When to use each
│   ├── migration-strategy.md        # 4-phase plan
│   └── warning-signs.md             # 7 symptoms
```

---

## UPDATED ANTIPATTERNS FOLDER STRUCTURE

The `/11-antipatterns/` folder should now include BOTH sets:

```
/11-antipatterns/
├── README.md                        # Overview: 8 + 5 = 13 total
│
├── chapter7-antipatterns/           # 8 "Timeless" antipatterns
│   ├── 01-blind-acceptance/
│   ├── 02-the-70-percent-trap/
│   ├── 03-vibe-production-deployment/
│   ├── 04-context-free-generation/
│   ├── 05-batch-size-explosion/
│   ├── 06-security-as-afterthought/
│   ├── 07-learning-loop-destruction/
│   └── 08-measurement-theater/
│
├── chapter10-pitfalls/              # 5 "2025-specific" pitfalls
│   ├── 01-shadow-it/
│   ├── 02-text-to-sql/
│   ├── 03-capacity-driven/
│   ├── 04-standalone-data-teams/
│   └── 05-mcp-token-bloat/
│
├── detection/                       # Cross-cutting detection tools
│   ├── organizational-audit.md      # Audit against all 13
│   └── pr-size-analyzer/            # GitHub Action
│
└── ANTIPATTERN_MATRIX.md            # Summary table of all 13
```

---

## HIGH-VALUE EXTRACTIONS FROM PITFALLS

### Summary Table from Book (Line 1600-1620)

| Pitfall | Core Problem | Primary Risk | Quick Test |
|---------|--------------|--------------|------------|
| AI-accelerated shadow IT | Ungoverned apps proliferate | Security, compliance, continuity | Do you know what your staff is building? |
| Text-to-SQL | AI generates unreliable queries | Wrong data → bad decisions | Can AI explain the business logic? |
| Capacity-driven development | Context switching destroys productivity | Congestion collapse, burnout | Are developers regularly switching streams? |
| Standalone data teams | Domain knowledge gap | Useless data products, bottlenecks | Do data engineers sit with product teams? |
| Unoptimized MCP token usage | Tool/data bloat in context | Cost explosion, context limits | What % of tokens do actual work? |

### Book Quote (Critical Framing)

> *"All five share a pattern: They optimize for the wrong thing. They look efficient in isolation but create systemic problems."*

---

## UPDATED PRIORITY RECOMMENDATIONS

### Antipatterns Folder - Now CRITICAL Priority

| Component | Source | Effort | Value |
|-----------|--------|--------|-------|
| Chapter 7: 8 antipatterns | chapter07_antipatterns.tex | High | Very High |
| Chapter 10: 5 pitfalls | chapter10/11_pitfalls.tex | High | Very High |
| MCP Token Optimization patterns | 11_pitfalls.tex (code samples) | Medium | Very High |
| Organizational audit checklist | Combined | Low | High |
| PR size analyzer GitHub Action | 11_pitfalls.tex reference | Medium | High |

**Total: 13 antipatterns/pitfalls to document**

---

## VALIDATION REQUESTED (Pitfalls Addition)

Please approve these additions from the pitfalls scan:

**New Structure:**
- [ ] Expand `/11-antipatterns/` to include both Chapter 7 antipatterns AND Chapter 10 pitfalls
- [ ] Create `chapter7-antipatterns/` subfolder (8 items)
- [ ] Create `chapter10-pitfalls/` subfolder (5 items)

**High-Value Code Extractions:**
- [ ] MCP token optimization patterns (progressive discovery, data filtering, privacy-preserving, skills persistence)
- [ ] Text-to-SQL alternatives (semantic layer YAML, GraphQL schema, query templates)
- [ ] Policy templates (AI tools policy, WIP limits policy)

**Detection Tools:**
- [ ] Organizational audit checklist (all 13 antipatterns)
- [ ] ANTIPATTERN_MATRIX.md summary table
