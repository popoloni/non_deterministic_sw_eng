# Exercise 5 Solutions

This folder contains agent definitions optimized for subagent workflows.

## Agent Files

| File | Purpose | Subagent-Ready |
|------|---------|----------------|
| [researcher.md](./researcher.md) | Research and analysis | ✅ `infer: true` |
| [feature-developer.md](./feature-developer.md) | Main agent with subagent support | Has `runSubagent` |

## Key Configuration

### Making an Agent Subagent-Ready

Add `infer: true` to the frontmatter:

```yaml
---
name: Researcher
tools: ['search', 'read', 'fetch']
infer: true  # <-- Enables subagent usage
---
```

### Enabling Subagent Invocation

Add `runSubagent` to main agent's tools:

```yaml
---
name: Feature Developer
tools: ['search', 'read', 'edit', 'runCommand', 'runSubagent']
---
```

## Workflow Example

```
# Verify subagent availability
Developer: What subagents can you use?

Agent: I can use:
       - researcher: Research technical topics
       - test-writer: Write test specifications

# Invoke subagent for research
Developer: Run researcher as subagent to analyze 
           our authentication patterns

Agent: [Spawns researcher in isolated context]
       [Researcher analyzes codebase]
       [Returns summary to main context]
       
       ## Research Summary: Authentication Patterns
       
       ### Key Findings
       - JWT in httpOnly cookies
       - Validation in middleware
       
       ### Recommendations
       - Add refresh token support

# Use research in implementation
Developer: Implement refresh tokens using those patterns
```

## Preventing Subagent Usage

For sensitive agents (deployment, production access):

```yaml
---
name: Deployer
tools: ['runCommand', 'read']
infer: false  # <-- Cannot be used as subagent
---
```

## Verification Checklist

- [ ] Researcher has `infer: true`
- [ ] Main agent has `runSubagent` in tools
- [ ] Subagent returns summary (not raw data)
- [ ] Main context stays clean
- [ ] Sensitive agents have `infer: false`

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
