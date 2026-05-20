# Model Context Protocol (MCP) Workshop

## Workshop Overview

A hands-on, 90-minute workshop on the **Model Context Protocol (MCP)** — what it is, where it's used, and how to build both a **local** MCP server (Python) and a **remote** MCP server hosted on **Azure Container Apps**.

**Duration**: 90 minutes
**Audience**: Software Engineers and Program Managers (mixed AI familiarity)
**Platforms**: Windows, macOS, Linux

This workshop builds on two earlier sessions in the AI Forum series:
- **GitHub Copilot CLI workshop** ([copilotcli2hrwkshp](../copilotcli2hrwkshp/))
- **Custom Agents workshop** ([customAgents](../customAgents/))

If you completed those, you already have most of the tooling we need.

---

## Table of Contents

| Section | Title | Duration | Description |
|---------|-------|----------|-------------|
| [00](./00-Prerequisites/) | Prerequisites | Pre-work | Install Python, uv, Azure CLI, Copilot CLI |
| [01](./01-What-Is-MCP/) | What is MCP? | 10 min | Concept, diagrams, transports |
| [02](./02-Where-MCP-Is-Used/) | Where MCP is Used | 10 min | Real-world server tour + live demo |
| [03](./03-Build-Local-MCP/) | Build a Local MCP — *Repo Doctor* | 35 min | Live-build a Python MCP server with FastMCP |
| **Break** | 5 minutes | | |
| [04](./04-Remote-MCP-on-Azure/) | Remote MCP on Azure | 25 min | Deploy Microsoft's Azure MCP to Container Apps |
| [05](./05-Wrap-Up/) | Wrap-up & Q&A | 5 min | Security, links, next steps |

**Total**: ~90 minutes

---

## Prerequisites

**Complete before the workshop!**

See [00-Prerequisites/README.md](./00-Prerequisites/README.md). Send it to participants **2 days prior**.

Quick checklist:
- [ ] GitHub account with Copilot license
- [ ] [GitHub Copilot CLI](https://github.com/github/copilot-cli) installed and authenticated
- [ ] Python 3.11+ and [uv](https://docs.astral.sh/uv/) installed
- [ ] [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed; `az login` works
- [ ] An Azure subscription where you can create a resource group + Container App
- [ ] A terminal you're comfortable with (PowerShell 7 on Windows; bash/zsh on macOS/Linux)

---

## Section Format

Each section follows **Concept → Practice → Q&A**, matching the style used in the earlier workshops.

1. **Concept**: Brief explanation with diagrams
2. **Practice**: Copy-pasteable steps you run yourself
3. **Q&A**: Quick multiple-choice questions to lock in understanding

---

## Schedule

| Time  | Section | Activity |
|-------|---------|----------|
| 0:00  | §1 | What is MCP — analogy + architecture |
| 0:10  | §2 | Where MCP is used — server tour + GitHub MCP demo |
| 0:20  | §3 | Build a local MCP — *Repo Doctor* |
| 0:55  | **Break** | 5 min |
| 1:00  | §4 | Deploy Microsoft Azure MCP to Azure Container Apps |
| 1:25  | §5 | Wrap-up & Q&A |

---

## What You'll Walk Away With

- A clear mental model of MCP: **host ↔ client ↔ server**, three primitives (tools, resources, prompts), two transports (stdio, HTTP)
- A working **Repo Doctor** MCP server you can keep using on your own repos
- A working **remote Azure MCP server** running on Azure Container Apps, callable from GitHub Copilot CLI
- An understanding of when to choose local vs. remote MCP, and the security considerations for each

---

## Hands-on Repos / Projects

- `03-Build-Local-MCP/server/` — reference Python implementation you can fall back to if you get stuck
- `04-Remote-MCP-on-Azure/manifests/` — Azure CLI scripts and example `mcp-config.json` snippets

---

## Quick Reference

### Copilot CLI MCP commands
```bash
/mcp                 # show configured MCP servers
/mcp add             # interactive add wizard
/mcp remove <name>   # remove an MCP server
/mcp help            # show help
```

### Where MCP config lives for Copilot CLI
```
~/.copilot/mcp-config.json
```

### Most common MCP transports
| Transport | Used by | When |
|-----------|---------|------|
| **stdio** | Local servers spawned as a subprocess | Default for local dev |
| **Streamable HTTP** | Remote servers reachable over the network | Sharing one server across users/teams |

---

## Files Structure

```
mcpwkshp/
├── README.md                              # This file
│
├── 00-Prerequisites/
│   └── README.md                          # Pre-workshop setup
│
├── 01-What-Is-MCP/
│   ├── README.md
│   └── 01-mcp-explained.md                # Concept + diagrams + Q&A
│
├── 02-Where-MCP-Is-Used/
│   ├── README.md
│   └── 01-real-world-examples.md          # Server tour + GitHub MCP demo
│
├── 03-Build-Local-MCP/
│   ├── README.md
│   ├── 01-scaffold.md                     # uv init + FastMCP hello
│   ├── 02-add-tools.md                    # Repo Doctor tools + resources
│   ├── 03-wire-to-copilot-cli.md          # mcp-config.json + verify + demo
│   └── server/                            # Reference implementation
│       ├── server.py
│       └── pyproject.toml
│
├── 04-Remote-MCP-on-Azure/
│   ├── README.md
│   ├── 01-azure-mcp-intro.md              # What Azure MCP is
│   ├── 02-deploy-to-aca.md                # Azure CLI deployment steps
│   ├── 03-connect-from-copilot.md         # Wire to Copilot CLI + demo
│   └── manifests/
│       └── deploy.azcli                   # All-in-one Azure CLI script
│
├── 05-Wrap-Up/
│   └── README.md                          # Recap, security, links
│
└── assets/
    └── diagrams/                          # ASCII diagrams (also inline)
```

---

## Contributing

Feedback and PRs welcome. Keep the **Concept → Practice → Q&A** rhythm and the ASCII-diagram style — it travels well across editors, slides, and terminals.

---

**Let's build! 🚀**
