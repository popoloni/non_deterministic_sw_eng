<!-- 
  Book Reference: Chapter 10, Section 3 - Static Context Engineering
  Tool: GitHub Copilot
  Last Verified: 2025-12-16
-->

# GitHub Copilot Instructions

This file provides project-wide instructions for GitHub Copilot.

## Project Overview

E-commerce platform built with:
- **Frontend:** React 18, TypeScript, TailwindCSS
- **Backend:** Node.js 20, Express 4, TypeScript
- **Database:** PostgreSQL 16 with Prisma ORM
- **Auth:** OAuth2 with JWT tokens

## Code Standards

### TypeScript
- Use strict mode, avoid `any` types
- All functions require explicit return types
- Use interfaces for object shapes
- Prefer `const` over `let`

### React
- Functional components only (no class components)
- Use custom hooks for shared logic
- Props interfaces named `{ComponentName}Props`
- Use React Query for server state management

### API Design
- RESTful endpoints following naming conventions
- Use zod schemas for request validation
- Standardized error responses
- All endpoints require authentication unless explicitly public

## Testing Requirements
- Minimum 80% coverage for new code
- Table-driven tests for utilities
- Integration tests for API endpoints
- Use React Testing Library for components

## Security Requirements
- Validate all user input at API boundary
- Use parameterized queries only
- Never hardcode secrets
- Sanitize output for XSS prevention

## Key Patterns

### API Calls
```typescript
// Use the API service, never raw fetch
import { api } from '@/services/api';
const users = await api.users.list();
```

### Error Handling
```typescript
import { ApplicationError, ErrorCode } from '@/errors';
throw new ApplicationError(ErrorCode.NOT_FOUND, 'User not found');
```

## Reference Files
- Component example: `src/components/UserProfile/`
- Service pattern: `src/services/authService.ts`
- Test example: `src/utils/__tests__/`
