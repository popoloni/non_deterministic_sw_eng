# Exercise 5: Subagents for Complex Tasks

> **Book Reference:** Chapter 10, Section "Multi-Agent Workflows"  
> **Time:** 1 hour  
> **Difficulty:** ⭐⭐⭐ Advanced

## Problem Statement

Use subagents to parallelize research and implementation. This exercise demonstrates delegating complex tasks to isolated contexts that return summaries without polluting the main session.

## Learning Objectives

After completing this exercise, you will:
- Create agents optimized for subagent use
- Enable subagent invocation from a main agent
- Execute research in isolated contexts
- Receive concise summaries back to main context

## Prerequisites

- Completed Exercises 1-4
- VS Code with GitHub Copilot (1.107+) or Claude Code
- Understanding of context window management

## Instructions

### Step 1: Create Researcher Agent (15 minutes)

Create `.github/agents/researcher.md`:

```markdown
---
name: Researcher
description: Researches technical topics, gathers information,
             and summarizes findings. Optimized for subagent use.
tools: ['search', 'read', 'fetch', 'githubRepo']
infer: true
---

# Researcher Agent

You research technical topics and provide concise summaries.

## Your Role
- Gather information from codebase and documentation
- Analyze existing patterns and implementations
- Summarize findings for the main agent

## Output Format
Always structure your response as:

```markdown
## Research Summary: [Topic]

### Key Findings
- [Finding 1]
- [Finding 2]

### Existing Patterns
- [Pattern with file reference]

### Recommendations
- [Actionable recommendation]

### Sources
- [File or URL references]
```

## Boundaries

### Always Do
- Reference specific files and line numbers
- Keep summaries concise (under 500 words)
- Focus on actionable information

### Never Do
- Make code changes
- Provide incomplete summaries
- Include irrelevant information
```

### Step 2: Enable Subagent Invocation (10 minutes)

Update your main agent (e.g., feature-developer) to include `runSubagent`:

```markdown
---
name: Feature Developer
description: Implements features using research and TDD.
tools: ['search', 'read', 'edit', 'runCommand', 'runSubagent']
---

# Feature Developer

When implementing complex features:
1. Use researcher subagent to understand existing patterns
2. Use test-writer subagent to create test specifications  
3. Implement code to pass tests

## Using Subagents

For research tasks, invoke:
"Run researcher as subagent to analyze [topic]"

For test creation, invoke:
"Run test-writer as subagent to create tests for [feature]"
```

### Step 3: Execute Workflow (35 minutes)

In VS Code Chat, with your main agent session active:

```
# First, verify available subagents
Developer: What subagents can you use?

Agent: I can use these custom agents as subagents:
       - researcher: Research technical topics
       - test-writer: Write test specifications
       - ...

# Invoke researcher as subagent
Developer: Run the researcher agent as a subagent to 
           analyze our current authentication patterns.
           I need to understand how we handle JWT tokens
           before implementing refresh tokens.

Agent: [Spawns researcher subagent]
       [Subagent researches independently]
       [Returns summary to main context]
       
       Based on the research:
       
       ## Research Summary: Authentication Patterns
       
       ### Key Findings
       - JWT tokens stored in httpOnly cookies
       - Token validation in middleware (src/middleware/auth.ts)
       - No refresh token implementation currently
       
       ### Existing Patterns
       - Token generation: src/services/auth/tokenService.ts:23-45
       - Token validation: src/middleware/auth.ts:12-34
       
       ### Recommendations
       - Add refreshToken field to User model
       - Create /auth/refresh endpoint
       - Implement token rotation on refresh

# Continue with implementation using research
Developer: Great. Now implement refresh tokens following
           those patterns. Start with the token service.
```

### Preventing Subagent Usage

For agents that should NOT be used as subagents (e.g., deployment):

```markdown
---
name: Deployer
description: Handles production deployments. Not for subagent use.
tools: ['runCommand', 'read']
infer: false
---
```

## Verification Checklist

- [ ] Researcher agent file created with `infer: true`
- [ ] Main agent includes `runSubagent` in tools
- [ ] Subagent completed research in isolated context
- [ ] Main session received only summary, not raw data
- [ ] Implementation used patterns from research
- [ ] Context window stayed manageable throughout

## Success Criteria

- [ ] Researcher agent created with proper format
- [ ] `infer: true` set on researcher agent
- [ ] Main agent can invoke subagents
- [ ] Research returned as concise summary
- [ ] Main context not polluted with research details
- [ ] Feature implemented using research findings

## Hints

1. **Set `infer: true`** — Required for agent to be usable as subagent
2. **Keep summaries concise** — Subagents should return summaries, not raw data
3. **Use for research** — Ideal for exploring codebase before implementation
4. **Check context** — Verify main context stays clean after subagent returns

## Next Steps

After completing this exercise:
1. Try [Exercise 6: Background Agents](../exercise-6-background-agents/) for parallel execution
2. Create specialized subagents for your project
3. Experiment with chained subagent calls

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Chapter 10.*
