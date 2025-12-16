# 02 - Specifications

> 📖 **Book Reference:** Chapter 7, Pattern 1 (Spec-First Generation)

---

## Overview

Spec-First Generation is the foundation pattern for professional AI-assisted development. By writing detailed specifications before asking AI to generate code, you:

- Reduce iteration cycles
- Get more accurate initial implementations
- Create documentation as a byproduct
- Maintain control over architectural decisions

---

## Contents

| File | Description |
|------|-------------|
| [auth-middleware-spec.md](./auth-middleware-spec.md) | Complete JWT authentication middleware specification |
| [api-endpoint-spec.md](./api-endpoint-spec.md) | Template for API endpoint specifications |
| [feature-spec-template.md](./feature-spec-template.md) | Generic feature specification template |

---

## How to Use

### 1. Choose the Right Template

- **auth-middleware-spec.md** — Use as a reference for security-critical components
- **api-endpoint-spec.md** — Use for any REST/GraphQL endpoint
- **feature-spec-template.md** — Use for general features

### 2. Fill in the Specification

Complete all sections, paying special attention to:
- Edge cases
- Error handling
- Security considerations
- Performance requirements

### 3. Prompt the AI

```
Implement the following specification exactly as described:

[Paste your completed specification]

Do not add features not mentioned in the spec.
Ask clarifying questions if any requirement is ambiguous.
```

### 4. Verify Against Spec

Use the specification as a checklist to verify the implementation covers all requirements.

---

## Specification Anatomy

A good specification includes:

```
## Purpose
What this component does and why it exists

## Requirements
Numbered list of functional requirements

## Interface
Function signatures, parameters, return types

## Edge Cases
Explicit handling for boundary conditions

## Error Handling
What errors can occur and how to handle them

## Security Considerations
Authentication, authorization, data validation

## Performance Requirements
Latency, throughput, resource constraints

## Examples
Sample inputs and expected outputs
```

---

## Tips

1. **Be specific about types** — "string" is vague; "ISO 8601 datetime string" is precise
2. **Include negative cases** — What should NOT happen is as important as what should
3. **Reference existing patterns** — "Use the same error format as UserService"
4. **Set boundaries** — "Maximum 100 items per request"
