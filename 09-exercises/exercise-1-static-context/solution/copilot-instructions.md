# Project Instructions

## Overview
Customer portal built with React 18 (frontend) and 
Node.js 20/Express (backend). PostgreSQL database.

## Commands
- `npm run dev` - Start both servers
- `npm test` - Run Jest tests
- `npm run lint` - ESLint check
- `npm run typecheck` - TypeScript compiler

## Code Standards
- TypeScript strict mode required
- Functional components only (no class components)
- Use React Query for server state
- Use Zod for validation

## Testing Requirements
- New features require tests before merge
- Use @testing-library/react for component tests
- Integration tests for API endpoints

## Reference Patterns
- Component example: src/components/UserCard/
- API service: src/services/apiClient.ts
- Custom hook: src/hooks/useAuth.ts
