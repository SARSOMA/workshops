# §5 — Wrap-up

You've built two MCP servers — one local stdio, one remote HTTP on Azure — and used both from the same Copilot CLI session. That's the whole protocol in a single afternoon.

---

## Recap

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Copilot CLI   ─── stdio ──►   Repo Doctor   (Python, local)     │
│  (single host) ─── HTTPS ──►   Azure MCP     (ACA, remote)       │
│                                                                  │
│  Same protocol. Two transports. One conversation.                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

| Concept | Where you saw it |
|---------|------------------|
| MCP = USB-C for AI | §1 |
| Host / Client / Server | §1 |
| Tools (verbs) vs. Resources (nouns) vs. Prompts (recipes) | §1, §3 |
| stdio vs. HTTP transports | §1, §3, §4 |
| FastMCP decorators in Python | §3 |
| Context hygiene (truncate subprocess output) | §3.2 |
| Registering MCPs in Copilot CLI (`mcp-config.json`) | §3.3, §4.3 |
| Hosting an MCP server on Azure Container Apps | §4.2 |
| Managed identity for outgoing Azure auth | §4.2 |
| Incoming auth (who can call the server) vs. outgoing auth (what the server can do) | §4.1, §4.2 |

---

## Security checklist for "real" deployments

Our demo took shortcuts to fit in 25 minutes. Before you ship an MCP server to a real team:

- **Incoming auth — re-enable it.** Drop `--dangerously-disable-http-incoming-auth`. Put an Entra App in front (see the [azmcp azd templates](https://github.com/microsoft/mcp/blob/main/servers/Azure.Mcp.Server/azd-templates/README.md) for a copy-pasteable example with OAuth 2.0 + `Mcp.Tools.ReadWrite.All` role).
- **Outgoing auth — least privilege.** Don't grant `Contributor`. Pick the smallest role that covers the tools you expose. Consider `UseOnBehalfOf` so each caller's permissions apply, instead of one shared identity.
- **Choose `--namespace` and `--mode` carefully.** Fewer tools exposed = smaller attack surface and better tool selection by the model.
- **Keep `--read-only` on** unless a tool genuinely needs to mutate.
- **Log everything.** Application Insights for the ACA-side, Copilot CLI session logs on the client side.
- **Pin image versions.** Use `azure-mcp:<sha>` not `:latest` in production.

---

## Useful links

- MCP spec & SDKs — https://modelcontextprotocol.io
- Python SDK (FastMCP) — https://github.com/modelcontextprotocol/python-sdk
- MCP server registry — https://github.com/mcp
- Azure MCP Server — https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server
- Azure MCP commands reference — https://github.com/microsoft/mcp/blob/main/servers/Azure.Mcp.Server/docs/azmcp-commands.md
- Azure MCP ACA azd templates (managed identity, OBO) — https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server/azd-templates
- GitHub Copilot CLI — https://github.com/github/copilot-cli
- This workshop's earlier sessions:
  - [GitHub Copilot CLI workshop](../../copilotcli2hrwkshp/)
  - [Custom Agents workshop](../../customAgents/)

---

## Build your own next

A few prompts to seed your imagination:

- 🧰 **Repo Doctor v2** — add `summarize_changelog`, `bisect_failure`, `suggest_owner` tools.
- 🗒️ **Decision Log MCP** — append/search ADRs in a folder; pair it with Copilot CLI to draft new decisions.
- 📊 **Sprint Pulse MCP** — wraps your project management tool's API (Jira, Linear, ADO) with read-only tools tailored for standups and retros.
- 🌐 **Internal API MCP** — pick one read-only internal API your team uses; wrap it in MCP. Watch adoption.

The litmus test: *"I keep writing glue code for this — could I write it once as an MCP server and stop?"*

---

## Cleanup (Azure)

```bash
az group delete -n rg-mcp-demo --yes --no-wait
```

---

## Thank you 👋

Questions, ideas, ways this could be better — open an issue or PR on this repo. See you at the next AI Forum.
