# 4.3 — Connect from Copilot CLI and try it

---

## Concept

A remote MCP server registers in Copilot CLI almost identically to a local one — same `mcp-config.json` file, different `type`.

```json
{
  "mcpServers": {
    "azure-mcp-remote": {
      "type": "http",
      "url": "https://<your-aca-fqdn>/mcp",
      "tools": ["*"]
    }
  }
}
```

That's it. No command, no stdio — just a URL.

> If you have a production deployment with Entra auth on the inbound (i.e., you removed `--dangerously-disable-http-incoming-auth`), you'd also include the appropriate `Authorization` header. We're skipping that for the demo.

---

## Practice

### Step 1 — Add the server

Pick your favourite (we recommend the wizard so you don't typo the JSON):

#### Option A: `/mcp add` wizard

Inside a Copilot CLI session:

```
/mcp add
```

| Field | Value |
|-------|-------|
| Server Name | `azure-mcp-remote` |
| Server Type | `2` (HTTP) |
| URL | `https://<your-aca-fqdn>/mcp`  ← from §4.2 step 5 |
| Headers | *(leave blank)* |
| Tools | `*` |

Press **Ctrl+S** (or **Cmd+S**) to save.

#### Option B: edit `~/.copilot/mcp-config.json`

Add this entry (merge with whatever else is in `mcpServers`):

```json
{
  "mcpServers": {
    "azure-mcp-remote": {
      "type": "http",
      "url": "https://<your-aca-fqdn>/mcp",
      "tools": ["*"]
    }
  }
}
```

### Step 2 — Verify

Restart Copilot CLI, then:

```
/mcp
```

You should see `azure-mcp-remote` listed. If the row shows it failed to connect, double-check:
- The URL ends in `/mcp` (not just the FQDN)
- ACA is up: `az containerapp show -n azmcp-demo -g rg-mcp-demo --query properties.runningStatus`

### Step 3 — Drive it from natural language

Try each of these in Copilot CLI. Watch the tool-call output to see which Azure MCP tool got picked.

```
List my Azure subscriptions.
```

```
What resource groups are in subscription "<your-sub-name>"?
```

```
Show me everything in resource group "rg-mcp-demo".
```

```
What's the FQDN of the Container App I just deployed? Use the Azure MCP server, not the CLI.
```

> Notice: every one of these is a call going over HTTPS from your laptop to Azure Container Apps. The model never sees your Azure credentials — the managed identity inside ACA does the talking to ARM.

### Step 4 — Show both servers working together

If §3's `repo-doctor` is still configured, ask Copilot CLI to do something that uses both:

```
Run a health check on this repo, then list my Azure resource groups so we can decide where to deploy it.
```

Copilot routes the first half to **Repo Doctor (stdio, local)** and the second half to **Azure MCP (HTTP, remote)** — two MCP servers, two transports, one conversation.

---

## What we just demonstrated

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Copilot CLI   ───── stdio ─────►  Repo Doctor   (Python, local) │
│  (single host) ───── HTTPS  ────►  Azure MCP     (ACA, remote)   │
│                                                                  │
│  One conversation. One agent. Two MCP servers. Two transports.   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

That's the whole point.

---

## Q&A

### Question 1
The only difference between registering a local MCP and a remote MCP in Copilot CLI is…

A) The model
B) `type: "local"` + `command` vs. `type: "http"` + `url`
C) Whether you need Python installed
D) The MCP protocol

<details><summary>Answer</summary>

**B.** Same config file, same protocol, different transport.

</details>

### Question 2
When you ran "List my Azure subscriptions", how did Copilot CLI authenticate to Azure?

A) It used your `az login` token
B) It didn't — the ACA-hosted Azure MCP used its **managed identity** to call Azure
C) The model included credentials in the prompt
D) Anonymous access to ARM

<details><summary>Answer</summary>

**B.** The client only talks to the MCP server. The MCP server uses its own identity to call downstream Azure APIs.

</details>

---

## Next

→ [4.4 — Auth deep-dive: incoming vs outgoing, OAuth 2.1, OBO](./04-auth-deep-dive.md)
→ [§5 — Wrap-up](../05-Wrap-Up/README.md)
