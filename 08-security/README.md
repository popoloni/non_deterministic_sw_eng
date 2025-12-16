# 08 - Security

> 📖 **Book Reference:** Chapter 7, Pattern 9 (Security-First Development)

---

## Overview

AI-generated code requires **heightened security vigilance**. AI assistants can introduce vulnerabilities through:

- Outdated security patterns from training data
- Missing input validation
- Hardcoded credentials in examples
- Insecure defaults
- Incomplete error handling that leaks information

This folder contains checklists and review guides to catch these issues.

---

## Contents

| Folder | Description |
|--------|-------------|
| [checklists/](./checklists/) | Security review checklists by category |

### Checklists

| File | Use When |
|------|----------|
| [auth-review.md](./checklists/auth-review.md) | Reviewing authentication/authorization code |
| [input-validation.md](./checklists/input-validation.md) | Reviewing data input handling |
| [data-protection.md](./checklists/data-protection.md) | Reviewing data storage and transmission |

---

## Security Review Process

### 1. Pre-Generation
Include security requirements in your specification:
```
## Security Requirements
- All inputs must be validated with zod schemas
- Use parameterized queries only (no string concatenation)
- Sanitize all output for XSS
- Log security events without sensitive data
```

### 2. Post-Generation Review
Use the appropriate checklist to review generated code:
- Run through each item
- Mark issues found
- Request fixes with specific guidance

### 3. Automated Scanning
Complement manual review with tools:
- **Semgrep** — Pattern-based static analysis
- **Snyk** — Dependency vulnerability scanning
- **GitGuardian** — Secrets detection
- **CodeQL** — Deep semantic analysis

---

## Common AI Security Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Hardcoded secrets | `const API_KEY = "sk-..."` | Use environment variables |
| SQL injection | `query = f"SELECT * WHERE id={id}"` | Parameterized queries |
| Missing auth checks | Endpoint without `requireAuth()` | Auth middleware on all routes |
| Verbose errors | `catch (e) { res.send(e.stack) }` | Generic error messages |
| Insecure defaults | `cors({ origin: '*' })` | Explicit origin allowlist |
| Eval usage | `eval(userInput)` | Never eval user input |

---

## Prompt Engineering for Security

When generating security-critical code, add explicit instructions:

```
Generate authentication middleware with the following security requirements:

1. Use constant-time comparison for token validation
2. Never log token contents, only token IDs
3. Set secure cookie flags (httpOnly, secure, sameSite)
4. Implement rate limiting (max 5 attempts per minute)
5. Return identical error messages for "user not found" and "wrong password"
6. Use bcrypt with cost factor 12 for password hashing
```

---

## Tips

1. **Assume AI code is insecure** — Verify everything
2. **Be explicit about security** — AI won't add security features unprompted
3. **Layer defenses** — Don't rely on a single security control
4. **Review dependencies** — AI may suggest outdated or vulnerable packages
5. **Test security** — Include security test cases in your test suite
