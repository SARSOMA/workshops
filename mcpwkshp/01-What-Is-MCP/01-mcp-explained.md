# Tutorial 1.1 — MCP Explained

---

## Concept

### The one-liner

> **MCP is USB-C for AI** — one open protocol that lets any AI client plug into any tool or data source.

Before MCP, every AI assistant + every tool was its own custom integration. M assistants × N tools = M×N point-to-point connectors that all had to be re-implemented, re-tested, and re-secured. MCP collapses that to M + N: each side only has to speak one protocol.

```
┌─────────────────────────────────────────────────────────────────┐
│            BEFORE MCP                                            │
│  Copilot  ─┬─► GitHub adapter                                    │
│            ├─► Azure adapter                                     │
│            ├─► Postgres adapter                                  │
│            └─► Figma adapter                                     │
│  Claude   ─┬─► GitHub adapter (rewritten)                        │
│            ├─► Azure adapter (rewritten)                         │
│            └─► …                                                 │
│  Cursor   ─┬─► …                                                 │
│                                                                  │
│  M clients × N tools = M×N bespoke integrations                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│            WITH MCP                                              │
│                                                                  │
│  Copilot ─┐                       ┌─► GitHub MCP server          │
│  Claude  ─┼──► MCP (one protocol) ┼─► Azure MCP server           │
│  Cursor  ─┘                       ├─► Postgres MCP server        │
│                                   └─► Figma MCP server           │
│                                                                  │
│  M clients + N servers = M+N integrations                        │
└─────────────────────────────────────────────────────────────────┘
```

### Who's who in MCP

```
┌──────────────────────────────────────────────────────────────────┐
│                      MCP ARCHITECTURE                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                       HOST (the AI app)                    │  │
│  │                 e.g. Copilot CLI, VS Code, Claude          │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐    │  │
│  │  │  Model     │  │  Tool      │  │  MCP CLIENT        │    │  │
│  │  │  + Agent   │◄─┤  Router    │◄─┤  (protocol talker) │    │  │
│  │  └────────────┘  └────────────┘  └─────────┬──────────┘    │  │
│  └─────────────────────────────────────────────┼──────────────┘  │
│                                                │                 │
│                JSON-RPC over stdio  OR  HTTP   │                 │
│                                                ▼                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                     MCP SERVER                             │  │
│  │   exposes:  Tools (do)  •  Resources (read)  •  Prompts    │  │
│  └────────────────────────┬───────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  THE REAL WORLD                                            │  │
│  │  GitHub API • Azure ARM • your filesystem • Postgres • …   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Three things to remember:

| Role | What it is | In our workshop |
|------|------------|-----------------|
| **Host** | The app the human talks to | GitHub Copilot CLI |
| **MCP Client** | Embedded inside the host; speaks MCP | The bit of Copilot CLI that handles `/mcp` |
| **MCP Server** | Exposes tools/resources/prompts | Our Repo Doctor (§3) and Azure MCP (§4) |

### The three primitives a server can expose

```
┌──────────────────────────────────────────────────────────────────┐
│  TOOLS  (actions — the agent CALLS to DO something)              │
│   • create_pr  • run_tests  • deploy_vm  • send_email            │
│   • can have side effects                                        │
├──────────────────────────────────────────────────────────────────┤
│  RESOURCES  (data — the agent READS to LEARN something)          │
│   • list_repos  • file_contents  • last_health_report            │
│   • read-only                                                    │
├──────────────────────────────────────────────────────────────────┤
│  PROMPTS  (templates — pre-baked instructions)                   │
│   • security_review_checklist  • deploy_runbook                  │
│   • picked by the user (often as a slash command)                │
└──────────────────────────────────────────────────────────────────┘
```

> Mental shortcut: **Tools = verbs, Resources = nouns, Prompts = recipes.**

### The two transports you'll actually see

```
┌──────────────────────────────┐    ┌──────────────────────────────┐
│  stdio (local)               │    │  Streamable HTTP (remote)    │
│                              │    │                              │
│  Host spawns the server as   │    │  Host opens an HTTPS         │
│  a subprocess.               │    │  connection to a URL.        │
│  JSON-RPC over stdin/stdout. │    │  JSON-RPC + SSE over HTTP.   │
│                              │    │                              │
│  ✓ Zero network surface      │    │  ✓ Share one server with     │
│  ✓ Easy: just run a command  │    │    many users                │
│  ✗ One server per user/host  │    │  ✓ Centralised auth          │
│                              │    │  ✗ Need to host + secure it  │
│  Our Repo Doctor (§3)        │    │  Our Azure MCP on ACA (§4)   │
└──────────────────────────────┘    └──────────────────────────────┘
```

### A full request → response, end to end

```
1. USER:    "What's the health of this repo?"
                │
2. HOST:    decides: "I should call the repo-doctor MCP server"
                │
3. CLIENT:  sends JSON-RPC over stdio:
            { "method": "tools/call",
              "params": { "name": "health_report", "arguments": { "path": "." } } }
                │
4. SERVER:  runs lint/test/build via subprocess, summarises
                │
5. CLIENT:  receives result
                │
6. HOST:    formats: "Lint passed, 12/12 tests passed, build OK. Score 92/100."
```

### Where MCP config lives in Copilot CLI

```
~/.copilot/
└── mcp-config.json          # all your MCP servers, both stdio and remote
```

Example shape (we'll write a real one in §3):

```json
{
  "mcpServers": {
    "repo-doctor": {
      "type": "local",
      "command": "uv",
      "args": ["run", "--project", "/abs/path/repo-doctor", "server.py"],
      "tools": ["*"]
    }
  }
}
```

---

## Practice

### Quick lap around your already-installed MCP

1. Launch Copilot CLI:
   ```bash
   copilot
   ```
2. Inside the session:
   ```
   /mcp
   ```
3. You should see the **built-in GitHub MCP** listed. That's MCP working for you already — every time you've asked Copilot CLI to "list my open PRs", that's a tool call going through the MCP client embedded in Copilot.

> Don't add anything yet — we'll add Repo Doctor and Azure MCP in §3 and §4.

---

## Q&A

### Question 1
What problem does MCP solve?

A) It makes models faster
B) It encrypts traffic between the model provider and you
C) It standardises how AI apps connect to external tools and data — turning M×N integrations into M+N
D) It replaces the LLM with a smaller one

<details><summary>Answer</summary>

**C.** MCP is the integration protocol — clients implement it once, servers implement it once, anything can talk to anything.

</details>

### Question 2
Which of these is **not** an MCP primitive?

A) Tools
B) Resources
C) Prompts
D) Fine-tunes

<details><summary>Answer</summary>

**D.** MCP servers expose Tools, Resources, and Prompts. Fine-tuning is unrelated.

</details>

### Question 3
You want one MCP server shared by your whole team. Which transport do you pick?

A) stdio
B) Streamable HTTP

<details><summary>Answer</summary>

**B.** stdio servers are subprocesses of the local host — not shareable. HTTP MCP servers can be deployed once and used by many clients.

</details>

---

## Next

→ [§2 — Where MCP is used](../02-Where-MCP-Is-Used/01-real-world-examples.md)
