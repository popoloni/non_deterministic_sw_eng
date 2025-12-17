# Customer Portal

React 18 frontend + Node.js 20/Express backend. PostgreSQL.

## Commands
- npm run dev: Start servers
- npm test: Jest tests  
- npm run lint: ESLint
- npm run typecheck: TypeScript

## Standards
- TypeScript strict, functional components only
- React Query for server state, Zod for validation
- Tests required before merge

## Patterns
See: src/components/UserCard/ (component pattern)
See: src/services/apiClient.ts (API calls)
See: src/hooks/useAuth.ts (custom hooks)
