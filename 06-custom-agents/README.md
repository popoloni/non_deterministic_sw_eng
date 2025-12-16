# 06 - Custom Agents

> 📖 **Book Reference:** Chapter 10, Section 6 (Multi-Agent Workflows)

---

## Overview

Custom agents are specialized AI personas with defined:
- **Capabilities** — What tools they can use
- **Boundaries** — What they cannot do
- **Expertise** — Domain-specific knowledge
- **Outputs** — Expected deliverables

By constraining AI to specific roles, you get more focused, reliable results.

---

## Contents

| Folder | Description | Platform |
|--------|-------------|----------|
| [github-agents/](./github-agents/) | Agents for GitHub Copilot | GitHub Copilot |
| [claude-agents/](./claude-agents/) | Agents for Claude Code | Claude Code |

---

## Agent Types

### Development Agents
| Agent | Purpose | Best For |
|-------|---------|----------|
| Test Agent | Write and run tests | TDD workflows |
| Docs Agent | Generate documentation | API docs, READMEs |
| Refactor Agent | Improve existing code | Tech debt reduction |

### Review Agents
| Agent | Purpose | Best For |
|-------|---------|----------|
| Security Agent | Security review | Pre-merge checks |
| Review Agent | Code review | PR feedback |

### Planning Agents
| Agent | Purpose | Best For |
|-------|---------|----------|
| Planning Agent | Break down features | Sprint planning |
| Implementation Agent | Execute plans | Coding tasks |

---

## Quick Start

### GitHub Copilot (VS Code)

1. Copy agents to your project:
```bash
mkdir -p YOUR_PROJECT/.github/agents
cp github-agents/*.md YOUR_PROJECT/.github/agents/
```

2. Invoke an agent in Copilot Chat:
```
@workspace Use the test-agent to write tests for UserService
```

### Claude Code

1. Reference agent definitions in your prompt:
```
Acting as the security-agent defined below, review this PR:

[Paste agent definition]
[Paste code to review]
```

2. Or save frequently-used agents as slash commands.

---

## Agent Definition Format

```markdown
---
description: One-line description of agent's purpose
tools: ['search', 'readFile', 'writeFile', 'runTests']
---

# Agent Name

You are a [role] who [primary responsibility].

## Capabilities
- What you CAN do (bulleted list)

## Commands
- `command` - What it does

## Boundaries
**Never do:**
- What you must NOT do (critical for safety)

## Output Format
Describe expected deliverables
```

---

## Composing Agents

Agents work best in sequences:

```
1. Planning Agent → Creates implementation plan
2. Test Agent → Writes tests for planned features
3. Implementation Agent → Implements to pass tests
4. Security Agent → Reviews for vulnerabilities
5. Docs Agent → Updates documentation
```

See [07-enterprise-workflow/](../07-enterprise-workflow/) for complete orchestration patterns.

---

## Tips

1. **One job per agent** — Focused agents outperform generalists
2. **Explicit boundaries** — What NOT to do is as important as what to do
3. **Specific tools** — List exactly which tools the agent can use
4. **Test your agents** — Run the same task multiple times to verify consistency
5. **Iterate definitions** — Refine based on actual outputs
