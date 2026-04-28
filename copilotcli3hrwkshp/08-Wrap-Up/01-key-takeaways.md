# Key Takeaways

## The Big Picture

### 1. Copilot CLI = Terminal-Native AI Partner

Copilot CLI is not just a chatbot—it's an **agentic coding assistant** that can:
- Read and write files
- Run commands and interpret output
- Create branches, commits, and PRs
- Interact with external services via MCP

**Key insight**: Think of it as a junior developer sitting next to you who can actually make changes.

---

## Core Concepts to Remember

### 2. Context is Everything

**The Rule**: Copilot only knows what's in its context window.

**What this means**:
- Explicitly include files with `@filename`
- Front-load important information
- Use instructions files for persistent context
- Clear context with `/clear` when switching tasks

### 3. Configuration Hierarchy

```
Command Line > Environment > Repository > User > Organization
```

**Tip**: Put team standards in repo-level `.github/copilot-instructions.md`.

### 4. Three Modes, Three Purposes

| Mode | When to Use |
|------|-------------|
| **Interactive** | Exploration, quick tasks, conversations |
| **Plan** | Complex features, multi-step work, review before action |
| **Autopilot** | Well-defined tasks you want automated |

**Switch with**: `Shift+Tab`

### 5. Session Management

- Sessions persist; resume with `/resume` or `copilot --continue`
- Auto-compaction happens at 95% capacity
- Use `/context` to see what's loaded

---

## Practical Skills

### 6. Effective Prompting

**DO**:
```
Create a UserService class that:
- Has CRUD methods for users
- Uses MongoDB via Mongoose
- Includes input validation with Joi
- Throws typed errors for each failure case
```

**DON'T**:
```
Make a user service
```

### 7. File and Reference Syntax

| Syntax | Meaning |
|--------|---------|
| `@filename` | Include file in context |
| `#123` | Reference issue or PR |
| `!command` | Run shell command |
| `/slash` | Built-in command |

### 8. Review Your Changes

Before committing:
1. `/diff` - See what changed
2. `/review` - Get AI code review
3. Run tests - Verify nothing broke

### 9. MCP for Extensibility

- GitHub MCP is built-in
- Add Azure DevOps, databases, custom tools
- Configure in `~/.copilot/mcp-config.json`

---

## Mental Models

### 10. The Agentic Loop

```
You ask → Copilot reasons → Copilot uses tools → 
Results returned → Copilot reasons → Repeats or responds
```

**You control the loop**: Approve tool usage, provide feedback, redirect.

### 11. Trust but Verify

- AI makes mistakes
- Always review generated code
- Run tests before committing
- Use `/review` for a second opinion

### 12. Incremental Over Ambitious

**Better**: Small, verifiable steps
**Risky**: Large changes all at once

```
// Good workflow:
1. Implement one function
2. Test it
3. Commit
4. Repeat
```

---

## What's Different from IDE Copilot?

| IDE Copilot | Copilot CLI |
|-------------|-------------|
| Code completion | Full conversation |
| Single file context | Multi-file operations |
| Inline suggestions | Can run commands |
| Passive | Agentic |
| IDE-bound | Terminal-based |

**Use both**: IDE for typing, CLI for complex tasks.

---

## Common Pitfalls to Avoid

### 1. Overloading Context
Don't include every file. Be selective.

### 2. Vague Prompts
Specific requests get specific results.

### 3. Not Verifying
Always test before committing.

### 4. Ignoring Instruction Files
Put persistent context in instruction files, not prompts.

### 5. Fighting the Tool
If it's not working, try a different approach.

---

## Quick Reference Card

```
# Essential Commands
copilot                    # Start session
Shift+Tab                  # Switch modes
/clear                     # Clear context
/context                   # Show loaded context
/diff                      # Show changes
/review                    # Code review
/mcp                       # MCP servers
Ctrl+C                     # Cancel current action
/exit                      # End session

# File Inclusion
@src/file.js               # Include specific file
@src/                      # Include directory info
@package.json              # Include config file

# Common Patterns
"Fix @filename issue"      # Targeted fix
"Create tests for @file"   # Generate tests
"Review my changes"        # Pre-commit review
"Create a PR for this"     # PR workflow
```

---

## Next Steps

After this workshop:
1. **Practice daily**: Use Copilot CLI for real tasks
2. **Create instructions**: Set up repo-level instructions
3. **Build muscle memory**: Learn the shortcuts
4. **Explore MCP**: Add tools you need
5. **Share learnings**: Help teammates adopt

---

Continue to [Best Practices](./02-best-practices.md) for patterns that lead to success.
