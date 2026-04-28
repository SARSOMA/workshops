# Tutorial 4.3: Terminal-First Workflows

## Introduction

Terminal-first development with Copilot CLI creates efficient workflows where you rarely need to leave your terminal. This tutorial covers practical patterns for common development tasks.

## Workflow Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│                    TERMINAL-FIRST DEVELOPMENT                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Traditional Flow:                                              │
│  Terminal → IDE → Browser → Terminal → IDE → ...                │
│                                                                 │
│  Terminal-First Flow:                                           │
│  Terminal ──────────────────────────────────────►               │
│    └── Copilot CLI handles: Code, Git, GitHub, Testing         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Common Workflows

### Workflow 1: Feature Development

**Typical Flow:**
```bash
# 1. Start Copilot CLI
copilot

# 2. Create a feature branch
Create a new branch called feature/user-settings based on main

# 3. Plan the implementation
[PLAN] Add a user settings page with theme and notification preferences

# 4. Implement (after approving plan)
Start implementing the plan

# 5. Review changes
/diff

# 6. Create PR
Create a pull request with the changes we just made
```

### Workflow 2: Bug Fixing

```bash
copilot

# 1. Understand the issue
Show me the recent commits that might have caused issue #234

# 2. Reproduce and diagnose
The bug is in the login flow. Help me trace through @src/auth/login.js

# 3. Fix
Fix the null reference error we found

# 4. Test
Run the tests for the auth module

# 5. Commit
Commit the fix with a message referencing issue #234
```

### Workflow 3: Code Review

```bash
copilot

# 1. Get PR details
Show me the changes in PR #567

# 2. Deep review
/review

# 3. Add comments (if needed)
Add a comment on PR #567 suggesting the validation logic could be improved

# 4. Approve or request changes
Approve PR #567
```

### Workflow 4: Exploring New Codebase

```bash
copilot

# 1. Get overview
Give me an overview of this project structure

# 2. Understand key files
Explain the main entry point @src/index.js

# 3. Trace a flow
Show me how user authentication works from login to session creation

# 4. Find patterns
What design patterns are used in this codebase?
```

---

## Shell Integration Patterns

### Direct Shell Commands

Run shell commands without AI:
```
!git log --oneline -5
!npm run build
!docker ps
```

### Combining Shell and AI

```
You: Run the tests and tell me what failed

Copilot: [Runs tests, analyzes output, explains failures]

You: Fix the failing test

Copilot: [Fixes the test]

!npm test  # Verify directly
```

### Using Output for Context

```
!cat package.json

Based on the dependencies above, suggest any security updates needed
```

---

## Git Workflows

### Daily Git Tasks

```
# Status check
!git status

# Or ask Copilot
What's the current git status and are there any uncommitted changes?

# Intelligent commit
Review my changes and suggest a commit message

# Branch management
List all my local branches and which ones are behind main
```

### Complex Git Operations

```
# Interactive rebase
Help me squash the last 3 commits into one

# Conflict resolution
I have a merge conflict in @src/app.js. Help me resolve it

# History analysis
Who changed @src/api/routes.js in the last month and what did they change?
```

---

## Testing Workflows

### Running Tests

```
# Direct execution
!npm test

# With analysis
Run the tests and analyze any failures

# Specific test
Run only the tests for the user service
```

### Test Development

```
# Generate tests
Create unit tests for @src/services/UserService.js

# Coverage analysis
!npm run coverage
Which functions in @src/utils/ are not covered by tests?

# TDD flow
I want to add a validateEmail function. Write the tests first, then the implementation
```

---

## Build and Deploy Workflows

### Building

```
# Build and diagnose
Run the build and if it fails, explain the errors

# Optimization
The build is slow. Analyze our webpack config and suggest improvements
```

### Deployment

```
# Pre-deployment checklist
Before I deploy, check for:
1. Any TODO comments in production code
2. Console.log statements that should be removed
3. Environment variables that need to be set

# GitHub Actions
Create a GitHub Actions workflow that deploys to production when merging to main
```

---

## Documentation Workflows

### README Generation

```
Generate a comprehensive README for this project including:
- Project description
- Installation steps
- Usage examples
- API documentation
- Contributing guidelines
```

### Code Documentation

```
Add JSDoc comments to all public functions in @src/api/handlers/

Generate API documentation for the endpoints in @src/routes/
```

---

## Multi-File Operations

### Batch Updates

```
# Search and replace
Find all uses of 'oldFunctionName' and rename to 'newFunctionName'

# Pattern application
Add error handling to all async functions in @src/api/

# Style updates
Convert all arrow functions to use explicit return statements in @src/utils/
```

### Project-Wide Changes

```
# Dependency updates
Update all React class components in @src/components/ to functional components

# Migration
Convert this JavaScript project to TypeScript
```

---

## IDE Connection (Optional)

### Connecting to VS Code

```
/ide
```

This allows Copilot CLI to:
- Access diagnostics (errors, warnings)
- Get selection context
- Work with LSP features

### When to Connect

| Connect IDE When | Stay Terminal-Only When |
|-----------------|------------------------|
| Need live diagnostics | Simple file operations |
| Working with types | Running scripts |
| Complex refactoring | Git operations |
| Debugging | GitHub interactions |

---

## Exercise: Terminal Workflows

### Exercise 4.3.1: Complete Feature Workflow

Perform this entire workflow in Copilot CLI:

1. Create a new branch: `feature/add-validation`
2. Add email validation to a form
3. Write tests for the validation
4. Run and verify tests
5. Commit with a descriptive message
6. Create a pull request

### Exercise 4.3.2: Bug Fix Workflow

1. Pick a bug or improvement in your project
2. Trace the issue using Copilot
3. Implement the fix
4. Test the fix
5. Commit with issue reference

### Exercise 4.3.3: Shell Integration

Practice mixing shell and AI:

```
1. !git status
2. What files have I changed?
3. !git diff src/app.js
4. Should I split this into multiple commits?
5. Help me create atomic commits for these changes
```

---

## Productivity Tips

### 1. Use Shell Aliases

Add to your `.bashrc` or `.zshrc`:
```bash
alias cop='copilot'
alias copc='copilot --continue'
```

### 2. Quick Context Switch

```
!pwd                 # Where am I?
/cwd ~/other-project # Switch projects
!git status          # Check state
```

### 3. Batch Similar Tasks

Instead of multiple prompts:
```
❌ Add validation to email field
❌ Add validation to password field
❌ Add validation to phone field
```

Use:
```
✅ Add validation to all fields in @src/components/SignupForm.jsx:
- Email: valid format
- Password: min 8 chars, 1 number, 1 special
- Phone: US format
```

### 4. Keep History Clean

Use `/ask` for quick lookups:
```
/ask What's the syntax for optional chaining in JavaScript?
```

Keeps your main conversation focused.

---

## Key Takeaways

1. **Stay in terminal** - Copilot handles code, Git, and GitHub
2. **Use ! for direct execution** - Mix shell commands with AI
3. **Batch operations** - Combine related tasks
4. **Choose mode wisely** - Plan for complex, Interactive for exploration
5. **Connect IDE when needed** - For diagnostics and refactoring
6. **Build workflows** - Combine commands into repeatable patterns

---

## Next Section

Continue to [Section 5: Advanced Capabilities](../05-Advanced-Capabilities/README.md) for advanced features.
