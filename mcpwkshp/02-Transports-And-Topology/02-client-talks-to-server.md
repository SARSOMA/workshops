# Tutorial 2.2 — How an MCP Client Discovers, Spawns & Talks to a Server

---

## Concept

You've seen the *roles* (Host / Client / Server) in §1 and the *transports* in §2.1. This page joins them: what actually happens on the wire, from "Copilot CLI starts up" to "the model gets a tool result back."

### Step 1 — Discovery: reading the config

The host doesn't auto-discover MCP servers. It reads a config file. For Copilot CLI that's:

```
~/.copilot/
└── mcp-config.json          # all your MCP servers, local AND remote
```

A typical entry — one local stdio server and one remote HTTP server:

```json
{
  "mcpServers": {
    "repo-doctor": {
      "type": "local",
      "command": "uv",
      "args": ["run", "--directory", "/abs/path/repo-doctor/server", "python", "server.py"],
      "tools": ["*"]
    },
    "azure-mcp": {
      "type": "http",
      "url": "https://my-azure-mcp.azurecontainerapps.io/mcp",
      "tools": ["*"]
    }
  }
}
```

One file, every MCP server Copilot CLI should know about. Local ones use `type: "local"` + a command to run; remote ones use `type: "http"` + a URL.

### Step 2 — Spawn (local) or connect (remote)

**Local (stdio)** — when Copilot CLI starts, for each `type: "local"` entry it:

1. Spawns the command as a child process
2. Inherits stdin/stdout/stderr — stdin/stdout become the JSON-RPC wire, stderr is for logging
3. Sends an `initialize` JSON-RPC request and waits for the server's reply listing its capabilities

```
   Copilot CLI                                       Repo Doctor (child)
   ────────────                                      ────────────────────
   spawn("uv run … python server.py")  ─────────►   process starts
                                                     waits on stdin

   write to child's stdin:                           reads from stdin:
   {"method":"initialize", …}        ─────────────► {"method":"initialize", …}

   read from child's stdout:         ◄────────────  writes to stdout:
   {"result":{"capabilities":…,                     {"result":{"capabilities":…,
              "tools":{…}}}                                    "tools":{…}}}
```

**Remote (HTTP)** — there's no spawning; the host just opens an HTTPS connection to the URL and sends the same JSON-RPC `initialize` as a POST.

### Step 3 — A full request → response, end to end

Concrete trace of the simplest possible call:

```
1. USER:    "What's the health of this repo?"
                │
2. HOST:    decides: "I should call the repo-doctor MCP server"
                │  (model picked from the tool list it learned in initialize)
                │
3. CLIENT:  sends JSON-RPC over the transport (stdio pipe OR HTTPS POST):
            { "method": "tools/call",
              "params": { "name": "health_report", "arguments": { "path": "." } } }
                │
4. SERVER:  runs lint/test/build via subprocess, truncates output, returns:
            { "result": { "content": [...], "isError": false } }
                │
5. CLIENT:  receives result, hands to host
                │
6. HOST:    formats: "Lint passed, 12/12 tests passed, build OK. Score 92/100."
```

That's it. Six steps. **Same shape for every MCP call you'll ever make**, whether the server is on your laptop or in Azure — only the transport in step 3 changes.

### Step 4 — Lifecycle: when the conversation ends

- **stdio:** Copilot CLI closes the child's stdin → the server detects EOF and exits cleanly. New session → new child process.
- **HTTP:** The connection closes; the server keeps running and waits for the next client.

> 🐞 **Failure pattern you'll see in §3:** if a local server's command isn't on PATH (or it crashes during import), the child dies *before* sending its `initialize` reply. The client sees the stdio pipe close with no data → `MCP error -32000: Connection closed`. Always reproduce by running the exact command in a shell — a healthy stdio server should silently *hang*, waiting for JSON-RPC input.

---

## Practice — Watch the discovery happen

1. Launch Copilot CLI:
   ```bash
   copilot
   ```
2. Inside the session:
   ```
   /mcp
   ```
3. You should see the **built-in GitHub MCP** listed as `✓ Ready`. That "Ready" status means Copilot CLI **spawned (or connected to) the server and got an `initialize` reply** with its tool list.

> Don't add anything yet — we'll add Repo Doctor in §3 and Azure MCP in §4.

---

## Q&A

### Question 1
You add a new MCP server to `mcp-config.json` but `/mcp` doesn't show it. What's the most likely cause?

A) The server is misconfigured
B) Copilot CLI only reads `mcp-config.json` at startup — you need to restart it
C) The config file is in the wrong place
D) Both B and C are common

<details><summary>Answer</summary>

**D.** Restart the CLI; double-check the path is exactly `~/.copilot/mcp-config.json` (`%USERPROFILE%\.copilot\mcp-config.json` on Windows).

</details>

### Question 2
A local stdio MCP server returns `MCP error -32000: Connection closed`. What does that *actually* mean?

A) The network dropped
B) The child process exited (or never started) before completing the `initialize` handshake
C) Your auth token expired
D) The model refused to call it

<details><summary>Answer</summary>

**B.** No initialize reply on the stdio pipe → client gives up with "Connection closed". Reproduce by running the exact command from a shell — you'll see the real error (usually "command not found" or a Python import traceback).

</details>

---

## Next

→ [§3 — Build a Local MCP: *Repo Doctor*](../03-Build-Local-MCP/README.md)
