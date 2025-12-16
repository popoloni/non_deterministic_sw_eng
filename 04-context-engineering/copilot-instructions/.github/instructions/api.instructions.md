---
applyTo: "src/api/**/*.ts"
---

# API Development Guidelines

When working with API endpoints in this project:

## Validation
- Use zod schemas for all request validation
- Validate at the route level, not in business logic
- Return 400 for validation errors with details

## Response Format
```typescript
// Success response
{ data: T, meta?: { page, total } }

// Error response  
{ error: { code: string, message: string, details?: unknown } }
```

## Authentication
- All routes require auth by default
- Use `@public` decorator for public routes
- Access user via `req.user` after auth middleware

## Error Handling
- Use `ApplicationError` for expected errors
- Let unexpected errors bubble to global handler
- Log errors with request context

## Reference
See `src/api/users/` for canonical implementation.
