# Tutorial 1.2: Environment Setup and First Launch

## Introduction

In this hands-on tutorial, you'll launch GitHub Copilot CLI, complete authentication, and explore the basic interface. We'll also cover essential configuration options.

## Prerequisites

- Copilot CLI installed (see [Prerequisites](../00-Prerequisites/README.md))
- GitHub account with Copilot access

---

## Part 1: First Launch

### Step 1: Open Your Terminal

**Windows:**
- Open PowerShell 7 (search for "pwsh" or "PowerShell 7")
- Or use VS Code's integrated terminal

**macOS/Linux:**
- Open Terminal
- Or use VS Code's integrated terminal

### Step 2: Navigate to a Project Directory

Navigate to a directory containing code you want to work with:

```bash
# Example: Navigate to a project
cd ~/projects/my-project

# Or create a test directory for the workshop
mkdir -p ~/copilot-workshop
cd ~/copilot-workshop
```

> ⚠️ **Important**: Never launch Copilot CLI from your home directory (`~` or `C:\Users\YourName`). Always work within a specific project folder.

### Step 3: Launch Copilot CLI

```bash
copilot
```

### Step 4: Trust the Directory

On first launch, you'll see a security prompt:

```
⚠️  During this GitHub Copilot CLI session, Copilot may attempt to 
read, modify, and execute files in and below this folder.

You should only proceed if you trust the files in this location.

1. Yes, proceed
2. Yes, and remember this folder for future sessions
3. No, exit (Esc)
```

For workshop purposes:
- Choose **Option 1** for temporary trust
- Choose **Option 2** for directories you'll use regularly

### Step 5: Authenticate (if needed)

If not already logged in:

```
/login
```

Follow the browser-based authentication flow:
1. A browser window opens
2. Review the permissions
3. Click "Authorize"
4. Return to your terminal

---

## Part 2: Understanding the Interface

### The Welcome Screen

When you launch Copilot CLI with the `--banner` flag, you'll see the animated banner:

```bash
copilot --banner
```

### Interface Elements

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Copilot CLI                    Model: Claude Sonnet │
│  Session: abc123                       Mode: Interactive    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Conversation history appears here]                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  > Your prompt here                                    │
└─────────────────────────────────────────────────────────────┘
```

### Key Interface Features

| Element | Description |
|---------|-------------|
| **Prompt box** | Where you type your requests |
| **Mode indicator** | Shows current mode (Interactive, Plan, Autopilot) |
| **Model name** | Current AI model being used |
| **Timeline** | Shows conversation history and actions taken |

---

## Part 3: Essential Commands

### Slash Commands

Slash commands start with `/` and provide quick access to features:

```
/help           # Show all available commands
/model          # Change AI model
/context        # Show token usage
/clear          # Start a new conversation
/exit           # Exit Copilot CLI
```

### Quick Reference Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle through modes (Interactive → Plan → Autopilot) |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+C` (x2) | Exit the CLI |
| `Ctrl+L` | Clear screen |
| `Ctrl+T` | Toggle reasoning visibility |
| `Esc` | Cancel current input |

### Special Prefixes

```
@filename       # Include a specific file in your prompt
#123            # Reference an issue or PR
!command        # Execute a shell command directly
```

---

## Part 4: Hands-On Exercises

### Exercise 1: Basic Conversation

Try these prompts to get familiar with the interface:

```
What is GitHub Copilot CLI?
```

Wait for the response, then try:

```
What can you help me with?
```

### Exercise 2: File References

Create a test file:
```
!echo "console.log('Hello, Copilot!');" > test.js
```

Then reference it:
```
Explain what @test.js does
```

### Exercise 3: Check Your Environment

```
/env
```

This shows:
- Loaded instruction files
- Configured MCP servers
- Available skills
- Custom agents

### Exercise 4: Explore Help

```
/help
```

Review the available commands and their descriptions.

### Exercise 5: Context Awareness

```
/context
```

This shows your current token usage—important for long conversations.

---

## Part 5: Configuration Overview

### Configuration Directory

GitHub Copilot CLI stores configuration in:

| Platform | Location |
|----------|----------|
| macOS/Linux | `~/.copilot/` |
| Windows | `%USERPROFILE%\.copilot\` |

You can change this by setting the `COPILOT_HOME` environment variable.

### Key Configuration Files

```
~/.copilot/
├── settings.json         # User preferences
├── mcp-config.json       # MCP server configurations
├── copilot-instructions.md  # Global custom instructions
└── agents/               # Custom agent definitions
```

### View Current Settings

```
copilot help config
```

### Essential Settings

Settings are stored in `~/.copilot/settings.json`:

```json
{
  "theme": "dark",
  "model": "claude-sonnet-4-5",
  "experimental": false
}
```

---

## Part 6: Mode Switching

GitHub Copilot CLI has multiple modes:

### Interactive Mode (Default)
Standard conversation mode for asking questions and executing tasks.

### Plan Mode
Collaborative planning before code is written.

Press `Shift+Tab` to enter plan mode:
```
[PLAN] Create a REST API with Express.js for user management
```

In plan mode, Copilot will:
1. Ask clarifying questions
2. Build a structured implementation plan
3. Wait for your approval before coding

### Autopilot Mode (Experimental)
Enable experimental features first:
```
/experimental
```

Then cycle to Autopilot mode with `Shift+Tab`. Copilot will work more autonomously to complete tasks.

---

## Exercise: Full Setup Verification

Complete this checklist to verify your setup:

- [ ] Launch Copilot CLI from a project directory
- [ ] Confirm authentication (your username is visible)
- [ ] Run `/help` to see available commands
- [ ] Run `/model` to see available models
- [ ] Run `/env` to see your environment
- [ ] Run `/context` to see token usage
- [ ] Ask a simple question and get a response
- [ ] Use `@` to reference a file
- [ ] Use `!` to run a shell command
- [ ] Switch to Plan mode with `Shift+Tab`
- [ ] Exit with `/exit`

---

## Common Issues and Solutions

### "copilot: command not found"
```bash
# Check if copilot is in your PATH
which copilot

# Restart terminal or source profile
source ~/.bashrc  # or ~/.zshrc
```

### Authentication Expired
```
/logout
/login
```

### Slow Response Times
- Check your internet connection
- Consider switching to a faster model: `/model`
- Use `/compact` to reduce context size

### Permission Denied Errors
- Ensure you trusted the directory
- Check file permissions in the directory
- Run from a directory you have write access to

---

## Key Takeaways

1. **Always launch from a project directory** - Never from home directory
2. **Trust is scoped** - Copilot only works in trusted directories
3. **Modes matter** - Use Plan mode for complex tasks
4. **Configuration is flexible** - Customize behavior with config files
5. **Help is available** - Use `/help` and `?` for assistance

---

## Next Section

Continue to [Section 2: Core Concepts & Architecture](../02-Core-Concepts-Architecture/README.md) to learn about how Copilot CLI works under the hood.
