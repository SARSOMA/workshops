# Tutorial 5.3: PR Workflow

---

## Concept

### The PR Workflow

A typical pull request workflow with Copilot CLI:

```
┌─────────────────────────────────────────────────────┐
│               PR WORKFLOW                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Create Branch ──► 2. Make Changes ──►           │
│                                                     │
│  3. Commit ──► 4. Push ──► 5. Create PR             │
│                                                     │
│  All via natural language in Copilot CLI!           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Git Operations via Copilot

| Task | Natural Language | Git Equivalent |
|------|------------------|----------------|
| New branch | "Create a branch called feature/docs-update" | `git checkout -b feature/docs-update` |
| Stage files | "Stage all my changes" | `git add .` |
| Commit | "Commit with message 'Fix typos in README'" | `git commit -m "..."` |
| Push | "Push my changes" | `git push -u origin branch-name` |
| Create PR | "Create a pull request" | GitHub CLI or web |

### Forking for Contributions

Since akri is not your repository, you'll need to:

1. **Fork** the repository to your account
2. **Clone** your fork
3. **Make changes** in your fork
4. **Create PR** from your fork to the original

---

## Practice

### Exercise 1: Fork the Repository (if contributing)

> **Note**: Skip this if you're just practicing locally without pushing.

1. **Go to** [github.com/SARSOMA/akri](https://github.com/SARSOMA/akri)
2. **Click Fork** (top right)
3. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/akri.git
   cd akri
   ```

### Exercise 2: Create a Feature Branch

In Copilot CLI:

```
Create a new branch called "docs/readme-improvements" from main
```

Verify:
```
!git branch --show-current
```

### Exercise 3: Make Your Changes

If you haven't already from the previous tutorial:

```
Make a small improvement to the README.md - fix any typo or improve clarity
```

### Exercise 4: Review Changes Before Committing

```
/diff
```

Or:
```
Show me all the changes I've made
```

### Exercise 5: Stage and Commit

```
Stage and commit all my changes with a descriptive commit message 
following conventional commit format
```

Copilot might create a commit like:
```
docs: improve README clarity and fix typos
```

### Exercise 6: Push the Branch

```
Push my branch to origin
```

If this is your first push to this branch:
```
Push my branch and set up tracking
```

### Exercise 7: Create a Pull Request

```
Create a pull request with:
- Title: "docs: Improve README clarity"
- Description: Explain what was changed and why
- Target branch: main
```

Copilot will:
1. Use GitHub MCP to create the PR
2. Return the PR URL

### Exercise 8: View Your PR

```
Show me the PR I just created
```

Or go to the URL Copilot provided.

---

## Alternative: Practice PR Without Pushing

If you can't push (no fork access), practice the workflow locally:

### Local-Only Practice

1. **Create branch:**
   ```
   Create a branch called "practice/local-changes"
   ```

2. **Make changes:**
   ```
   Add a comment to any source file
   ```

3. **Commit locally:**
   ```
   Commit my changes with message "practice: add code comment"
   ```

4. **View commit history:**
   ```
   !git log --oneline -5
   ```

5. **Clean up:**
   ```
   Switch back to main and delete the practice branch
   ```

---

## Q&A

### Question 1

Why do you need to fork a repository before contributing?

A) Forking makes the code run faster  
B) You don't have write access to repositories you don't own  
C) Forking is required by Git  
D) It's just a convention with no real purpose  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

You fork a repository because you don't have write access to repositories you don't own. The fork creates a copy under your account where you have full access, then you create PRs from your fork to the original.

</details>

---

### Question 2

What command shows your pending changes before committing?

A) `/status`  
B) `/diff`  
C) `/pending`  
D) `/changes`  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

The `/diff` command shows pending file changes. You should always review the diff before committing to ensure changes are correct.

</details>

---

### Question 3

What is "conventional commit format"?

A) A random commit message  
B) Structured messages like "type: description" (e.g., "docs: fix typos")  
C) Commits that follow Git defaults  
D) Commits with exactly 50 characters  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Conventional commits follow a structured format: `type: description` (e.g., `docs: fix README typos`, `feat: add user validation`, `fix: null pointer exception`). This makes commit history readable and enables automated changelogs.

</details>

---

## Branch Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/description` | `feature/user-auth` |
| Bug fix | `fix/description` | `fix/null-check` |
| Documentation | `docs/description` | `docs/readme-update` |
| Refactor | `refactor/description` | `refactor/auth-module` |

---

## Next Steps

Continue to [Tutorial 5.4: Code Review](./04-code-review.md) to learn how to review PRs and add comments.
