# Migration Pattern: React Class to Hooks

> 📖 **Book Reference:** Chapter 7, Pattern 12 - Migration as Learning  
> **Status:** Production-Ready Documentation

---

## Overview

This document captures the learnings from manually migrating React class components to functional components with hooks. Use this as reference when scaling migrations with AI.

---

## Key Transformations

### 1. State Management

**Before (Class):**
```typescript
class MyComponent extends React.Component<Props, State> {
  state = {
    loading: true,
    data: null,
    error: null
  };
}
```

**After (Hooks):**
```typescript
function MyComponent(props: Props) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Data | null>(null);
  const [error, setError] = useState<Error | null>(null);
}
```

**Rules:**
- Create separate `useState` for each state variable
- Preserve type information
- Initialize with same default values

---

### 2. Lifecycle Methods

#### componentDidMount → useEffect with empty deps

**Before:**
```typescript
componentDidMount() {
  this.fetchData();
}
```

**After:**
```typescript
useEffect(() => {
  fetchData();
}, []); // Empty dependency array = runs once on mount
```

#### componentDidUpdate → useEffect with deps

**Before:**
```typescript
componentDidUpdate(prevProps) {
  if (prevProps.userId !== this.props.userId) {
    this.fetchUser();
  }
}
```

**After:**
```typescript
useEffect(() => {
  fetchUser();
}, [userId]); // Runs when userId changes
```

#### componentWillUnmount → useEffect cleanup

**Before:**
```typescript
componentDidMount() {
  this.subscription = api.subscribe(this.handleUpdate);
}

componentWillUnmount() {
  this.subscription.unsubscribe();
}
```

**After:**
```typescript
useEffect(() => {
  const subscription = api.subscribe(handleUpdate);
  
  return () => {
    subscription.unsubscribe(); // Cleanup function
  };
}, []);
```

---

### 3. Methods

#### Regular methods → functions or useCallback

**Before:**
```typescript
handleClick = () => {
  this.setState({ clicked: true });
};

render() {
  return <button onClick={this.handleClick}>Click</button>;
}
```

**After (simple case):**
```typescript
function handleClick() {
  setClicked(true);
}

return <button onClick={handleClick}>Click</button>;
```

**After (passed to children - use useCallback):**
```typescript
const handleClick = useCallback(() => {
  setClicked(true);
}, []);

return <ChildComponent onClick={handleClick} />;
```

**Rules:**
- Use `useCallback` when:
  - Function is passed as prop to child components
  - Function is a dependency of another hook
- Use regular function when:
  - Function is only used in the same component's JSX
  - Performance isn't a concern

---

### 4. Props Access

**Before:**
```typescript
class MyComponent extends React.Component<Props> {
  render() {
    return <div>{this.props.title}</div>;
  }
}
```

**After:**
```typescript
function MyComponent({ title }: Props) {
  return <div>{title}</div>;
}
```

---

### 5. Refs

**Before:**
```typescript
class MyComponent extends React.Component {
  private inputRef = React.createRef<HTMLInputElement>();
  
  focusInput = () => {
    this.inputRef.current?.focus();
  };
  
  render() {
    return <input ref={this.inputRef} />;
  }
}
```

**After:**
```typescript
function MyComponent() {
  const inputRef = useRef<HTMLInputElement>(null);
  
  function focusInput() {
    inputRef.current?.focus();
  }
  
  return <input ref={inputRef} />;
}
```

---

## Edge Cases Discovered

### 1. Async Operations Need Cleanup

**Problem:** Component unmounts before async operation completes.

**Solution:**
```typescript
useEffect(() => {
  let cancelled = false;
  
  async function fetchData() {
    const result = await api.getData();
    if (!cancelled) {
      setData(result);
    }
  }
  
  fetchData();
  
  return () => {
    cancelled = true;
  };
}, []);
```

### 2. useEffect Dependencies Must Be Complete

**Problem:** Missing dependencies cause stale closures.

**Wrong:**
```typescript
useEffect(() => {
  api.fetchUser(userId); // userId in closure but not in deps
}, []); // Bug: uses stale userId
```

**Correct:**
```typescript
useEffect(() => {
  api.fetchUser(userId);
}, [userId]); // userId in deps
```

### 3. Multiple State Updates

**Problem:** Multiple `setState` calls batch in class but not always in hooks.

**Class (batches automatically):**
```typescript
this.setState({ loading: false, data: result });
```

**Hooks (may not batch in async callbacks):**
```typescript
// Option 1: Call separately (React 18+ batches these)
setLoading(false);
setData(result);

// Option 2: Use useReducer for complex state
const [state, dispatch] = useReducer(reducer, initialState);
dispatch({ type: 'FETCH_SUCCESS', payload: result });
```

### 4. Preserving Reference Identity

**Problem:** Object/array recreated every render breaks child memoization.

**Wrong:**
```typescript
function Parent() {
  const config = { theme: 'dark' }; // New object every render!
  return <MemoizedChild config={config} />;
}
```

**Correct:**
```typescript
function Parent() {
  const config = useMemo(() => ({ theme: 'dark' }), []);
  return <MemoizedChild config={config} />;
}
```

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Forgetting dependency array | Infinite loop | Add `[]` or `[deps]` |
| Missing dependencies | Stale data | Add all used values to deps |
| Not handling unmount | Memory leak | Return cleanup function |
| Calling hooks conditionally | React error | Always call hooks at top level |
| Object deps without useMemo | Infinite loop | Use `useMemo` or primitive deps |

---

## Verification Checklist

After each migration, verify:

### Functional Correctness
- [ ] Component renders without errors
- [ ] All user interactions work
- [ ] Data fetching works correctly
- [ ] Loading states appear correctly
- [ ] Error states handled properly

### Hook Rules
- [ ] Hooks called at top level (not in conditions/loops)
- [ ] Hooks called in same order every render
- [ ] All useEffect dependencies included
- [ ] Cleanup functions provided where needed

### Performance
- [ ] No unnecessary re-renders
- [ ] useCallback for functions passed as props
- [ ] useMemo for expensive computations
- [ ] useRef for mutable values that don't trigger re-render

### Type Safety (TypeScript)
- [ ] Props interface unchanged
- [ ] State types preserved
- [ ] No `any` types introduced
- [ ] Ref types correct

---

## When NOT to Migrate

Some class components are better left as-is:

1. **Error Boundaries** - Still require class components
2. **getSnapshotBeforeUpdate** - No hooks equivalent
3. **Complex optimization** - shouldComponentUpdate with complex logic
4. **Working, stable code** - If it ain't broke...

---

## Metrics to Track

| Metric | Target | Measurement |
|--------|--------|-------------|
| Migration accuracy | > 95% | Tests pass first try |
| Time saved | > 50% | vs. manual estimate |
| Bugs introduced | < 2% | Issues in 2 weeks post-migration |
| Learning retention | 100% | Engineer can explain changes |
