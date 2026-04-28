# Tutorial 4.1: MCP Overview

---

## Concept

### What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables AI models to access external tools and data sources. Think of it as a universal adapter between Copilot CLI and any external system.

### MCP Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       MCP ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                      COPILOT CLI (Host)                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│ │
│  │  │   Agent     │  │   Tool      │  │     MCP Client          ││ │
│  │  │   Core      │◄─┤   Router    │◄─┤  (Protocol Handler)     ││ │
│  │  └─────────────┘  └─────────────┘  └───────────┬─────────────┘│ │
│  └────────────────────────────────────────────────┼──────────────┘ │
│                                                   │                 │
│                         JSON-RPC over stdio       │                 │
│                                                   ▼                 │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                     MCP SERVER LAYER                           │ │
│  │                                                                │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │ │
│  │  │   GitHub    │  │    Azure    │  │     ADO     │    ...     │ │
│  │  │   Server    │  │   Server    │  │   Server    │            │ │
│  │  │  (built-in) │  │             │  │             │            │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │ │
│  └─────────┼────────────────┼────────────────┼───────────────────┘ │
│            │                │                │                      │
│            ▼                ▼                ▼                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  GitHub     │  │    Azure    │  │ Azure DevOps│                 │
│  │  REST API   │  │  ARM APIs   │  │  REST APIs  │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### How Data Flows

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP REQUEST/RESPONSE FLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. USER PROMPT                                                     │
│     "List my Azure VMs in production"                               │
│                     │                                               │
│                     ▼                                               │
│  2. AGENT CORE interprets and plans                                 │
│     → Decides: "I need to call Azure MCP server"                    │
│                     │                                               │
│                     ▼                                               │
│  3. MCP CLIENT sends JSON-RPC request                               │
│     ┌─────────────────────────────────────────┐                    │
│     │ {                                       │                    │
│     │   "method": "tools/call",               │                    │
│     │   "params": {                           │                    │
│     │     "name": "azure_list_vms",           │                    │
│     │     "arguments": {                      │                    │
│     │       "resource_group": "production"    │                    │
│     │     }                                   │                    │
│     │   }                                     │                    │
│     │ }                                       │                    │
│     └─────────────────────────────────────────┘                    │
│                     │                                               │
│                     ▼                                               │
│  4. MCP SERVER executes tool                                        │
│     → Calls Azure ARM API with your credentials                     │
│     → Returns VM list as JSON                                       │
│                     │                                               │
│                     ▼                                               │
│  5. AGENT CORE receives data                                        │
│     → Formats response for user                                     │
│     → "You have 3 VMs in production: vm-web-01..."                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### MCP Server Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                   MCP SERVER LIFECYCLE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SESSION START                                                      │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────┐                       │
│  │ 1. Copilot reads mcp.json configs       │                       │
│  │    (user-level + repo-level)            │                       │
│  └───────────────────┬─────────────────────┘                       │
│                      │                                              │
│                      ▼                                              │
│  ┌─────────────────────────────────────────┐                       │
│  │ 2. Spawns each server as subprocess     │                       │
│  │    • Runs command from config           │                       │
│  │    • Sets environment variables         │                       │
│  │    • Establishes stdio communication    │                       │
│  └───────────────────┬─────────────────────┘                       │
│                      │                                              │
│                      ▼                                              │
│  ┌─────────────────────────────────────────┐                       │
│  │ 3. Server advertises capabilities       │                       │
│  │    • Available tools                    │                       │
│  │    • Available resources                │                       │
│  │    • Available prompts                  │                       │
│  └───────────────────┬─────────────────────┘                       │
│                      │                                              │
│                      ▼                                              │
│  ┌─────────────────────────────────────────┐                       │
│  │ 4. Server stays running for session     │  ◄── Ready for calls  │
│  │    • Handles tool calls on demand       │                       │
│  │    • Maintains connection state         │                       │
│  └───────────────────┬─────────────────────┘                       │
│                      │                                              │
│                      ▼                                              │
│  SESSION END → Server processes terminated                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Why MCP Matters

| Benefit | Description |
|---------|-------------|
| **Extensibility** | Add capabilities without modifying Copilot CLI |
| **Standardization** | One protocol for many integrations |
| **Security** | Servers run locally with your credentials |
| **Real-time Data** | Access live data from external systems |
| **Isolation** | Each server runs in its own process |

### MCP Components

MCP servers can expose three types of capabilities:

| Component | Purpose | Example |
|-----------|---------|---------|
| **Tools** | Actions the AI can perform | Create PR, deploy resource, query database |
| **Resources** | Data the AI can read | Issues list, file contents, API responses |
| **Prompts** | Context templates | Code review guidelines, deployment checklist |

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP CAPABILITY TYPES                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  TOOLS (Actions)                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Agent CALLS these to DO something                          │   │
│  │ • Examples: create_issue, deploy_vm, send_message            │   │
│  │ • Can have side effects (modify external state)              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  RESOURCES (Data)                                                   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Agent READS these to GET information                       │   │
│  │ • Examples: list_repos, get_pipeline_status, fetch_metrics   │   │
│  │ • Read-only, no side effects                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  PROMPTS (Templates)                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ • Pre-defined context/instructions the agent can use         │   │
│  │ • Examples: security_review_checklist, deploy_runbook        │   │
│  │ • Provides consistent guidance for specific tasks            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Where Configuration Lives

```
MCP Configuration Locations:

~/.copilot/
├── mcp.json              # User-level MCP servers (all projects)
└── copilot-instructions.md  # User-level instructions

<repository>/.github/
└── mcp.json              # Repository-level MCP servers (this project)

Priority: Repository config merges with User config
          (same server name → repo wins)
```

**Example `mcp.json`:**
```json
{
  "servers": {
    "azure-devops": {
      "command": "npx",
      "args": ["@anthropic/mcp-server-azure-devops"],
      "env": {
        "AZURE_DEVOPS_ORG": "your-org",
        "AZURE_DEVOPS_PAT": "your-pat"
      }
    }
  }
}
```

### Built-in MCP Server: GitHub

Copilot CLI comes with GitHub MCP **pre-configured**:

| Tool | Description |
|------|-------------|
| `search_repositories` | Search for repos |
| `create_pull_request` | Create a PR |
| `list_issues` | List repo issues |
| `get_file_contents` | Read files from repos |
| `search_code` | Search code across GitHub |

---

## Practice

### Exercise 1: Check MCP Status

1. **Launch Copilot CLI:**
   ```bash
   copilot
   ```

2. **View MCP servers:**
   ```
   /mcp
   ```

3. **Note which servers are active**

### Exercise 2: Use GitHub MCP

Try these prompts that use the built-in GitHub MCP:

```
List my 5 most recent repositories
```

```
Search for repositories related to "kubernetes" with more than 1000 stars
```

```
What open issues are in SARSOMA/akri?
```

### Exercise 3: Explore Available Tools

Ask Copilot about its capabilities:

```
What tools do you have available for interacting with GitHub?
```

```
What MCP servers are configured?
```

### Exercise 4: View Configuration File

Check if you have custom MCP configuration:

```bash
cat ~/.copilot/mcp.json
```

If the file doesn't exist, that's okay — you're using defaults.

---

## Q&A

### Question 1

What is the primary purpose of MCP (Model Context Protocol)?

A) To make Copilot CLI run faster  
B) To enable AI models to access external tools and data sources  
C) To encrypt communication between Copilot and GitHub  
D) To manage Copilot CLI licenses  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

MCP (Model Context Protocol) is an open standard that enables AI models to access external tools and data sources. It provides a standardized way to connect Copilot CLI with external systems like Azure DevOps, databases, and more.

</details>

---

### Question 2

Where is the user-level MCP configuration stored?

A) `~/.copilot/mcp.json`  
B) `~/.copilot/mcp.json`  
C) `/etc/copilot/mcp.json`  
D) `.github/mcp.json` (repository root)  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

User-level MCP configuration is stored in `~/.copilot/mcp.json`. Repository-level configuration goes in `.github/mcp.json`.

</details>

---

### Question 3

Which command shows the status of configured MCP servers?

A) `/servers`  
B) `/mcp`  
C) `/config`  
D) `/status`  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

The `/mcp` command shows the status of configured MCP servers, including which are running and available.

</details>

---

## Next Steps

Continue to [Tutorial 4.2: Configuring MCPs](./02-configuring-mcps.md) to set up Azure, ADO, WorkIQ, and Bluebird MCP servers.
