# Tutorial 6.3: Azure DevOps Integration

## Introduction

Azure DevOps (ADO) integration via MCP allows Copilot CLI to interact with your ADO organization—work items, repos, pipelines, and more. This tutorial covers setup and practical usage.

## Prerequisites

- Azure DevOps account
- Personal Access Token (PAT) with appropriate permissions
- Copilot CLI installed

---

## Creating an Azure DevOps PAT

### Step 1: Access PAT Settings

1. Go to [dev.azure.com](https://dev.azure.com)
2. Click your profile icon (top right)
3. Select **Personal access tokens**
4. Click **+ New Token**

### Step 2: Configure Token

| Setting | Value |
|---------|-------|
| Name | Copilot CLI Integration |
| Organization | Your organization (or All accessible) |
| Expiration | Custom (recommend 90+ days) |

### Step 3: Select Scopes

Minimum required scopes:

| Scope | Access Level | Purpose |
|-------|--------------|---------|
| Code | Read & Write | Repository access |
| Work Items | Read & Write | Work item management |
| Build | Read & Execute | Pipeline operations |
| Pull Request | Read & Write | PR management |
| Project | Read | Project information |

### Step 4: Save Token

Copy and save the token securely—you won't see it again!

---

## Configuring ADO MCP Server

### Set Environment Variable

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or PowerShell profile):

```bash
# Bash/Zsh
export AZURE_DEVOPS_PAT="your-pat-token"
export AZURE_DEVOPS_ORG="https://dev.azure.com/your-organization"
```

```powershell
# PowerShell
$env:AZURE_DEVOPS_PAT = "your-pat-token"
$env:AZURE_DEVOPS_ORG = "https://dev.azure.com/your-organization"
```

### Add to MCP Configuration

Edit `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "npx",
      "args": ["-y", "@azure/mcp-server-azure-devops"],
      "env": {
        "AZURE_DEVOPS_PAT": "${AZURE_DEVOPS_PAT}",
        "AZURE_DEVOPS_ORG": "${AZURE_DEVOPS_ORG}"
      }
    }
  }
}
```

### Verify Setup

1. Restart Copilot CLI
2. Check server status:
   ```
   /mcp
   ```
3. Look for "azure-devops" in running state

---

## ADO MCP Capabilities

### Available Tools

| Tool | Description |
|------|-------------|
| `list_projects` | List ADO projects |
| `get_work_items` | Get work items by IDs |
| `create_work_item` | Create a new work item |
| `update_work_item` | Update existing work item |
| `list_repositories` | List repos in a project |
| `get_pull_requests` | Get PRs for a repo |
| `create_pull_request` | Create a new PR |
| `list_pipelines` | List build pipelines |
| `trigger_pipeline` | Run a pipeline |
| `get_pipeline_runs` | Get pipeline run history |

---

## Practical Usage Examples

### Work Items

```
# List work items
Show me all active bugs in the WebApp project

# Create work item
Create a user story in WebApp project titled "Add dark mode support" 
with acceptance criteria

# Update work item
Update work item 12345 to set status to "In Progress" and assign to me

# Query work items
Find all work items assigned to me that are due this sprint
```

### Repositories

```
# List repos
What repositories exist in the WebApp project?

# Get file contents
Show me the README from the frontend repo in WebApp

# Compare branches
What's the difference between main and feature/login in the API repo?
```

### Pull Requests

```
# List PRs
Show me all open PRs in the API repository

# Create PR
Create a PR from my feature/dark-mode branch to main in the frontend repo

# Review PR
What files changed in PR 567 in the API repo?

# Complete PR
Approve and complete PR 567 with a squash merge
```

### Pipelines

```
# List pipelines
What build pipelines exist for the WebApp project?

# Get status
What's the status of the latest run of the "Build and Deploy" pipeline?

# Trigger build
Run the "CI Pipeline" for the main branch

# Investigate failure
Show me the logs from the failed build in pipeline run 1234
```

---

## Integration Workflows

### Workflow 1: Issue to PR

Complete flow from work item to pull request:

```
1. Show me work item 5678

2. I'll work on this. Create a branch called feature/wi-5678-implement-caching

3. [Make code changes locally]

4. Create a PR linking to work item 5678

5. Add reviewers: john@company.com and jane@company.com
```

### Workflow 2: Pipeline Debugging

Investigate and fix pipeline failures:

```
1. Show me the recent failed builds for the API Pipeline

2. Get the logs for build run 4321

3. The error is in the test step. Show me the failing tests.

4. [Fix the issue locally]

5. Trigger a new build to verify the fix
```

### Workflow 3: Sprint Planning

Work with backlog and sprint items:

```
1. Show me all product backlog items in the WebApp project

2. What items are in the current sprint?

3. Create a task under user story 111 titled "Write API documentation"

4. Move work item 222 to the current sprint
```

---

## Advanced Configuration

### Multiple Organizations

```json
{
  "mcpServers": {
    "ado-main": {
      "command": "npx",
      "args": ["-y", "@azure/mcp-server-azure-devops"],
      "env": {
        "AZURE_DEVOPS_PAT": "${ADO_MAIN_PAT}",
        "AZURE_DEVOPS_ORG": "https://dev.azure.com/main-org"
      }
    },
    "ado-client": {
      "command": "npx",
      "args": ["-y", "@azure/mcp-server-azure-devops"],
      "env": {
        "AZURE_DEVOPS_PAT": "${ADO_CLIENT_PAT}",
        "AZURE_DEVOPS_ORG": "https://dev.azure.com/client-org"
      }
    }
  }
}
```

Reference specific server:
```
Using the ado-client server, show me open PRs in the ClientPortal project
```

### On-Premises Azure DevOps Server

```json
{
  "mcpServers": {
    "ado-onprem": {
      "command": "npx",
      "args": ["-y", "@azure/mcp-server-azure-devops"],
      "env": {
        "AZURE_DEVOPS_PAT": "${ADO_ONPREM_PAT}",
        "AZURE_DEVOPS_ORG": "https://tfs.company.com/tfs/DefaultCollection"
      }
    }
  }
}
```

---

## Troubleshooting

### Authentication Errors

```
Error: TF400813: The user is not authorized
```

Solutions:
1. Verify PAT hasn't expired
2. Check PAT has required scopes
3. Ensure PAT is for correct organization

### Server Not Starting

```
Error: Cannot find module '@azure/mcp-server-azure-devops'
```

Solutions:
1. Run `npm cache clean --force`
2. Try installing directly: `npm install -g @azure/mcp-server-azure-devops`

### Project Not Found

```
Error: Project 'XYZ' not found
```

Solutions:
1. Check project name spelling (case-sensitive)
2. Verify PAT has access to that project
3. Try using project ID instead of name

---

## Exercise: ADO Integration

### Exercise 6.3.1: Basic Setup

1. Create an ADO PAT with required permissions
2. Set environment variables
3. Configure MCP server
4. Verify connection: `List projects in my organization`

### Exercise 6.3.2: Work Item Management

1. List work items in a project
2. Create a new task
3. Update the task status
4. Add a comment to the task

### Exercise 6.3.3: PR Workflow

1. View open PRs in a repository
2. Get details of a specific PR
3. Add a comment to the PR
4. (If appropriate) Approve the PR

---

## Security Best Practices

### 1. Minimum Scope PATs

Create PATs with only required permissions:
- Read-only PAT for queries
- Full PAT for automation

### 2. Short Expiration

Set 90-day expiration and rotate regularly.

### 3. Named PATs

Use descriptive names:
- `Copilot-CLI-Dev`
- `Copilot-CLI-CI-ReadOnly`

### 4. Audit Access

Regularly review PAT usage in ADO:
- User Settings → Personal access tokens → Usage

---

## Key Takeaways

1. **PAT required** with appropriate scopes
2. **Environment variables** for credentials
3. **Rich capabilities** - work items, repos, pipelines
4. **Full workflows** possible entirely in CLI
5. **Multiple orgs** supported with multiple configs
6. **Security first** - minimum scope, regular rotation

---

## Next Section

Continue to [Section 8: End-to-End Workflows](../08-End-to-End-Workflows/README.md) for hands-on scenarios.
