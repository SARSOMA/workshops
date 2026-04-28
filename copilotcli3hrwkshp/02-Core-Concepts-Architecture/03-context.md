# Tutorial 2.3: Context Building

## Introduction

Context is everything in AI-assisted development. Understanding how GitHub Copilot CLI builds and manages context helps you craft better prompts and work more efficiently.

## What is Context?

Context includes everything Copilot knows about:
- Your current conversation
- Files you've referenced
- Commands you've run
- Custom instructions loaded
- Project structure
- Previous tool outputs

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTEXT WINDOW                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  System Instructions                                       │  │
│  │  • How to behave                                           │  │
│  │  • Available tools                                         │  │
│  │  • Security constraints                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Custom Instructions                                       │  │
│  │  • ~/.copilot/copilot-instructions.md                      │  │
│  │  • .github/copilot-instructions.md                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Conversation History                                      │  │
│  │  • Your prompts                                            │  │
│  │  • Copilot's responses                                     │  │
│  │  • Tool outputs                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Active File Contents                                      │  │
│  │  • Files referenced with @                                 │  │
│  │  • Files Copilot read during exploration                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Available Space                                           │  │
│  │  [█████████████████████░░░░░░░░░░░░░░░] 68% used           │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Context Window Size

### Understanding Limits

Different models have different context windows:

| Model | Context Window | Effective Working Space |
|-------|----------------|------------------------|
| Claude Sonnet 4.5 | ~200K tokens | ~150K for conversation |
| GPT-5 | ~128K tokens | ~100K for conversation |

> **Note**: System instructions and tool definitions consume part of the context window.

### Checking Usage

View your current context usage:

```
/context
```

Output:
```
Context Window Usage
────────────────────────────────
System prompts:     15,234 tokens (8%)
Instructions:        2,456 tokens (1%)
Conversation:       45,678 tokens (23%)
────────────────────────────────
Total:              63,368 tokens (32%)
Available:         136,632 tokens (68%)
```

---

## How Copilot Builds Context

### 1. Automatic Context Gathering

When you ask a question, Copilot may automatically:

```
Your Prompt: "Fix the authentication bug"
                    ↓
┌─────────────────────────────────────────────────────────────┐
│  Copilot's Context Building                                  │
│                                                             │
│  1. Read relevant files:                                     │
│     • src/auth/login.js                                      │
│     • src/auth/middleware.js                                 │
│     • src/utils/jwt.js                                       │
│                                                             │
│  2. Check project structure:                                 │
│     • List of files in /src                                  │
│     • Package.json dependencies                              │
│                                                             │
│  3. Search for related code:                                 │
│     • Grep for "authentication"                              │
│     • Find usages of auth functions                          │
└─────────────────────────────────────────────────────────────┘
```

### 2. Explicit File References

Use `@` to explicitly include files:

```
Explain @src/auth/login.js and how it connects to @src/db/users.js
```

This ensures specific files are in context.

### 3. Issue/PR References

Use `#` to reference GitHub issues or PRs:

```
Work on #123
Review the changes in #456
```

---

## Context Management Strategies

### Strategy 1: Start Specific

❌ **Too broad:**
```
Fix the bugs in this project
```

✅ **Specific:**
```
Fix the null pointer exception in @src/utils/parser.js line 45
```

### Strategy 2: Reference Files Explicitly

❌ **Relies on discovery:**
```
Update the user model
```

✅ **Explicit reference:**
```
Update @models/User.js to add an email validation field
```

### Strategy 3: Provide Context in Prompts

❌ **Assumes knowledge:**
```
Use the standard pattern
```

✅ **Provides context:**
```
Following our repository pattern in @src/repositories/UserRepository.js, 
create a ProductRepository with the same structure
```

---

## Automatic Context Management

### Auto-Compaction

When context reaches 95% capacity, Copilot automatically:

1. Summarizes older conversation turns
2. Compresses tool outputs
3. Maintains essential context
4. Continues seamlessly

This enables virtually infinite sessions!

### Manual Compaction

Force context compression:

```
/compact
```

Use when:
- Working on a long session
- Switching topics significantly
- Context feels "stale"

### Starting Fresh

Clear all context and start new:

```
/clear
```

Use when:
- Starting a completely new task
- Context is confusing Copilot
- You want a clean slate

---

## Session Persistence

### Session Resumption

Copilot saves session state automatically:

```bash
# Resume last session
copilot --continue

# Resume a specific session
copilot --resume
```

### Session Management

View and manage sessions:

```
/session list        # Show all sessions
/session             # Session management menu
/resume              # Pick a session to resume
```

### What's Preserved

| Saved | Not Saved |
|-------|-----------|
| Conversation history | Approved tool permissions |
| File modifications | Running processes |
| Context state | Temporary files |

---

## Context Optimization Tips

### 1. Use Targeted File References

```
# Good: Specific file
Review @src/api/routes/users.js

# Better: With line range context
The error is around line 45 in @src/api/routes/users.js
```

### 2. Chunk Large Tasks

Instead of:
```
Refactor the entire authentication system
```

Do:
```
1. First, review @src/auth/login.js and suggest improvements
2. [After review] Implement the improvements
3. [After implementation] Update the tests
```

### 3. Summarize Long Outputs

After getting a long response:
```
Summarize the key changes you just made
```

This creates a compressed reference for future prompts.

### 4. Use Conversation Branches

For exploratory work:
```
/ask How would I implement caching here?
```

`/ask` doesn't add to conversation history, keeping context clean.

---

## Exercise: Context Management

### Exercise 2.3.1: Check Context Usage

1. Start a new Copilot CLI session
2. Have a few interactions
3. Check usage: `/context`
4. Note the distribution

### Exercise 2.3.2: Explicit vs. Implicit Context

1. Ask without file reference:
   ```
   How does the authentication work?
   ```
   
2. Watch Copilot explore to find relevant files

3. Now ask with explicit reference:
   ```
   Explain the authentication flow starting from @src/auth/index.js
   ```

4. Compare the response quality and speed

### Exercise 2.3.3: Context Compaction

1. Have a lengthy conversation (10+ turns)
2. Check context: `/context`
3. Run: `/compact`
4. Check context again
5. Verify you can still reference earlier topics

---

## Monitoring Context Health

### Signs of Context Overload

- Slower responses
- Copilot "forgetting" earlier conversation
- Confused or contradictory responses
- Context usage over 90%

### Remediation

1. **Check usage**: `/context`
2. **Compact if needed**: `/compact`
3. **Start fresh for new topics**: `/clear`
4. **Be explicit**: Reference files with `@`

---

## Key Takeaways

1. **Context is limited**: Monitor with `/context`
2. **Be explicit**: Use `@` for file references
3. **Auto-compaction**: Context compresses automatically at 95%
4. **Manual control**: Use `/compact` or `/clear` when needed
5. **Sessions persist**: Use `--continue` to resume
6. **Quality over quantity**: Specific prompts > vague requests

---

## Next Section

Continue to [Section 3: Context Management & Optimization](../03-Context-Management/README.md) for advanced context techniques.
