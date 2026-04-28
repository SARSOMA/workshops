# Scenario 8.3: Addressing PR Feedback

## Introduction

This scenario covers efficiently addressing review feedback on your pull requests using Copilot CLI.

## Scenario Overview

You've received review comments on your PR. You'll learn to:
1. Fetch and understand review feedback
2. Systematically address each comment
3. Respond to reviewers appropriately
4. Update the PR with fixes

---

## Step 1: Get Review Comments

### Fetch All Comments

```
Show me all review comments on PR #234
```

### Prioritize by Severity

```
List the review comments on PR #234 sorted by severity, 
with blocking issues first
```

### Example Output

```
## Review Comments on PR #234

### Blocking (Must Fix)
1. **@src/api/search.js:34** - @reviewer1
   "SQL injection vulnerability - please use parameterized queries"

2. **@src/services/UserSearch.js:78** - @reviewer2
   "Missing null check will cause runtime error"

### Should Fix
3. **@src/api/search.js:67** - @reviewer1
   "Consider adding rate limiting to this endpoint"

4. **@src/services/UserSearch.js:45** - @reviewer2
   "This could be more efficient with a single query"

### Suggestions
5. **@src/api/search.js:12** - @reviewer1
   "Minor: Consider extracting this to a constant"
```

---

## Step 2: Address Each Comment

### Work Through Systematically

```
Let's address comment #1 about SQL injection in @src/api/search.js:34
```

Copilot will:
1. Read the file and understand the context
2. Propose a fix
3. Explain the changes

### Example Fix Session

```
You: Fix the SQL injection issue at line 34 of @src/api/search.js

Copilot: I see the issue. The current code concatenates user input:

```javascript
const query = `SELECT * FROM users WHERE name LIKE '%${term}%'`;
```

Here's the fix using parameterized queries:

```javascript
const query = 'SELECT * FROM users WHERE name LIKE ?';
const results = await db.query(query, [`%${term}%`]);
```

Should I apply this change?

You: Yes

Copilot: [Applies change]
Fixed. The query now uses parameterized input to prevent SQL injection.
```

### Continue to Next Item

```
Now let's fix comment #2 about the null check
```

---

## Step 3: Batch Similar Fixes

For related comments:

```
Fix all the null check issues mentioned in the review comments
```

Or for style issues:

```
Address all the minor suggestions from the review (constants, naming, etc.)
```

---

## Step 4: Respond to Comments

### Draft Responses

```
Draft a response to comment #1 explaining what I fixed
```

Example:
```markdown
Fixed! I've updated to use parameterized queries:
```javascript
const query = 'SELECT * FROM users WHERE name LIKE ?';
const results = await db.query(query, [`%${term}%`]);
```
This prevents SQL injection by separating query structure from data.
```

### Post Response via CLI

```
Reply to comment #1 with the fix explanation
```

### Handle Disagreements

```
I disagree with comment #5 about extracting to a constant - 
draft a polite response explaining why I prefer to keep it inline
```

---

## Step 5: Verify All Fixes

### Run Tests

```
Run the tests to make sure my fixes didn't break anything
```

### Re-Review Changes

```
Review my changes since the last commit to make sure the fixes are correct
```

### Check Off Items

```
Show me which review comments I've addressed and which remain
```

---

## Step 6: Update the PR

### Commit Fixes

```
Commit my changes with a message like "Address review feedback"
```

### Or Atomic Commits

```
Create separate commits for each review item I addressed
```

### Push and Notify

```
Push my changes

Then summarize what I fixed for the reviewers
```

---

## Complete Workflow Example

```
You: Show me review comments on my PR #234

Copilot: Found 5 comments:
1. [Blocking] SQL injection at search.js:34
2. [Blocking] Null check at UserSearch.js:78
3. [Should Fix] Rate limiting at search.js:67
4. [Should Fix] Query efficiency at UserSearch.js:45
5. [Minor] Extract constant at search.js:12

You: Fix the blocking issues first

Copilot: Starting with SQL injection...
[Fixes issue 1]
Fixed. Now the null check...
[Fixes issue 2]
Fixed. Both blocking issues resolved.

You: Run tests to verify

Copilot: Running tests... All 47 tests passing.

You: Now fix issues 3 and 4

Copilot: [Fixes remaining issues]
Done. Added rate limiting middleware and optimized query.

You: Create a commit for these fixes

Copilot: Created commit "Address review feedback"
- Fixed SQL injection vulnerability
- Added null safety checks
- Added rate limiting
- Optimized database queries

You: Push and draft a summary for reviewers

Copilot: Pushed to origin/feature/search

Summary for reviewers:
"Hi team, I've addressed all the review feedback:
✅ SQL injection - now using parameterized queries
✅ Null checks - added safety checks throughout
✅ Rate limiting - added middleware (100 req/min)
✅ Query optimization - combined into single query

All tests passing. Ready for re-review!"
```

---

## Handling Complex Feedback

### When You Need Clarification

```
Comment #3 asks for rate limiting but doesn't specify the limits.
Draft a question asking for clarification on requirements.
```

### When You Disagree

```
I disagree with the suggestion to use a different algorithm.
Help me draft a response that:
1. Acknowledges the feedback
2. Explains my reasoning
3. Proposes a compromise or discussion
```

### When It's a Larger Change

```
Comment #4 would require significant refactoring.
Help me:
1. Estimate the scope of the change
2. Decide if it should be in this PR or a follow-up
3. Draft a response explaining the decision
```

---

## Exercise: Practice Addressing Feedback

### Exercise 8.3.1: Simulated Review

1. Make changes to a file with some intentional issues
2. Run `/review` to generate feedback
3. Address each item systematically
4. Verify with tests

### Exercise 8.3.2: Real PR Feedback

If you have a PR with feedback:
1. Fetch the comments
2. Work through each one with Copilot
3. Commit and push the fixes
4. Draft responses

### Exercise 8.3.3: Handling Disagreement

Practice drafting constructive disagreement responses:
```
Draft a response disagreeing with this review comment: 
"You should use a different database library"
Be professional and explain the reasoning for keeping current approach.
```

---

## Tips for Efficient Feedback Handling

### 1. Triage First

Start by categorizing:
```
Group the review comments by: blocking, should-fix, and optional
```

### 2. Fix Blocking First

```
Let's focus on blocking issues only for now
```

### 3. Batch Similar Fixes

```
Fix all the import ordering issues at once
```

### 4. Test Frequently

After each fix:
```
Run the tests for the file I just changed
```

### 5. Track Progress

```
Which comments have I addressed so far?
```

---

## Key Takeaways

1. **Fetch first**: Get all comments before starting
2. **Prioritize**: Address blocking issues first
3. **Systematic**: Work through methodically
4. **Respond thoughtfully**: Explain your fixes
5. **Verify**: Test after each set of changes
6. **Communicate**: Keep reviewers informed

---

## Next Scenario

Continue to [Scenario 8.4: Pipeline Debugging](./04-pipeline-debugging.md) for handling CI/CD failures.
