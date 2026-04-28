# Tutorial 3.2: Session Management

## Introduction

Effective session management helps you maintain productivity across work sessions. This tutorial covers session persistence, resumption, and efficient workflow patterns.

## Session Basics

### What is a Session?

A session includes:
- Complete conversation history
- Context and file states
- Tool approval history (for current run)
- Actions taken and their results

### Session Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     SESSION LIFECYCLE                            │
│                                                                 │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐    │
│  │  Start  │───►│  Active  │───►│  Paused  │───►│ Resumed │    │
│  └─────────┘    └──────────┘    └──────────┘    └─────────┘    │
│       │              │               │               │          │
│       │              │               │               │          │
│       │              ▼               │               ▼          │
│       │         ┌──────────┐        │          ┌──────────┐    │
│       │         │  /clear  │        │          │ Continue │    │
│       │         └──────────┘        │          │ Working  │    │
│       │              │               │          └──────────┘    │
│       │              ▼               │                          │
│       │         ┌──────────┐        │                          │
│       └────────►│   New    │◄───────┘                          │
│                 │ Session  │                                    │
│                 └──────────┘                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Starting Sessions

### Default Start

```bash
copilot
```
Creates a new session or prompts to resume.

### With Fresh Start

```bash
copilot --new
```
Always starts a new session.

### With Banner

```bash
copilot --banner
```
Shows the animated welcome banner.

### Resume Previous

```bash
copilot --continue
```
Resumes the most recent session immediately.

---

## Session Commands

### Viewing Sessions

```
/session list
```

Output:
```
Recent Sessions
───────────────────────────────────────────────────────────
ID          Started              Project            Turns
───────────────────────────────────────────────────────────
abc123      2024-01-15 14:30    /home/user/myapp   42
def456      2024-01-15 10:15    /home/user/api     15
ghi789      2024-01-14 16:45    /home/user/docs    8
───────────────────────────────────────────────────────────
```

### Resuming a Session

```
/resume
```
Shows a picker to select from recent sessions.

```
/resume abc123
```
Resumes a specific session by ID.

### Renaming Sessions

```
/rename My Authentication Work
```
Gives the session a memorable name.

```
/rename
```
Auto-generates a name from conversation content.

### Clearing (New Session)

```
/clear
```
Abandons current session and starts fresh.

---

## Session Persistence

### What's Automatically Saved

| Saved | Details |
|-------|---------|
| Conversation | All prompts and responses |
| Context | Files read, tools used |
| State | Current working directory |
| Timeline | Actions and their results |

### What's NOT Saved

| Not Saved | Details |
|-----------|---------|
| Tool permissions | Must re-approve in new runs |
| Running processes | Processes stop when CLI exits |
| Temporary files | Cleaned up on exit |

---

## Workflow Patterns

### Pattern 1: Daily Continuation

**Morning:** Resume yesterday's work
```bash
copilot --continue
```

**Throughout Day:** Work on tasks

**End of Day:** Exit normally
```
/exit
```
Session is automatically saved.

### Pattern 2: Task-Based Sessions

```bash
# Start feature work
copilot
/rename Feature: User Authentication

# ... work on feature ...

# Start different task - new session
/clear

# ... work on bug fix ...
/rename Bug: Login Timeout Fix
```

### Pattern 3: Multiple Projects

Terminal 1 (Project A):
```bash
cd ~/project-a
copilot
```

Terminal 2 (Project B):
```bash
cd ~/project-b
copilot
```

Sessions are independent and scoped to directory.

### Pattern 4: Cloud to Local

Start on GitHub.com with Copilot coding agent, then continue locally:

```bash
copilot --resume
```

Select the cloud session to bring it to your local environment.

---

## Context Preservation Techniques

### Technique 1: Checkpoint Important State

When you've reached a good stopping point:
```
Summarize what we've accomplished in this session so far
```

This creates a compressed summary you can reference later.

### Technique 2: Use Session Sharing

Save session to a file for reference:
```
/share
```

Options:
- Markdown file
- HTML file  
- GitHub Gist

### Technique 3: Document in Code

Leave TODOs in code for context:
```
// TODO(copilot-session): Continue implementing auth middleware
// Next steps: Add token refresh logic
```

---

## Session Statistics

### View Usage

```
/usage
```

Output:
```
Session Statistics
───────────────────────────────
Duration:           2h 34m
Turns:              47
Premium Requests:   52
Files Modified:     12
Lines Changed:      +342 / -89
───────────────────────────────
Model Usage:
  Claude Sonnet 4.5: 48 requests
  Claude Opus:       4 requests
───────────────────────────────
```

### Why Track Usage?

- Monitor premium request consumption
- Understand session efficiency
- Track productivity metrics

---

## Exercise: Session Management

### Exercise 3.2.1: Session Workflow

1. Start a new session:
   ```
   copilot
   ```

2. Have a few interactions:
   ```
   What files are in this directory?
   Create a file called session-test.txt with today's date
   ```

3. View session info:
   ```
   /usage
   ```

4. Exit:
   ```
   /exit
   ```

5. Resume:
   ```bash
   copilot --continue
   ```

6. Verify context is preserved:
   ```
   What files did we just work with?
   ```

### Exercise 3.2.2: Session Naming

1. Start a new session

2. Create a meaningful context:
   ```
   Let's work on improving the test coverage for this project
   ```

3. Rename the session:
   ```
   /rename Improving Test Coverage
   ```

4. Exit and list sessions:
   ```
   /exit
   ```
   ```bash
   copilot
   /session list
   ```

5. Verify your named session appears in the list

### Exercise 3.2.3: Multi-Session Workflow

1. Start Session A for one task:
   ```bash
   copilot
   /rename Task A: Documentation
   ```
   Do some work, then:
   ```
   /exit
   ```

2. Start Session B for another task:
   ```bash
   copilot
   /rename Task B: Bug Fix
   ```
   Do some work, then:
   ```
   /exit
   ```

3. List all sessions:
   ```bash
   copilot
   /session list
   ```

4. Resume Session A:
   ```
   /resume
   ```
   Select "Task A: Documentation"

---

## Best Practices

### 1. Name Your Sessions

```
/rename Feature: Dark Mode Implementation
```

Makes it easy to find and resume the right session.

### 2. Regular Compaction for Long Sessions

Every 20-30 turns:
```
/compact
```

Keeps context efficient.

### 3. Clear Start for New Topics

When switching to unrelated work:
```
/clear
```

Avoids context confusion.

### 4. Share Before Major Milestones

```
/share
```

Creates a reference point you can return to.

### 5. Check Usage Periodically

```
/usage
```

Stay aware of premium request consumption.

---

## Key Takeaways

1. **Sessions auto-save**: Your work is preserved automatically
2. **Resume easily**: Use `copilot --continue` for quick return
3. **Name sessions**: `/rename` for easy identification
4. **Manage context**: `/compact` and `/clear` as needed
5. **Track usage**: `/usage` shows consumption
6. **Share progress**: `/share` creates shareable exports

---

## Next Section

Continue to [Section 4: CLI Fundamentals](../04-CLI-Fundamentals/README.md) for core CLI skills.
