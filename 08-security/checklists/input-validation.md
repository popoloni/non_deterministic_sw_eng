# Input Validation Review Checklist

> 📖 **Book Reference:** Chapter 7, Pattern 9 - Security-First Development  
> **Status:** Production-Ready Checklist

---

## Overview

This checklist targets AI-generated input validation vulnerabilities. AI assistants frequently generate code with SQL injection, XSS, and other injection vulnerabilities because training data contains insecure patterns.

As the book notes: AI is trained on "the lowest common denominator" of open-source code and doesn't optimize for security best practices.

---

## When to Use This Checklist

Use when reviewing code that:
- Accepts user input (forms, API endpoints)
- Constructs database queries
- Generates HTML or other output
- Handles file uploads
- Processes URLs or paths
- Parses JSON, XML, or other formats

---

## Pre-Review: AI-Specific Red Flags

Scan for these immediate red flags:

| Red Flag | Pattern | Risk |
|----------|---------|------|
| String interpolation in SQL | `` `SELECT * WHERE id=${id}` `` | SQL Injection |
| innerHTML with user data | `element.innerHTML = userInput` | XSS |
| Path concatenation | `path.join(base, userInput)` | Path Traversal |
| eval/Function with user data | `eval(userCode)` | Code Injection |
| Regex from user input | `new RegExp(userPattern)` | ReDoS |

---

## The Checklist

### 1. SQL Injection Prevention

#### 1.1 Query Construction
- [ ] All queries use parameterized statements
- [ ] No string concatenation in queries
- [ ] No template literals in queries
- [ ] ORM used correctly (not raw queries)
- [ ] Dynamic table/column names validated against allowlist

**AI Common Mistake:**
```typescript
// WRONG: AI often generates this pattern
const user = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);

// ALSO WRONG: Template literals are still injection-prone
const user = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);

// CORRECT: Parameterized query
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// CORRECT: With ORM
const user = await prisma.user.findUnique({
  where: { email }
});
```

#### 1.2 Dynamic SQL
- [ ] Dynamic column names validated against allowlist
- [ ] Dynamic table names validated against allowlist
- [ ] ORDER BY columns validated
- [ ] LIMIT/OFFSET values are integers

```typescript
// WRONG: Dynamic column from user input
const sortBy = req.query.sortBy;
const results = await db.query(
  `SELECT * FROM products ORDER BY ${sortBy}` // INJECTION!
);

// CORRECT: Allowlist validation
const ALLOWED_SORT_COLUMNS = ['name', 'price', 'created_at'];
const sortBy = ALLOWED_SORT_COLUMNS.includes(req.query.sortBy)
  ? req.query.sortBy
  : 'created_at';
```

---

### 2. Cross-Site Scripting (XSS) Prevention

#### 2.1 Output Encoding
- [ ] All user data HTML-encoded before display
- [ ] Context-appropriate encoding used (HTML, URL, JS, CSS)
- [ ] Template engine auto-escaping enabled
- [ ] innerHTML/outerHTML avoided with user data
- [ ] dangerouslySetInnerHTML justified and sanitized

**AI Common Mistake:**
```typescript
// WRONG: AI doesn't consider XSS
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${req.query.q}</h1>`); // XSS!
});

// CORRECT: HTML encode
import { escape } from 'html-escaper';
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${escape(req.query.q)}</h1>`);
});

// BETTER: Use template engine with auto-escaping
app.get('/search', (req, res) => {
  res.render('search', { query: req.query.q }); // Auto-escaped
});
```

#### 2.2 JavaScript Context
- [ ] User data not inserted into `<script>` tags
- [ ] JSON.stringify used for data in scripts
- [ ] Event handlers don't include user data
- [ ] URL javascript: protocol blocked

```typescript
// WRONG: User data in script context
const script = `<script>var name = "${userName}";</script>`; // XSS!

// CORRECT: JSON encode for script context
const script = `<script>var name = ${JSON.stringify(userName)};</script>`;
```

#### 2.3 Rich Text/HTML
- [ ] HTML sanitizer used (DOMPurify, sanitize-html)
- [ ] Allowlist of safe tags/attributes
- [ ] No dangerous attributes (onclick, onerror)
- [ ] Sanitization on server side, not just client

---

### 3. Path Traversal Prevention

#### 3.1 File Path Handling
- [ ] User input not used directly in file paths
- [ ] Path.join result validated within allowed directory
- [ ] Symlinks resolved before validation
- [ ] Double-encoding attacks prevented
- [ ] Null bytes filtered

**AI Common Mistake:**
```typescript
// WRONG: AI often generates unsafe file handling
app.get('/files/:filename', (req, res) => {
  const filepath = path.join('/uploads', req.params.filename);
  res.sendFile(filepath); // Path traversal: ../../../etc/passwd
});

// CORRECT: Validate resolved path
app.get('/files/:filename', (req, res) => {
  const uploadsDir = path.resolve('/uploads');
  const filepath = path.resolve(uploadsDir, req.params.filename);
  
  // Verify file is within allowed directory
  if (!filepath.startsWith(uploadsDir)) {
    return res.status(400).json({ error: 'Invalid path' });
  }
  
  res.sendFile(filepath);
});
```

#### 3.2 URL Handling
- [ ] URLs validated against allowlist of domains
- [ ] Open redirects prevented
- [ ] SSRF attacks considered for server-side requests
- [ ] Protocol validated (http/https only)

---

### 4. Data Type Validation

#### 4.1 Type Coercion
- [ ] Input types explicitly validated (not just coerced)
- [ ] Schema validation used (Zod, Joi, JSON Schema)
- [ ] Array/object structure validated
- [ ] Numeric bounds checked

```typescript
// WRONG: Trusting type coercion
app.post('/api/items', (req, res) => {
  const quantity = req.body.quantity; // Could be string, array, anything!
  await db.updateStock(quantity);
});

// CORRECT: Schema validation
import { z } from 'zod';

const ItemSchema = z.object({
  quantity: z.number().int().min(1).max(1000)
});

app.post('/api/items', (req, res) => {
  const result = ItemSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.issues });
  }
  await db.updateStock(result.data.quantity);
});
```

#### 4.2 String Validation
- [ ] Maximum length enforced
- [ ] Format validated (email, URL, UUID, etc.)
- [ ] Character set validated where appropriate
- [ ] Unicode normalization applied where needed

#### 4.3 Number Validation
- [ ] Integer vs float distinguished
- [ ] Range bounds enforced
- [ ] NaN and Infinity handled
- [ ] Precision limits for financial calculations

---

### 5. Server-Side Validation

#### 5.1 Trust Boundaries
- [ ] All validation performed server-side
- [ ] Client-side validation is UX only, not security
- [ ] Request body size limited
- [ ] Request rate limited

**AI Common Mistake:**
```typescript
// WRONG: AI sometimes only validates client-side
// client.js
if (email.match(/@/)) {
  fetch('/api/subscribe', { body: { email } });
}

// server.js - NO VALIDATION!
app.post('/api/subscribe', (req, res) => {
  await db.addSubscriber(req.body.email);
});

// CORRECT: Server-side validation required
app.post('/api/subscribe', (req, res) => {
  const email = req.body.email;
  if (!email || !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  await db.addSubscriber(email);
});
```

---

### 6. File Upload Validation

#### 6.1 File Type Validation
- [ ] File extension validated
- [ ] MIME type validated (from content, not header)
- [ ] Magic bytes checked
- [ ] Image files re-processed to strip metadata

#### 6.2 File Size Limits
- [ ] Maximum file size enforced
- [ ] Total upload size limited
- [ ] Number of files limited

#### 6.3 File Storage
- [ ] Uploaded files stored outside web root
- [ ] Files renamed to random names
- [ ] Original filename sanitized if stored
- [ ] Content-Disposition header set for downloads

---

## Security Tests to Require

```typescript
describe('Input Validation Security', () => {
  test('prevents SQL injection', async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    
    const response = await request(app)
      .get(`/api/search?q=${encodeURIComponent(maliciousInput)}`);
    
    // Should sanitize, not execute
    expect(response.status).not.toBe(500);
    
    // Verify users table still exists
    const userCount = await db.query('SELECT COUNT(*) FROM users');
    expect(userCount.rows[0].count).toBeGreaterThan(0);
  });
  
  test('prevents XSS in search results', async () => {
    const xssPayload = '<script>alert("xss")</script>';
    
    const response = await request(app)
      .get(`/api/search?q=${encodeURIComponent(xssPayload)}`);
    
    // Response should not contain unescaped script
    expect(response.text).not.toContain('<script>');
    expect(response.text).toContain('&lt;script&gt;');
  });
  
  test('prevents path traversal', async () => {
    const response = await request(app)
      .get('/api/files/../../../etc/passwd');
    
    expect(response.status).toBe(400);
  });
  
  test('validates input types', async () => {
    const response = await request(app)
      .post('/api/items')
      .send({ quantity: 'not-a-number' });
    
    expect(response.status).toBe(400);
    expect(response.body.errors).toBeDefined();
  });
});
```

---

## Review Sign-Off

| Check | Reviewer | Date |
|-------|----------|------|
| SQL injection prevented | | |
| XSS prevented | | |
| Path traversal prevented | | |
| Input types validated | | |
| Server-side validation present | | |

**Reviewer Notes:**
```
[Document any concerns, exceptions, or follow-up items]
```

---

## Quick Reference: AI Input Validation Mistakes

| Mistake | Grep Pattern | Fix |
|---------|-------------|-----|
| SQL string concat | `` `SELECT.*\$\{`` | Parameterized queries |
| innerHTML | `innerHTML\s*=` | Use textContent or sanitize |
| Path.join with input | `path\.join.*req\.` | Validate resolved path |
| No schema validation | Missing Zod/Joi | Add schema validation |
| Client-only validation | Check server handlers | Add server validation |
