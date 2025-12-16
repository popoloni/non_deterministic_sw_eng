# Data Protection Review Checklist

> 📖 **Book Reference:** Chapter 7, Pattern 9 - Security-First Development  
> **Status:** Production-Ready Checklist

---

## Overview

This checklist focuses on data protection vulnerabilities commonly introduced by AI-generated code. AI assistants often log sensitive data, use weak cryptography, and mishandle secrets because training data contains these anti-patterns.

---

## When to Use This Checklist

Use when reviewing code that:
- Handles passwords or credentials
- Stores or transmits sensitive data
- Implements encryption or hashing
- Logs user activity
- Manages API keys or secrets
- Processes PII (Personally Identifiable Information)
- Handles financial data

---

## Pre-Review: AI-Specific Red Flags

Scan for these immediate red flags:

| Red Flag | Pattern | Risk |
|----------|---------|------|
| MD5/SHA1 for passwords | `crypto.createHash('md5')` | Weak hashing |
| Hardcoded secrets | `const API_KEY = "sk-..."` | Secret exposure |
| Full object logging | `console.log(user)` | PII leakage |
| Error stack in response | `res.send(err.stack)` | Information disclosure |
| Symmetric encryption for passwords | `encrypt(password)` | Should be hashed |

---

## The Checklist

### 1. Password & Credential Storage

#### 1.1 Password Hashing
- [ ] Passwords are hashed, NOT encrypted
- [ ] Using approved algorithm (bcrypt, argon2, scrypt)
- [ ] Cost factor/iterations appropriate (bcrypt ≥10)
- [ ] Salt is automatic (built into algorithm)
- [ ] NOT using MD5, SHA1, SHA256 alone

**AI Common Mistake:**
```typescript
// WRONG: AI often uses simple hash or encryption
const hashedPassword = crypto
  .createHash('sha256')
  .update(password)
  .digest('hex'); // INSECURE: No salt, too fast

// ALSO WRONG: Encryption is reversible
const encryptedPassword = encrypt(password); // Can be decrypted!

// CORRECT: Use bcrypt or argon2
import bcrypt from 'bcrypt';
const hashedPassword = await bcrypt.hash(password, 12);

// Verification
const isValid = await bcrypt.compare(inputPassword, hashedPassword);
```

#### 1.2 Credential Comparison
- [ ] Constant-time comparison used
- [ ] No short-circuit evaluation for secrets
- [ ] Timing attacks mitigated

```typescript
// WRONG: Timing attack vulnerability
if (providedToken === storedToken) { // Short-circuits!
  return true;
}

// CORRECT: Constant-time comparison
import crypto from 'crypto';
const isValid = crypto.timingSafeEqual(
  Buffer.from(providedToken),
  Buffer.from(storedToken)
);
```

---

### 2. Secrets Management

#### 2.1 Secret Storage
- [ ] Secrets in environment variables, not code
- [ ] No secrets in version control
- [ ] Production secrets in secure vault
- [ ] Secrets rotatable without deployment
- [ ] Secret access logged/audited

**AI Common Mistake:**
```typescript
// WRONG: Hardcoded secrets (very common AI mistake)
const API_KEY = 'sk-1234567890abcdef'; // In code!
const DB_PASSWORD = 'production-password'; // Never do this!

// CORRECT: Environment variables
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;

// Better: Secret manager
const API_KEY = await secretManager.getSecret('api-key');
```

#### 2.2 Secret Handling
- [ ] Secrets not logged
- [ ] Secrets not in error messages
- [ ] Secrets not in URLs (query params)
- [ ] Secrets masked in debug output
- [ ] Memory cleared after use (where possible)

---

### 3. Data Encryption

#### 3.1 Encryption at Rest
- [ ] Sensitive data encrypted in database
- [ ] Using approved algorithms (AES-256-GCM)
- [ ] Keys managed separately from data
- [ ] Key rotation possible
- [ ] NOT using ECB mode

**AI Common Mistake:**
```typescript
// WRONG: ECB mode (patterns visible)
const cipher = crypto.createCipheriv('aes-256-ecb', key, null);

// WRONG: No authentication
const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);

// CORRECT: Authenticated encryption
const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
// ... encrypt ...
const authTag = cipher.getAuthTag(); // Store with ciphertext
```

#### 3.2 Encryption in Transit
- [ ] TLS required for all external communication
- [ ] Certificate validation enabled
- [ ] Minimum TLS 1.2 (preferably 1.3)
- [ ] Strong cipher suites only
- [ ] HSTS enabled

---

### 4. Logging & Monitoring

#### 4.1 Sensitive Data in Logs
- [ ] Passwords never logged
- [ ] Full credit card numbers never logged
- [ ] SSN/Tax IDs never logged
- [ ] API keys/tokens never logged in full
- [ ] Session IDs masked or not logged

**AI Common Mistake:**
```typescript
// WRONG: Logging full user object (contains PII)
console.log('User logged in:', user);
// Output: { id: 1, email: 'john@example.com', password: 'hashed', ssn: '123-45-6789' }

// WRONG: Logging full request
console.log('Request:', req.body);
// Could contain passwords, tokens, etc.

// CORRECT: Log only safe fields
console.log('User logged in:', { userId: user.id, email: user.email });

// CORRECT: Sanitize before logging
const sanitizedBody = omit(req.body, ['password', 'token', 'ssn']);
console.log('Request:', sanitizedBody);
```

#### 4.2 Error Information Leakage
- [ ] Stack traces not shown in production
- [ ] Internal error details not exposed
- [ ] Database errors sanitized
- [ ] Generic error messages for users

```typescript
// WRONG: AI often passes through errors
app.use((err, req, res, next) => {
  res.status(500).json({ 
    error: err.message,
    stack: err.stack // NEVER in production!
  });
});

// CORRECT: Generic errors in production
app.use((err, req, res, next) => {
  // Log full error internally
  logger.error('Unhandled error', { 
    error: err.message, 
    stack: err.stack,
    requestId: req.id 
  });
  
  // Generic message to user
  res.status(500).json({ 
    error: 'An unexpected error occurred',
    requestId: req.id // For support reference
  });
});
```

---

### 5. PII Handling

#### 5.1 Data Minimization
- [ ] Only necessary PII collected
- [ ] PII not duplicated across systems
- [ ] Retention period defined
- [ ] Deletion mechanism implemented
- [ ] PII inventory maintained

#### 5.2 Access Control
- [ ] PII access logged
- [ ] PII access restricted by role
- [ ] PII masked in non-production environments
- [ ] Export/download of PII controlled

#### 5.3 Compliance
- [ ] Consent recorded where required
- [ ] Data subject requests handleable (GDPR)
- [ ] Breach notification process defined
- [ ] Privacy policy accurate

---

### 6. API Key Management

#### 6.1 Key Properties
- [ ] Keys are rotatable
- [ ] Keys can be revoked
- [ ] Keys have scoped permissions
- [ ] Keys have expiration where appropriate
- [ ] Key usage is logged

#### 6.2 Key Security
- [ ] Keys transmitted only over HTTPS
- [ ] Keys in Authorization header, not URL
- [ ] Keys not in browser-accessible code
- [ ] Keys stored encrypted in database

---

### 7. Database Security

#### 7.1 Connection Security
- [ ] Database credentials in secure config
- [ ] SSL/TLS for database connections
- [ ] Connection pooling with limits
- [ ] Principle of least privilege for DB user

#### 7.2 Query Security
- [ ] Parameterized queries only
- [ ] No dynamic SQL with user input
- [ ] Row-level security where appropriate
- [ ] Audit trail for sensitive operations

---

## Security Tests to Require

```typescript
describe('Data Protection', () => {
  test('passwords are hashed correctly', async () => {
    const user = await createUser({ password: 'test123' });
    
    // Password should be hashed, not plaintext
    expect(user.password).not.toBe('test123');
    
    // Should use bcrypt format ($2b$...)
    expect(user.password).toMatch(/^\$2[ab]\$\d{2}\$/);
  });
  
  test('sensitive data not in error responses', async () => {
    const response = await request(app)
      .get('/api/protected')
      .set('Authorization', 'Bearer invalid-token');
    
    expect(response.body.stack).toBeUndefined();
    expect(response.body.error).not.toContain('secret');
    expect(response.body.error).not.toContain('key');
  });
  
  test('PII not logged', async () => {
    const logSpy = jest.spyOn(logger, 'info');
    
    await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'secret123' });
    
    // Check no log call contains password
    for (const call of logSpy.mock.calls) {
      expect(JSON.stringify(call)).not.toContain('secret123');
    }
  });
  
  test('API keys not in URLs', async () => {
    // All API endpoints should use header auth
    const response = await request(app)
      .get('/api/data?api_key=test-key');
    
    expect(response.status).toBe(401); // Should reject query param auth
  });
});
```

---

## Review Sign-Off

| Check | Reviewer | Date |
|-------|----------|------|
| Password hashing correct | | |
| Secrets not hardcoded | | |
| Encryption appropriate | | |
| Logging sanitized | | |
| PII handling compliant | | |

**Reviewer Notes:**
```
[Document any concerns, exceptions, or follow-up items]
```

---

## Quick Reference: AI Data Protection Mistakes

| Mistake | Grep Pattern | Fix |
|---------|-------------|-----|
| Weak password hashing | `createHash\('md5\|sha1\|sha256'\)` | Use bcrypt/argon2 |
| Hardcoded secrets | `= ['"]sk-\|api.key\|password` | Environment variables |
| Logging user objects | `console\.log.*user\)` | Log only safe fields |
| Error stacks exposed | `err\.stack` in response | Generic error messages |
| ECB mode | `aes.*ecb` | Use GCM mode |
| Encrypting passwords | `encrypt.*password` | Hash, don't encrypt |

---

## Data Classification Quick Reference

| Classification | Examples | Requirements |
|----------------|----------|--------------|
| **Public** | Marketing content | None |
| **Internal** | Employee names | Access control |
| **Confidential** | Customer PII | Encryption, access logging |
| **Restricted** | Passwords, keys | Hashing, secrets vault |
| **Regulated** | Credit cards, health | Compliance controls |
