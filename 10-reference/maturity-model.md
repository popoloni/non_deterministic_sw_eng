# Context Engineering Maturity Model

> **Book Reference:** Chapter 10, Sections 1 & 6 — "Understanding Tool Maturity Levels" & "Context Engineering Maturity Model"

This guide combines two complementary maturity models from *Non-Deterministic Software Engineering*:

1. **Tool Maturity Model** — ThoughtWorks-style rings for evaluating AI tool readiness
2. **Context Engineering Maturity Model** — Organizational progression through context sophistication levels

Use both together: Tool Maturity tells you *which tools to use*, Context Engineering Maturity tells you *how to use them effectively*.

---

## Part 1: Tool Maturity Model (Four Rings)

The ThoughtWorks Technology Radar model has proven effective for 15+ years across hundreds of enterprises. Apply it to AI tools and practices.

### 🟢 ADOPT: Production-Ready

| Aspect | Description |
|--------|-------------|
| **Definition** | Proven across multiple organizations and contexts |
| **Confidence** | High — strongly recommend adoption |
| **When to use** | Default choice for critical workflows |
| **Risk level** | Low — well-understood failure modes and mitigations |

**Examples (as of December 2025):**
- GitHub Copilot
- Cursor
- Pre-commit hooks
- TDD with AI
- Context flow control (Plan/Act mode)

**Your Action:** Start here. These are battle-tested.

---

### 🟡 TRIAL: Context-Proven

| Aspect | Description |
|--------|-------------|
| **Definition** | Proven in specific contexts, important to understand how to build capability |
| **Confidence** | Medium — worth pursuing, handle with care |
| **When to use** | Projects that can handle some risk, pilot teams |
| **Risk level** | Medium — understand failure modes before scaling |

**Examples (as of December 2025):**
- Claude Code (agentic mode)
- Context7 MCP server
- MCP servers (general)
- Custom agent personas
- Static context (AGENTS.md)
- Dynamic context (MCP)

**Your Action:** Try with pilot teams, validate in your context.

---

### 🔵 ASSESS: Emerging

| Aspect | Description |
|--------|-------------|
| **Definition** | Worth exploring to understand potential impact |
| **Confidence** | Low — experimental, may not work for you |
| **When to use** | Innovation time, hackathons, non-critical exploration |
| **Risk level** | High — may be immature, rapidly changing |

**Examples (as of December 2025):**
- Spec-driven development tools
- Teams of coding agents
- Multi-agent workflows
- Toxic flow analysis

**Your Action:** Explore carefully, don't bet critical projects on these.

---

### 🔴 HOLD: Proceed with Extreme Caution

| Aspect | Description |
|--------|-------------|
| **Definition** | Significant concerns, antipatterns, or risks identified |
| **Confidence** | Strong negative signal |
| **When to use** | Only with significant mitigations in place |
| **Risk level** | Very high — can cause serious problems |

**Examples (as of December 2025):**
- Text-to-SQL without guardrails
- Naive API-to-MCP conversion
- AI-accelerated shadow IT

**Your Action:** Avoid, or implement only with robust safeguards.

---

## Part 2: Context Engineering Maturity Model (Five Levels)

Progress through these levels systematically. Most successful teams reach Level 2 within three months and Level 3 within 6-12 months.

### Level 0: No Context Engineering

**Characteristics:**
- Developers use AI tools with no team guidance
- Everyone prompts differently
- Results are inconsistent
- No shared standards or documentation

**Symptoms:**
- "It works for me but not for others"
- Repeated explanations of project context
- Inconsistent code quality from AI assistance
- Team frustration with AI tools

**Timeline:** Exit within 2 weeks of adopting AI tools

---

### Level 1: Basic Static Context

**Checklist:**
- [ ] AGENTS.md file exists with basic standards
- [ ] Development commands documented
- [ ] ⚠️ Not regularly updated
- [ ] ⚠️ No dynamic retrieval

**What to Implement:**
```
.github/
└── copilot-instructions.md    # Basic project context

# OR

AGENTS.md                       # 40-line starter template
```

**Minimum AGENTS.md Content:**
```markdown
# Project: [Name]
## Tech Stack
- [Language/Framework]
- [Database]
- [Key libraries]

## Commands
- `npm test` - Run tests
- `npm run lint` - Check code style

## Coding Standards
- [2-3 key rules]
```

**Timeline:** Week 1 of AI adoption

---

### Level 2: Managed Context

**Checklist:**
- [ ] Comprehensive, maintained AGENTS.md
- [ ] Plan mode used for complex features
- [ ] 1-2 MCP servers for critical resources
- [ ] Shared prompt library for common tasks

**What to Implement:**
```
.github/
├── copilot-instructions.md
└── instructions/
    ├── api.instructions.md
    └── tests.instructions.md

# AND

MCP servers:
- context7 (framework docs)
- company-docs (internal knowledge)
```

**Key Practices:**
- Weekly AGENTS.md review in team meetings
- Plan mode before implementing features > 2 hours
- Shared prompt templates for code review, testing
- At least one MCP server connected

**Timeline:** Month 1-3

---

### Level 3: Advanced Multi-Agent

**Checklist:**
- [ ] Multiple MCP servers for different domains
- [ ] Custom agents for specialized workflows
- [ ] Handoffs between agents with human checkpoints
- [ ] Context7 or similar for framework documentation
- [ ] Enterprise workflow implemented

**What to Implement:**
```
.github/
├── agents/
│   ├── planner.md
│   ├── implementer.md
│   ├── reviewer.md
│   └── test-writer.md
└── copilot-instructions.md

MCP servers:
- context7 (frameworks)
- company-docs (internal)
- database-schema (real-time)
- api-contracts (OpenAPI)
```

**Key Practices:**
- Custom agents for recurring workflows
- Handoff configuration between agents
- Human checkpoints at phase boundaries
- Automated context freshness checks

**Timeline:** Month 3-12

---

### Level 4: Autonomous Context (Experimental)

**Checklist:**
- [ ] Self-updating context from codebase changes
- [ ] AI-assisted context curation
- [ ] Cross-agent context sharing

**Characteristics:**
- Context automatically updates when code changes
- AI suggests context improvements
- Agents share learned context with each other

**Important:** Level 4 is experimental. No organization has fully achieved this yet. Focus on mastering Levels 1-3 first.

**Timeline:** 12+ months (when tooling matures)

---

## Maturity Assessment Tool

### Quick Self-Assessment

Answer these questions to determine your current level:

```
1. Do you have an AGENTS.md or copilot-instructions.md file?
   [ ] No  → Level 0
   [ ] Yes → Continue

2. Is it updated at least monthly?
   [ ] No  → Level 1
   [ ] Yes → Continue

3. Do you use at least one MCP server?
   [ ] No  → Level 1
   [ ] Yes → Continue

4. Do you use Plan mode for complex features?
   [ ] No  → Level 1
   [ ] Yes → Level 2

5. Do you have custom agents for specific workflows?
   [ ] No  → Level 2
   [ ] Yes → Continue

6. Do you use handoffs between agents?
   [ ] No  → Level 2
   [ ] Yes → Level 3

7. Does your context auto-update from code changes?
   [ ] No  → Level 3
   [ ] Yes → Level 4 (experimental)
```

### Detailed Assessment Checklist

#### Level 1 Criteria (All required for Level 1)
- [ ] Static context file exists (AGENTS.md or equivalent)
- [ ] Tech stack documented
- [ ] Key commands documented
- [ ] Basic coding standards captured

#### Level 2 Criteria (All required for Level 2)
- [ ] All Level 1 criteria met
- [ ] Context file updated within last 30 days
- [ ] Plan mode documented and used by team
- [ ] At least 1 MCP server configured
- [ ] Shared prompts for common tasks

#### Level 3 Criteria (All required for Level 3)
- [ ] All Level 2 criteria met
- [ ] 3+ MCP servers configured
- [ ] Custom agents defined for 2+ workflows
- [ ] Handoff patterns documented
- [ ] Human checkpoint policy enforced
- [ ] Context freshness monitoring in place

---

## Progression Roadmap

### From Level 0 → Level 1 (Week 1)

**Day 1-2:**
1. Create minimal AGENTS.md (40 lines)
2. Document tech stack and key commands
3. Share with team

**Day 3-5:**
1. Add 3-5 coding standards
2. Document common workflows
3. Test with team members

**Success Criteria:**
- All team members can use the context file
- AI responses reference project-specific patterns

---

### From Level 1 → Level 2 (Month 1-3)

**Week 1-2:**
1. Expand AGENTS.md to full template
2. Add file-specific instruction files
3. Introduce Plan mode for complex work

**Week 3-4:**
1. Set up Context7 MCP server
2. Create shared prompt library
3. Establish weekly context review

**Month 2-3:**
1. Add second MCP server (company docs)
2. Create prompt templates for common tasks
3. Train team on managed context practices

**Success Criteria:**
- Context file updated at least monthly
- MCP servers provide real-time context
- Team consistently uses Plan mode

---

### From Level 2 → Level 3 (Month 3-12)

**Month 3-4:**
1. Define first custom agent (test-writer or docs)
2. Implement basic handoff pattern
3. Document human checkpoint policy

**Month 5-6:**
1. Add 2-3 more custom agents
2. Configure agent handoffs
3. Implement enterprise workflow (if applicable)

**Month 7-12:**
1. Connect 3+ domain-specific MCP servers
2. Automate context freshness checks
3. Measure and optimize workflow efficiency

**Success Criteria:**
- Multiple specialized agents in use
- Handoffs work smoothly
- Human checkpoints prevent automation failures

---

## Tool Recommendations by Maturity Level

| Level | Primary Tools | Context Strategy | Risk Tolerance |
|-------|---------------|------------------|----------------|
| 0 | GitHub Copilot basic | None | N/A |
| 1 | Copilot + static context | AGENTS.md only | Low |
| 2 | Copilot/Cursor + MCP | Static + 1-2 MCP servers | Medium |
| 3 | Multi-agent + MCP suite | Static + Dynamic + Agentic | Medium-High |
| 4 | Autonomous systems | Self-managing | Experimental |

### Recommended Tools by Ring

**🟢 ADOPT (All Levels):**
- GitHub Copilot Chat
- Cursor Editor
- Pre-commit hooks
- TDD practices

**🟡 TRIAL (Level 2+):**
- Claude Code (agentic mode)
- Context7 MCP server
- Custom agent personas
- MCP servers

**🔵 ASSESS (Level 3+):**
- Multi-agent workflows
- Spec-driven development
- Teams of agents

**🔴 HOLD (Avoid):**
- Text-to-SQL without validation
- Unsandboxed code execution
- Unreviewed AI commits

---

## Mapping to Organization Stages

### Stage 1: Just Starting (0-3 months)

| Action | Status |
|--------|--------|
| Focus on 🟢 ADOPT tools | ✅ Required |
| Master fundamentals | ✅ Required |
| 🟡 TRIAL experiments | ❌ Avoid |
| 🔵 ASSESS tools | ❌ Never |

**Target:** Level 1 maturity by end of month 1

---

### Stage 2: Building Competence (3-6 months)

| Action | Status |
|--------|--------|
| Continue 🟢 ADOPT for critical work | ✅ Required |
| Pilot 🟡 TRIAL with experienced teams | ✅ Encouraged |
| Limited 🔵 ASSESS (innovation time) | ⚠️ Careful |
| 🔴 HOLD patterns | ❌ Avoid |

**Target:** Level 2 maturity by end of month 3

---

### Stage 3: Advanced Capability (6+ months)

| Action | Status |
|--------|--------|
| 🟢 ADOPT as default | ✅ Required |
| 🟡 TRIAL where valuable | ✅ Expected |
| Selective 🔵 ASSESS | ⚠️ With hypotheses |
| 🔴 HOLD with safeguards | ⚠️ Careful |

**Target:** Level 3 maturity by month 6-12

---

## Important: Status Labels Change

What was 🔵 ASSESS in 2024 may be 🟢 ADOPT in 2025. Tools mature, practices crystallize, and confidence grows.

**Example Trajectory:**
| Date | Tool/Practice | Status |
|------|---------------|--------|
| Oct 2024 | GenAI for legacy code | 🔵 ASSESS |
| Apr 2025 | Multiple client successes | 🟡 TRIAL |
| Nov 2025 | Proven across 50+ orgs | 🟢 ADOPT |

**Recommendation:** Check [ThoughtWorks Technology Radar](https://thoughtworks.com/radar) biannually for updated recommendations.

---

## Quick Reference Card

### Current Level Indicators

| Level | Key Indicator | Timeline |
|-------|---------------|----------|
| 0 | No shared context | Exit in 2 weeks |
| 1 | Basic AGENTS.md exists | Week 1 |
| 2 | MCP + Plan mode active | Month 1-3 |
| 3 | Custom agents + handoffs | Month 3-12 |
| 4 | Auto-updating context | 12+ months |

### Tool Ring Summary

| Ring | Confidence | Action |
|------|------------|--------|
| 🟢 ADOPT | High | Use immediately |
| 🟡 TRIAL | Medium | Pilot carefully |
| 🔵 ASSESS | Low | Explore in innovation time |
| 🔴 HOLD | Negative | Avoid or heavily mitigate |

---

## Related Resources

- [AGENTS.md Templates](../04-context-engineering/agents-md/) — Static context examples
- [MCP Servers](../05-mcp-servers/) — Dynamic context setup
- [Custom Agents](../06-custom-agents/) — Agent configurations
- [Enterprise Workflow](../07-enterprise-workflow/) — Level 3 implementation

---

*Based on patterns from "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10 — Tool Maturity and Context Engineering Maturity models.*
