# Migration Prompt Template

> 📖 **Book Reference:** Chapter 7, Pattern 12 - Migration as Learning  
> **Status:** Production-Ready Prompt

---

## Usage Instructions

1. First, manually migrate ONE component yourself (see MIGRATION_PATTERN.md)
2. Use this prompt template for subsequent migrations
3. Review AI output against the checklist
4. Refine prompt based on any issues found

---

## The Prompt

```
Migrate the following React class component to a functional component with hooks.

## BEFORE example (what I did manually):

```tsx
class UserProfile extends React.Component<Props, State> {
  state = { loading: true, user: null };
  
  componentDidMount() {
    this.fetchUser();
  }
  
  async fetchUser() {
    const user = await api.getUser(this.props.userId);
    this.setState({ loading: false, user });
  }
  
  render() {
    if (this.state.loading) return <Spinner />;
    return <div>{this.state.user.name}</div>;
  }
}
```

## AFTER example (the pattern to follow):

```tsx
function UserProfile({ userId }: Props) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    let cancelled = false;
    
    async function fetchUser() {
      const result = await api.getUser(userId);
      if (!cancelled) {
        setLoading(false);
        setUser(result);
      }
    }
    
    fetchUser();
    
    return () => {
      cancelled = true;
    };
  }, [userId]);
  
  if (loading) return <Spinner />;
  return <div>{user?.name}</div>;
}
```

## File to migrate:

[PASTE YOUR CLASS COMPONENT HERE]

## Rules (from my learning):

1. Convert state object to separate useState hooks
2. Convert componentDidMount to useEffect with [] deps
3. Convert componentDidUpdate to useEffect with specific deps
4. Convert componentWillUnmount to useEffect cleanup function
5. Convert methods to functions or useCallback (if passed as props)
6. Destructure props in function signature
7. Preserve all logic exactly
8. Keep prop types identical
9. Maintain the same behavior
10. Add cleanup for async operations (cancelled flag)
11. Include ALL dependencies in useEffect deps array
12. Use useRef for mutable values that don't trigger re-render
13. Use useMemo for expensive computations

## Do NOT:

- Change the component's public API (props)
- Add new features or "improvements"
- Remove existing functionality
- Change error handling behavior
- Modify the JSX structure unnecessarily

## Output format:

Provide:
1. The migrated component
2. Brief explanation of key changes
3. Any edge cases or concerns noted
```

---

## Pro Tip from Laura Tacho

After doing your first manual migration, ask AI:

```
Give me a prompt that will reproduce this result for subsequent files 
that match the structure and format of file A.
```

This gives you a **prompt optimized for YOUR specific migration** AND ensures you understand the transformation.

---

## Verification Checklist

After each AI migration, verify:

### Compile & Test
- [ ] TypeScript compiles without errors
- [ ] All existing tests pass
- [ ] Manual smoke test passes

### Pattern Correctness
- [ ] useState used for each state variable
- [ ] useEffect dependencies are complete
- [ ] Cleanup functions present where needed
- [ ] useCallback used for props callbacks

### Behavior Preservation
- [ ] Same props interface
- [ ] Same rendering output
- [ ] Same event handling
- [ ] Same side effects timing

### Edge Cases
- [ ] Async operations handle unmount
- [ ] No stale closure issues
- [ ] No infinite loops

---

## Iteration

If the AI makes mistakes:

1. Note what went wrong
2. Add specific guidance to the prompt
3. Add another example if needed
4. Test again

Example refinement:

```
ADDITIONAL RULE (added after review):
- When converting this.setState with callback, use the functional 
  form of setState: setCount(prev => prev + 1)
```

---

## Batch Processing

For large migrations, process in batches:

```
For each batch of 10 files:
1. Run AI migration
2. Quick human review (~2 min per file)
3. Run tests
4. Manually review 2-3 files in detail
5. Commit batch
```

The detailed review of samples keeps you learning:
- Are there patterns you didn't anticipate?
- Is AI handling edge cases well?
- Are there improvements to make?
