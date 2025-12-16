---
tool: generic
tool_version: "1.0"
last_verified: 2025-12-16
book_chapter: 10
book_section: "Static Context Engineering"
---

# Project Instructions

## Overview
E-commerce API built with Node.js 20, Express 4, PostgreSQL 14.
Monorepo with packages: api/, web/, shared/.

## Commands
- `npm run dev` - Start development servers
- `npm run test` - Run all tests  
- `npm run lint` - Run ESLint
- `npm run typecheck` - Run TypeScript compiler

## Code Standards
- TypeScript strict mode, no `any` types
- Functional components only (React)
- All functions need explicit return types
- Use zod for request validation

## Testing
- Minimum 80% coverage
- Use Jest with table-driven tests
- Integration tests for all API endpoints

## Patterns
- API calls: Use `src/services/apiService.ts` (never raw fetch)
- Error handling: Use `ApplicationError` class
- Auth: OAuth2 with JWT, see `src/auth/` for examples

## Architecture  
- Dependency flow: UI -> Service -> Data (never reverse)
- All user input validated at API boundary
- Parameterized queries only (no string concatenation)

## When Stuck
Reference implementations:
- Good component: `src/components/UserProfile/`
- Service pattern: `src/services/authService.ts`
- Custom hook: `src/hooks/useAsync.ts`
