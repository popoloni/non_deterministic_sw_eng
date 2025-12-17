# 07 - Enterprise Workflow

> 📖 **Book Reference:** Appendix C (Solutions and Implementation Guide)

---

## Overview

Enterprise AI workflows orchestrate multiple specialized agents to handle complex software development tasks. This folder contains production-ready agent configurations for:

- **Planning Phase** — Requirements analysis, architecture design, API contracts
- **Execution Phase** — Test development, implementation, verification
- **Artifacts** — Templates for deliverables at each stage

---

## Contents

| Folder | Description |
|--------|-------------|
| [planning-phase/](./planning-phase/) | Agents for requirements and design |
| [execution-phase/](./execution-phase/) | Agents for implementation and testing |
| [artifacts/](./artifacts/) | Document templates for each workflow stage |
| [handoffs/](./handoffs/) | Configuration for agent-to-agent transitions |
| [checklists/](./checklists/) | **Validation checklists** for human checkpoints |

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      PLANNING PHASE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Requirements │───▶│  Architect   │───▶│    API       │       │
│  │   Analyst    │    │    Agent     │    │  Champion    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│   Business Context    Solution Design     API Definitions        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EXECUTION PHASE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │    Test      │───▶│     Test     │───▶│   Software   │       │
│  │  Explorer    │    │   Engineer   │    │   Engineer   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│    Test Cases          Test Code          Implementation         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Roles

### Planning Phase

| Agent | Input | Output | Purpose |
|-------|-------|--------|---------|
| Requirements Analyst | User story | Business Context | Extract and clarify requirements |
| Architect Agent | Business Context | Solution Design | Design technical approach |
| API Champion | Solution Design | API Definitions | Define contracts and interfaces |
| Messaging Champion | Solution Design | Event Schemas | Define async communication |

### Execution Phase

| Agent | Input | Output | Purpose |
|-------|-------|--------|---------|
| Test Explorer | API Definitions | Test Cases | Identify test scenarios |
| Test Engineer | Test Cases | Test Code | Implement automated tests |
| Software Engineer | Test Code + Design | Implementation | Build production code |

---

## Handoff Protocol

Each agent produces artifacts that feed into the next agent. Handoffs are defined in YAML:

```yaml
# handoffs/workflow-config.yaml
workflow:
  - agent: requirements-analyst
    inputs: [user-story]
    outputs: [business-context]
    next: architect-agent
    
  - agent: architect-agent
    inputs: [business-context]
    outputs: [solution-design]
    next: api-champion
```

---

## Quick Start

### 1. Start with Planning

```
Acting as the Requirements Analyst agent, analyze this user story:

[Paste your user story]

Produce a Business Context document following the template in artifacts/.
```

### 2. Chain to Architecture

```
Acting as the Architect Agent, design a solution for this Business Context:

[Paste Business Context from step 1]

Produce a Solution Design document following the template in artifacts/.
```

### 3. Continue Through Execution

Follow the workflow through Test Explorer → Test Engineer → Software Engineer.

---

## Tips

1. **Don't skip phases** — Each agent's output is the next agent's input
2. **Review artifacts** — Human review at each handoff catches issues early
3. **Maintain artifacts** — Store all intermediate documents for traceability
4. **Customize for your domain** — Adapt agent prompts to your tech stack
5. **Start simple** — Begin with 2-3 agents before full workflow
