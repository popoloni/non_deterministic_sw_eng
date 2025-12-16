# Authentication & Authorization Review Checklist

> 📖 **Book Reference:** Chapter 7, Pattern 9 - Security-First Development  
> **Status:** Production-Ready Checklist

---

## Overview

This checklist is specifically designed to catch AI-generated security vulnerabilities in authentication and authorization code. AI often generates code that works functionally but has critical security holes from insecure patterns in training data.

---

## When to Use This Checklist

Use when reviewing code that involves:
- User login/logout
- Session management
- API authentication
- Permission checks
- Role-based access control
- Admin functions
- Multi-tenant data access

---

## Pre-Review: AI-Specific Red Flags

Before detailed review, scan for these common AI mistakes:

| Red Flag | What to Look For |
|----------|------------------|
| User ID from request body | `const userId = req.body.userId` (spoofable!) |
| Only checking authentication | Auth check without permission check |
| Hardcoded test credentials | `password === 'admin123'` |
| Console.log with secrets | `console.log('Token:', token)` |
| Symmetric JWT secret | Using same key for sign and verify |

---

## The Checklist

### 1. Authentication Implementation

#### 1.1 Credential Handling
- [ ] Passwords are hashed, not encrypted or plaintext
- [ ] Using strong hashing algorithm (bcrypt, argon2, scrypt)
- [ ] Salt is unique per password (not global)
- [ ] Credentials never logged
- [ ] Credentials never exposed in error messages

#### 1.2 Session Management
- [ ] Session tokens are cryptographically random
- [ ] Sessions expire after reasonable time
- [ ] Sessions invalidated on logout
- [ ] Session tokens regenerated after privilege change
- [ ] Session fixation attack prevented

#### 1.3 Token Handling (JWT/OAuth)
- [ ] Tokens stored securely (httpOnly cookies or secure storage)
- [ ] Tokens have expiration
- [ ] Token signature verified on every request
- [ ] Algorithm explicitly specified (no algorithm: 'none')
- [ ] Refresh token rotation implemented
- [ ] Token blacklisting for logout/revocation

**AI Common Mistake:**
```typescript
// WRONG: AI often generates this - no algorithm validation
const decoded = jwt.decode(token); // decode != verify!

// CORRECT: Always verify with algorithm specified
const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
```

---

### 2. Authorization Implementation

#### 2.1 Permission Checks
- [ ] Authorization checked on every protected endpoint
- [ ] Authorization checked server-side (not just UI)
- [ ] User can only access their own resources
- [ ] Role/permission checked, not just authentication
- [ ] Privilege escalation not possible

**AI Common Mistake:**
```typescript
// WRONG: AI often checks only if user exists
app.get('/api/users/:id/data', authenticate, async (req, res) => {
  const data = await db.getUserData(req.params.id); // No authorization!
  res.json(data);
});

// CORRECT: Check user can access this resource
app.get('/api/users/:id/data', authenticate, async (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const data = await db.getUserData(req.params.id);
  res.json(data);
});
```

#### 2.2 Resource Access Control
- [ ] User ID comes from authenticated session, not request
- [ ] Database queries scoped to user's resources
- [ ] Tenant isolation enforced (multi-tenant apps)
- [ ] Horizontal privilege escalation prevented
- [ ] Vertical privilege escalation prevented

**AI Common Mistake:**
```typescript
// WRONG: User ID from request body is spoofable
app.post('/api/orders', (req, res) => {
  const order = await db.createOrder({
    userId: req.body.userId, // DANGER: Client-supplied!
    items: req.body.items
  });
});

// CORRECT: User ID from authenticated session
app.post('/api/orders', authenticate, (req, res) => {
  const order = await db.createOrder({
    userId: req.user.id, // From verified session
    items: req.body.items
  });
});
```

#### 2.3 Admin Functions
- [ ] Admin endpoints have explicit admin role check
- [ ] Admin actions are logged/audited
- [ ] Admin cannot bypass data validation
- [ ] Super-admin cannot be created via API
- [ ] Bulk operations rate-limited

---

### 3. Authentication Flows

#### 3.1 Login Flow
- [ ] Rate limiting on login attempts
- [ ] Account lockout after N failures
- [ ] Timing attacks mitigated (constant-time comparison)
- [ ] Generic error messages (not "user exists")
- [ ] Brute force protection

#### 3.2 Password Reset Flow
- [ ] Reset tokens are single-use
- [ ] Reset tokens expire quickly (< 1 hour)
- [ ] Old password not required to change password (for reset)
- [ ] User notified of password change
- [ ] All sessions invalidated on password change

#### 3.3 Multi-Factor Authentication
- [ ] TOTP secrets stored encrypted
- [ ] Backup codes hashed like passwords
- [ ] MFA cannot be disabled without verification
- [ ] Rate limiting on MFA attempts
- [ ] Recovery flow is secure

---

### 4. API Security

#### 4.1 API Key Management
- [ ] API keys are rotatable
- [ ] API keys can be scoped (read/write/admin)
- [ ] API keys can be revoked
- [ ] API keys never logged in full
- [ ] API key exposure triggers rotation

#### 4.2 OAuth/OIDC Implementation
- [ ] State parameter used and verified
- [ ] Redirect URI strictly validated
- [ ] Authorization codes are single-use
- [ ] PKCE implemented for public clients
- [ ] Token endpoint authenticated

---

## Security Tests to Require

```typescript
describe('Authorization Security', () => {
  test('prevents access to other users data', async () => {
    const userA = await createUser();
    const userB = await createUser();
    const tokenA = generateToken(userA);
    
    // Try to access userB's data with userA's token
    const response = await request(app)
      .get(`/api/users/${userB.id}/data`)
      .set('Authorization', `Bearer ${tokenA}`);
    
    expect(response.status).toBe(403);
    expect(response.body).not.toContain(userB.email);
  });
  
  test('prevents privilege escalation', async () => {
    const regularUser = await createUser({ role: 'user' });
    const token = generateToken(regularUser);
    
    // Try to access admin endpoint
    const response = await request(app)
      .delete('/api/admin/users/123')
      .set('Authorization', `Bearer ${token}`);
    
    expect(response.status).toBe(403);
  });
  
  test('prevents user ID spoofing', async () => {
    const user = await createUser();
    const token = generateToken(user);
    
    // Try to create order with different user ID
    const response = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${token}`)
      .send({ userId: 'other-user-id', items: [...] });
    
    // Order should be created for authenticated user, not spoofed ID
    const order = await db.getOrder(response.body.id);
    expect(order.userId).toBe(user.id);
  });
});
```

---

## Review Sign-Off

| Check | Reviewer | Date |
|-------|----------|------|
| Authentication implementation reviewed | | |
| Authorization checks verified | | |
| Security tests adequate | | |
| No AI-specific vulnerabilities | | |

**Reviewer Notes:**
```
[Document any concerns, exceptions, or follow-up items]
```

---

## Quick Reference: AI Auth Mistakes

| Mistake | Risk | Detection |
|---------|------|-----------|
| User ID from request body | Data theft | Grep for `req.body.userId` |
| Only auth, no authz | Data exposure | Check all protected endpoints |
| Hardcoded credentials | Account compromise | Secret scanning tools |
| Logging tokens | Token theft | Grep for `console.log.*token` |
| jwt.decode vs jwt.verify | Token bypass | Search for `jwt.decode` |
| Missing rate limiting | Brute force | Check login/reset endpoints |
