---
tool: generic
tool_version: "1.0"
last_verified: 2025-12-16
book_chapter: 10
book_section: "Static Context Engineering"
---

# Project Instructions

## Overview
Full-stack SaaS application for project management.
- **Frontend:** React 18 with TypeScript, Vite, TailwindCSS
- **Backend:** Node.js 20, Express 4, TypeScript
- **Database:** PostgreSQL 16 with Prisma ORM
- **Auth:** OAuth2 with Auth0
- **Deployment:** Docker, Kubernetes, AWS

## Project Structure
```
/
├── apps/
│   ├── web/              # React frontend
│   ├── api/              # Express backend
│   └── admin/            # Admin dashboard
├── packages/
│   ├── shared/           # Shared types and utilities
│   ├── ui/               # Component library
│   └── config/           # Shared configs (ESLint, TSConfig)
├── prisma/               # Database schema and migrations
└── docs/                 # Architecture documentation
```

## Commands
### Development
- `npm run dev` - Start all services in development mode
- `npm run dev:web` - Start frontend only
- `npm run dev:api` - Start backend only

### Testing
- `npm run test` - Run all tests
- `npm run test:unit` - Unit tests only
- `npm run test:integration` - Integration tests only
- `npm run test:e2e` - End-to-end tests (Playwright)
- `npm run test:coverage` - Generate coverage report

### Building
- `npm run build` - Build all packages
- `npm run typecheck` - Run TypeScript compiler
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Auto-fix lint issues

### Database
- `npm run db:migrate` - Run Prisma migrations
- `npm run db:generate` - Generate Prisma client
- `npm run db:seed` - Seed development data
- `npm run db:studio` - Open Prisma Studio

## Code Standards

### TypeScript
- Strict mode enabled, no `any` types
- All functions require explicit return types
- Use interfaces for object shapes, types for unions
- Prefer `unknown` over `any` for external data

### React
- Functional components only
- Use custom hooks for shared logic
- Props interfaces named `{ComponentName}Props`
- Use React Query for server state

### API Design
- RESTful endpoints with consistent naming
- Use zod schemas for request/response validation
- Standardized error responses (see `packages/shared/errors.ts`)
- All endpoints require authentication unless explicitly public

### Testing
- Minimum 80% coverage for new code
- Table-driven tests for utilities
- Integration tests for API endpoints
- Component tests with React Testing Library

## Patterns

### API Calls (Frontend)
```typescript
// Always use the API client, never raw fetch
import { api } from '@/services/api';
const users = await api.users.list();
```

### Error Handling
```typescript
// Use ApplicationError for all thrown errors
import { ApplicationError, ErrorCode } from '@packages/shared';
throw new ApplicationError(ErrorCode.NOT_FOUND, 'User not found');
```

### Authentication
```typescript
// Use the auth hook for user context
import { useAuth } from '@/hooks/useAuth';
const { user, isLoading, logout } = useAuth();
```

### Database Queries
```typescript
// Use Prisma with typed queries
import { prisma } from '@/lib/prisma';
const user = await prisma.user.findUnique({ where: { id } });
```

## Architecture Decisions

### Why Monorepo?
Enables code sharing between apps while maintaining separate deployments.
See `docs/ADR-001-monorepo.md`.

### Why Prisma?
Type-safe database access with excellent DX. Migrations are version-controlled.
See `docs/ADR-002-orm-choice.md`.

### Why React Query?
Handles caching, background updates, and optimistic mutations consistently.
See `docs/ADR-003-data-fetching.md`.

## Security Requirements
- All user input validated at API boundary
- Parameterized queries only (no string concatenation)
- Secrets in environment variables, never hardcoded
- Rate limiting on authentication endpoints
- CORS configured for specific origins only

## Reference Implementations
When unsure about patterns, consult these files:
- **Component:** `apps/web/src/components/UserProfile/`
- **API Route:** `apps/api/src/routes/users/`
- **Service:** `apps/api/src/services/authService.ts`
- **Custom Hook:** `apps/web/src/hooks/useAsync.ts`
- **Prisma Model:** `prisma/schema.prisma` (User model)
- **Test:** `apps/api/src/routes/users/__tests__/`

## Common Mistakes to Avoid
- ❌ Using `any` type - use `unknown` and type guards
- ❌ Raw SQL queries - use Prisma's query builder
- ❌ Direct DOM manipulation - use React state
- ❌ Storing secrets in code - use environment variables
- ❌ Skipping error handling - wrap async operations in try/catch
