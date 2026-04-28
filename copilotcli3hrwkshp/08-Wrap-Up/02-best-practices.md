# Best Practices & Common Pitfalls

## Best Practices

### 1. Start Every Session Right

**Set the stage before asking**:
```
I'm working on the payment processing module.
The current issue is that refunds aren't being tracked properly.
Let me show you the relevant files:

@src/payments/RefundService.js
@src/payments/TransactionLogger.js
```

**Why it works**: Gives Copilot the context it needs immediately.

---

### 2. Use Instruction Files

**Repository-level** (`.github/copilot-instructions.md`):
```markdown
# Project Standards

## Technology Stack
- Node.js 20 with TypeScript
- PostgreSQL with Prisma ORM
- Jest for testing

## Code Style
- Use functional components with hooks
- Prefer named exports
- Error messages must be user-friendly

## Security
- Never log sensitive data (passwords, tokens, PII)
- Always validate user input
- Use parameterized queries
```

**Why it works**: Every session automatically gets project context.

---

### 3. Plan Before You Build

For any non-trivial task:

1. **Switch to Plan mode** (`Shift+Tab`)
2. **Describe the feature**
3. **Review the plan**
4. **Adjust before execution**

```
[PLAN] Add user authentication with:
- JWT tokens (access + refresh)
- Secure password hashing
- Rate limiting on login attempts
- Session management
```

**Why it works**: Catches architectural issues before code is written.

---

### 4. Work Incrementally

**Good workflow**:
```
1. Create the data model → Test → Commit
2. Create the service layer → Test → Commit
3. Create the API endpoint → Test → Commit
4. Create the UI component → Test → Commit
```

**Bad workflow**:
```
1. Create everything at once → Hope it works
```

**Why it works**: Smaller changes = easier to debug, review, and revert.

---

### 5. Verify Before Trusting

**Always**:
```
You: Create unit tests for the UserService

Copilot: [Creates tests]

You: Run the tests

Copilot: All 12 tests passing

You: Now let's also test edge cases...
```

**Why it works**: AI makes mistakes; tests catch them.

---

### 6. Keep Context Focused

**Good**:
```
I'm working on the login form validation.
@src/components/LoginForm.tsx
@src/utils/validation.ts
```

**Bad**:
```
@src/
Let me tell you about the entire application architecture...
```

**Why it works**: Focused context = better responses.

---

### 7. Use the Right Mode

| Situation | Mode |
|-----------|------|
| Exploring code | Interactive |
| Quick fix | Interactive |
| New feature | Plan |
| Refactoring | Plan |
| Well-defined task | Autopilot |
| Learning/asking questions | Interactive |

---

### 8. Review Changes Before Committing

```
/diff              # See what changed
/review            # Get AI review
!npm test          # Run tests
!git commit        # Only if clean
```

---

### 9. Use MCP for Integrations

Instead of switching between tools:
```
Show me my assigned ADO work items
→ Work item #1234 looks good
Create a branch for #1234
→ [Creates branch]
When done: Create a PR linking to #1234
→ [Creates PR with work item link]
```

---

### 10. Maintain Session Hygiene

- `/clear` when switching contexts
- `/resume` to continue previous work
- `/compact` if responses slow down

---

## Common Pitfalls

### Pitfall 1: "Make it work" Syndrome

**Problem**: Asking for vague solutions
```
❌ "Fix the bug"
❌ "Make it better"
❌ "Add authentication"
```

**Solution**: Be specific
```
✅ "Fix the null pointer error in @src/api/users.js line 45"
✅ "Refactor this function to reduce cyclomatic complexity"
✅ "Add JWT authentication with 15-minute access tokens"
```

---

### Pitfall 2: Context Overload

**Problem**: Including too much
```
❌ @src/
❌ "Here's all 50 files in my project..."
```

**Solution**: Include only what's needed
```
✅ @src/services/PaymentService.js
✅ @src/models/Payment.js
```

---

### Pitfall 3: Blind Trust

**Problem**: Accepting output without verification
```
You: Generate the database migration
Copilot: [Creates migration]
You: Run it in production  # 😱
```

**Solution**: Always verify
```
You: Generate the database migration
Copilot: [Creates migration]
You: Show me what this migration will do
You: Run it locally first
You: [Review results, then proceed]
```

---

### Pitfall 4: Fighting the Response

**Problem**: Continuing to ask the same thing when it's not working
```
You: Write it differently
You: No, not like that
You: Try again
```

**Solution**: Reframe the request
```
You: Let me clarify. I need:
1. [Specific requirement]
2. [Specific constraint]
3. [Specific format]
```

---

### Pitfall 5: Ignoring Errors

**Problem**: Not reading error messages
```
You: Run the tests
Copilot: Tests failed with error...
You: Fix it
Copilot: [Guesses at fix]
```

**Solution**: Analyze before fixing
```
You: What does this error mean?
You: Show me where in the code this error originates
You: Now that we understand it, fix it
```

---

### Pitfall 6: No Instructions File

**Problem**: Repeating context every session
```
[Every session]
You: We use TypeScript, Jest, PostgreSQL...
```

**Solution**: Create instruction files once
```
# .github/copilot-instructions.md
[Project context lives here forever]
```

---

### Pitfall 7: Wrong Mode for the Task

**Problem**: Using Interactive for complex tasks
```
You: Build the entire user management system
[Copilot starts making changes without plan]
```

**Solution**: Use Plan mode for complex work
```
[PLAN] Build user management with:
- User CRUD operations
- Role-based permissions
- Audit logging
→ Review plan → Then execute
```

---

### Pitfall 8: Skipping the Review

**Problem**: Committing without review
```
You: Make the changes
You: Commit and push
[Bug ships to production]
```

**Solution**: Review before commit
```
/diff
/review
!npm test
[Then commit]
```

---

## Quick Fixes for Common Issues

| Issue | Quick Fix |
|-------|-----------|
| Responses seem off-topic | `/clear` and restart |
| Context too large | `/compact` or `/clear` |
| Not understanding project | Add instruction file |
| MCP not working | Check `/mcp` status |
| Slow responses | Check network, reduce context |
| Tool approval prompts annoying | Trust tool for session |

---

## The Golden Rules

1. **Be specific** - Vague input = vague output
2. **Provide context** - Include relevant files
3. **Verify everything** - AI makes mistakes
4. **Work incrementally** - Small steps win
5. **Use instruction files** - Persistent context
6. **Match mode to task** - Plan for complex work
7. **Review before commit** - Trust but verify

---

Continue to [Resources](./03-resources.md) for further learning.
