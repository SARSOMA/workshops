# Tutorial 3.1: Prompt Engineering for Copilot CLI

## Introduction

Effective prompts lead to better results. This tutorial covers techniques for crafting prompts that get the most out of Copilot CLI.

## The Anatomy of a Good Prompt

### Basic Structure

```
[Context] + [Task] + [Constraints] + [Output Format]
```

**Example:**
```
In @src/api/users.js (context),
add input validation for the createUser function (task)
using Joi for schema validation (constraint).
Include JSDoc comments explaining each validation rule (output format).
```

---

## Prompt Techniques

### 1. Be Specific About Files

❌ **Vague:**
```
Fix the login bug
```

✅ **Specific:**
```
Fix the authentication error in @src/auth/login.js where the token 
validation fails for expired tokens
```

### 2. Provide Examples

❌ **Abstract:**
```
Add logging to the API
```

✅ **With example:**
```
Add logging to @src/api/routes.js following this pattern:

logger.info('Operation started', { userId, action: 'create' });
// ... operation code ...
logger.info('Operation completed', { userId, result: 'success' });
```

### 3. Define Success Criteria

❌ **Open-ended:**
```
Improve the performance
```

✅ **Measurable:**
```
Optimize @src/utils/dataProcessor.js to handle 10,000 records 
without exceeding 100ms processing time. Use batch processing 
and avoid loading all records into memory.
```

### 4. Break Down Complex Tasks

❌ **Monolithic:**
```
Build a complete user authentication system with registration, 
login, password reset, OAuth, 2FA, and session management
```

✅ **Incremental:**
```
Let's build user authentication step by step.

Step 1: Create a basic User model with email and password fields 
in @src/models/User.js. Use bcrypt for password hashing.

[Wait for completion]

Step 2: Now add the registration endpoint in @src/routes/auth.js
```

### 5. Reference Existing Patterns

```
Following the pattern established in @src/services/UserService.js,
create a ProductService in @src/services/ProductService.js with 
the same structure for CRUD operations.
```

---

## Prompt Templates

### Bug Fix Template

```
Bug: [Description of the issue]
Location: @[file path]
Expected behavior: [What should happen]
Actual behavior: [What is happening]
Steps to reproduce: [If applicable]

Please fix this bug and explain the root cause.
```

**Example:**
```
Bug: Users receive "undefined" error when submitting empty form
Location: @src/components/ContactForm.jsx
Expected behavior: Form should show validation errors
Actual behavior: JavaScript error "Cannot read property 'trim' of undefined"
Steps to reproduce: Submit the form without filling any fields

Please fix this bug and explain the root cause.
```

### Feature Addition Template

```
Feature: [Name/description]
Files affected: @[file1], @[file2]
Requirements:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

Please implement this feature following our existing code patterns.
```

### Code Review Template

```
Review @[file path] for:
- [ ] Security vulnerabilities
- [ ] Performance issues
- [ ] Code style consistency
- [ ] Error handling completeness
- [ ] Test coverage suggestions

Prioritize issues by severity (critical, high, medium, low).
```

### Refactoring Template

```
Refactor @[file path] to:
- [Goal 1]
- [Goal 2]

Constraints:
- Don't change the public API
- Maintain backward compatibility
- Keep all existing tests passing
```

---

## Context-Efficient Prompts

### Use File References Wisely

```
# Good: Specific file
Explain the error handling in @src/api/middleware/errorHandler.js

# Better: Focused section
Explain lines 25-50 in @src/api/middleware/errorHandler.js 
where async errors are caught
```

### Minimize Exploration Overhead

```
# Forces broad search
Find where we handle authentication

# Provides starting point
Starting from @src/auth/index.js, trace how user authentication 
flows through to @src/api/middleware/auth.js
```

### Reference Previous Context

```
Using the User model we just created, now add an API endpoint 
to fetch user profiles by ID
```

---

## Interactive Refinement

### Steering Mid-Task

While Copilot is working, you can add clarifications:

```
[Copilot is implementing a feature]

You: Actually, use axios instead of fetch for the HTTP calls
```

### Inline Feedback on Rejection

When you reject a tool permission:

```
[Copilot wants to run: rm -rf node_modules]

You: [Press Esc] No, let me handle the cleanup. Just show me 
what dependencies need updating.
```

### Iterative Improvement

```
Turn 1: Create a basic React component for user profiles
Turn 2: Add loading and error states
Turn 3: Add TypeScript types
Turn 4: Add unit tests
```

---

## Special Syntax

### File References (@)

```
@src/app.js                    # Specific file
@src/                          # Directory (Copilot lists contents)
@package.json                  # Project metadata
```

### Issue/PR References (#)

```
#123                           # Issue or PR number
Work on #123                   # Pull issue context into prompt
Review changes in PR #456      # Get PR diff context
```

### Shell Commands (!)

```
!git status                    # Run without AI
!npm test                      # Direct execution
```

### Side Questions (/ask)

```
/ask What's the best library for date handling in JavaScript?
```

This doesn't add to conversation history—useful for quick lookups.

---

## Exercise: Prompt Crafting

### Exercise 3.1.1: Transform Vague to Specific

Transform these vague prompts into effective ones:

1. "Fix the bug"
2. "Add tests"  
3. "Make it faster"
4. "Add a feature"

<details>
<summary>Example Solutions</summary>

1. **Fix the bug:**
   ```
   Fix the null reference error in @src/utils/parser.js line 42
   where the 'data' parameter is undefined when called from
   @src/api/handlers/import.js. Add null checking and return
   an appropriate error message.
   ```

2. **Add tests:**
   ```
   Add unit tests for @src/services/UserService.js following the
   patterns in @tests/services/AuthService.test.js. Cover:
   - createUser with valid input
   - createUser with invalid email
   - updateUser permissions check
   - deleteUser cascade behavior
   ```

3. **Make it faster:**
   ```
   Optimize @src/utils/dataLoader.js which currently takes 5+ 
   seconds to load 1000 records. Profile and identify bottlenecks.
   Consider: batch processing, lazy loading, caching, or 
   database query optimization.
   ```

4. **Add a feature:**
   ```
   Add email verification to the user registration flow.
   
   Files to modify:
   - @src/services/UserService.js - Add sendVerificationEmail method
   - @src/models/User.js - Add emailVerified and verificationToken fields
   - @src/routes/auth.js - Add /verify-email endpoint
   
   Use our existing email service in @src/services/EmailService.js
   ```

</details>

### Exercise 3.1.2: Practice Templates

Pick a file in your project and create prompts using each template:
1. Bug fix prompt
2. Feature addition prompt
3. Code review prompt
4. Refactoring prompt

---

## Anti-Patterns to Avoid

### 1. Ambiguous Scope

❌ `Update the project to use the latest best practices`

Why: Too broad, no clear end condition

### 2. Assuming Context

❌ `Use the usual pattern`

Why: Copilot doesn't know your "usual" without references

### 3. Multiple Unrelated Tasks

❌ `Fix the login bug, add dark mode, and update the README`

Why: Mix of concerns leads to partial execution

### 4. Unclear Success Criteria

❌ `Make the code better`

Why: Subjective and unmeasurable

---

## Key Takeaways

1. **Structure matters**: Context + Task + Constraints + Format
2. **Be explicit**: Reference files with `@`
3. **Break it down**: Large tasks into small steps
4. **Show examples**: Demonstrate the pattern you want
5. **Iterate**: Refine through conversation
6. **Use templates**: Consistent structure improves results

---

## Next Tutorial

Continue to [Tutorial 3.2: Session Management](./02-session-management.md) for efficient session handling.
