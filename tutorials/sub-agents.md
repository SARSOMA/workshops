# GitHub Copilot CLI: Sub-Agents Tutorial

A practical guide to understanding, configuring, and using sub-agents in GitHub Copilot CLI.

---

## Table of Contents

1. [What Are Sub-Agents?](#1-what-are-sub-agents)
2. [Architecture: How the Main Agent Calls Sub-Agents](#2-architecture-how-the-main-agent-calls-sub-agents)
3. [Built-in Agent Types](#3-built-in-agent-types)
4. [Defining Custom Agents](#4-defining-custom-agents)
5. [User-Level vs Repo-Level Configuration](#5-user-level-vs-repo-level-configuration)
6. [Comparison: Built-in `code-review` vs Custom `codereviewer`](#6-comparison-built-in-code-review-vs-custom-codereviewer)
7. [The MCP Problem: Why Sub-Agents Can't Access Your MCP Servers](#7-the-mcp-problem-why-sub-agents-cant-access-your-mcp-servers)
8. [Workarounds: Getting MCP-Like Access in Sub-Agents](#8-workarounds-getting-mcp-like-access-in-sub-agents)
9. [Execution Modes: Sync vs Background](#9-execution-modes-sync-vs-background)
10. [Practical Examples](#10-practical-examples)
11. [Best Practices](#11-best-practices)

---

## 1. What Are Sub-Agents?

Sub-agents are **specialized AI agents** that the main Copilot CLI agent can spawn to handle specific tasks. Think of them as team members the main agent can delegate work to.

Each sub-agent runs in its own **isolated context window** — a separate conversation with its own set of tools, system prompt, and model. The main agent sends a prompt, the sub-agent does the work, and returns results.

```
You (user)
  └── Main Agent (Copilot CLI)
        ├── Sub-agent: explore (research task)
        ├── Sub-agent: code-review (review changes)
        ├── Sub-agent: codereviewer (your custom agent)
        └── Sub-agent: task (run tests)
```

### Key Characteristics

- **Stateless**: Each invocation starts fresh — no memory of previous calls
- **Isolated**: Runs in a separate context window from the main agent
- **Disposable**: Created for a task, destroyed when done
- **Parallel-capable**: Multiple sub-agents can run simultaneously

---

## 2. Architecture: How the Main Agent Calls Sub-Agents

### The `task` Tool

The main agent uses an internal tool called `task` to launch sub-agents. Here's what happens under the hood:

```
┌──────────────────────────────────────────────────────────┐
│  MAIN AGENT CONTEXT                                      │
│                                                          │
│  Tools available:                                        │
│  ├── Built-in: bash, grep, glob, view, edit, create      │
│  ├── GitHub MCP Server (ships by default)                │
│  ├── Azure DevOps MCP Server (user-configured)           │
│  ├── Azure MCP Server (user-configured)                  │
│  ├── Bluebird MCP Server (user-configured)               │
│  └── task (launches sub-agents)                          │
│                                                          │
│  task(agent_type="code-review", prompt="Review PR...")    │
│         │                                                │
│         ▼                                                │
│  ┌────────────────────────────────────────────────────┐   │
│  │  SUB-AGENT CONTEXT (separate process)              │   │
│  │                                                    │   │
│  │  Tools available:                                  │   │
│  │  ├── Built-in: bash, grep, glob, view, edit        │   │
│  │  ├── GitHub MCP Server (ships by default)          │   │
│  │  ╳── Azure DevOps MCP ← NOT AVAILABLE             │   │
│  │  ╳── Azure MCP ← NOT AVAILABLE                    │   │
│  │  ╳── Bluebird MCP ← NOT AVAILABLE                 │   │
│  │                                                    │   │
│  │  [does work, returns results]                      │   │
│  └────────────────────────────────────────────────────┘   │
│         │                                                │
│         ▼                                                │
│  Main agent receives results and continues               │
└──────────────────────────────────────────────────────────┘
```

### What Gets Inherited

| Resource | Inherited by Sub-Agent? | Notes |
|----------|------------------------|-------|
| Built-in CLI tools | ✅ Yes | bash, grep, glob, view, edit, create |
| GitHub MCP Server | ✅ Yes | Ships with Copilot CLI by default |
| User-configured MCP Servers | ❌ No | Azure DevOps, Azure, Bluebird, etc. |
| Environment variables | ✅ Yes | Available via bash tool |
| File system access | ✅ Yes | Same filesystem, same permissions |
| Git repos | ✅ Yes | Can use git commands via bash |
| Conversation history | ❌ No | Sub-agent starts with only the prompt |
| Session state | ❌ No | No access to parent's SQL DB or session |

---

## 3. Built-in Agent Types

Copilot CLI ships with these built-in agent types:

### `explore`

- **Purpose**: Fast codebase exploration and research
- **Model**: Haiku (fast/cheap)
- **Tools**: grep, glob, view, bash
- **Best for**: Searching code, understanding architecture, parallel research threads
- **Limitation**: Lightweight model — not ideal for complex reasoning

### `task`

- **Purpose**: Running commands with verbose output (tests, builds, lints)
- **Model**: Haiku (fast/cheap)
- **Tools**: All CLI tools
- **Best for**: Build/test execution where you only need pass/fail status
- **Behavior**: Returns brief summary on success, full output on failure

### `general-purpose`

- **Purpose**: Full-capability agent for complex multi-step work
- **Model**: Sonnet (standard)
- **Tools**: All CLI tools
- **Best for**: Complex tasks requiring reasoning + tool use
- **Note**: Runs in subprocess — keeps main conversation clean

### `code-review`

- **Purpose**: Reviewing code changes with high signal-to-noise ratio
- **Model**: Sonnet (standard)
- **Tools**: All CLI tools for investigation
- **Best for**: Local git diffs, staged changes, branch comparisons, GitHub PRs
- **Limitation**: Will NOT modify code — read-only analysis
- **Limitation**: No access to external APIs (Azure DevOps, Jira, etc.)

### `research`

- **Purpose**: Deep research using GitHub search and web sources
- **Model**: Varies
- **Tools**: GitHub search, web fetch, file tools
- **Best for**: Investigating libraries, finding examples, verifying claims

### Summary Table

| Agent | Model | Speed | Capability | Use Case |
|-------|-------|-------|-----------|----------|
| `explore` | Haiku | ⚡ Fast | Research only | Code search, reading files |
| `task` | Haiku | ⚡ Fast | Execute commands | Tests, builds, linting |
| `general-purpose` | Sonnet | 🔄 Medium | Full toolset | Complex multi-step tasks |
| `code-review` | Sonnet | 🔄 Medium | Read-only analysis | Git diffs, PR reviews |
| `research` | Varies | 🐢 Slower | Web + GitHub search | Deep investigation |

---

## 4. Defining Custom Agents

Custom agents let you create specialized sub-agents tailored to your workflows.

### Agent Definition File

Custom agents are defined as Markdown files with YAML frontmatter. The file must be named
with the pattern `<name>.agent.md`.

#### Example: `codereviewer.agent.md`

```markdown
---
description: Reviews Azure DevOps pull requests for code quality, bugs, and best practices
tools: ['azure-devops/*', 'search', 'read']
model: Claude Opus 4.7 (copilot)
---

# ADO Code Reviewer

You are a senior engineer performing code reviews on Azure DevOps pull requests.

## Workflow

1. When given an ADO pull request URL, use the azure-devops tools to fetch the PR details
2. Review each changed file for issues
3. Provide your review in the format below

## What to Check

- Logic errors and potential bugs
- Security issues (hardcoded secrets, injection, missing validation)
- Performance concerns (unnecessary loops, missing indexes, N+1 queries)
- Missing error handling

## Response Format

For each file with findings:

### `<filename>`

- 🔴 **Critical** — must fix before merge
- 🟡 **Warning** — should address
- 🟢 **Suggestion** — nice to have

End with a brief summary: approve, request changes, or needs discussion.
```

### Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Short description shown in agent listings |
| `tools` | array | Tool patterns the agent can use (e.g., `['azure-devops/*']`) |
| `model` | string | AI model to use (e.g., `Claude Opus 4.7 (copilot)`) |

### Browsing Available Agents

Use the `/agent` command in Copilot CLI to browse and select from available agents.

---

## 5. User-Level vs Repo-Level Configuration

Agents (and instructions) can be configured at two levels:

### User-Level (Local to Your Devbox)

**Location**: `~/.copilot/agents/<name>.agent.md`

```
~/.copilot/
├── agents/
│   ├── codereviewer.agent.md     # Available in ALL sessions
│   └── deployment-helper.agent.md
├── mcp-config.json               # MCP servers for main agent
├── copilot-instructions.md       # Global custom instructions
└── config.json                   # CLI settings
```

**Characteristics**:
- Available in **every** Copilot CLI session on this machine
- Personal to you — not shared with the team
- Ideal for: personal workflows, org-specific tools, devbox-specific integrations

### Repo-Level (Shared with the Team)

**Location**: `.github/` directory in your git repository

```
your-repo/
├── .github/
│   ├── agents/
│   │   └── codereviewer.agent.md  # Available when working in this repo
│   ├── copilot-instructions.md    # Repo-specific instructions
│   └── instructions/
│       └── *.instructions.md      # Additional instruction files
├── AGENTS.md                      # Repo-level agent instructions
└── src/
```

**Characteristics**:
- Available only when Copilot CLI is launched **within this repo**
- Committed to git — **shared with the entire team**
- Ideal for: project-specific review standards, team coding conventions, shared workflows

### Comparison

| Aspect | User-Level (`~/.copilot/`) | Repo-Level (`.github/`) |
|--------|---------------------------|------------------------|
| Scope | All sessions on this machine | Only this repository |
| Sharing | Personal, not in git | Committed, shared with team |
| Persistence | Survives repo changes | Lives with the codebase |
| Use case | Personal tools & preferences | Team standards & workflows |
| MCP config | `~/.copilot/mcp-config.json` | `.github/mcp.json` (if supported) |

### Impact on Sub-Agents

Whether an agent is defined at user-level or repo-level **does not change its runtime behavior**. The same isolation rules apply:

- Sub-agents still run in isolated contexts
- Sub-agents still **do not inherit** user-configured MCP servers
- Sub-agents still get the same built-in tools regardless of where they're defined

The only difference is **visibility** — where and when the agent definition is available to be invoked.

### Instructions Hierarchy

Copilot CLI loads instructions from multiple locations (in order):

```
CLAUDE.md / GEMINI.md / AGENTS.md    (in git root & cwd)
.github/instructions/**/*.instructions.md
.github/copilot-instructions.md
$HOME/.copilot/copilot-instructions.md
COPILOT_CUSTOM_INSTRUCTIONS_DIRS     (env var for additional dirs)
```

These instructions affect the **main agent's** behavior, not sub-agents. Sub-agents only receive the prompt you send them.

---

## 6. Comparison: Built-in `code-review` vs Custom `codereviewer`

Here's a detailed comparison based on real-world usage:

| Aspect | `code-review` (Built-in) | `codereviewer` (Custom) |
|--------|--------------------------|------------------------|
| **Origin** | Ships with Copilot CLI | User-defined in `~/.copilot/agents/` |
| **Model** | Sonnet (standard) | Claude Opus 4.7 (as configured) |
| **Invocation** | `task(agent_type="code-review")` | `task(agent_type="codereviewer")` |
| **Designed for** | Local git diffs, GitHub PRs | Azure DevOps PRs |
| **PR sources** | ✅ Local git, ✅ GitHub | ❌ Cannot reach ADO APIs (see §7) |
| **Tools available** | CLI tools (bash, git, grep, etc.) | CLI tools + declared `azure-devops/*` |
| **Will modify code?** | ❌ Never | ❌ As configured, review-only |
| **Review style** | High signal-to-noise, no style nits | Structured (🔴🟡🟢), acknowledges good code |
| **Customizable?** | ❌ No | ✅ Full control over prompt & behavior |
| **MCP access** | ❌ No custom MCPs | ❌ Declares tools but can't connect (see §7) |

### The Core Problem

The `codereviewer` agent **declares** `tools: ['azure-devops/*']` in its frontmatter, which
signals _intent_ to use Azure DevOps tools. However, the MCP server connections that provide
those tools are established at the **main session level** and are **not propagated** to
sub-agent processes.

This means: **the tool declaration is currently aspirational, not functional.**

---

## 7. The MCP Problem: Why Sub-Agents Can't Access Your MCP Servers

### How MCP Servers Work

MCP (Model Context Protocol) servers extend Copilot CLI with external capabilities. Your
configuration at `~/.copilot/mcp-config.json` might look like:

```json
{
  "mcpServers": {
    "azure-devops": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "msazure", "--authentication", "azcli"],
      "tools": ["*"]
    },
    "azure-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"],
      "tools": ["*"]
    }
  }
}
```

### The Isolation Problem

When the main agent starts, it:
1. Reads `~/.copilot/mcp-config.json`
2. Spawns MCP server processes (e.g., `npx @azure-devops/mcp ...`)
3. Establishes stdio/HTTP connections to each server
4. Registers the tools from each server in its tool inventory

When a sub-agent is launched:
1. A **new, separate** context window is created
2. Only **built-in tools** and the **GitHub MCP server** are available
3. The parent's MCP connections are **not shared or duplicated**
4. The sub-agent has **no way to reach** Azure DevOps, Azure, Bluebird, etc.

```
Main Agent Process
├── MCP Connection: azure-devops  ──→  npx @azure-devops/mcp (PID 1234)
├── MCP Connection: azure-mcp     ──→  npx @azure/mcp (PID 1235)
├── MCP Connection: bluebird      ──→  HTTPS connection
│
└── Sub-Agent Process (isolated)
    ├── ✅ Built-in tools
    ├── ✅ GitHub MCP (default)
    └── ❌ No connection to parent's MCP servers
```

### Why This Design Exists

- **Security**: Sub-agents are sandboxed to prevent unintended access
- **Simplicity**: Each context is self-contained and predictable
- **Resource management**: MCP server processes aren't duplicated per sub-agent

---

## 8. Workarounds: Getting MCP-Like Access in Sub-Agents

Since sub-agents can't directly use MCP servers, here are practical workarounds:

### Workaround A: Do the Work Inline (Recommended for Now)

Skip the sub-agent entirely. The main agent has full MCP access and can do the review directly.

```
User: "Review this ADO PR"
Main Agent: [uses azure-devops MCP to fetch PR] → [reviews code itself]
```

**Pros**: Works today, full MCP access, no limitations
**Cons**: Uses main agent's context window, not parallelizable

### Workaround B: Use `bash` + `curl` + Environment Variables

Sub-agents **do** inherit environment variables and can use `bash`. Configure a PAT:

```bash
# In your shell profile (~/.bashrc or ~/.zshrc):
export AZURE_DEVOPS_PAT="your-personal-access-token"
```

Then in your custom agent prompt, instruct it to use curl:

```markdown
## How to Fetch PR Data

Use curl with the AZURE_DEVOPS_PAT environment variable:

\```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/{org}/{project}/_apis/git/pullrequests/{id}?api-version=7.1"
\```
```

**Pros**: Works in sub-agents, no MCP needed
**Cons**: Requires PAT management, more complex agent prompts, raw JSON responses

### Workaround C: Pre-Fetch and Pass Data

Have the main agent fetch the data, then pass it to the sub-agent in the prompt:

```
Main Agent:
  1. Fetch PR details via azure-devops MCP
  2. Fetch PR diff via azure-devops MCP
  3. task(agent_type="codereviewer", prompt="Review this diff:\n{diff_content}")
```

**Pros**: Sub-agent gets exactly the data it needs, works today
**Cons**: Large diffs may exceed prompt limits, two-step process

### Workaround D: Clone the Repo Locally

If the repo is cloned, the sub-agent can use `git` commands via bash:

```bash
git diff main...feature-branch
```

**Pros**: Full git access, works with code-review built-in agent
**Cons**: Requires repo clone, doesn't work for external PRs

### Future: Native MCP in Sub-Agents

As Copilot CLI evolves, sub-agents may gain the ability to specify their own MCP server
connections. Watch for updates to the agent definition frontmatter — a potential future
syntax might look like:

```yaml
---
description: Reviews ADO PRs
tools: ['azure-devops/*']
mcp:
  azure-devops:
    type: stdio
    command: npx
    args: ["-y", "@azure-devops/mcp", "msazure", "--authentication", "azcli"]
---
```

This is speculative — check the [Copilot CLI changelog](https://github.com/githubnext/copilot-cli)
and `/changelog` command for updates.

---

## 9. Execution Modes: Sync vs Background

Sub-agents can run in two modes:

### Sync Mode

```
task(agent_type="explore", mode="sync", prompt="Find all auth files")
```

- Main agent **blocks** until the sub-agent completes
- Results are immediately available
- Best for: Quick tasks where you need the result before continuing

### Background Mode

```
task(agent_type="code-review", mode="background", prompt="Review changes")
```

- Main agent **continues working** while the sub-agent runs
- You receive a notification when the sub-agent completes
- Use `read_agent(agent_id="...")` to retrieve results
- Best for: Long-running tasks, parallel work

### Parallel Execution

Multiple sub-agents can run simultaneously in background mode:

```
# Launch 3 explore agents in parallel
task(agent_type="explore", mode="background", name="auth", prompt="Analyze auth module")
task(agent_type="explore", mode="background", name="api", prompt="Analyze API layer")
task(agent_type="explore", mode="background", name="db", prompt="Analyze DB schema")
```

Use `/tasks` to view and manage running sub-agents.
Use `/fleet` to enable fleet mode for parallel sub-agent execution.

---

## 10. Practical Examples

### Example 1: Custom Agent for Terraform Reviews

**File**: `~/.copilot/agents/terraform-reviewer.agent.md`

```markdown
---
description: Reviews Terraform plans and configurations for best practices
tools: ['bash', 'read', 'search']
model: Claude Sonnet 4.5
---

# Terraform Reviewer

You review Terraform configurations for:

- Security misconfigurations (open security groups, public S3 buckets)
- Cost optimization (oversized instances, missing reservations)
- Best practices (module usage, state management, naming conventions)
- Drift risks (hardcoded values that should be variables)

When reviewing, run `terraform validate` and `terraform fmt -check` if available.
```

### Example 2: Custom Agent for Database Migration Reviews

**File**: `.github/agents/migration-reviewer.agent.md` (repo-level, shared with team)

```markdown
---
description: Reviews database migration files for safety
tools: ['bash', 'read', 'search']
model: Claude Sonnet 4.5
---

# Migration Reviewer

Check migration files for:

- Backward compatibility (can the old code still work during rollout?)
- Data loss risks (DROP COLUMN, TRUNCATE, etc.)
- Lock contention (ALTER TABLE on large tables)
- Rollback safety (is there a down migration?)
- Index impact (adding indexes on large tables blocks writes)
```

### Example 3: Using the Main Agent as a Coordinator

For Azure DevOps PR reviews today, the most effective pattern is:

```
User: "Review PR #12345 on ADO"

Main Agent (has MCP access):
  1. azure-devops: get_pull_request_by_id(12345)     → PR metadata
  2. azure-devops: get_pull_request_changes(12345)   → Code diff
  3. Reviews the diff directly using its own reasoning
  4. Returns structured review to user
```

No sub-agent needed — the main agent acts as both fetcher and reviewer.

---

## 11. Best Practices

### When to Use Sub-Agents

| Scenario | Recommendation |
|----------|---------------|
| Simple code review (local git) | ✅ Use `code-review` built-in |
| Complex multi-file refactor analysis | ✅ Use `general-purpose` |
| Running tests/builds | ✅ Use `task` |
| Parallel codebase research | ✅ Use multiple `explore` agents |
| Azure DevOps PR review | ⚠️ Do inline (main agent) until MCP propagation is supported |
| Quick file lookup | ❌ Don't use sub-agent — use grep/glob yourself |

### Writing Good Agent Prompts

1. **Be complete**: Sub-agents have no context. Include everything they need.
2. **Be specific**: Tell them exactly what to do, not just what to think about.
3. **Include data**: If they can't fetch it themselves, pass it in the prompt.
4. **Set format**: Define the expected output structure.

### Agent Definition Tips

1. **Keep descriptions clear**: They appear in `/agent` listings
2. **Choose the right model**: Haiku for speed, Sonnet for quality, Opus for complex reasoning
3. **Declare tools intentionally**: Even if MCP tools aren't propagated today, the declarations document intent
4. **Write actionable system prompts**: The markdown body is the agent's system prompt — make it operational, not philosophical

---

## Appendix: File Locations Reference

```
~/.copilot/
├── agents/
│   └── *.agent.md              # User-level custom agents
├── mcp-config.json             # MCP server configuration (main agent only)
├── copilot-instructions.md     # Global custom instructions
├── config.json                 # CLI settings
├── settings.json               # UI/behavior settings
└── lsp-config.json             # Language server configuration

<repo>/.github/
├── agents/
│   └── *.agent.md              # Repo-level custom agents (shared with team)
├── copilot-instructions.md     # Repo-specific instructions
├── instructions/
│   └── *.instructions.md       # Additional instruction files
├── mcp.json                    # Repo-level MCP config (if supported)
└── lsp.json                    # Repo-level LSP config

<repo>/
├── AGENTS.md                   # Agent instructions (git root & cwd)
├── CLAUDE.md                   # Claude-specific instructions
└── GEMINI.md                   # Gemini-specific instructions
```

---

## Appendix: CLI Commands for Agent Management

| Command | Description |
|---------|-------------|
| `/agent` | Browse and select from available agents |
| `/tasks` | View and manage running sub-agents |
| `/fleet` | Enable fleet mode for parallel sub-agent execution |
| `/mcp` | Manage MCP server configuration |
| `/env` | Show loaded environment details (agents, MCPs, instructions) |
| `/skills` | Manage skills for enhanced capabilities |

---

*Last updated: May 2026*
*Based on Copilot CLI v1.0.44*
