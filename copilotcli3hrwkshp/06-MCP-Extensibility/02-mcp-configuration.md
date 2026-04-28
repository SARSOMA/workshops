# Tutorial 6.2: Configuring MCP Servers

## Introduction

This tutorial covers how to add, configure, and manage MCP servers in Copilot CLI to extend its capabilities.

## MCP Configuration

### Configuration File

MCP servers are configured in:
```
~/.copilot/mcp-config.json
```

Override location with `COPILOT_HOME` environment variable.

### Basic Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

---

## Adding MCP Servers

### Method 1: Using /mcp Command

Interactive configuration:
```
/mcp add
```

Fill in the form:
- **Name**: Unique identifier
- **Command**: Executable to run
- **Arguments**: Command arguments
- **Environment**: Variables needed

Press `Ctrl+S` to save.

### Method 2: Direct JSON Edit

Edit `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

### Method 3: Command-Line Initialization

For some servers:
```bash
npx @modelcontextprotocol/create-server filesystem
```

---

## Common MCP Server Configurations

### GitHub (Built-in)

Usually pre-configured, but can be customized:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Filesystem

Access local filesystem:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/you/projects",
        "/Users/you/documents"
      ]
    }
  }
}
```

### PostgreSQL

Database access:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost:5432/db"
      }
    }
  }
}
```

### Slack

Slack integration:

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "T0123456789"
      }
    }
  }
}
```

---

## Environment Variable Handling

### Inline Values (Not Recommended for Secrets)

```json
{
  "env": {
    "API_KEY": "actual-key-value"
  }
}
```

### Environment Variable References (Recommended)

```json
{
  "env": {
    "API_KEY": "${API_KEY}"
  }
}
```

Set in your shell:
```bash
export API_KEY="your-actual-key"
```

### Multiple Variables

```json
{
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}",
    "GITHUB_ENTERPRISE_URL": "${GH_ENTERPRISE_URL}"
  }
}
```

---

## Managing MCP Servers

### View Status

```
/mcp
```

Shows:
- Configured servers
- Running status
- Available tools

### Restart Servers

```
/mcp restart server-name
```

### Remove a Server

Edit `~/.copilot/mcp-config.json` and remove the server entry.

### Disable Temporarily

Add `"disabled": true`:

```json
{
  "mcpServers": {
    "expensive-server": {
      "command": "...",
      "disabled": true
    }
  }
}
```

---

## Troubleshooting MCP

### Common Issues

#### Server Won't Start

1. Check command exists:
   ```bash
   which npx
   ```

2. Try running manually:
   ```bash
   npx -y @modelcontextprotocol/server-github
   ```

3. Check for missing environment variables

#### Authentication Errors

1. Verify token is set:
   ```bash
   echo $GITHUB_TOKEN
   ```

2. Check token permissions

3. Regenerate token if expired

#### Connection Timeouts

1. Check network connectivity
2. Verify firewall rules
3. Try increasing timeout in config

### Debug Mode

Run Copilot CLI with verbose logging:
```bash
DEBUG=mcp:* copilot
```

### View Server Logs

Check MCP server output:
```bash
copilot --mcp-debug
```

---

## Security Considerations

### 1. Token Management

❌ **Never commit tokens:**
```json
{
  "env": {
    "TOKEN": "ghp_actualtokenvalue123"
  }
}
```

✅ **Use environment variables:**
```json
{
  "env": {
    "TOKEN": "${MY_TOKEN}"
  }
}
```

### 2. Restrict Access

For filesystem server, only allow specific directories:
```json
{
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/specific/project",
    "--read-only"
  ]
}
```

### 3. Review Server Sources

Only use MCP servers from:
- Official `@modelcontextprotocol` packages
- Trusted organizations
- Audited open-source projects

### 4. Principle of Least Privilege

Configure only the MCP servers you need.

---

## Exercise: Configure MCP

### Exercise 6.2.1: Add Filesystem Server

1. Create a test directory:
   ```bash
   mkdir ~/mcp-test-data
   echo "Test content" > ~/mcp-test-data/test.txt
   ```

2. Add filesystem server to config:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-filesystem", "~/mcp-test-data"]
       }
     }
   }
   ```

3. Restart Copilot CLI

4. Test:
   ```
   Read the contents of test.txt using the filesystem server
   ```

### Exercise 6.2.2: View MCP Tools

1. Open Copilot CLI
2. Check servers: `/mcp`
3. Ask: `What tools do you have available from MCP servers?`
4. Try using a specific tool

---

## Best Practices

### 1. Organize Servers by Purpose

```json
{
  "mcpServers": {
    "dev-github": { ... },
    "dev-postgres": { ... },
    "dev-filesystem": { ... }
  }
}
```

### 2. Document Your Configuration

Add comments (not in JSON, but in adjacent docs):
```markdown
# MCP Configuration Notes

## github
- Uses PAT from GITHUB_TOKEN
- Required permissions: repo, workflow

## postgres  
- Connects to local dev database
- Read-only access
```

### 3. Version Control Config (Without Secrets)

Share configuration structure, not values:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 4. Test Servers Individually

Before adding to Copilot:
```bash
GITHUB_TOKEN=xxx npx -y @modelcontextprotocol/server-github
```

---

## Key Takeaways

1. **Config location**: `~/.copilot/mcp-config.json`
2. **Add with /mcp**: Interactive or edit JSON directly
3. **Use env vars**: For secrets and sensitive data
4. **Verify with /mcp**: Check server status
5. **Security first**: Audit servers, restrict access

---

## Next Tutorial

Continue to [Tutorial 6.3: Azure DevOps Integration](./03-azure-devops.md) for ADO-specific MCP setup.
