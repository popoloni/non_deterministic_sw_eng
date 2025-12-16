---
applyTo: "**/*.test.ts,**/*.spec.ts"
---

# Test File Guidelines

When writing tests in this project:

## Structure
- Use `describe` blocks to group related tests
- Test descriptions should start with a verb
- One assertion per test when possible

## Table-Driven Tests
For utilities with multiple input/output cases:

```typescript
const cases = [
  { input: x, expected: y, name: 'description' },
];
cases.forEach(({ input, expected, name }) => {
  it(name, () => expect(fn(input)).toBe(expected));
});
```

## Mocking
- Use `vi.mock` for module mocking
- Use MSW for API mocking
- Reset mocks in `beforeEach`

## Coverage
- New code requires 80% coverage
- Critical paths require 100% coverage
