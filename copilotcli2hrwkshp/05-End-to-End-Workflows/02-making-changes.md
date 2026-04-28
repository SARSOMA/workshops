# Tutorial 5.2: Making Changes

---

## Concept

### Making Changes with Copilot CLI

Copilot CLI can help you make changes through natural language:

1. **Describe what you want** — in plain English
2. **Copilot plans the change** — shows what it will do
3. **You review and approve** — nothing happens without consent
4. **Copilot implements** — makes the actual changes
5. **You verify** — check the results

### Types of Changes

| Change Type | Example Prompt |
|-------------|----------------|
| Bug fix | "Fix the null check in @src/auth.rs line 45" |
| Feature | "Add input validation to the user form" |
| Refactor | "Extract the validation logic into a separate function" |
| Documentation | "Add JSDoc comments to all public functions" |
| Tests | "Add unit tests for the calculateTotal function" |

### Best Practices

- **Be specific** — mention files, line numbers, function names
- **Incremental changes** — small steps, verify each
- **Review diffs** — always check `/diff` before committing
- **Test after changes** — run tests to verify nothing broke

---

## Practice

### Exercise 1: Identify a Small Change

First, let's find something to improve:

```
Look at the README.md file. Are there any typos, unclear sections, 
or areas that could be improved?
```

Or:

```
Find a simple documentation improvement I could make to this project
```

### Exercise 2: Plan the Change

Switch to Plan mode (`Shift+Tab`) and describe your change:

```
[PLAN] Improve the README.md by:
1. Fixing any typos or grammatical errors
2. Adding clearer installation instructions
3. Improving the formatting
```

Review the plan before proceeding.

### Exercise 3: Implement the Change

Switch back to Interactive mode (`Shift+Tab`):

```
Let's implement the README improvements step by step.
Start with fixing any typos.
```

After each step, review:
```
/diff
```

### Exercise 4: Make a Code-Level Change

Find a simple code improvement:

```
Are there any functions missing documentation or comments?
Pick one and add appropriate documentation.
```

Or:

```
Find a TODO comment in the codebase and help me address it
```

### Exercise 5: Add or Improve Tests

```
Find a function that could use better test coverage and write a test for it
```

Or:

```
Are there any edge cases in existing tests that aren't covered?
```

### Exercise 6: Verify Your Changes

After making changes:

1. **View all changes:**
   ```
   /diff
   ```

2. **Review for issues:**
   ```
   /review
   ```

3. **Run tests (if applicable):**
   ```
   !cargo test
   ```
   or
   ```
   Run the project tests
   ```

### Exercise 7: Interactive Refinement

If something isn't quite right:

```
The change you made to line 45 looks good, but can you also handle 
the case where the input is empty?
```

```
Revert the last change and try a different approach
```

---

## Q&A

### Question 1

What should you do after Copilot makes a code change?

A) Immediately commit and push  
B) Review the diff and verify the change is correct  
C) Close the terminal  
D) Delete the original file  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Always review the diff (`/diff`) and verify the change is correct before committing. Copilot is helpful but not infallible — human review is essential.

</details>

---

### Question 2

Which prompt style is better for making changes?

A) "Fix the code"  
B) "Fix the null pointer exception in @src/api/users.rs at line 45 by adding a proper check before accessing the user object"  
C) "Make it work"  
D) "Do something with the file"  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Specific prompts with file names, line numbers, and clear descriptions lead to better results. Vague prompts often lead to incorrect or incomplete changes.

</details>

---

### Question 3

What is the recommended approach for making multiple changes?

A) Make all changes at once in a single prompt  
B) Make changes incrementally, verifying each step  
C) Skip verification to save time  
D) Let Copilot decide the order  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Make changes incrementally and verify each step. This makes it easier to identify issues, rollback if needed, and maintain a clear history of what was changed and why.

</details>

---

## Useful Commands

| Command | Purpose |
|---------|---------|
| `/diff` | Show pending changes |
| `/review` | Review code changes |
| `/clear` | Start fresh |
| `!git status` | Check Git status |
| `!git diff` | Show Git diff |

---

## Next Steps

Continue to [Tutorial 5.3: PR Workflow](./03-pr-workflow.md) to learn how to commit and create a pull request.
