# §3 — Build a Local MCP: *Repo Doctor* 🧪

**Duration**: 35 min

**Goal**: by the end of this section you have a working Python MCP server that diagnoses the health of any local repo — runs its lint, tests, and build, then writes a one-page health report. You'll wire it into GitHub Copilot CLI and use it on a real project.

## Why this project

Every SWE and PM has wondered "is this repo healthy?". Repo Doctor turns that into a tool the AI can call:

- Detects what kind of project you're in (Node / Python / Rust / Go / .NET)
- Runs the right lint / test / build commands
- Summarises potentially-huge subprocess output into a tight report (this is a great place to teach **context hygiene**)
- Exposes a markdown template + the last report as **resources**

## What you'll learn

- Scaffolding a Python MCP server with [FastMCP](https://github.com/modelcontextprotocol/python-sdk)
- The difference between **tools** (verbs) and **resources** (nouns)
- How the LLM picks which tool to call (and why your descriptions matter)
- Truncation / timeout patterns so subprocess output doesn't blow up the context window
- Registering a stdio MCP server with Copilot CLI

## Pages

1. [01-scaffold.md](./01-scaffold.md) — uv init, install MCP SDK, first `hello` tool
2. [02-add-tools.md](./02-add-tools.md) — add all the Repo Doctor tools + resources
3. [03-wire-to-copilot-cli.md](./03-wire-to-copilot-cli.md) — register with Copilot CLI, verify, demo

## ⚡ Quick start (clone-and-go)

If you just want a working server in 60 seconds — skip the build steps and use the reference code:

```bash
# 1. Clone (or pull) this repo, then:
cd mcpwkshp/03-Build-Local-MCP/server
uv sync              # one-time — installs deps into .venv

# 2. Grab the absolute path
pwd                  # macOS/Linux
(Get-Location).Path  # Windows PowerShell
```

Add to `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "repo-doctor": {
      "type": "local",
      "command": "uv",
      "args": ["run", "--directory", "<ABS_PATH_TO_server_FOLDER>", "python", "server.py"],
      "tools": ["*"]
    }
  }
}
```

Restart Copilot CLI → `/mcp` should show `repo-doctor ✓ Ready`.

> Prerequisites: [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (`winget install --id=astral-sh.uv` on Windows). Open a fresh shell after installing so PATH picks it up.

## Reference code

If you get stuck or fall behind, [`server/`](./server/) contains a complete working implementation. You can point Copilot CLI directly at it.
