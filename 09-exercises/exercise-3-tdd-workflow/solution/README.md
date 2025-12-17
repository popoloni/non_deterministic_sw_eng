# Exercise 3 Solutions

This folder contains the complete TDD workflow agent definitions.

## Agent Files

| File | Purpose | Boundaries |
|------|---------|------------|
| [test-writer.md](./test-writer.md) | Write failing tests | tests/ only |
| [implementer.md](./implementer.md) | Make tests pass | src/ only |

## Workflow Execution Examples

### VS Code Interactive

```
1. Open Chat view (Ctrl+Alt+I)
2. Select "test-writer" from agents dropdown
3. Enter: "Write failing tests for user password reset..."
4. Review generated tests
5. Click "Hand off to Implementer" button
6. Review implementation
```

### Command Line

```bash
# Start with test-writer agent
copilot --agent=test-writer --prompt "Write failing tests for 
user password reset: request with email, token expiry 1hr, 
set new password with valid token"

# After reviewing tests, invoke implementer
copilot --agent=implementer --prompt "Make the password reset 
tests pass. Start with the request endpoint."
```

### GitHub.com

1. Create an issue describing the feature
2. Click "Assign to Copilot" and select "test-writer"
3. Review the PR with generated tests
4. Reassign to "implementer" agent

## Sample Test Output

```typescript
/**
 * TC-001: Password Reset Request
 * Requirement: User can request password reset with email
 */
describe('Password Reset', () => {
  describe('requestReset', () => {
    it('should create a reset token for valid email', async () => {
      const user = await createUser({ email: 'test@example.com' });
      const result = await passwordReset.requestReset('test@example.com');
      
      expect(result.success).toBe(true);
      expect(result.token).toBeDefined();
    });

    it('should return error for unknown email', async () => {
      const result = await passwordReset.requestReset('unknown@example.com');
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('User not found');
    });
  });

  describe('token expiry', () => {
    it('should expire token after 1 hour', async () => {
      const token = await createResetToken({ createdAt: hourAgo });
      
      expect(await isTokenValid(token)).toBe(false);
    });
  });
});
```

## Verification Checklist

- [ ] Test-writer only created files in `tests/`
- [ ] Tests initially failed (TDD verification)
- [ ] Implementer only created files in `src/`
- [ ] All tests now pass
- [ ] No test files were modified by implementer
- [ ] Handoff preserved context between agents

---

*From "Non-Deterministic Software Engineering" (2025) by Enrico Papalini, Appendix C.*
