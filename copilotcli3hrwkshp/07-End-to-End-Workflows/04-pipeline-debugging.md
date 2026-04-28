# Scenario 8.4: Pipeline Debugging

## Introduction

This scenario covers using Copilot CLI to diagnose and fix CI/CD pipeline failures efficiently.

## Scenario Overview

Your CI/CD pipeline is failing. You'll learn to:
1. Identify the failing step
2. Get and analyze logs
3. Diagnose the root cause
4. Fix the issue
5. Verify the fix

---

## Part 1: Identifying the Failure

### Check Pipeline Status

**GitHub Actions:**
```
Show me the status of the latest GitHub Actions run for this branch
```

**Azure DevOps:**
```
Show me recent pipeline runs for this project
```

### Get Failure Details

```
Show me which step failed in the latest pipeline run
```

Example output:
```
## Pipeline Run #1234 - Failed

**Branch:** feature/add-auth
**Trigger:** Push
**Duration:** 3m 45s

### Steps
1. ✅ Checkout
2. ✅ Install dependencies
3. ✅ Lint
4. ❌ Test (Failed)
5. ⏭️ Build (Skipped)
6. ⏭️ Deploy (Skipped)

**Failed Step:** Test
**Exit Code:** 1
```

---

## Part 2: Analyzing Logs

### Get Failure Logs

```
Show me the logs from the failed Test step
```

### Focus on Errors

```
Extract just the error messages from the pipeline logs
```

### Example Log Analysis

```
You: Show me why the tests failed in pipeline run #1234

Copilot: Analyzing logs from the Test step...

## Test Failures

**3 tests failed out of 147:**

1. `UserService.test.js`
   - `should create user with valid data`
   - Error: `Expected status code 201, received 500`
   - Stack: DatabaseError at connection.js:45

2. `AuthController.test.js`  
   - `should return token for valid credentials`
   - Error: `TypeError: Cannot read property 'id' of undefined`
   - Stack: AuthController.login at auth.js:23

3. `UserService.test.js`
   - `should update user profile`
   - Error: `Connection timeout after 30000ms`

**Root Cause Analysis:**
All failures appear related to database connectivity issues.
The connection pool may not be properly initialized in the test environment.
```

---

## Part 3: Diagnosing Root Cause

### Trace the Error

```
Show me @src/db/connection.js around line 45 where the DatabaseError occurred
```

### Compare with Working Version

```
What changed in the database configuration since the last successful run?
```

### Check Environment

```
Compare the test environment configuration with production
```

---

## Part 4: Fixing the Issue

### Implement the Fix

```
The tests are failing because the database pool initialization is async 
but tests start before it's ready. Add proper initialization handling.
```

### Example Fix Session

```
You: Fix the database connection issue in the tests

Copilot: I see the problem. In @tests/setup.js, the database connection 
is initiated but tests don't wait for it to complete.

Current code:
```javascript
beforeAll(() => {
  initDatabase(); // Async but not awaited
});
```

Fix:
```javascript
beforeAll(async () => {
  await initDatabase();
  await waitForConnection();
});
```

Should I apply this fix?

You: Yes, and also add a connection check

Copilot: [Applies fix with connection verification]
```

### Alternative: Environment Fix

```
The CI environment is missing the DATABASE_URL secret. 
Show me how to add it to GitHub Actions
```

---

## Part 5: Verifying the Fix

### Run Tests Locally

```
Run the tests locally to verify my fix works
```

### Push and Monitor

```
Commit my fix and push to trigger a new pipeline run
```

### Check Pipeline Status

```
Monitor the new pipeline run and tell me when it completes
```

---

## Common Pipeline Issues

### Issue 1: Missing Environment Variables

**Symptoms:**
```
Error: MONGODB_URI is not defined
```

**Diagnosis:**
```
Check if the pipeline has access to the MONGODB_URI secret
```

**Fix:**
```
Show me how to add secrets to this pipeline configuration
```

### Issue 2: Dependency Version Mismatch

**Symptoms:**
```
Error: Cannot find module 'react-dom/client'
```

**Diagnosis:**
```
Compare local package.json with what's installed in CI
```

**Fix:**
```
Update the lockfile and ensure CI uses the same Node version
```

### Issue 3: Test Timeout

**Symptoms:**
```
Timeout - Async callback was not invoked within 5000ms
```

**Diagnosis:**
```
Which tests are timing out and why?
```

**Fix:**
```
Increase timeout for database tests or fix async handling
```

### Issue 4: Build Failure

**Symptoms:**
```
TypeScript error TS2345: Argument of type...
```

**Diagnosis:**
```
Show me the TypeScript errors and where they occur
```

**Fix:**
```
Fix the type errors in @src/components/UserForm.tsx
```

---

## Pipeline Configuration Issues

### Debugging Workflow Files

**GitHub Actions:**
```
Check my .github/workflows/ci.yml for any configuration issues
```

**Azure DevOps:**
```
Review my azure-pipelines.yml for problems
```

### Common Config Fixes

```
The pipeline is using Node 14 but my code requires Node 18.
Update the workflow to use the correct Node version.
```

```
The pipeline isn't caching dependencies. Add caching to speed it up.
```

---

## Exercise: Debug a Pipeline

### Exercise 8.4.1: Analyze Failure

1. Find a failed pipeline run (or create one with a failing test)
2. Get the failure logs
3. Identify the root cause
4. Plan the fix

### Exercise 8.4.2: Fix and Verify

1. Implement the fix identified above
2. Run tests locally
3. Push and verify the pipeline passes

### Exercise 8.4.3: Pipeline Optimization

1. Analyze your pipeline for inefficiencies
2. Ask Copilot for optimization suggestions:
   ```
   How can I make this pipeline faster?
   ```
3. Implement improvements

---

## Debug Workflow Checklist

```
□ Identify which step failed
□ Get relevant logs
□ Find the specific error
□ Understand the root cause
□ Check for recent changes that might have caused it
□ Implement fix
□ Test locally
□ Push and verify
□ Document the fix (if it could happen again)
```

---

## Tips for Pipeline Debugging

### 1. Read Logs Carefully

```
Show me the full log context around the error, not just the error message
```

### 2. Compare with Last Success

```
What changed between the last successful run and this failure?
```

### 3. Reproduce Locally

```
Help me reproduce this pipeline failure locally for debugging
```

### 4. Check Common Causes

- Missing secrets/env vars
- Version mismatches (Node, npm, etc.)
- Network/timeout issues
- Flaky tests

### 5. Use Pipeline History

```
Has this pipeline failed before with similar errors?
```

---

## Key Takeaways

1. **Systematic approach**: Identify → Analyze → Diagnose → Fix → Verify
2. **Read logs thoroughly**: Context matters
3. **Compare changes**: What's different from last success?
4. **Test locally first**: Don't debug in CI
5. **Document fixes**: Help future you and teammates

---

## Next Section

Continue to [Section 9: Wrap-Up](../09-Wrap-Up/README.md) for key takeaways and best practices.
