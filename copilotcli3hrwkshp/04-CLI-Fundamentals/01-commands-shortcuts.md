# Tutorial 4.1: Commands & Shortcuts

## Introduction

Mastering Copilot CLI commands and shortcuts makes you significantly more productive. This tutorial provides a comprehensive reference with practical examples.

## Slash Command Categories

### Quick Reference Table

| Category | Key Commands |
|----------|--------------|
| Navigation | `/help`, `/exit`, `/clear` |
| Session | `/session`, `/resume`, `/rename` |
| Context | `/context`, `/compact`, `/usage` |
| Tools | `/model`, `/mcp`, `/agent`, `/skills` |
| Code | `/diff`, `/pr`, `/review`, `/lsp` |
| Permissions | `/allow-all`, `/add-dir`, `/list-dirs` |

---

## Navigation Commands

### /help

Show all available commands:
```
/help
```

Get help for a specific command:
```
/help context
```

### /exit

Exit Copilot CLI gracefully:
```
/exit
```

Session is saved automatically.

### /clear

Start a new session (abandons current):
```
/clear
```

### /new

Start a fresh conversation within the same session:
```
/new
```

### /cwd

Change or display working directory:
```
/cwd                     # Show current directory
/cwd /path/to/project    # Change directory
/cd /path/to/project     # Alias for /cwd
```

---

## Session Commands

### /session

View and manage sessions:
```
/session          # Show session menu
/session list     # List recent sessions
```

### /resume

Resume a previous session:
```
/resume           # Show session picker
/resume abc123    # Resume specific session ID
```

### /rename

Give your session a name:
```
/rename My Feature Work
/rename           # Auto-generate name from conversation
```

### /share

Export session content:
```
/share            # Show export options
```

Options:
- Markdown file
- HTML file
- GitHub Gist

---

## Context Management Commands

### /context

View token usage breakdown:
```
/context
```

Output shows distribution of:
- System prompts
- Custom instructions
- Conversation history
- File contents
- Available space

### /compact

Compress conversation history:
```
/compact
```

Use when context is getting full or you're switching topics.

### /usage

View session statistics:
```
/usage
```

Shows:
- Session duration
- Turn count
- Premium requests used
- Files modified
- Model usage breakdown

---

## Tool & Configuration Commands

### /model

View or change AI model:
```
/model            # Show model picker
```

Available models (typical):
- Claude Sonnet 4.5 (default)
- Claude Sonnet 4
- GPT-5
- Claude Opus (higher cost)

### /mcp

Manage MCP servers:
```
/mcp              # Show MCP server status
/mcp add          # Add new MCP server
```

### /agent

View or select custom agents:
```
/agent            # Browse available agents
```

### /skills

Manage skills:
```
/skills           # View and configure skills
```

### /env

Show loaded environment:
```
/env
```

Displays:
- Active instruction files
- Connected MCP servers
- Available agents
- Configured skills
- LSP servers

### /instructions

View active instruction files:
```
/instructions     # List active instructions
```

---

## Code Commands

### /diff

Review changes in current directory:
```
/diff             # Show all changes
```

### /pr

Operate on pull requests for current branch:
```
/pr               # PR operations menu
```

### /review

Run code review agent:
```
/review           # Review current changes
```

### /lsp

Manage language server configuration:
```
/lsp              # LSP server status
```

### /ide

Connect to an IDE workspace:
```
/ide              # IDE connection options
```

---

## Permission Commands

### /allow-all

Enable all permissions for the session:
```
/allow-all
```

Also available as `/yolo`.

> ⚠️ Use with caution—allows all tool execution without prompts.

### /add-dir

Add a trusted directory:
```
/add-dir /path/to/trusted/directory
```

### /list-dirs

Show all trusted directories:
```
/list-dirs
```

### /reset-allowed-tools

Reset tool permissions:
```
/reset-allowed-tools
```

---

## Utility Commands

### /ask

Quick side question (doesn't add to history):
```
/ask What's the best npm package for date formatting?
```

### /copy

Copy last response to clipboard:
```
/copy
```

### /rewind or /undo

Undo last turn and revert file changes:
```
/rewind
/undo             # Alias
```

### /search

Search conversation timeline:
```
/search authentication
```

### /login and /logout

Authentication management:
```
/login            # Start auth flow
/logout           # End current session
```

### /version

Display version information:
```
/version
```

### /update

Check for and install updates:
```
/update
```

### /changelog

View recent changes:
```
/changelog                    # Show changelog
/changelog summarize          # AI summary of changes
```

### /feedback

Submit feedback to GitHub:
```
/feedback
```

---

## Keyboard Shortcuts

### Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle through modes |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+C` (x2) | Exit CLI |
| `Ctrl+D` | Shutdown |
| `Ctrl+L` | Clear screen |
| `Esc` | Cancel current input |

### Navigation Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Go to line start |
| `Ctrl+E` | Go to line end |
| `Meta+←/→` | Move cursor by word |

### Editing Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+H` | Delete previous character |
| `Ctrl+W` | Delete previous word |
| `Ctrl+U` | Delete to line beginning |
| `Ctrl+K` | Delete to line end |
| `Ctrl+G` | Edit prompt in $EDITOR |

### View Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | Toggle reasoning display |
| `Ctrl+O/E` | Expand all timeline |
| `Ctrl+X → O` | Open most recent link |

### Execution Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Run command, preserve input |
| `Enter` | Submit prompt |

---

## Special Prefixes

### @ - File References

Include file contents in your prompt:
```
Explain @src/app.js
Compare @src/old.js with @src/new.js
```

Autocomplete available—start typing path after `@`.

### # - Issue/PR References

Reference GitHub issues or PRs:
```
Work on issue #123
Review changes in #456
Implement the feature described in #789
```

### ! - Shell Commands

Execute shell commands directly:
```
!git status
!npm test
!ls -la
```

Runs without AI processing—direct shell execution.

---

## Exercise: Command Mastery

### Exercise 4.1.1: Navigation Challenge

Complete these tasks using commands:

1. Display help: `______`
2. Check your context usage: `______`
3. List your sessions: `______`
4. Change to your home directory: `______`
5. Show all active instructions: `______`

<details>
<summary>Answers</summary>

1. `/help`
2. `/context`
3. `/session list`
4. `/cwd ~` or `/cd ~`
5. `/instructions`

</details>

### Exercise 4.1.2: Keyboard Efficiency

Practice these shortcuts (in Copilot CLI):

1. Type a long prompt, then clear it: `______`
2. Cancel a running operation: `______`
3. Switch to Plan mode: `______`
4. Clear the screen: `______`
5. Show/hide reasoning: `______`

<details>
<summary>Answers</summary>

1. `Ctrl+U` (clear to beginning)
2. `Ctrl+C`
3. `Shift+Tab`
4. `Ctrl+L`
5. `Ctrl+T`

</details>

### Exercise 4.1.3: Special Prefixes

1. List files in current directory without AI:
   ```
   !_______
   ```

2. Ask about a specific file:
   ```
   Explain @_______
   ```

3. Work on a GitHub issue:
   ```
   Start working on #_______
   ```

---

## Command Cheat Sheet

```
┌─────────────────────────────────────────────────────────────────┐
│                    COPILOT CLI CHEAT SHEET                      │
├─────────────────────────────────────────────────────────────────┤
│  MODES                                                          │
│  Shift+Tab        Cycle: Interactive → Plan → Autopilot         │
├─────────────────────────────────────────────────────────────────┤
│  QUICK ACTIONS                                                  │
│  /help            Show all commands                             │
│  /context         Token usage                                   │
│  /compact         Compress history                              │
│  /clear           New session                                   │
│  /exit            Exit CLI                                      │
├─────────────────────────────────────────────────────────────────┤
│  FILE & CODE                                                    │
│  @file            Include file                                  │
│  !command         Run shell                                     │
│  /diff            Show changes                                  │
│  /review          Code review                                   │
├─────────────────────────────────────────────────────────────────┤
│  SESSIONS                                                       │
│  /session         Session menu                                  │
│  /resume          Resume session                                │
│  /rename          Name session                                  │
├─────────────────────────────────────────────────────────────────┤
│  SHORTCUTS                                                      │
│  Ctrl+C           Cancel                                        │
│  Ctrl+L           Clear screen                                  │
│  Ctrl+T           Toggle reasoning                              │
│  Esc              Cancel input                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Next Tutorial

Continue to [Tutorial 4.2: Modes & Interaction](./02-modes-interaction.md) to learn about different working modes.
