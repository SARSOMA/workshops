# Tutorial 5.4: Code Review

---

## Concept

### Code Review with Copilot CLI

Copilot CLI can help you:

1. **Review your own changes** before submitting
2. **Review others' PRs** from the command line
3. **Add comments** to specific lines
4. **Approve or request changes**

### Review Commands

| Action | Prompt |
|--------|--------|
| Review pending changes | `/review` |
| Review a specific PR | "Review PR #123 in SARSOMA/akri" |
| Get PR details | "Show me PR #123" |
| Add a comment | "Add a comment on line 45 about the null check" |

### What Good Reviews Look For

- **Correctness**: Does the code do what it's supposed to?
- **Style**: Does it follow project conventions?
- **Documentation**: Are changes documented?
- **Tests**: Are there adequate tests?
- **Security**: Any security concerns?
- **Performance**: Any performance implications?

---

## Practice

### Exercise 1: Review Your Own Changes

Before creating a PR, always review your work:

```
/review
```

Or more specifically:

```
Review my pending changes. Look for:
- Potential bugs
- Style issues
- Missing documentation
- Edge cases not handled
```

### Exercise 2: Find a PR to Review

```
Show me open pull requests in SARSOMA/akri
```

```
Pick one and show me the details
```

### Exercise 3: Review a PR

> **Note for workshop**: The instructor may have created a PR with intentional issues for practice.

```
Review PR #[number] in SARSOMA/akri. 
Focus on code style, logic errors, and documentation gaps.
```

### Exercise 4: Identify Specific Issues

Practice finding different types of issues:

```
Are there any code style issues in this PR?
```

```
Are there any logic errors or edge cases not handled?
```

```
Is the documentation adequate for these changes?
```

### Exercise 5: Add Review Comments

If you have write access to the PR (or are practicing):

```
Add a review comment on [file] line [number] suggesting 
a better variable name for clarity
```

```
Add a comment asking why [specific code decision] was made
```

### Exercise 6: Practice Review Workflow

For a complete review simulation:

1. **Get the diff:**
   ```
   Show me the diff for PR #[number]
   ```

2. **Summarize changes:**
   ```
   Summarize what this PR changes
   ```

3. **Check for issues:**
   ```
   What potential issues do you see in this PR?
   ```

4. **Suggest improvements:**
   ```
   What improvements would you suggest?
   ```

### Exercise 7: Responding to Review Feedback

If you received feedback on your PR:

```
Show me the comments on my PR
```

```
Help me address the feedback about [specific comment]
```

```
The reviewer suggested [change]. Help me implement that.
```

---

## Sample PR Review Exercise

> **Instructor Note**: A sample PR with intentional issues has been prepared.

### The Practice PR

Review the workshop practice PR which contains intentional issues:
- Code style inconsistencies
- A logic error in edge case handling  
- Missing documentation for a new function

```
Review the workshop practice PR and identify:
1. Any code style issues
2. Potential logic errors
3. Documentation gaps
```

### Issues to Find

<details>
<summary>Click to reveal what to look for</summary>

**Code Style Issues:**
- Inconsistent indentation
- Missing trailing newline
- Variable naming doesn't follow conventions

**Logic Errors:**
- Missing null check before accessing property
- Off-by-one error in loop condition
- Incorrect handling of empty input

**Documentation Gaps:**
- New function without documentation comment
- Updated behavior not reflected in README
- Missing parameter descriptions

</details>

---

## Q&A

### Question 1

What command starts a code review of your pending changes?

A) `/check`  
B) `/review`  
C) `/lint`  
D) `/inspect`  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

The `/review` command reviews your pending code changes, looking for potential issues, style problems, and improvements.

</details>

---

### Question 2

Which of these is NOT typically part of a code review?

A) Checking for potential bugs  
B) Verifying code style  
C) Checking the developer's lunch schedule  
D) Ensuring adequate test coverage  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Code reviews focus on code quality: bugs, style, tests, documentation, security, and performance. Personal schedules are not part of code review.

</details>

---

### Question 3

How can you see comments left on your PR?

A) "What comments are on my PR?"  
B) "Show me feedback on my PR"  
C) Both A and B work  
D) Neither works  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Natural language queries like "Show me the comments on my PR" or "What feedback did I get on my PR?" both work. Copilot uses GitHub MCP to fetch PR comments.

</details>

---

### Question 4

Why is it important to review your own changes before creating a PR?

A) It's not important  
B) It catches issues early, before reviewers see them  
C) It makes the code run faster  
D) It's required by Git  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Self-review catches issues early, reducing back-and-forth with reviewers and improving code quality. It's a professional best practice.

</details>

---

## Review Checklist

Use this checklist when reviewing code:

- [ ] **Correctness**: Does the code work as intended?
- [ ] **Style**: Follows project conventions?
- [ ] **Documentation**: Changes documented?
- [ ] **Tests**: Adequate test coverage?
- [ ] **Security**: No security vulnerabilities?
- [ ] **Performance**: No obvious performance issues?
- [ ] **Readability**: Code is clear and maintainable?

---

## Summary: Complete Workflow

You've now completed a full development workflow:

```
1. Explore    →  Understand the codebase
2. Plan       →  Design your changes
3. Implement  →  Make changes via Copilot
4. Review     →  Self-review with /review
5. Commit     →  Stage and commit
6. Push       →  Push to remote
7. PR         →  Create pull request
8. Review     →  Review and iterate
```

All without leaving your terminal! 🎉

---

## Next Steps

Continue to [Section 6: Wrap-Up](../06-Wrap-Up/README.md) for key takeaways and resources.
