# Tutorial 1.1 — MCP Explained

> 👋 **Brand new to MCP?** This page assumes you've never heard the term before. We'll define it, motivate it, and draw a diagram you can re-draw on a napkin afterwards.

---

## Concept

### First — what does MCP stand for?

**MCP = Model Context Protocol.**

It's an **open standard** introduced by **Anthropic in November 2024** and now adopted by OpenAI, Microsoft, Google DeepMind, GitHub, Cloudflare, and many others. It's a small protocol — basically a JSON message format — that defines **how an AI app talks to the tools and data it needs.**

> 🧠 One-liner you can quote: *"MCP is USB-C for AI — one open protocol that lets any AI client plug into any tool or data source."*

#### The USB-C analogy, visually

USB-C is the universal port. **One physical connector** lets your laptop talk to a charger, an external drive, a monitor, a phone, a docking station — without you needing a different cable for each. Devices and accessories all agree on one shape.

MCP plays the same role for AI applications. **One protocol shape** lets any AI app talk to any data source or tool — no per-vendor adapter.

```
            BEFORE                            AFTER
        (no common port)                  (one common port)

   ┌──────┐  ╔═══════╗                  ┌──────┐
   │Phone │──║weird-A║──┐               │Phone │──┐
   ├──────┤  ╚═══════╝  │               ├──────┤  │
   │ HDD  │──╔═══════╗──┤  Laptop       │ HDD  │──┤   Laptop
   ├──────┤  ║weird-B║  │  ──────       ├──────┤  ├──[ USB-C ]──
   │Mon.  │──╚═══════╝──┤               │Mon.  │──┤
   ├──────┤  ╔═══════╗  │               ├──────┤  │
   │Charge│──║weird-C║──┘               │Charge│──┘
   └──────┘  ╚═══════╝                  └──────┘

   N devices × M ports                  N devices share 1 port

   ──────────────────────────────────────────────────────────────

       BEFORE MCP                         WITH MCP
   (custom plugin per pair)         (one protocol everyone speaks)

   ┌─────────┐ ╔═══════╗                  ┌─────────┐
   │ GitHub  │─║GH-API ║──┐               │ GitHub  │──┐
   ├─────────┤ ╚═══════╝  │               ├─────────┤  │
   │ Azure   │─╔═══════╗──┤   Copilot     │ Azure   │──┤   Copilot
   ├─────────┤ ║Az-API ║  │   Claude      ├─────────┤  ├──[  MCP  ]──── Claude
   │Postgres │─╚═══════╝──┤   Cursor      │Postgres │──┤              Cursor
   ├─────────┤ ╔═══════╗  │   ChatGPT     ├─────────┤  │              ChatGPT
   │ Figma   │─║Fig-API║──┘               │ Figma   │──┘
   └─────────┘ ╚═══════╝                  └─────────┘

   N tools × M assistants                  N tools share 1 protocol
   = M×N bespoke plugins                   = M+N total integrations
```

Same shape of problem, same shape of solution.

| USB-C | MCP |
|---|---|
| The physical connector | The JSON-RPC message format |
| The cable / wire | stdio pipe (local) or HTTPS (remote) |
| Devices that plug in | AI hosts (Copilot, Claude, Cursor, …) |
| Accessories on the other end | MCP servers (GitHub, Azure, Postgres, …) |
| Power-delivery / DisplayPort modes | MCP primitives (tools, resources, prompts) |
| The USB-IF consortium | The MCP open spec |

If that already makes sense, jump to **Who's who** below. Otherwise keep reading — the next two sections explain *why anyone needed a protocol for this at all.*

---

### A concrete story (why the protocol exists)

Imagine you're using an AI assistant — Copilot, Claude, Cursor, ChatGPT, whatever — and you type:

> *"What's broken in our prod cluster, and which deploy caused it?"*

For the assistant to actually answer that, it can't just rely on what's in the model's head. It needs to:

1. Read recent **logs** (maybe from Datadog or Splunk)
2. Pull **metrics** (Prometheus, Azure Monitor)
3. Look at the **deploy history** (GitHub Actions, Argo CD)
4. Cross-reference with **incidents** (PagerDuty, ServiceNow)

That's four external systems. The model itself can't call any of them — models output text. *Something else* has to do the calling and feed the results back in. That "something else" is what MCP standardises.

---

### What problem is MCP actually solving?

Before MCP, every (AI app ↔ external tool) pair was a custom integration. Concretely:

| Pain point | What it meant in practice |
|---|---|
| **Every AI app reinvents tool integrations** | Copilot writes a "GitHub plugin", Claude writes a separate "GitHub plugin", Cursor writes a third one. Same tool, three bespoke integrations. |
| **Every tool has to support each AI app separately** | A Postgres team that wants AI access has to build N adapters for N assistants. |
| **No common vocabulary** | No standard way to describe what a tool does, what inputs it takes, how to authenticate, how to stream results. Everyone invented their own. |
| **Vendor lock-in** | Once your workflow depended on Copilot's plugin format, switching to Claude meant rebuilding everything. |

If you have **M** AI apps and **N** tools, that's **M × N** custom integrations — and they all rot independently as APIs change.

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
```

MCP collapses that to **M + N**: each AI app speaks MCP once, each tool exposes itself as an MCP server once. Anyone who speaks the protocol can talk to anyone else who speaks the protocol.

```
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

That's the entire pitch. Same idea as USB-C, HTTP, or SQL: pick one shared interface, let many vendors plug into it.

---

### A tiny vocabulary (the only 6 words you need)

Before we go further, here are the only terms that matter on this page:

| Term | Meaning in one line |
|---|---|
| **Host** | The AI application the human is talking to (Copilot CLI, VS Code, Claude Desktop, …). |
| **Client** | A little piece of code *inside* the host that knows how to speak MCP. |
| **Server** | A separate program that exposes tools / data via MCP. May be on your laptop or in the cloud. |
| **Tool** | An action the AI can perform (`create_pr`, `list_subscriptions`, `send_email`). Has side effects. |
| **Resource** | A piece of data the AI can read (`file_contents`, `last_report`). Read-only. |
| **Prompt** | A pre-baked instruction template the user can invoke (often as a slash command). |

We'll keep coming back to these.

---

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
│                Messages exchanged as JSON-RPC  │                 │
│                over a pipe OR over HTTP        │                 │
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

Read it top-to-bottom:

1. **You** type something into the **Host** (Copilot CLI).
2. The model inside the host decides "I need to call a tool." The host's **MCP client** picks which **server** to ask.
3. The client sends a message — a **JSON-RPC** call, which is a tiny standard format that looks like `{"method": "tools/call", "params": {...}}` — to the server.
4. The **server** runs the tool (hits an API, runs a command, reads a file) and sends the result back.
5. The host hands the result to the model so it can keep reasoning, and ultimately gives you an answer.

> 🧠 **JSON-RPC** = JSON Remote Procedure Call. Just a tiny format for "here's a function name and some arguments, please run it and send back the result." It's been around since 2005. MCP didn't invent it — it just picked it.

In our workshop:

| Role | Who plays it |
|---|---|
| **Host** | GitHub Copilot CLI |
| **MCP Client** | The bit of Copilot CLI that handles `/mcp` |
| **MCP Server** | Our Repo Doctor (§3) and Azure MCP (§4) |

---

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

A given MCP server can expose any mix of the three. Most servers focus on tools.

---

## Q&A

### Question 1
What does MCP stand for, and who introduced it?

A) Model Context Protocol — Anthropic (Nov 2024)
B) Microsoft Copilot Protocol — Microsoft (2023)
C) Multi-Component Pipeline — Google (2025)
D) Managed Container Plugin — Docker (2024)

<details><summary>Answer</summary>

**A.** Anthropic published MCP as an open standard in November 2024; OpenAI, Microsoft, Google, GitHub, Cloudflare and others adopted it within months.

</details>

### Question 2
What problem does MCP solve?

A) It makes models faster
B) It encrypts traffic between the model provider and you
C) It standardises how AI apps connect to external tools and data — turning M×N integrations into M+N
D) It replaces the LLM with a smaller one

<details><summary>Answer</summary>

**C.** MCP is the integration protocol — clients implement it once, servers implement it once, anything can talk to anything.

</details>

### Question 3
Which of these is **not** an MCP primitive?

A) Tools
B) Resources
C) Prompts
D) Fine-tunes

<details><summary>Answer</summary>

**D.** MCP servers expose Tools, Resources, and Prompts. Fine-tuning is unrelated to MCP.

</details>

---

## Next

→ [Where MCP is used today](./02-where-used-today.md)

