# §3 — Build a Local MCP: *Repo Doctor* 🧪

**Duration**: 35 min

**Goal**: by the end of this section you have a working Python MCP server that diagnoses the health of any local repo — runs its lint, tests, and build, then writes a one-page health report. You'll wire it into GitHub Copilot CLI and use it on a real project.

## Why this project

Every SWE and PM has wondered "is this repo healthy?". Repo Doctor turns that into a tool the AI can call:

- Detects what kind of project you're in (Node / Python / Rust / Go)
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

## Reference code

If you get stuck or fall behind, [`server/`](./server/) contains a complete working implementation. You can point Copilot CLI directly at it.
