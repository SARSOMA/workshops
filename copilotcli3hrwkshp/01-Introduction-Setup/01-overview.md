# Tutorial 1.1: Overview of GitHub Copilot CLI

## Introduction

GitHub Copilot CLI brings AI-powered coding assistance directly to your command line. It's not just another chatbot—it's an **agentic AI assistant** that can understand your code, execute commands, modify files, and interact with GitHub on your behalf.

## What is GitHub Copilot CLI?

GitHub Copilot CLI is a terminal-native development tool that:

- **Understands context**: Reads and comprehends your codebase
- **Takes action**: Can modify files, run commands, and interact with GitHub
- **Learns from you**: Supports custom instructions and configuration
- **Integrates deeply**: Works with your existing Git and GitHub workflow

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Terminal-native** | Work directly in your command line—no context switching |
| **Agentic** | Plans and executes complex multi-step tasks |
| **GitHub integration** | Access repos, issues, and PRs using natural language |
| **Secure by default** | Nothing happens without your explicit approval |
| **Extensible** | Add MCP servers to connect external tools and data |

## Copilot CLI vs Other Copilot Experiences

Understanding where Copilot CLI fits in the GitHub Copilot ecosystem:

| Feature | Copilot in IDE | Copilot CLI | Copilot in GitHub.com |
|---------|---------------|-------------|----------------------|
| Primary Interface | Code editor | Terminal | Web browser |
| Main Use Case | Code completion | Full task automation | PR reviews, issue triage |
| Context Source | Open files | Entire directory tree | Repository content |
| Can Execute Commands | Limited | ✅ Full shell access | ❌ No |
| Can Modify Files | Via suggestions | ✅ Direct file operations | Via Copilot Workspace |
| GitHub API Access | Limited | ✅ Full access | ✅ Native |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Copilot CLI                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Your       │  │  AI Model    │  │   GitHub     │       │
│  │   Terminal   │◄─►│  (Claude/    │◄─►│   API       │       │
│  │              │  │   GPT)       │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                │                  │               │
│         ▼                ▼                  ▼               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Tool Execution Layer                     │  │
│  │  • File Operations  • Shell Commands  • Git Actions   │  │
│  │  • MCP Servers      • Custom Skills   • GitHub MCP    │  │
│  └──────────────────────────────────────────────────────┘  │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Your Local Environment                    │  │
│  │  • Source Code  • Configuration  • Build Tools         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Use Cases

### 1. Local Development Tasks

```
"Change the background-color of H1 headings to dark blue"
"Suggest improvements to content.js"
"Commit the changes to this repo"
```

### 2. GitHub Interactions

```
"List my open PRs"
"Create a pull request to add this file"
"Merge all open PRs I've created in owner/repo"
```

### 3. Code Understanding

```
"Show me the last 5 changes made to CHANGELOG.md"
"Explain how the authentication flow works in this project"
"Find any security issues in the API routes"
```

### 4. Building Applications

```
"Create a Next.js app with Tailwind CSS that displays GitHub API data"
"Add unit tests for the user service"
"Refactor this function to use async/await"
```

## Security Model

GitHub Copilot CLI is designed with security as a first principle:

### 1. Trusted Directories
- You must explicitly trust the directory where you launch Copilot CLI
- Copilot can only work with files in trusted directories
- Never launch from your home directory or untrusted locations

### 2. Tool Approval
When Copilot needs to modify files or run commands, it asks for permission:

```
Copilot wants to run: npm install express

1. Yes
2. Yes, and approve npm for the rest of this session
3. No, and tell Copilot what to do differently (Esc)
```

### 3. Review Before Execution
- Every action can be reviewed before execution
- You maintain full control over what happens
- Nothing runs without your explicit approval (unless you enable auto-approve)

## Default AI Model

- **Default**: Claude Sonnet 4.5
- **Other options**: Claude Sonnet 4, GPT-5, and more
- Use `/model` command to switch models
- Each prompt uses your premium request quota

---

## Exercise 1.1: Knowledge Check

Before moving on, make sure you can answer these questions:

1. What makes Copilot CLI different from Copilot in your IDE?
2. What does "agentic" mean in the context of Copilot CLI?
3. Why should you never launch Copilot CLI from your home directory?
4. What happens when Copilot wants to modify a file?

<details>
<summary>Click to reveal answers</summary>

1. **Difference from IDE Copilot**: CLI has full shell access, can execute commands, modify files directly, and has deep GitHub integration. IDE Copilot focuses on inline code completion.

2. **Agentic**: Copilot CLI can plan and execute multi-step tasks autonomously, making decisions about which tools to use and how to accomplish goals, rather than just responding to single queries.

3. **Not home directory**: The home directory typically contains sensitive configuration files, credentials, and a broad range of files. Limiting Copilot's scope to project directories reduces risk.

4. **File modification approval**: Copilot will ask for explicit permission before modifying any file, showing you what it wants to do and giving you the option to approve, deny, or suggest an alternative approach.

</details>

---

## Next Steps

Continue to [Tutorial 1.2: Environment Setup](./02-setup.md) to launch Copilot CLI and explore the interface.
