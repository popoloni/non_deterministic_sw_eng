# JWT Authentication Middleware Specification

> 📖 **Book Reference:** Chapter 7, Pattern 1 - Spec-First Generation  
> **Status:** Production-Ready Example

---

## Purpose

Verify JWT tokens and attach user context to incoming requests. This middleware sits in the Express middleware chain and gates access to protected endpoints.

---

## Requirements

1. Extract JWT from the `Authorization` header (Bearer token format)
2. Verify token signature using the configured public key
3. Check token expiration timestamp
4. Attach decoded user object to `request.user`
5. Call `next()` on successful authentication
6. Return `401 Unauthorized` if token is invalid or missing
7. Return `403 Forbidden` if token is expired

---

## Interface

### Function Signature

```typescript
function authMiddleware(
  options?: AuthMiddlewareOptions
): RequestHandler
```

### Options

```typescript
interface AuthMiddlewareOptions {
  /** Public key for JWT verification (default: from env) */
  publicKey?: string;
  
  /** Paths to exclude from authentication */
  excludePaths?: string[];
  
  /** Custom error handler */
  onError?: (error: AuthError, req: Request, res: Response) => void;
  
  /** Enable rate limiting for failed attempts */
  rateLimitEnabled?: boolean;
  
  /** Max failed attempts before blocking (default: 5) */
  maxFailedAttempts?: number;
}
```

### User Object

```typescript
interface AuthenticatedUser {
  id: string;
  email: string;
  roles: string[];
  permissions: string[];
  iat: number;  // issued at
  exp: number;  // expiration
}
```

### Request Extension

```typescript
declare global {
  namespace Express {
    interface Request {
      user?: AuthenticatedUser;
    }
  }
}
```

---

## Edge Cases

| Scenario | Response | Error Code |
|----------|----------|------------|
| Missing `Authorization` header | 401 | `AUTH_HEADER_MISSING` |
| Header present but no token | 401 | `TOKEN_MISSING` |
| Malformed token (not valid JWT) | 401 | `TOKEN_MALFORMED` |
| Signature verification fails | 401 | `INVALID_SIGNATURE` |
| Token expired | 403 | `TOKEN_EXPIRED` |
| Token not yet valid (future `iat`) | 401 | `TOKEN_NOT_ACTIVE` |
| Valid token but user deleted | 403 | `USER_NOT_FOUND` |
| Valid token but user disabled | 403 | `USER_DISABLED` |

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Authentication token has expired",
    "details": {
      "expiredAt": "2024-01-15T10:30:00Z"
    }
  }
}
```

### Error Logging

- Log all authentication failures with request metadata
- Include correlation ID for tracing
- **Never** log token contents or secrets
- Rate limit failed attempts to prevent brute force

---

## Security Considerations

### Must Implement

- [x] Use constant-time comparison for signature verification
- [x] Validate token algorithm matches expected (prevent algorithm switching attacks)
- [x] Check `aud` (audience) claim if configured
- [x] Check `iss` (issuer) claim if configured
- [x] Rate limit failed authentication attempts
- [x] Sanitize error messages (don't leak implementation details)

### Must Avoid

- [ ] Logging token contents
- [ ] Including stack traces in production error responses
- [ ] Using symmetric algorithms (HS256) for public APIs
- [ ] Accepting tokens from query parameters

---

## Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response time (P95) | < 50ms | Middleware execution only |
| Response time (P99) | < 100ms | Including key retrieval |
| Memory overhead | < 5MB | Per instance |
| Cache hit rate | > 95% | Public key cache |

### Optimization Notes

- Cache public key retrieval (default: 1 hour TTL)
- Use connection pooling for user existence checks
- Consider async validation for non-blocking behavior

---

## Integration Points

### Dependencies

```typescript
// Required peer dependencies
import { Request, Response, NextFunction, RequestHandler } from 'express';
import jwt from 'jsonwebtoken';
import { RateLimiter } from './rate-limiter';
import { UserService } from '../services/user-service';
import { logger } from '../utils/logger';
import { metrics } from '../utils/metrics';
```

### Middleware Chain Position

```typescript
app.use('/api', [
  corsMiddleware,
  rateLimitMiddleware,
  authMiddleware(),      // <-- This middleware
  requestLoggingMiddleware,
  // ... route handlers
]);
```

### Configuration

```typescript
// Environment variables
JWT_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----...
JWT_ISSUER=https://auth.example.com
JWT_AUDIENCE=api.example.com
AUTH_RATE_LIMIT_WINDOW=900000  // 15 minutes
AUTH_RATE_LIMIT_MAX=5
```

---

## Examples

### Example 1: Valid Request

**Request:**
```http
GET /api/users/me HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Result:**
- `request.user` populated with decoded claims
- `next()` called
- Request continues to route handler

### Example 2: Expired Token

**Request:**
```http
GET /api/users/me HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...  (expired)
```

**Response:**
```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Authentication token has expired"
  }
}
```

### Example 3: Invalid Token

**Request:**
```http
GET /api/users/me HTTP/1.1
Authorization: Bearer not-a-valid-jwt
```

**Response:**
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": {
    "code": "TOKEN_MALFORMED",
    "message": "Invalid authentication token"
  }
}
```

---

## Verification Checklist

Use this checklist to verify implementation:

### Functional Requirements
- [ ] Extracts token from Bearer header
- [ ] Validates signature with public key
- [ ] Checks expiration
- [ ] Attaches user to request
- [ ] Returns correct status codes

### Edge Cases
- [ ] Handles missing header
- [ ] Handles empty token
- [ ] Handles malformed JWT
- [ ] Handles signature mismatch
- [ ] Handles expired token
- [ ] Handles deleted user
- [ ] Handles disabled user

### Security
- [ ] Uses constant-time comparison
- [ ] Validates algorithm
- [ ] Rate limits failures
- [ ] Never logs tokens
- [ ] Sanitizes error messages

### Performance
- [ ] Caches public key
- [ ] Meets P95 latency target
- [ ] Integrates with metrics

---

## Usage with AI

### Prompt Template

```
Implement the JWT authentication middleware exactly as specified in this document.

Key requirements:
1. TypeScript with strict types
2. Express middleware pattern
3. All edge cases from the specification
4. Security measures as listed
5. Integration with our existing UserService

Our existing patterns:
[Paste example middleware from your codebase]

Do not add features not in the spec.
Ask clarifying questions if anything is ambiguous.
```

### Iteration Prompt (if gaps exist)

```
The implementation doesn't handle [specific edge case from spec].
According to the specification, this should [expected behavior].
Please update the implementation.
```
