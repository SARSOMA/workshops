# 4.1 — Meet the Azure MCP Server

---

## Concept

**Azure MCP Server** is Microsoft's official MCP server for talking to Azure. It exposes tools across **40+ Azure services** — storage, KQL, Cosmos DB, Key Vault, Service Bus, AI Search, Resource Graph, and more — through one MCP server.

- Source: https://github.com/microsoft/mcp (`servers/Azure.Mcp.Server`)
- Public container image: `mcr.microsoft.com/azure-sdk/azure-mcp:latest`
- Also distributed as an `npm` package (`@azure/mcp`) and a NuGet tool (`Azure.Mcp`)

You can run it three ways:

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  1) LOCAL stdio              2) LOCAL Docker         3) REMOTE   │
│                                                       HTTP/ACA   │
│  npx -y @azure/mcp@latest    docker run --rm -i      ┌─────────┐ │
│      server start              mcr.microsoft.com/    │ Container│ │
│                                azure-sdk/azure-mcp   │  App     │ │
│  (uses your `az login`        :latest                │  +       │ │
│   creds via Azure CLI                                │  Managed │ │
│   credential chain)          (uses .env creds)       │ Identity │ │
│                                                      └─────────┘ │
│                                                                  │
│  ◄── this section ──►                                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

We're going for **#3**. Why:

- It demonstrates the **HTTP transport** end-to-end
- One deployment can be **shared by a whole team**
- It's the canonical way Microsoft recommends running Azure MCP for Foundry / Copilot Studio / cross-client use
- It lets you use **managed identity** to authenticate to Azure — no secrets handed out to clients

### The deployment we're going to build

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Your Copilot CLI  ──HTTPS──►  Azure Container App               │
│  (MCP client)                  ├─ Azure MCP server               │
│                                │   args: --transport http        │
│                                │         --mode all              │
│                                │         --read-only             │
│                                │         --namespace group       │
│                                │         --namespace subscription│
│                                └─ System-assigned managed        │
│                                   identity (calls Azure ARM)     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### What you'll be able to ask

Once it's wired up, from Copilot CLI you can ask things like:

- "List my Azure subscriptions"
- "What resource groups are in subscription X?"
- "Show me the resources in resource group `rg-prod`"

…and the model will route those to the Azure MCP server you just deployed.

> 🔒 **Important**: we deploy with `--read-only` so this stage demo can't accidentally delete anything. Removing that flag enables write operations — only do that for trusted clients.

### Two flavours of "auth" to keep straight

There are **two separate auth boundaries** to think about with remote MCP. People conflate them all the time.

| Boundary | Question | Our demo answer |
|----------|----------|------------------|
| **Incoming auth** (client → MCP) | Who is allowed to *call* this MCP server? | Demo flag `--dangerously-disable-http-incoming-auth`. **Anyone with the URL can call it.** Acceptable only for a short-lived demo on a throwaway sub. |
| **Outgoing auth** (MCP → Azure) | What permissions does the server use to call Azure? | The Container App's **system-assigned managed identity**, granted **Reader** on the subscription. |

In §5 we'll discuss the production-grade alternative (Entra App + OAuth on the way in).

---

## Q&A

### Question 1
Why deploy Azure MCP to ACA instead of just running `npx @azure/mcp` locally?

A) ACA is required by the spec
B) HTTP transport + a shared deployment means one configured server is usable by every team member with an MCP client
C) It's cheaper
D) Better latency

<details><summary>Answer</summary>

**B.** A single ACA deployment with managed identity replaces N local installs and N copies of credentials.

</details>

### Question 2
"Incoming auth" and "outgoing auth" — which is which?

A) Both refer to the same thing
B) Incoming = who can call the MCP server; outgoing = what the MCP server is allowed to do in Azure
C) Incoming is bandwidth, outgoing is bandwidth
D) Only outgoing exists for MCP

<details><summary>Answer</summary>

**B.** Keep them mentally separated. Each has its own knob.

</details>

---

## Next

→ [4.2 — Deploy Azure MCP to Azure Container Apps](./02-deploy-to-aca.md)
