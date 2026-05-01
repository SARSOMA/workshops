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

## Node.js 18+ (Required for Part 2)

Install Node.js 18 or later. Verify your version:

```bash
node --version
```

If you need to install or update:

- **macOS/Linux (via nvm):**
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  nvm install 18
  nvm use 18
  ```
- **Windows (via nvm-windows):** Download from [nvm-windows releases](https://github.com/coreybutler/nvm-windows/releases), then:
  ```powershell
  nvm install 18
  nvm use 18
  ```
- **Direct download:** [https://nodejs.org/](https://nodejs.org/) — choose the LTS version

npm is included with Node.js. Verify:

```bash
npm --version
```
