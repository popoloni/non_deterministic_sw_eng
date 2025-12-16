---
tool: generic
tool_version: "1.0"
last_verified: 2025-12-16
book_chapter: 10
book_section: "Static Context Engineering"
---

# Monorepo Project Instructions

## Overview
Enterprise monorepo containing multiple services and shared packages.
- **Architecture:** Microservices with shared libraries
- **Build System:** Turborepo with pnpm workspaces
- **Languages:** TypeScript (services), Python (ML pipelines)
- **Infrastructure:** Kubernetes on AWS EKS

## Repository Structure
```
/
├── apps/
│   ├── web-app/              # Customer-facing React app
│   ├── admin-portal/         # Internal admin dashboard
│   ├── mobile-api/           # React Native backend
│   └── marketing-site/       # Next.js marketing pages
├── services/
│   ├── user-service/         # User management (Node.js)
│   ├── order-service/        # Order processing (Node.js)
│   ├── notification-service/ # Email/SMS/Push (Node.js)
│   ├── analytics-service/    # Event processing (Python)
│   └── ml-pipeline/          # ML model training (Python)
├── packages/
│   ├── shared-types/         # TypeScript type definitions
│   ├── ui-components/        # React component library
│   ├── api-client/           # Generated API clients
│   ├── logger/               # Structured logging
│   ├── config/               # Shared ESLint/TSConfig
│   └── testing/              # Test utilities
├── infrastructure/
│   ├── terraform/            # AWS infrastructure
│   ├── kubernetes/           # K8s manifests
│   └── docker/               # Dockerfiles
└── docs/
    ├── architecture/         # System design docs
    ├── adr/                  # Architecture Decision Records
    └── runbooks/             # Operational runbooks
```

## Commands

### Development
- `pnpm dev` - Start all services locally
- `pnpm dev --filter=web-app` - Start specific app
- `pnpm dev --filter=user-service` - Start specific service

### Building
- `pnpm build` - Build all packages
- `pnpm build --filter=...^user-service` - Build service with deps
- `turbo run build --dry-run` - Preview build plan

### Testing
- `pnpm test` - Run all tests
- `pnpm test --filter=user-service` - Test specific service
- `pnpm test:e2e` - End-to-end tests
- `pnpm test:coverage` - Coverage report

### Code Quality
- `pnpm lint` - Lint all packages
- `pnpm typecheck` - Type check all TypeScript
- `pnpm format` - Format with Prettier

### Infrastructure
- `pnpm infra:plan` - Terraform plan
- `pnpm infra:apply` - Terraform apply
- `pnpm k8s:deploy:staging` - Deploy to staging

## Service-Specific Guidelines

### Node.js Services (user-service, order-service, notification-service)
- Express with TypeScript
- Prisma for database access
- Zod for validation
- Jest for testing
- OpenTelemetry for tracing

### Python Services (analytics-service, ml-pipeline)
- FastAPI with Pydantic
- SQLAlchemy for database
- pytest for testing
- Poetry for dependencies

### Frontend Apps (web-app, admin-portal)
- React 18 with TypeScript
- TailwindCSS for styling
- React Query for data fetching
- Vitest for testing

## Inter-Service Communication

### Synchronous (REST/gRPC)
```typescript
// Use the generated API client
import { UserServiceClient } from '@packages/api-client';
const client = new UserServiceClient();
const user = await client.getUser(userId);
```

### Asynchronous (Events)
```typescript
// Publish events via the event bus
import { eventBus } from '@packages/events';
await eventBus.publish('user.created', { userId, email });
```

### Event Schema Registry
All events are defined in `packages/shared-types/events/`.
Use the schema validator before publishing.

## Code Standards

### TypeScript Services
- Strict mode, no `any`
- Explicit return types on all functions
- Use dependency injection pattern
- Structured logging with correlation IDs

### Python Services
- Type hints required
- Black for formatting
- Pydantic for data validation
- Async handlers where possible

### All Services
- 80% test coverage minimum
- OpenAPI spec for all endpoints
- Health check endpoint at `/health`
- Metrics endpoint at `/metrics`

## Database Conventions

### Schema Ownership
- `user-service` owns: users, profiles, sessions
- `order-service` owns: orders, order_items, payments
- `notification-service` owns: notifications, templates

### Cross-Service Data
Never query another service's database directly.
Use the API client or subscribe to events.

## Deployment

### Environments
- `development` - Local development
- `staging` - Pre-production testing
- `production` - Live environment

### CI/CD Pipeline
1. PR triggers: lint, typecheck, test
2. Merge to main: build, push images
3. Deploy to staging: automatic
4. Deploy to production: manual approval

## Reference Implementations

When implementing new features, reference these:
- **New Service:** `services/user-service/` (canonical structure)
- **New Package:** `packages/logger/` (minimal package setup)
- **API Endpoint:** `services/user-service/src/routes/users.ts`
- **Event Handler:** `services/notification-service/src/handlers/`
- **Integration Test:** `services/order-service/tests/integration/`
- **Terraform Module:** `infrastructure/terraform/modules/service/`
- **K8s Manifest:** `infrastructure/kubernetes/services/user-service/`

## Architecture Decision Records
- **ADR-001:** Monorepo with Turborepo (accepted)
- **ADR-002:** Event-driven communication (accepted)
- **ADR-003:** Prisma vs TypeORM (Prisma selected)
- **ADR-004:** Authentication strategy (Auth0 selected)
- **ADR-005:** Observability stack (OpenTelemetry + Grafana)

## Getting Help
- **Architecture questions:** See `docs/architecture/`
- **Operational issues:** See `docs/runbooks/`
- **On-call escalation:** See `docs/runbooks/on-call.md`
