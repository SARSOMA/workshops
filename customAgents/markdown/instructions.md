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

### Creating a Custom Agent

**Option 1: Through the UI**

1. In the Chat view, select the **gear icon** (Configure Chat) to open the Agent Customizations editor
2. Select the **Agents** tab
3. Click **New Agent (Workspace)** or **New Agent (User)** from the dropdown
4. Fill in the YAML frontmatter and write your instructions in the body

**Option 2: Generate with AI**

Type `/create-agent` in the chat and describe the persona you want. Copilot will ask clarifying questions and generate the `.agent.md` file for you.

**Option 3: Create the file manually**

Create a file at `.github/agents/my-agent.agent.md` in your workspace:

```markdown
---
description: Reviews code for security vulnerabilities and best practices
tools:
  - search
  - readFile
  - listFiles
---

# Security Reviewer

You are a senior security engineer performing code reviews.

## What to Check
- SQL injection and XSS vulnerabilities
- Hardcoded credentials or secrets
- Missing input validation
- Authentication/authorization issues

## Response Format
1. **Critical** — must fix before merge
2. **Warning** — should address
3. **Suggestion** — nice to have
4. **Positive** — what's done well
```

### Using the Agent

Select your custom agent from the **agents dropdown** in the Chat view. All your messages in that session will use the agent's instructions and tool restrictions.

---

## GitHub Copilot CLI

### What's Built-In

Copilot CLI runs in interactive mode with access to the same agent format. It includes default agents for general tasks, and custom agents run as **subagents** — temporary agents with their own context window that handle delegated work.

### Creating a Custom Agent

**Option 1: Through the CLI wizard**

1. Start Copilot CLI in interactive mode
2. Type `/agent`
3. Select **Create new agent**
4. Choose where to store it:
   - **Project** (`.github/agents/`) — shared with your team
   - **User** (`~/.copilot/agents/`) — personal across all repos
5. Either let Copilot generate the agent from a description, or fill in name/description/instructions manually
6. Choose which tools the agent should have access to
7. Restart the CLI to load the new agent

**Option 2: Create the file manually**

Create the same `.agent.md` file as shown above — the CLI reads from the same locations (`.github/agents/` and `~/.copilot/agents/`).

### Using the Agent

Custom agents can be invoked in four ways:

```bash
# 1. Slash command — interactive selection
/agent

# 2. Explicit instruction in your prompt
Use the security-reviewer agent on all files in /src

# 3. By inference — Copilot picks the agent based on your prompt
Check all TypeScript files for security problems

# 4. Programmatically — specify the agent by name
copilot --agent security-reviewer --prompt "Check /src/app/validator.go"
```

The programmatic mode (`--agent`) is especially useful for scripting and CI/CD pipelines.

---

## Agency

Agency is a wrapper around Copilot CLI that adds Microsoft-specific integrations (Azure DevOps, Bluebird MCP, and streamlined Microsoft auth). Agent creation and usage are identical to Copilot CLI — use `/agent` in interactive mode or create `.agent.md` files manually in the same locations. The key difference is that Microsoft-internal MCP tools are pre-configured in the Agency client.

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