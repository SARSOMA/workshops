# Tutorial 3.1: Commands & Modes

---

## Concept

### Essential Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all available commands | `/help` |
| `/clear` | Clear context and start fresh | `/clear` |
| `/context` | Show loaded context | `/context` |
| `/diff` | Show pending file changes | `/diff` |
| `/review` | Review code changes | `/review` |
| `/mcp` | Manage MCP servers | `/mcp` |
| `/model` | View or change AI model | `/model claude-sonnet-4` |
| `/exit` | Exit Copilot CLI | `/exit` |
| `/compact` | Summarize history to reduce context | `/compact` |

### Special Syntax

| Syntax | Purpose | Example |
|--------|---------|---------|
| `@file` | Include file in context | `@src/main.py` |
| `@dir/` | Include directory structure | `@src/` |
| `!command` | Run shell command | `!git status` |
| `#number` | Reference GitHub issue/PR | `#123` |

### Interaction Modes

Copilot CLI offers three distinct modes that control how the agent works with you:

```
┌─────────────────────────────────────────────────────────────────────┐
│                       INTERACTION MODES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│      ┌──────────────┐                      ┌──────────────┐         │
│      │  INTERACTIVE │ ◄── Shift+Tab ──►   │     PLAN     │         │
│      │    (chat)    │                      │   (plan)     │         │
│      └──────┬───────┘                      └──────┬───────┘         │
│             │                                     │                 │
│             └─────────► Shift+Tab ◄───────────────┘                 │
│                              │                                      │
│                              ▼                                      │
│                      ┌──────────────┐                               │
│                      │     AUTO     │                               │
│                      │  (yolo/auto) │                               │
│                      └──────────────┘                               │
│                                                                     │
│  Current mode shown in prompt: [chat] [plan] [auto]                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Mode Comparison

| Aspect | Interactive (chat) | Plan | Auto |
|--------|-------------------|------|------|
| **Control Level** | Maximum | Medium | Minimum |
| **Speed** | Slowest | Medium | Fastest |
| **Confirmations** | Every action | Plan approval, then batch | Almost none |
| **Best For** | Learning, debugging, careful work | Multi-step features | Routine/trusted tasks |
| **Risk Level** | Lowest | Low | Higher |

#### Interactive Mode (Default)

The safest, most hands-on mode — you approve every action:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      INTERACTIVE MODE FLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  You: "Add error handling to the login function"                    │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ Agent: "I'll read src/auth.ts first"       │                    │
│  │ [Approve] [Deny] [Edit]                    │ ◄── You decide     │
│  └────────────────────────────────────────────┘                    │
│                              │ Approve                              │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ Agent: "I'll add try-catch blocks..."      │                    │
│  │ [View Diff] [Approve] [Deny]               │ ◄── You decide     │
│  └────────────────────────────────────────────┘                    │
│                              │ Approve                              │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ Agent: "I'll run the tests to verify"      │                    │
│  │ [Approve] [Deny] [Edit]                    │ ◄── You decide     │
│  └────────────────────────────────────────────┘                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**When to use Interactive:**
- Learning how Copilot CLI works
- Working with unfamiliar codebases
- Tasks involving sensitive files or credentials
- Debugging issues where you need to observe each step
- When you want to understand the agent's reasoning

#### Plan Mode

Create and review a plan before any execution:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PLAN MODE FLOW                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  You: "Implement user authentication with JWT"                      │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ Agent creates plan:                        │                    │
│  │                                            │                    │
│  │ ## Plan: JWT Authentication                │                    │
│  │                                            │                    │
│  │ 1. Create src/auth/jwt.ts                  │                    │
│  │ 2. Add login endpoint to src/api/routes.ts │                    │
│  │ 3. Create middleware src/auth/middleware.ts│                    │
│  │ 4. Add tests in tests/auth.test.ts         │                    │
│  │ 5. Update .env.example with JWT_SECRET     │                    │
│  │                                            │                    │
│  │ [Approve Plan] [Edit Plan] [Cancel]        │ ◄── You review     │
│  └────────────────────────────────────────────┘                    │
│                              │ Approve                              │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ Agent executes all steps...                │                    │
│  │ ████████████████░░░░░░░░ 60%               │ ◄── Batched        │
│  └────────────────────────────────────────────┘      execution     │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ "Plan complete. 5 files created/modified." │                    │
│  └────────────────────────────────────────────┘                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**When to use Plan:**
- Multi-file features or refactoring
- When you want to review the approach before execution
- Complex tasks where you want a "map" first
- Collaborative work where you want to share the plan
- Tasks where order of operations matters

**Plan mode tips:**
- Edit the plan.md file to adjust before execution
- Add/remove steps as needed
- Agent will follow your modified plan

#### Auto Mode

Minimal confirmations — the agent acts autonomously:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AUTO MODE FLOW                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  You: "Fix all ESLint errors in the project"                        │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ Agent: Scanning for ESLint errors...       │                    │
│  │ Agent: Found 12 errors in 5 files          │                    │
│  │ Agent: Fixing src/utils.ts...              │ ◄── No approval    │
│  │ Agent: Fixing src/api/routes.ts...         │     needed         │
│  │ Agent: Fixing src/components/Button.tsx... │                    │
│  │ Agent: Running eslint --fix...             │                    │
│  │ Agent: Verifying all errors resolved...    │                    │
│  └────────────────────────────────────────────┘                    │
│                              │                                      │
│                              ▼                                      │
│  ┌────────────────────────────────────────────┐                    │
│  │ "Done! Fixed 12 ESLint errors in 5 files." │                    │
│  │                                            │                    │
│  │ You can review changes with /diff          │                    │
│  └────────────────────────────────────────────┘                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**When to use Auto:**
- Routine, well-understood tasks
- Bulk operations (formatting, linting, imports)
- When you trust the codebase and the task
- Time-sensitive work where speed matters
- Tasks with easy rollback (git)

**Auto mode safety tips:**
- Always have uncommitted changes backed up
- Use `git diff` or `/diff` to review after
- Start with Interactive to understand what the agent does
- Keep tasks focused and specific

#### Switching Modes

| Method | Description |
|--------|-------------|
| `Shift+Tab` | Cycle through modes during session |
| Mid-conversation | Switch anytime — takes effect on next action |

#### Mode Selection Guide

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WHICH MODE SHOULD I USE?                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Is this task risky or unfamiliar?                                  │
│       │                                                             │
│       ├── YES ──► Use INTERACTIVE                                   │
│       │                                                             │
│       └── NO                                                        │
│            │                                                        │
│            ▼                                                        │
│  Does it involve multiple files/steps?                              │
│       │                                                             │
│       ├── YES ──► Use PLAN                                          │
│       │                                                             │
│       └── NO                                                        │
│            │                                                        │
│            ▼                                                        │
│  Is it routine and easily reversible?                               │
│       │                                                             │
│       ├── YES ──► Use AUTO                                          │
│       │                                                             │
│       └── NO ───► Use INTERACTIVE                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Prompt Engineering Tips

**Be Specific:**
```
❌ "Fix the bug"
✅ "Fix the null pointer exception in @src/api/users.ts line 45"
```

**Provide Context:**
```
❌ "Add tests"
✅ "Add unit tests for the validateEmail function in @src/utils.ts using Jest"
```

**State Your Goal:**
```
❌ "Change the function"
✅ "Refactor calculateTotal to use reduce instead of a for loop for better readability"
```

**Be Iterative:**
```
1. "Show me @src/auth.ts"
2. "What security issues do you see?"
3. "Fix the SQL injection vulnerability you identified"
```

---

## Practice

### Exercise 1: Command Exploration

1. **Launch Copilot CLI in your practice directory:**
   ```bash
   cd ~/copilot-workshop-practice
   copilot
   ```

2. **Explore help:**
   ```
   /help
   ```

3. **Check your model:**
   ```
   /model
   ```

4. **View context:**
   ```
   /context
   ```

### Exercise 2: File Reference Syntax

1. **Create a project structure:**
   ```
   Create a simple Express.js API project with:
   - src/index.js (main server file)
   - src/routes/users.js (user routes)
   - src/utils/validation.js (helper functions)
   - package.json
   ```

2. **Reference specific files:**
   ```
   Explain what @src/routes/users.js does
   ```

3. **Reference a directory:**
   ```
   What's the structure of @src/
   ```

4. **Run a shell command:**
   ```
   !cat package.json
   ```

### Exercise 3: Mode Switching

1. **Check current mode** (shown in prompt)

2. **Switch to Plan mode:**
   Press `Shift+Tab` until you see `[PLAN]`

3. **Create a plan:**
   ```
   [PLAN] Add authentication middleware to the Express app:
   1. Create auth middleware in src/middleware/auth.js
   2. Add JWT verification
   3. Apply to protected routes
   4. Add tests
   ```

4. **Review the plan** but don't execute yet

5. **Switch back to Interactive:**
   Press `Shift+Tab`

6. **Clear for fresh start:**
   ```
   /clear
   ```

### Exercise 4: Diff and Review

1. **Make some changes:**
   ```
   Add input validation to the user routes - check for valid email and non-empty name
   ```

2. **View the changes:**
   ```
   /diff
   ```

3. **Request a review:**
   ```
   /review
   ```

4. **Ask for improvements:**
   ```
   What could be improved in these changes?
   ```

### Exercise 5: Session Management

1. **Compact conversation history (reduces context usage):**
   ```
   /compact
   ```

2. **View session info:**
   ```
   /session
   ```

3. **Exit the session:**
   ```
   /exit
   ```

4. **Resume later:**
   ```bash
   copilot
   ```
   Then use `/resume` to switch to a previous session.

5. **Verify context was preserved:**
   ```
   What did we do in this session?
   ```

---

## Q&A

### Question 1

Which syntax correctly references a file in Copilot CLI?

A) `#src/main.py`  
B) `@src/main.py`  
C) `$src/main.py`  
D) `file:src/main.py`  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Use `@` prefix to reference files. The `#` is used for GitHub issues/PRs, and `!` is for running shell commands.

</details>

---

### Question 2

What is the keyboard shortcut to switch between Interactive, Plan, and Auto modes?

A) `Ctrl+Tab`  
B) `Alt+M`  
C) `Shift+Tab`  
D) `Ctrl+Shift+M`  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Press `Shift+Tab` to cycle between modes. The current mode is indicated in the prompt.

</details>

---

### Question 3

Which command clears the current context to start fresh?

A) `/reset`  
B) `/new`  
C) `/clear`  
D) `/flush`  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

The `/clear` command clears the current context, which is useful when switching between different tasks in the same session.

</details>

---

### Question 4

How do you run a shell command from within Copilot CLI?

A) `$git status`  
B) `!git status`  
C) `run git status`  
D) `/exec git status`  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Use `!` prefix to run shell commands directly. For example, `!git status`, `!npm test`, or `!ls -la`.

</details>

---

### Question 5

Which mode is best for complex, multi-file changes where you want to review the approach first?

A) Interactive mode  
B) Plan mode  
C) Auto mode  
D) Debug mode  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Plan mode allows you to create and review a plan before execution, which is ideal for complex changes spanning multiple files. You can review and modify the plan before Copilot executes it.

</details>

---

## Next Steps

Continue to [Section 4: MCP & Advanced Features](../04-MCP-Extensibility/README.md) for MCP configuration, skills, and custom agents.
