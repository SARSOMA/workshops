# 00 — Prerequisites

**Please complete these steps before the workshop.** If anything fails, ping the workshop channel — we want to start coding, not installing.

> ⏱️ Allow ~20 minutes if you're starting from scratch. Most attendees who completed the earlier Copilot CLI / Custom Agents workshops already have most of this.

---

## 1. Accounts and licenses

- [ ] GitHub account with an active **Copilot** license
- [ ] Azure subscription where you can create resources (a personal MSDN sub or a sandbox sub works fine)

---

## 2. CLI tooling

| Tool | Why we need it | Install link / command |
|------|----------------|------------------------|
| **Git** | Repo Doctor reads git history | https://git-scm.com/downloads |
| **GitHub CLI (`gh`)** | Quality-of-life for GitHub | https://cli.github.com |
| **GitHub Copilot CLI** | The MCP **client** we'll use all workshop | https://github.com/github/copilot-cli |
| **Python 3.11+** | The local MCP server is Python | https://www.python.org/downloads |
| **uv** | Fast Python package manager (recommended over pip for this workshop) | https://docs.astral.sh/uv/getting-started/installation/ |
| **Azure CLI** | Deploy the remote MCP to Azure Container Apps | https://learn.microsoft.com/cli/azure/install-azure-cli |
| **Node.js LTS** *(optional)* | If you want to try `npx @azure/mcp` locally | https://nodejs.org |

### Verify the basics

```bash
git --version
gh --version
copilot --version
python --version          # 3.11+
uv --version
az --version
```

---

## 3. Authenticate

```bash
# GitHub CLI
gh auth login

# Copilot CLI — first run will walk you through device flow
copilot

# Azure CLI
az login
az account show           # confirm you're on the sub you want
```

If you have multiple subscriptions, set the one you'll use for the workshop:

```bash
az account set --subscription "<your-subscription-name-or-id>"
```

---

## 4. Verify Copilot CLI is happy

Inside a Copilot CLI session, run:

```
/mcp
```

You should see a list of MCP servers (the GitHub MCP server is built in). If you see that, you're good.

> If `/mcp` errors out, run `/help` to confirm your Copilot CLI version is recent enough.

---

## 5. Pre-pull (optional but recommended)

To save time during the workshop, pre-pull / pre-resolve the heavy dependencies:

```bash
# Python MCP SDK (for §3)
uv tool install "mcp[cli]" || true

# Azure MCP container image (for §4)
docker pull mcr.microsoft.com/azure-sdk/azure-mcp:latest   # only if Docker is installed; not required
```

Neither of these is strictly required — `uv` will resolve at workshop time — but pre-pulling avoids "the conference Wi-Fi is slow" tears.

---

## 6. Bring a real repo

For the **Repo Doctor** section, we'll run lint/test/build on a real local repo. Bring one of:

- A small **Python** project you know well (e.g., a side project with `pyproject.toml` or `requirements.txt`), **or**
- A **Node.js** project with `package.json`, **or**
- This very `workshops` repo (it has markdown and works for the demo)

We'll use this as the "patient" Repo Doctor diagnoses.

---

## ✅ Done

If all the above succeeded, you're ready. See you at the session!
