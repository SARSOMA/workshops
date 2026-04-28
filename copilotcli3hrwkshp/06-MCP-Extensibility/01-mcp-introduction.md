# Tutorial 6.1: Introduction to MCP

## Introduction

Model Context Protocol (MCP) is an open standard that enables AI models to access external tools and data sources. Copilot CLI uses MCP to extend its capabilities beyond basic code operations.

## What is MCP?

```
┌─────────────────────────────────────────────────────────────────┐
│                     MCP ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌──────────────┐                    ┌──────────────────┐    │
│    │   Copilot    │                    │  External System │    │
│    │    CLI       │◄───── MCP ─────►   │  (GitHub, ADO,   │    │
│    │   (Client)   │                    │   Databases...)  │    │
│    └──────────────┘                    └──────────────────┘    │
│                                                                 │
│    MCP provides a standardized way for AI to:                  │
│    • Call tools (execute actions)                              │
│    • Access resources (read data)                              │
│    • Receive prompts (get context)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### MCP vs Direct Integration

| Approach | Pros | Cons |
|----------|------|------|
| Direct Integration | Tight coupling, optimized | Requires code changes for each service |
| MCP | Standardized, pluggable | Additional layer, setup required |

MCP enables **one protocol, many integrations**.

---

## Key Concepts

### 1. MCP Servers

An MCP server is a program that:
- Implements the MCP protocol
- Exposes tools and resources
- Handles requests from Copilot CLI

### 2. Tools

Tools are actions the AI can perform:

```
┌─────────────────────────────────────────────────────────────────┐
│ Tool: create_pull_request                                       │
├─────────────────────────────────────────────────────────────────┤
│ Parameters:                                                     │
│   - title: string (required)                                    │
│   - body: string                                                │
│   - base: string (default: "main")                              │
│   - head: string (required)                                     │
│                                                                 │
│ Returns:                                                        │
│   - PR URL                                                      │
│   - PR number                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Resources

Resources are data the AI can access:

```
┌─────────────────────────────────────────────────────────────────┐
│ Resource: github://repos/{owner}/{repo}/issues                  │
├─────────────────────────────────────────────────────────────────┤
│ Returns:                                                        │
│   - List of issues                                              │
│   - Issue metadata (title, body, labels, etc.)                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Prompts

Prompts provide context or templates:

```
┌─────────────────────────────────────────────────────────────────┐
│ Prompt: code_review_guidelines                                  │
├─────────────────────────────────────────────────────────────────┤
│ Provides:                                                       │
│   - Organization's code review standards                        │
│   - Checklist items                                             │
│   - Examples                                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Built-in MCP Server: GitHub

Copilot CLI comes with the GitHub MCP server pre-configured:

### Available Tools

| Tool | Description |
|------|-------------|
| `search_repositories` | Search for repositories |
| `create_repository` | Create a new repository |
| `get_file_contents` | Read file from a repo |
| `create_or_update_file` | Write file to a repo |
| `create_pull_request` | Create a PR |
| `merge_pull_request` | Merge a PR |
| `create_issue` | Create an issue |
| `list_issues` | List repository issues |
| `add_issue_comment` | Comment on an issue |
| `search_code` | Search code across GitHub |

### Usage Example

```
List open issues in my-org/my-repo labeled as "bug"

Copilot uses GitHub MCP to:
1. Call list_issues tool
2. Filter by label
3. Return results
```

---

## MCP Server Ecosystem

### Official Servers

| Server | Purpose |
|--------|---------|
| `@modelcontextprotocol/server-github` | GitHub integration |
| `@modelcontextprotocol/server-filesystem` | Local file operations |
| `@modelcontextprotocol/server-postgres` | PostgreSQL database |
| `@modelcontextprotocol/server-slack` | Slack integration |

### Third-Party Servers

| Server | Purpose |
|--------|---------|
| `@azure/mcp-server` | Azure DevOps |
| `mcp-server-notion` | Notion integration |
| `mcp-server-linear` | Linear issue tracking |

### Custom Servers

You can build your own MCP server for:
- Internal tools
- Proprietary systems
- Custom workflows

---

## How MCP Works in Practice

### Flow Diagram

```
User Prompt: "Create a PR with my changes"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  Copilot CLI (MCP Client)                                       │
│                                                                 │
│  1. Understands intent                                          │
│  2. Identifies relevant MCP server (GitHub)                     │
│  3. Selects tool (create_pull_request)                          │
│  4. Formats parameters                                          │
└───────────────────────────────────────┬─────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  GitHub MCP Server                                              │
│                                                                 │
│  1. Receives tool call                                          │
│  2. Authenticates with GitHub API                               │
│  3. Executes operation                                          │
│  4. Returns result                                              │
└───────────────────────────────────────┬─────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  Copilot CLI                                                    │
│                                                                 │
│  1. Receives result                                             │
│  2. Formats response                                            │
│  3. Presents to user                                            │
└─────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
Output: "Created PR #123: https://github.com/org/repo/pull/123"
```

---

## Why MCP Matters

### 1. Extensibility Without Core Changes

Add new capabilities without modifying Copilot CLI itself.

### 2. Standardized Integration

One protocol works across different AI tools and services.

### 3. Security Model

MCP servers run locally with your credentials—data stays under your control.

### 4. Real-Time Data

Access live data from external systems, not just static context.

### 5. Organization Customization

Build MCP servers for internal tools and workflows.

---

## Exercise: Explore MCP

### Exercise 6.1.1: View MCP Status

1. Launch Copilot CLI
2. Check MCP servers:
   ```
   /mcp
   ```
3. Note the GitHub server status

### Exercise 6.1.2: Use GitHub MCP

Try these prompts that use the GitHub MCP server:

```
List my most recent repositories

Search for repositories related to machine learning

Show me the README of github/copilot-cli

What issues are open in [your-org]/[your-repo]?
```

### Exercise 6.1.3: Explore Tools

Ask Copilot about available tools:
```
What tools do you have available for interacting with GitHub?
```

---

## Key Takeaways

1. **MCP is a protocol** for AI-external system communication
2. **Tools** = actions, **Resources** = data, **Prompts** = context
3. **GitHub MCP is built-in** to Copilot CLI
4. **Extensible** with official, third-party, or custom servers
5. **Secure** - servers run locally with your credentials

---

## Next Tutorial

Continue to [Tutorial 6.2: Configuring MCP Servers](./02-mcp-configuration.md) to add more MCP integrations.
