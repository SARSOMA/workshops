# Part 1: Markdown-Based Custom Agents

Custom agents in VS Code Chat, Copilot CLI, and Agency all share the same file format: a `.agent.md` Markdown file with optional YAML frontmatter. You define the agent once and it works across all three tools.

This section covers how to set up custom agents in each tool.

---

## The `.agent.md` File Format

All three tools use the same agent definition format:

```markdown
---
description: A brief description of what this agent does
tools: [read, browser, edit, search, 'ado/*', 'enghub/*']
model: GPT-4.1 (copilot)
---

# Your Agent Instructions

Write natural language instructions here describing how the agent should behave,
what it should focus on, and any rules it should follow.
```

Note that `tools` and `model` fields will auto complete only if you have the `.agent.md` file extension in vscode.

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Recommended | Shown as placeholder text; also used by Copilot to decide when to invoke the agent |
| `tools` | No | List of tools the agent can use. Omit to allow all tools |
| `model` | No | Specific AI model to use (e.g., `GPT-4.1 (copilot)`, `Claude Sonnet 4 (copilot)`) |
| `name` | No | Display name. Defaults to the file name |
| `handoffs` | No | Transitions to other agents with pre-filled prompts |

### File Locations

| Scope | Path |
|-------|------|
| **Workspace** (shared with team via repo) | `.github/agents/my-agent.agent.md` |
| **User** (personal, across all workspaces) | `~/.copilot/agents/my-agent.agent.md` |

If agents with the same name exist in both locations, the user-level agent takes precedence.

---

## VS Code Copilot Chat

### What's Built-In

VS Code ships with built-in agents you can select from the agents dropdown:
- **Agent** (default) — general-purpose with full tool access
- **Plan** — generates implementation plans with read-only tools
- **Explore** — fast codebase exploration and Q&A

See the [exercise](exercise.md) for step-by-step instructions on creating and using agents in VS Code and Copilot CLI.

---

## GitHub Copilot CLI

### What's Built-In

Copilot CLI runs in interactive mode with access to the same agent format. It includes default agents for general tasks, and custom agents run as **subagents** — temporary agents with their own context window that handle delegated work.

---

## Agency

Agency is a wrapper around Copilot CLI that adds Microsoft-specific integrations (Azure DevOps, Bluebird MCP, and streamlined Microsoft auth). Agent creation and usage are identical to Copilot CLI — use `/agent` in interactive mode or create `.agent.md` files manually in the same locations. The key difference is that Microsoft-internal MCP tools are pre-configured in the Agency client.

---

## Sub-Agents: Delegation and Composition

One of the most powerful features of custom agents is the ability to **call other agents as sub-agents**. Instead of building one monolithic agent that does everything, you can compose small, focused agents that delegate to each other — each with its own tools and least-privilege boundaries.

### Why Sub-Agents Matter

- **Context saving** - Each agent gets their own context window, so only nessicary context is on each context window.
- **Least privilege** — Each agent only gets the tools it needs. A coordinating agent doesn't need file access if it delegates reading to a sub-agent.
- **Separation of concerns** — One agent handles orchestration, another handles a specific task. Each is simpler and easier to maintain.
- **Reusability** — A sub-agent can be called by multiple parent agents. Build it once, use it everywhere.
- **Security boundaries** — Sensitive operations (reading secrets, calling APIs) can be isolated in a sub-agent with restricted tools, while the parent agent has no direct access to those resources.

### Example: `get-secret` and `sub-agent`

This repo includes a working example of sub-agent delegation:

### How It Works

```
User → get-secret agent → sub-agent agent → reads secret-word.txt → returns "hello123"
         (tool: agent)      (tool: read)
```

The user asks `get-secret` for the secret word. `get-secret` delegates to `sub-agent`, which reads the file and returns the value. The result flows back up the chain.

### When to Use Sub-Agents

| Pattern | Example |
|---------|---------|
| **Privilege isolation** | A coordinator delegates to a reader agent that has file access |
| **Multi-step workflows** | A release agent calls a changelog agent, then a PR agent |
| **Shared capabilities** | Multiple agents delegate to a common "fetch ADO work item" agent |
| **Different models** | A fast triage agent delegates complex analysis to an agent using a stronger model |

---

## Key Takeaways

- **One format, three tools** — the `.agent.md` file works across VS Code Chat, Copilot CLI, and Agency
- **Tool restrictions** keep agents focused — a read-only planning agent can't accidentally modify files
- **Workspace agents** (`.github/agents/`) are shared via your repo — commit them and your whole team gets them
- **User agents** (`~/.copilot/agents/`) are personal and travel with you across projects

---

## Sources

| Tool | Official Documentation |
|------|----------------------|
| VS Code Copilot Chat | [Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents) |
| GitHub Copilot CLI | [Creating and using custom agents for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli) |
| Agency | [Agency Overview (eng.ms)](https://eng.ms/docs/coreai/devdiv/one-engineering-system-1es/1es-jacekcz/startrightgitops/agency/overview/overview) |
| Customization Cheat Sheet | [Copilot customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet) |
| Custom Instructions | [About customizing GitHub Copilot responses](https://docs.github.com/en/copilot/concepts/prompting/response-customization) |