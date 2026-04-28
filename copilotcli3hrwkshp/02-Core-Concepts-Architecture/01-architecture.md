# Tutorial 2.1: Architecture & Interaction Model

## Introduction

Understanding how GitHub Copilot CLI works under the hood helps you craft better prompts, troubleshoot issues, and leverage its full capabilities.

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         Your Terminal                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    GitHub Copilot CLI                        │   │
│  │                                                              │   │
│  │   ┌──────────────┐    ┌───────────────┐    ┌─────────────┐  │   │
│  │   │   Input      │───►│  Orchestrator │◄──►│  AI Model   │  │   │
│  │   │   Handler    │    │               │    │  (Claude/   │  │   │
│  │   └──────────────┘    └───────────────┘    │   GPT)      │  │   │
│  │                              │              └─────────────┘  │   │
│  │                              ▼                               │   │
│  │   ┌──────────────────────────────────────────────────────┐  │   │
│  │   │                  Tool Layer                           │  │   │
│  │   │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────────┐ │  │   │
│  │   │  │ File   │ │ Shell  │ │ Git    │ │ MCP Servers    │ │  │   │
│  │   │  │ System │ │ Exec   │ │ Ops    │ │ (GitHub, etc.) │ │  │   │
│  │   │  └────────┘ └────────┘ └────────┘ └────────────────┘ │  │   │
│  │   └──────────────────────────────────────────────────────┘  │   │
│  │                              │                               │   │
│  └──────────────────────────────│───────────────────────────────┘   │
│                                 ▼                                   │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Your Project Files                           │ │
│  │        /src  /tests  /config  package.json  README.md           │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Input Handler

The input handler processes:
- **Text prompts**: Natural language requests
- **Slash commands**: `/help`, `/model`, `/context`, etc.
- **Special prefixes**: `@files`, `#issues`, `!shell commands`
- **Keyboard shortcuts**: `Ctrl+C`, `Shift+Tab`, etc.

### 2. Orchestrator

The brain of Copilot CLI:
- Manages conversation state
- Decides which tools to invoke
- Handles multi-step task planning
- Manages context window
- Coordinates sub-agents

### 3. AI Model Layer

Communicates with the underlying AI model:

| Model | Use Case | Premium Multiplier |
|-------|----------|-------------------|
| Claude Sonnet 4.5 | Default, balanced | 1x |
| Claude Sonnet 4 | Faster responses | 1x |
| GPT-5 | Alternative reasoning | 1x |
| Claude Opus | Complex tasks | Higher |

### 4. Tool Layer

Provides capabilities to the AI:

| Tool Category | Examples |
|--------------|----------|
| **File Operations** | Read, write, create, delete files |
| **Shell Execution** | Run any shell command |
| **Git Operations** | Commit, branch, diff, log |
| **GitHub API** | PRs, issues, repos, actions |
| **MCP Servers** | Custom integrations |

---

## The Agentic Loop

When you submit a prompt, Copilot CLI follows this loop:

```
┌─────────────────────────────────────────────────────────┐
│                     1. UNDERSTAND                        │
│   Parse prompt → Gather context → Identify intent        │
└─────────────────────────────┬───────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│                     2. PLAN                              │
│   Break into steps → Identify tools needed               │
└─────────────────────────────┬───────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│                     3. EXECUTE                           │
│   Run tools → Get results → Handle errors                │
└─────────────────────────────┬───────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────┐
│                     4. EVALUATE                          │
│   Check outcome → Determine if complete → Report         │
└─────────────────────────────┬───────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
      [Task Complete]                    [Continue Loop]
```

### Example: "Fix the bug in auth.js"

1. **Understand**: Read auth.js, identify the bug
2. **Plan**: Determine the fix, plan the changes
3. **Execute**: Modify the file (with your approval)
4. **Evaluate**: Verify the change, offer to test

---

## Tool Execution Model

### Permission System

When Copilot needs to execute a potentially impactful tool:

```
┌─────────────────────────────────────────────────────────┐
│  Copilot wants to run: npm test                          │
│                                                         │
│  1. Yes                                                 │
│  2. Yes, and approve npm for the rest of this session   │
│  3. No, and tell Copilot what to do differently (Esc)   │
└─────────────────────────────────────────────────────────┘
```

### Tool Categories

| Category | Permission Required | Examples |
|----------|-------------------|----------|
| **Read** | No | View file contents, list directory |
| **Write** | Yes (first time) | Create file, edit file |
| **Execute** | Yes (first time) | Run npm, python, etc. |
| **Delete** | Yes (each time) | Remove files |
| **Network** | Depends on tool | API calls via MCP |

### Safe Tools

Some tools are always allowed:
- Reading file contents
- Viewing directory structure
- Searching code
- Getting Git status

---

## Sub-Agent Architecture

Copilot CLI can delegate tasks to specialized sub-agents:

```
┌─────────────────────────────────────────────────────────┐
│                    Main Agent                            │
│                         │                               │
│        ┌───────────────┼───────────────┐               │
│        ▼               ▼               ▼               │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐           │
│  │ Explore  │   │  Task    │   │  Code    │           │
│  │  Agent   │   │  Agent   │   │  Review  │           │
│  └──────────┘   └──────────┘   └──────────┘           │
│       │               │               │                │
│       ▼               ▼               ▼                │
│   Research       Build/Test      Analyze              │
│   Codebase       Execute         Changes              │
└─────────────────────────────────────────────────────────┘
```

### Default Sub-Agents

| Agent | Purpose | When Used |
|-------|---------|-----------|
| **Explore** | Quick codebase analysis | "Find where X is defined" |
| **Task** | Run commands | "Run the tests" |
| **General-purpose** | Complex tasks | Multi-step implementations |
| **Code-review** | Analyze changes | "Review my changes" |

---

## Communication with GitHub

### GitHub MCP Server

Copilot CLI includes the GitHub MCP server by default:

```
┌─────────────────────────────────────────────────────────┐
│                    Copilot CLI                           │
│                         │                               │
│                         ▼                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │              GitHub MCP Server                     │  │
│  │                                                    │  │
│  │  • Repository Operations                           │  │
│  │  • Pull Request Management                         │  │
│  │  • Issue Tracking                                  │  │
│  │  • GitHub Actions                                  │  │
│  │  • Code Search                                     │  │
│  └───────────────────────────────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│               GitHub.com API                            │
└─────────────────────────────────────────────────────────┘
```

### Available GitHub Operations

```
List my repositories
Create a pull request
Merge PR #123
Close issue #456
List workflow runs
Search code for "authentication"
```

---

## Exercise: Explore the Architecture

### Exercise 2.1.1: Watch the Tool Execution

1. Launch Copilot CLI in a project directory
2. Enable reasoning visibility: Press `Ctrl+T`
3. Ask: "List all JavaScript files in this directory"
4. Watch the reasoning and tool calls
5. Note which tools are used

### Exercise 2.1.2: Experience Sub-Agents

1. Ask: "Explain the structure of this project"
2. Watch if Copilot delegates to the Explore agent
3. Ask: "Run any tests in this project"
4. Watch if Copilot uses the Task agent

### Exercise 2.1.3: Examine Tool Permissions

1. Create a new file request: "Create a file called hello.txt with 'Hello World'"
2. Note the permission prompt
3. Approve with option 1 (one-time)
4. Try creating another file
5. Note you're prompted again

---

## Key Takeaways

1. **Agentic Loop**: Copilot thinks, plans, executes, and evaluates in a loop
2. **Tool-Based**: Capabilities come from tools that can be allowed/denied
3. **Sub-Agents**: Complex tasks may be delegated to specialized agents
4. **GitHub Integration**: The GitHub MCP server is built-in
5. **Transparent**: You can watch reasoning with `Ctrl+T`

---

## Next Tutorial

Continue to [Tutorial 2.2: Configuration Layers](./02-configuration.md) to learn how to customize Copilot CLI's behavior.
