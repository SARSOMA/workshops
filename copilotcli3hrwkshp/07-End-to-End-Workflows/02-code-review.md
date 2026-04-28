# Scenario 8.2: Code Review

## Introduction

This scenario covers using Copilot CLI to perform thorough code reviews—whether reviewing your own changes before a PR or reviewing someone else's contributions.

## Scenario Overview

You'll learn to:
1. Review local changes before committing
2. Review PR changes from teammates
3. Identify different types of issues
4. Provide constructive feedback

---

## Part 1: Self-Review Before PR

### Review Your Staged Changes

```
/diff
```

Or for more detail:

```
Review my staged changes for potential issues
```

### Deep Self-Review

```
/review
```

The code-review agent analyzes your changes for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code style problems
- Missing error handling

### Example Self-Review Session

```
You: /review

Copilot: Analyzing changes in 3 files...

## Review Summary

### Critical Issues (1)
**src/api/users.js:45** - SQL Injection Vulnerability
The query uses string concatenation with user input:
```javascript
const query = `SELECT * FROM users WHERE id = ${userId}`;
```
Fix: Use parameterized queries.

### Warnings (2)
1. **src/api/users.js:23** - Missing error handling
   The async function doesn't catch potential errors.
   
2. **src/utils/validate.js:15** - Inefficient regex
   This regex runs in O(n²) time. Consider optimizing.

### Suggestions (1)
1. **src/api/users.js:67** - Consider adding logging
   This operation would benefit from audit logging.

Shall I help fix any of these issues?
```

---

## Part 2: Reviewing a PR

### Get PR Information

```
Show me the changes in PR #123
```

Copilot retrieves:
- PR title and description
- Changed files
- Diff content
- Current status

### Perform Code Review

```
Review PR #123 for:
- Security vulnerabilities
- Performance issues
- Code correctness
- Test coverage
```

### Example PR Review

```
You: Review PR #456 from teammate for security and correctness

Copilot: Analyzing PR #456: "Add user search functionality"

## PR Review: Add user search functionality

### Files Changed
- src/api/search.js (+85, -0)
- src/services/UserSearchService.js (+120, -0)
- tests/search.test.js (+45, -0)

### Security Analysis

**HIGH: SQL Injection in search.js:34**
User input is concatenated directly into query string.

**MEDIUM: Missing rate limiting**
Search endpoint has no rate limiting, vulnerable to abuse.

**LOW: Sensitive data in logs**
Line 67 logs full user objects including email addresses.

### Correctness Analysis

**Issue: Off-by-one error in pagination**
Line 45 uses `offset = page * limit` instead of `(page - 1) * limit`

**Issue: Missing null check**
Line 78 accesses `user.profile.name` without checking if profile exists

### Test Coverage

Current test coverage: ~60%
Missing tests for:
- Empty search results
- Special characters in search query
- Pagination edge cases

### Positive Notes
- Good separation of concerns
- Clear function naming
- Proper TypeScript types

Shall I help draft review comments for these issues?
```

---

## Part 3: Providing Feedback

### Draft Review Comments

```
Create a constructive review comment for the SQL injection issue
```

Example output:
```markdown
**Security Concern: SQL Injection**

The current implementation constructs the SQL query using string concatenation:

```javascript
const query = `SELECT * FROM users WHERE name LIKE '%${searchTerm}%'`;
```

This is vulnerable to SQL injection attacks. For example, a user could input:
`'; DROP TABLE users; --`

**Suggested Fix:**
```javascript
const query = 'SELECT * FROM users WHERE name LIKE ?';
const results = await db.query(query, [`%${searchTerm}%`]);
```

Happy to discuss if you have questions!
```

### Post Comments via CLI

```
Add a comment to PR #456 on line 34 of search.js about the SQL injection issue
```

---

## Part 4: Review Checklist

### Security Review

```
Check PR #456 specifically for security issues like:
- Injection vulnerabilities
- Authentication/authorization bypasses
- Sensitive data exposure
- Missing input validation
```

### Performance Review

```
Analyze PR #456 for performance concerns:
- N+1 query problems
- Unnecessary data fetching
- Missing caching opportunities
- Algorithm efficiency
```

### Architecture Review

```
Review the architecture decisions in PR #456:
- Does it follow our existing patterns?
- Is the code properly modularized?
- Are dependencies appropriate?
```

---

## Review Best Practices

### 1. Be Specific

❌ Vague:
```
This code has issues
```

✅ Specific:
```
Line 45 has an off-by-one error in pagination calculation
```

### 2. Explain the Why

❌ Just the fix:
```
Use parameterized queries
```

✅ With explanation:
```
Use parameterized queries to prevent SQL injection, which could 
allow attackers to read or modify database contents
```

### 3. Provide Solutions

❌ Problem only:
```
This is vulnerable
```

✅ With solution:
```
This is vulnerable to XSS. Consider using DOMPurify to sanitize:
`const clean = DOMPurify.sanitize(userInput);`
```

### 4. Acknowledge Good Work

```
Also mention what's done well in this PR
```

---

## Exercise: Practice Code Review

### Exercise 8.2.1: Self-Review

1. Make some changes to a file in your project
2. Run `/review` to analyze your changes
3. Evaluate the feedback—which items would you address?

### Exercise 8.2.2: Review a PR

1. Find an open PR in a repository (yours or open source)
2. Ask Copilot to review it:
   ```
   Review PR [URL] focusing on security and correctness
   ```
3. Evaluate the review output
4. Consider what additional context you might add

### Exercise 8.2.3: Comparative Review

1. Review the same changes twice:
   - First with minimal context
   - Then with project context (instructions file)
2. Compare the quality of reviews

---

## Review Workflow Integration

### Before Creating PR

```
1. !git diff --staged                    # See changes
2. /review                               # Get AI review
3. [Fix issues found]
4. !git commit                           # Commit clean code
5. Create PR
```

### When Reviewing Others

```
1. Show me PR #123                       # Get overview
2. Review PR #123 thoroughly             # Deep analysis
3. Draft review comments for issues      # Prepare feedback
4. [Submit review via GitHub/ADO]
```

---

## Key Takeaways

1. **Self-review first**: Use `/review` before creating PRs
2. **Be specific**: Ask for focused reviews (security, performance)
3. **Constructive feedback**: Explain why and provide solutions
4. **Acknowledge good work**: Balance criticism with praise
5. **Automate patterns**: Use agents for consistent review quality

---

## Next Scenario

Continue to [Scenario 8.3: Addressing Feedback](./03-addressing-feedback.md) for handling review comments.
