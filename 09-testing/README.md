# 09 - Testing

> 📖 **Book Reference:** Chapter 7, Pattern 3 (Test-Driven AI Development)

---

## Overview

Testing is your primary defense against AI-generated bugs. This folder contains:

- Testing patterns that work well with AI assistance
- Example test structures
- Strategies for test-driven AI development

---

## Contents

| Folder | Description |
|--------|-------------|
| [examples/](./examples/) | Example test files and patterns |

---

## Test-Driven AI Development (TDAID)

A workflow where tests are written **before** asking AI to generate implementation:

```
1. Write test specification
2. Ask AI to generate test code from specification
3. Verify tests fail appropriately
4. Ask AI to implement code that passes tests
5. Verify all tests pass
6. Review implementation for edge cases
```

### Benefits
- Forces clear requirements thinking
- Provides immediate verification of AI output
- Creates documentation as a byproduct
- Catches AI hallucinations early

---

## Testing Patterns for AI Code

### 1. Table-Driven Tests

Ideal for AI generation — structured input/output pairs:

```typescript
const testCases = [
  { input: "hello", expected: "HELLO", description: "lowercase" },
  { input: "HELLO", expected: "HELLO", description: "already uppercase" },
  { input: "HeLLo", expected: "HELLO", description: "mixed case" },
  { input: "", expected: "", description: "empty string" },
];

testCases.forEach(({ input, expected, description }) => {
  test(`toUpperCase: ${description}`, () => {
    expect(toUpperCase(input)).toBe(expected);
  });
});
```

### 2. Property-Based Tests

Let AI generate properties, not cases:

```typescript
test('reverse is involutory', () => {
  fc.assert(
    fc.property(fc.string(), (s) => {
      expect(reverse(reverse(s))).toBe(s);
    })
  );
});
```

### 3. Snapshot Tests

Useful for catching unexpected changes:

```typescript
test('component renders correctly', () => {
  const tree = renderer.create(<UserCard user={mockUser} />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

---

## Prompt Templates

### Generate Tests from Spec

```
Generate Jest tests for the following specification:

[Paste specification]

Requirements:
- Use table-driven tests where applicable
- Include edge cases: empty inputs, null values, boundary conditions
- Test error cases explicitly
- Use descriptive test names
```

### Generate Implementation from Tests

```
Implement a function that passes all the following tests:

[Paste test file]

Requirements:
- Match the function signature exactly
- Do not modify the tests
- Handle all edge cases shown in tests
```

---

## Coverage Strategy

| Coverage Type | Target | AI Capability |
|--------------|--------|---------------|
| Line coverage | 80%+ | ⭐⭐⭐⭐⭐ AI excellent |
| Branch coverage | 75%+ | ⭐⭐⭐⭐ AI good |
| Edge cases | Complete | ⭐⭐⭐ Needs prompting |
| Integration tests | Critical paths | ⭐⭐⭐ Needs guidance |
| Security tests | All auth paths | ⭐⭐ Needs explicit spec |

---

## Tips

1. **Tests first** — Write tests before asking for implementation
2. **Be specific about edges** — AI won't think of edge cases unprompted
3. **Review test logic** — AI-generated tests can have bugs too
4. **Maintain test quality** — Don't accept tests that always pass
5. **Use test coverage tools** — Verify AI claims about coverage
