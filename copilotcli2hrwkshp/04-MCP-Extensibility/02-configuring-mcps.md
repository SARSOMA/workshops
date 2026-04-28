# Tutorial 4.2: Configuring MCP Servers

---

## Concept

### MCP Servers We'll Configure

| Server | Purpose | Key Capabilities |
|--------|---------|------------------|
| **Azure MCP** | Azure resource management | Resource queries, deployments, diagnostics, Cosmos DB, Key Vault |
| **Azure DevOps MCP** | Azure DevOps integration | Work items, pipelines, repos, PRs, wikis, test plans |
| **Bluebird MCP** | Code search & intelligence | Semantic search, file history, commits, wiki search |
| **WorkIQ MCP** | Microsoft 365 Copilot | Emails, meetings, documents, Teams, workplace intelligence |

### Configuration Structure

MCP servers are configured in `~/.copilot/mcp.json`:

```json
{
  "servers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

> **Note**: Some MCP servers (like Azure, ADO, Bluebird, WorkIQ) may be pre-configured by your organization or come built-in with Copilot CLI. Check `/mcp` to see what's already available.

---

## Server Configuration Details

### 1. Azure MCP

Provides comprehensive access to Azure resources and services.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AZURE MCP                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  RESOURCE MANAGEMENT          │  DATA SERVICES                      │
│  • List subscriptions         │  • Cosmos DB queries                │
│  • List resource groups       │  • Storage accounts                 │
│  • Query via Resource Graph   │  • Key Vault secrets                │
│  • Check resource health      │  • App Configuration                │
│                               │                                     │
│  COMPUTE & NETWORKING         │  MONITORING & DIAGNOSTICS           │
│  • VM management              │  • Azure Monitor logs               │
│  • AKS clusters               │  • Application Insights             │
│  • Container Apps             │  • Advisor recommendations          │
│  • Function Apps              │  • Resource health status           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Configuration (if manual setup needed):**
```json
{
  "servers": {
    "azure": {
      "command": "npx",
      "args": ["@azure/mcp"],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "your-subscription-id",
        "AZURE_TENANT_ID": "your-tenant-id"
      }
    }
  }
}
```

**Authentication**: Azure MCP typically uses Azure CLI credentials (`az login`). Ensure you're logged in:
```bash
az login
az account set --subscription "your-subscription-name"
```

**Example Prompts:**
```
List my Azure subscriptions
What VMs are running in resource group "production"?
Show me Advisor recommendations for cost optimization
Query Cosmos DB container "users" in account "mydb"
```

---

### 2. Azure DevOps MCP

Full integration with Azure DevOps for work tracking, pipelines, and code.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      AZURE DEVOPS MCP                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  WORK ITEMS                   │  PIPELINES                          │
│  • Create/query/update        │  • List pipeline definitions        │
│  • Search work items          │  • Get build status                 │
│  • Link work items to PRs     │  • View build logs                  │
│  • Manage iterations          │  • Trigger pipeline runs            │
│                               │                                     │
│  REPOSITORIES                 │  ADDITIONAL                         │
│  • List repos/branches        │  • Wiki pages                       │
│  • Get file contents          │  • Test plans                       │
│  • Create/manage PRs          │  • Project/team management          │
│  • PR comments & reviews      │  • Advanced Security alerts         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Configuration (if manual setup needed):**
```json
{
  "servers": {
    "azure-devops": {
      "command": "npx",
      "args": ["@anthropic/mcp-server-azure-devops"],
      "env": {
        "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/your-org",
        "AZURE_DEVOPS_PAT": "your-personal-access-token"
      }
    }
  }
}
```

**Creating a PAT:**
1. Go to Azure DevOps → User Settings → Personal Access Tokens
2. Create new token with scopes: `Code (Read & Write)`, `Work Items (Read & Write)`, `Build (Read & Execute)`
3. Copy the token (you won't see it again!)

**Example Prompts:**
```
Show my assigned work items in project "MyProject"
What's the status of the latest build for pipeline "CI-Main"?
Create a bug titled "Login fails on mobile" in project "WebApp"
List open PRs in repo "backend-api"
```

---

### 3. Bluebird MCP

Advanced code intelligence, search, and history across your codebase.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        BLUEBIRD MCP                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CODE SEARCH                  │  CODE HISTORY                       │
│  • Keyword search             │  • File history (commits)           │
│  • Semantic/concept search    │  • Commit details & diffs           │
│  • File path search           │  • Pull request info                │
│  • Cross-repo search          │  • Blame/authorship                 │
│                               │                                     │
│  NAVIGATION                   │  ADDITIONAL                         │
│  • Get file contents          │  • Wiki search                      │
│  • List directory structure   │  • Work item search                 │
│  • Branch-aware file access   │  • Repository exploration           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Note**: Bluebird MCP is often pre-configured in enterprise environments. Check `/mcp` to see if it's available.

**Key Tools:**
| Tool | Purpose |
|------|---------|
| `search_code` | Search code by keywords (supports AND, OR, NOT, wildcards) |
| `search_file_paths` | Find files by name or path pattern |
| `get_file_content` | Retrieve file contents (optionally by line range) |
| `list_directory` | Explore directory structure |
| `code_history` | View commits, diffs, file history, PR details |
| `search_wiki` | Search Azure DevOps wiki pages |
| `search_work_items` | Search bugs, user stories, tasks |

**Example Prompts:**
```
Search for files containing "authentication" in the codebase
Show the commit history for src/auth/login.ts
What changed in commit abc1234?
Find all TypeScript files in the src/components folder
Search the wiki for "deployment process"
```

---

### 4. WorkIQ MCP

Microsoft 365 Copilot integration for workplace intelligence.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WORKIQ MCP                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  WorkIQ queries Microsoft 365 Copilot to answer questions about:    │
│                                                                     │
│  • Emails (sent, received, threads)                                 │
│  • Meetings (past, upcoming, attendees)                             │
│  • Documents (SharePoint, OneDrive)                                 │
│  • Teams messages and conversations                                 │
│  • People information and org structure                             │
│  • Project status and decisions from communications                 │
│                                                                     │
│  ⚠️  Requires EULA acceptance on first use                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**EULA Acceptance**: On first use, you'll need to accept the WorkIQ EULA. The tool will prompt you with instructions.

**Key Tools:**
| Tool | Purpose |
|------|---------|
| `ask_work_iq` | Query M365 Copilot about emails, meetings, files, people |
| `accept_eula` | Accept the EULA (required before first use) |
| `get_debug_link` | Generate shareable links for conversations |

**Example Prompts:**
```
What did John say about the product launch in his last email?
What meetings do I have tomorrow?
Find documents about the Q4 budget
What are the priorities my manager mentioned this week?
Summarize the Teams discussion about the new feature
```

---

## Complete Configuration Example

Here's a complete `~/.copilot/mcp.json` with all servers:

```json
{
  "servers": {
    "azure": {
      "command": "npx",
      "args": ["@azure/mcp"],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      }
    },
    "azure-devops": {
      "command": "npx",
      "args": ["@anthropic/mcp-server-azure-devops"],
      "env": {
        "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/your-org",
        "AZURE_DEVOPS_PAT": "your-pat-token"
      }
    }
  }
}
```

> **Note**: Bluebird and WorkIQ are typically enterprise-managed and may not require manual configuration. They appear automatically when your organization enables them.

---

## Practice

### Exercise 1: View Current MCP Configuration

1. **Check existing MCP config file:**
   ```bash
   cat ~/.copilot/mcp.json 2>/dev/null || echo "No custom MCP config found"
   ```

2. **In Copilot CLI, view active MCP servers:**
   ```
   /mcp
   ```

3. **View environment details including MCPs:**
   ```
   /env
   ```

### Exercise 2: Explore Azure MCP

Try these Azure resource management prompts:

```
List my Azure subscriptions
```

```
What resource groups do I have?
```

```
Show me the VMs in resource group "production"
```

```
What Azure Advisor recommendations do I have for cost optimization?
```

```
Query Cosmos DB: Show me the first 5 documents in container "users"
```

### Exercise 3: Explore Azure DevOps MCP

Try these ADO work tracking and pipeline prompts:

```
Show my assigned work items
```

```
List pipelines in project "MyProject"
```

```
What's the status of the latest build for "CI-Pipeline"?
```

```
Show open pull requests in repository "backend-api"
```

```
Create a bug titled "Login button unresponsive" with description "Users report..."
```

```
Search work items for "authentication error"
```

### Exercise 4: Explore Bluebird MCP

Try these code search and history prompts:

```
Search the codebase for "validateUser"
```

```
Find all TypeScript files containing "async function"
```

```
Show the commit history for src/auth/login.ts
```

```
What changed in the last 5 commits?
```

```
Search the wiki for "deployment runbook"
```

```
Find work items related to "performance"
```

### Exercise 5: Explore WorkIQ MCP

> **Note**: WorkIQ requires EULA acceptance on first use. Follow the prompts.

Try these Microsoft 365 workplace intelligence prompts:

```
What meetings do I have today?
```

```
What did my manager say about priorities this week?
```

```
Find emails about the product launch from last week
```

```
What documents has the team shared about the Q4 roadmap?
```

```
Summarize the recent Teams discussion about the new feature
```

### Exercise 6: Combined Multi-MCP Workflow

Try prompts that leverage multiple MCPs together:

```
I have bug #1234 in Azure DevOps. Find the related code and suggest a fix.
```

```
Show me the Azure resources used by the code in src/infrastructure/
```

```
Find work items related to the authentication module and show me recent commits to that code
```

```
What Azure costs are associated with the services mentioned in our wiki deployment guide?
```

---

## Q&A

### Question 1

Which file contains user-level MCP server configurations?

A) `~/.copilot/config.json`  
B) `~/.copilot/mcp.json`  
C) `~/.copilot/servers.json`  
D) `/etc/github-copilot/mcp.json`  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

MCP server configurations are stored in `~/.copilot/mcp.json`. The `config.json` file is for general Copilot CLI settings.

</details>

---

### Question 2

What environment variable is typically required for Azure DevOps MCP?

A) `AZURE_DEVOPS_TOKEN`  
B) `ADO_API_KEY`  
C) `AZURE_DEVOPS_PAT`  
D) `DEVOPS_SECRET`  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Azure DevOps MCP typically requires `AZURE_DEVOPS_PAT` (Personal Access Token) and `AZURE_DEVOPS_ORG` (organization URL) to authenticate.

</details>

---

### Question 3

What is the primary benefit of having multiple MCP servers configured?

A) Faster response times  
B) Lower API costs  
C) Ability to combine data and actions across different systems  
D) Better security  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Having multiple MCP servers configured allows Copilot CLI to combine data and actions across different systems. For example, you could query a work item from ADO, find related code via Bluebird, and create a fix.

</details>

---

### Question 4

Which MCP server would you use to find recent Teams messages?

A) Azure MCP  
B) ADO MCP  
C) WorkIQ MCP  
D) Bluebird MCP  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

WorkIQ MCP provides Microsoft 365 workplace intelligence, including access to Teams messages, emails, calendar, and documents via Microsoft Graph.

</details>

---

## Next Steps

Continue to [Tutorial 4.3: Skills](./03-skills.md) to learn about automating repeatable tasks.
