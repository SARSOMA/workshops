# Prerequisites

Before the workshop, ensure you have vscode copilot chat and **at least one** of the following cli tools installed and authenticated with your **Microsoft corp GitHub account**.

---

## VS Code with GitHub Copilot Chat

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Toggle the chat to access vscode copilot chat
3. Sign in with your Microsoft corp GitHub account in the account section, and turn on copilot features. This should be in the bottom left corner.

## Option 1: GitHub Copilot CLI

1. Install the [GitHub CLI](https://cli.github.com/)
2. Authenticate with your Microsoft corp GitHub account:
   ```bash
   gh auth login
   ```
3. Install the Copilot CLI extension:
   ```bash
   gh extension install github/gh-copilot
   ```

## Option 2: Agency

Agency is Microsoft's internal agent platform — a thin client layer around agentic CLIs (GitHub Copilot CLI, Claude Code) that adds Microsoft-specific integrations: internal tools (Azure DevOps, Bluebird MCP), custom agent definitions, and streamlined auth setup.

1. Follow the installation instructions in the [Agency documentation](https://eng.ms/docs/coreai/devdiv/one-engineering-system-1es/1es-jacekcz/startrightgitops/agency)
2. Agency handles Microsoft-specific authentication during setup — follow the prompts to sign in with your Microsoft corp GitHub account
3. Verify the installation by launching Agency and confirming you can start a session

---

## Verifying Authentication

Run the following to confirm you're signed in with the correct account:

```bash
gh auth status
```

You should see your `@microsoft.com`-associated GitHub username listed.

---

## Python 3.10+ (Required for Part 2)

Install Python 3.10 or later. Verify your version:

```bash
python3 --version
```

If you need to install or update:

- **macOS (via Homebrew):**
  ```bash
  brew install python@3.12
  ```
- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update && sudo apt install python3 python3-pip python3-venv
  ```
- **Windows:** Download from [https://www.python.org/downloads/](https://www.python.org/downloads/) — check "Add Python to PATH" during installation

Verify pip is available:

```bash
pip3 --version
```

Install the required Python packages:

```bash
pip install mcp github-copilot-sdk
```

---

## Node.js 18+ (Required for ADO MCP Server)

The ADO MCP server runs via `npx`, which requires Node.js. Verify your version:

```bash
node --version
```

If you need to install:

- **macOS (via Homebrew):**
  ```bash
  brew install node
  ```
- **Linux (Debian/Ubuntu):**
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt install -y nodejs
  ```
- **Windows:** Download from [https://nodejs.org/](https://nodejs.org/) — choose the LTS version

Verify npm/npx are available:

```bash
npx --version
```

---

## ADO MCP Server (Required for Part 1 Exercise)

The Part 1 exercise uses the Azure DevOps MCP server so agents can fetch pull request data. You need to add it to your VS Code MCP configuration.

### Step 1 — Add the MCP config

Open (or create) `.vscode/mcp.json` in your workspace and add the `ado` server:

```json
{
  "servers": {
    "ado": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "msazure"]
    }
  }
}
```

The organization is `msazure` and the default project is `one` for all workshop participants.

> **Note:** If you already have other MCP servers configured, just add the `"ado"` entry inside the existing `"servers"` object.

### Step 2 — Authenticate with Azure DevOps

The first time the MCP server runs, it will prompt you to authenticate. You can also pre-authenticate by running:

```bash
npx -y @azure-devops/mcp msazure
```

Follow the browser-based auth flow to sign in with your Microsoft account.

### Step 3 — Verify in VS Code

1. Open VS Code in your workspace
2. Open Copilot Chat and type a message — the ADO MCP tools should now be available
3. You can confirm by checking the tools list in the agent dropdown (gear icon → MCP Servers) or by asking an agent that has `ado/*` tools to list a PR
