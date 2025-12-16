# API Endpoint Specification Template

> 📖 **Book Reference:** Chapter 7, Pattern 1 - Spec-First Generation  
> **Status:** Template - Fill in for your endpoint

---

## Metadata

| Property | Value |
|----------|-------|
| **Endpoint** | `[METHOD] /api/v1/[resource]` |
| **Version** | v1 |
| **Owner** | [Team/Person] |
| **Last Updated** | [Date] |

---

## Purpose

[One paragraph describing what this endpoint does and why it exists]

---

## Requirements

### Functional Requirements

1. [FR-001] [Requirement description]
2. [FR-002] [Requirement description]
3. [FR-003] [Requirement description]

### Non-Functional Requirements

1. [NFR-001] Response time < [X]ms (P95)
2. [NFR-002] Must support [X] requests/second
3. [NFR-003] [Other constraints]

---

## Interface

### Request

```http
[METHOD] /api/v1/[resource]
Content-Type: application/json
Authorization: Bearer {token}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string (UUID) | Yes | Resource identifier |

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number |
| `limit` | integer | No | 20 | Items per page (max 100) |
| `sort` | string | No | `createdAt` | Sort field |
| `order` | string | No | `desc` | Sort order (asc/desc) |

#### Request Body

```typescript
interface CreateResourceRequest {
  /** Resource name (3-100 characters) */
  name: string;
  
  /** Optional description */
  description?: string;
  
  /** Resource type */
  type: 'typeA' | 'typeB' | 'typeC';
  
  /** Associated tags */
  tags?: string[];
}
```

#### Validation Rules

| Field | Rule | Error Code |
|-------|------|------------|
| `name` | Required, 3-100 chars | `INVALID_NAME` |
| `name` | Must be unique | `NAME_EXISTS` |
| `type` | Must be valid enum | `INVALID_TYPE` |
| `tags` | Max 10 items | `TOO_MANY_TAGS` |

### Response

#### Success Response (200/201)

```typescript
interface ResourceResponse {
  data: {
    id: string;
    name: string;
    description: string | null;
    type: ResourceType;
    tags: string[];
    createdAt: string;  // ISO 8601
    updatedAt: string;  // ISO 8601
    createdBy: {
      id: string;
      name: string;
    };
  };
  meta?: {
    requestId: string;
  };
}
```

#### List Response (200)

```typescript
interface ResourceListResponse {
  data: ResourceResponse['data'][];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
  meta: {
    requestId: string;
  };
}
```

#### Error Response (4xx/5xx)

```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    requestId: string;
  };
}
```

---

## Edge Cases

| # | Scenario | Expected Behavior | Status Code |
|---|----------|-------------------|-------------|
| 1 | Resource not found | Return error with `NOT_FOUND` code | 404 |
| 2 | Duplicate name | Return error with `NAME_EXISTS` code | 409 |
| 3 | Invalid ID format | Return error with `INVALID_ID` code | 400 |
| 4 | Page beyond results | Return empty data array | 200 |
| 5 | Unauthorized access | Return `UNAUTHORIZED` error | 401 |
| 6 | Forbidden (no permission) | Return `FORBIDDEN` error | 403 |
| 7 | Rate limit exceeded | Return `RATE_LIMITED` error | 429 |
| 8 | Request body too large | Return `PAYLOAD_TOO_LARGE` error | 413 |

---

## Error Codes

| Code | HTTP Status | Description | User Message |
|------|-------------|-------------|--------------|
| `INVALID_REQUEST` | 400 | Request validation failed | "Invalid request parameters" |
| `UNAUTHORIZED` | 401 | Missing or invalid auth | "Authentication required" |
| `FORBIDDEN` | 403 | Insufficient permissions | "Access denied" |
| `NOT_FOUND` | 404 | Resource doesn't exist | "Resource not found" |
| `NAME_EXISTS` | 409 | Duplicate name | "A resource with this name already exists" |
| `RATE_LIMITED` | 429 | Too many requests | "Too many requests, try again later" |
| `INTERNAL_ERROR` | 500 | Server error | "An unexpected error occurred" |

---

## Security Considerations

### Authentication
- [ ] Requires valid JWT token
- [ ] Token must not be expired
- [ ] User must exist and be active

### Authorization
- [ ] User must have `[permission]` permission
- [ ] Resource must belong to user's organization
- [ ] Admin can access all resources

### Input Validation
- [ ] Sanitize all string inputs
- [ ] Validate against schema before processing
- [ ] Reject unknown fields (strict mode)

### Rate Limiting
- [ ] [X] requests per [Y] seconds per user
- [ ] Return `429` when exceeded
- [ ] Include `Retry-After` header

---

## Performance Requirements

| Metric | Target | Notes |
|--------|--------|-------|
| P50 Latency | < 50ms | Cached responses |
| P95 Latency | < 200ms | Cold queries |
| P99 Latency | < 500ms | Complex filters |
| Max Throughput | 1000 req/s | Per instance |
| Max Payload | 1MB | Request body |

### Caching Strategy

- Cache key: `resource:{id}` or `resource:list:{hash(params)}`
- TTL: 5 minutes for single resource, 1 minute for lists
- Invalidate on: create, update, delete

---

## Integration Points

### Dependencies

| Service | Purpose | Failure Handling |
|---------|---------|------------------|
| PostgreSQL | Data storage | Return 503, retry |
| Redis | Caching | Proceed without cache |
| Auth Service | Token validation | Return 401 |

### Events Emitted

| Event | When | Payload |
|-------|------|---------|
| `resource.created` | After successful create | `{ id, name, createdBy }` |
| `resource.updated` | After successful update | `{ id, changes, updatedBy }` |
| `resource.deleted` | After successful delete | `{ id, deletedBy }` |

---

## Examples

### Example 1: Create Resource

**Request:**
```http
POST /api/v1/resources
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "name": "My Resource",
  "type": "typeA",
  "tags": ["important", "reviewed"]
}
```

**Response:**
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Resource",
    "description": null,
    "type": "typeA",
    "tags": ["important", "reviewed"],
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z",
    "createdBy": {
      "id": "user-123",
      "name": "John Doe"
    }
  },
  "meta": {
    "requestId": "req-abc123"
  }
}
```

### Example 2: Validation Error

**Request:**
```http
POST /api/v1/resources
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "name": "AB",
  "type": "invalid"
}
```

**Response:**
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Validation failed",
    "details": {
      "name": "Must be at least 3 characters",
      "type": "Must be one of: typeA, typeB, typeC"
    },
    "requestId": "req-def456"
  }
}
```

---

## Verification Checklist

### Functional
- [ ] All CRUD operations work correctly
- [ ] Pagination works as specified
- [ ] Sorting works for all allowed fields
- [ ] Filtering works as specified

### Validation
- [ ] All validation rules enforced
- [ ] Appropriate error codes returned
- [ ] Error messages are helpful

### Security
- [ ] Auth required for all operations
- [ ] Authorization checks pass
- [ ] Rate limiting works
- [ ] Input sanitization active

### Performance
- [ ] Meets latency targets
- [ ] Caching works correctly
- [ ] No N+1 queries

---

## AI Prompt Template

```
Implement the API endpoint specified in this document.

Technology stack:
- Express.js with TypeScript
- PostgreSQL with Prisma ORM
- Zod for validation
- Our existing patterns: [provide example]

Requirements:
1. Implement all CRUD operations as specified
2. Handle all edge cases listed
3. Return correct error codes
4. Include request validation with Zod
5. Add integration with our event system

Do not add features not in the spec.
```
