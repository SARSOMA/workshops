# Tutorial 2.2: Configuration Layers

## Introduction

GitHub Copilot CLI supports multiple layers of configuration, allowing you to customize behavior at the user, repository, and organization levels. Understanding this hierarchy helps you set up efficient workflows.

## Configuration Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                     HIGHEST PRIORITY                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Command-line flags                                        │  │
│  │  copilot --model gpt-5 --allow-all-tools                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Environment Variables                                     │  │
│  │  COPILOT_HOME, GITHUB_TOKEN, etc.                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Repository-level Configuration                            │  │
│  │  .github/copilot-instructions.md                           │  │
│  │  .github/instructions/**/*.instructions.md                 │  │
│  │  .github/agents/*.md                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  User-level Configuration                                  │  │
│  │  ~/.copilot/settings.json                                  │  │
│  │  ~/.copilot/copilot-instructions.md                        │  │
│  │  ~/.copilot/mcp-config.json                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Organization/Enterprise Configuration                     │  │
│  │  .github-private repository /agents directory              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                     LOWEST PRIORITY                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## User-Level Configuration

### Configuration Directory

Default location: `~/.copilot/`

Override with: `export COPILOT_HOME=/path/to/config`

### Directory Structure

```
~/.copilot/
├── settings.json              # Main settings file
├── mcp-config.json            # MCP server configurations
├── lsp-config.json            # Language server configurations
├── copilot-instructions.md    # Global custom instructions
├── agents/                    # Custom agent definitions
│   └── my-agent.md
└── session-state/             # Session persistence data
```

### settings.json

Your primary configuration file:

```json
{
  "theme": "dark",
  "model": "claude-sonnet-4-5",
  "experimental": false,
  "telemetry": true,
  "autoCompact": true
}
```

### Key Settings

| Setting | Type | Description |
|---------|------|-------------|
| `theme` | string | Color theme: "dark", "light", "system" |
| `model` | string | Default AI model |
| `experimental` | boolean | Enable experimental features |
| `autoCompact` | boolean | Auto-compress context at 95% |
| `telemetry` | boolean | Send usage data to GitHub |

### Viewing Current Configuration

```bash
copilot help config
```

---

## Repository-Level Configuration

### Supported Files

Files are read from both **git root** and **current working directory**:

| File/Location | Purpose |
|---------------|---------|
| `.github/copilot-instructions.md` | Repository-wide instructions |
| `.github/instructions/**/*.instructions.md` | Path-specific instructions |
| `.github/agents/*.md` | Custom agents for this repo |
| `.github/lsp.json` | Repository-level LSP config |
| `CLAUDE.md` | Instructions file (Claude-style) |
| `GEMINI.md` | Instructions file (Gemini-style) |
| `AGENTS.md` | Agent instructions |

### Example: copilot-instructions.md

```markdown
# Project Guidelines

## Tech Stack
- TypeScript with strict mode
- React 18 with hooks
- Express.js backend
- PostgreSQL database

## Coding Standards
- Use functional components only
- Prefer async/await over .then()
- All functions must have JSDoc comments
- Use Prettier for formatting

## Testing
- Write tests for all new functions
- Use Jest for unit tests
- Use Cypress for E2E tests
- Run `npm test` before committing

## Build & Deploy
- Build: `npm run build`
- Test: `npm test`
- Deploy: GitHub Actions handles CI/CD
```

### Path-Specific Instructions

Create files matching `.github/instructions/**/*.instructions.md`:

**`.github/instructions/api.instructions.md`**
```markdown
# API Development Instructions

When working on API endpoints:
- Follow REST conventions
- Include request/response examples
- Document with OpenAPI 3.0 spec
- Add rate limiting to all endpoints
```

**`.github/instructions/frontend/react.instructions.md`**
```markdown
# React Component Guidelines

- Use functional components with TypeScript
- Props interfaces should be named ComponentNameProps
- Use CSS Modules for styling
- Implement loading and error states
```

---

## Organization-Level Configuration

### Using .github-private Repository

Organizations can define shared configurations:

```
.github-private/
└── agents/
    ├── security-reviewer.md
    ├── documentation-writer.md
    └── code-standards.md
```

These agents are available to all repositories in the organization.

---

## Environment Variables

### Essential Variables

| Variable | Purpose |
|----------|---------|
| `COPILOT_HOME` | Custom config directory location |
| `GITHUB_TOKEN` | Authentication token (PAT) |
| `GH_TOKEN` | Alternative auth token |
| `HTTPS_PROXY` | Proxy for HTTPS connections |
| `HTTP_PROXY` | Proxy for HTTP connections |

### Setting Variables

**Linux/macOS (~/.bashrc or ~/.zshrc):**
```bash
export COPILOT_HOME="$HOME/.my-copilot-config"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

**Windows (PowerShell profile):**
```powershell
$env:COPILOT_HOME = "$HOME\.my-copilot-config"
$env:GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"
```

### View Environment Info

```bash
copilot help environment
```

---

## MCP Server Configuration

### Configuration File

`~/.copilot/mcp-config.json`:

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
    "azure-devops": {
      "command": "npx",
      "args": ["-y", "@azure/mcp-server"],
      "env": {
        "AZURE_DEVOPS_PAT": "${ADO_TOKEN}"
      }
    }
  }
}
```

### Adding MCP Servers via CLI

```
/mcp add
```

Fill in the configuration form and save with `Ctrl+S`.

---

## Exercise: Configure Your Environment

### Exercise 2.2.1: Explore User Configuration

1. View your config directory:
   ```bash
   ls -la ~/.copilot/
   ```

2. Check current settings:
   ```bash
   cat ~/.copilot/settings.json
   ```

3. View loaded environment:
   ```
   /env
   ```

### Exercise 2.2.2: Create Repository Instructions

1. Navigate to a test project:
   ```bash
   mkdir -p ~/copilot-test-project
   cd ~/copilot-test-project
   git init
   ```

2. Create instructions file:
   ```bash
   mkdir -p .github
   cat > .github/copilot-instructions.md << 'EOF'
   # Test Project Guidelines
   
   This is a test project for learning Copilot CLI.
   
   ## Rules
   - Use Python 3.10+
   - Follow PEP 8 style guide
   - Include type hints
   
   ## Testing
   - Run tests with: pytest
   EOF
   ```

3. Launch Copilot CLI and verify:
   ```
   /instructions
   ```
   
   You should see your custom instructions loaded.

### Exercise 2.2.3: Test Instruction Override

1. Create a global instruction:
   ```bash
   echo "Always be concise in responses." > ~/.copilot/copilot-instructions.md
   ```

2. Launch Copilot CLI in your test project
3. Run `/instructions` to see both loaded
4. Ask: "How should I format Python code?"
5. Notice it uses project-specific guidance

---

## Viewing Active Configuration

### /instructions Command

Shows which instruction files are currently loaded:

```
/instructions
```

Output:
```
Active instructions:
✓ ~/.copilot/copilot-instructions.md
✓ .github/copilot-instructions.md
```

### /env Command

Shows full environment:

```
/env
```

Output:
```
Instructions:
  ~/.copilot/copilot-instructions.md
  .github/copilot-instructions.md

MCP Servers:
  github (running)
  
Agents:
  explore (built-in)
  task (built-in)
  code-review (built-in)
  
Skills:
  (none configured)
```

---

## Best Practices

### 1. Layer Appropriately

| Scope | Use For |
|-------|---------|
| User | Personal preferences, common settings |
| Repository | Project-specific guidelines |
| Organization | Company standards, security rules |

### 2. Keep Instructions Clear

✅ **Good:**
```markdown
## Testing
Run tests with `npm test` before committing.
All new functions require unit tests.
```

❌ **Bad:**
```markdown
Make sure you test stuff and write good code.
```

### 3. Commit Repository Config

Include in version control:
- `.github/copilot-instructions.md`
- `.github/instructions/**/*.instructions.md`
- `.github/agents/*.md`

Don't commit:
- Personal tokens or credentials
- User-specific preferences

---

## Key Takeaways

1. **Hierarchy Matters**: Command-line > Environment > Repository > User > Organization
2. **Instructions Combine**: All instruction files are merged, not replaced
3. **Repository-Specific**: Use `.github/copilot-instructions.md` for project rules
4. **MCP Configuration**: Stored in `~/.copilot/mcp-config.json`
5. **View with /env**: Always check loaded config with `/env` or `/instructions`

---

## Next Tutorial

Continue to [Tutorial 2.3: Context Building](./03-context.md) to learn how Copilot understands your project.
