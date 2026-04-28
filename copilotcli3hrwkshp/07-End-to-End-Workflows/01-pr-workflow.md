# Scenario 8.1: Pull Request Workflow

## Introduction

This hands-on scenario walks through a complete pull request workflow using Copilot CLI—from feature branch to merged PR.

## Scenario Overview

You're adding a new feature to a project. You'll:
1. Create a feature branch
2. Implement the feature
3. Write tests
4. Create a pull request
5. Handle review feedback
6. Merge the PR

---

## Step 1: Start the Session

Launch Copilot CLI in your project:

```bash
cd your-project
copilot
```

### Initial Context

```
I want to add a password strength indicator to the registration form.
Let me start by understanding the current implementation.

Show me @src/components/RegistrationForm.jsx
```

---

## Step 2: Create Feature Branch

```
Create a new branch called feature/password-strength-indicator from main
```

Copilot will:
1. Check current branch status
2. Fetch latest from main
3. Create and checkout new branch

**Verify:**
```
!git branch --show-current
```

---

## Step 3: Plan the Implementation

Switch to Plan mode (`Shift+Tab`) and plan:

```
[PLAN] Add a password strength indicator to the registration form that:
1. Shows strength as: Weak, Medium, Strong
2. Uses visual color coding (red, yellow, green)
3. Updates in real-time as user types
4. Considers: length, numbers, special chars, uppercase
```

Review and approve the plan.

---

## Step 4: Implement the Feature

Switch back to Interactive mode (`Shift+Tab`):

```
Let's implement step 1: Create the password strength utility function
```

After Copilot creates the utility:

```
Now create the PasswordStrengthIndicator component
```

Then:

```
Integrate the indicator into the RegistrationForm
```

---

## Step 5: Write Tests

```
Write tests for the password strength utility covering:
- Empty password (returns weak)
- Short password (returns weak)  
- Medium complexity password
- Strong password with all requirements
- Edge cases
```

Then:

```
Write component tests for PasswordStrengthIndicator
```

---

## Step 6: Verify Changes

### Run Tests

```
Run the tests to make sure everything passes
```

### Review Changes

```
/diff
```

Or ask:
```
Show me a summary of all the changes I've made
```

### Check for Issues

```
/review
```

---

## Step 7: Commit Changes

```
Create atomic commits for my changes:
1. One commit for the utility function
2. One commit for the component
3. One commit for the integration
4. One commit for the tests
```

Or for a single commit:

```
Commit all changes with a descriptive message following conventional commit format
```

---

## Step 8: Create Pull Request

```
Create a pull request with:
- Title: "Add password strength indicator to registration"
- Description: Explain what was added and why
- Link to any related issues
- Include screenshots section (I'll add those manually)
```

Copilot will:
1. Push the branch
2. Create the PR via GitHub MCP
3. Return the PR URL

---

## Step 9: Handle Pre-Merge Checks

```
Check if there are any failing status checks on my PR
```

If tests are failing:

```
Show me the failing tests and help me fix them
```

If there are merge conflicts:

```
Help me resolve the merge conflicts with main
```

---

## Step 10: Merge the PR

Once approved:

```
Merge my PR using squash merge
```

Then clean up:

```
Delete the feature branch locally and remotely
```

---

## Complete Session Example

Here's what a full session might look like:

```
You: I want to add a password strength indicator to the registration form

Copilot: I'll help you with that. Let me first understand the current 
implementation. [Reads RegistrationForm.jsx]

The form currently has email and password fields. Here's my plan:
1. Create a passwordStrength utility function
2. Create a PasswordStrengthIndicator component
3. Integrate it into the form
4. Add tests

Should I proceed?

You: Yes, start with the utility function

Copilot: [Creates src/utils/passwordStrength.js]
Created the utility function. It evaluates password strength based on:
- Length (8+ chars required for medium, 12+ for strong)
- Contains numbers
- Contains special characters
- Contains uppercase and lowercase

Want me to continue with the component?

You: Yes

Copilot: [Creates src/components/PasswordStrengthIndicator.jsx]
Created the component with visual indicators...

[... continues through implementation ...]

You: Create the PR

Copilot: Created PR #234: "Add password strength indicator to registration"
URL: https://github.com/org/repo/pull/234

The PR includes:
- 4 new files
- 127 lines added
- Test coverage for new functionality
```

---

## Tips for PR Workflow

### 1. Incremental Implementation

Don't try to do everything at once:
```
Let's implement just the utility function first
```

### 2. Verify As You Go

After each step:
```
Run the tests for what we just added
```

### 3. Clean Commits

Request atomic commits:
```
Create separate commits for each logical change
```

### 4. Descriptive PR

Ask for good descriptions:
```
Write a detailed PR description explaining the changes and reasoning
```

---

## Exercise: Practice PR Workflow

### Your Turn

1. Choose a small feature or improvement for your project
2. Follow this workflow to implement it
3. Create a real PR (or draft PR for practice)

Suggested practice tasks:
- Add input validation to a form
- Add a loading spinner to an async operation
- Create a new utility function with tests
- Add error handling to an API call

---

## Troubleshooting

### Branch Creation Fails

```
I can't create the branch - it says it already exists
```

Ask:
```
Delete the local feature branch and create a fresh one from main
```

### Tests Fail After Changes

```
My tests are failing after the changes
```

Ask:
```
Analyze the failing tests and determine if the tests need updating 
or if there's a bug in my implementation
```

### PR Creation Fails

```
I can't create the PR - authentication error
```

Check:
```
/mcp
```

Verify GitHub MCP server is running and authenticated.

---

## Key Takeaways

1. **End-to-end in CLI**: Complete PR workflow without leaving terminal
2. **Incremental approach**: Implement, test, commit in small steps
3. **Plan first**: Use Plan mode for complex features
4. **Verify often**: Run tests and review changes frequently
5. **Clean history**: Use atomic commits for clear history

---

## Next Scenario

Continue to [Scenario 8.2: Code Review](./02-code-review.md) for reviewing changes.
