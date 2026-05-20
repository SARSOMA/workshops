# Tutorial 2.1 — Where MCP Is Used in the Real World

---

## Concept

MCP went from "interesting Anthropic spec" to "everywhere" in about a year. Most major dev tools now ship MCP support, and there's an [official registry](https://github.com/mcp) of servers.

Here's a tour of servers you'll meet in the wild. Each entry tells you the **one thing it unlocks**.

### Developer / cloud platforms

| Server | One-liner | Where to find it |
|--------|-----------|------------------|
| **GitHub MCP** | List/create issues & PRs, search code, manage releases — without leaving your terminal | Built into Copilot CLI; also `github/github-mcp-server` |
| **Azure MCP** | Talk to 40+ Azure services in natural language — storage, KQL, Cosmos, Key Vault, etc. | `microsoft/mcp` (we deploy it in §4) |
| **Azure DevOps MCP** | Query work items, pipelines, repos in ADO | `microsoft/azure-devops-mcp` |
| **Kubernetes MCP** | Inspect clusters, get pod logs, describe resources | Several community servers |
| **Terraform / Bicep MCPs** | Generate / explain IaC from natural language | Community |

### Data & search

| Server | One-liner |
|--------|-----------|
| **Postgres / SQLite MCP** | Run SQL against your DB in natural language with schema awareness |
| **Filesystem MCP** | Give the agent scoped read/write access to a folder |
| **Brave Search / Tavily MCP** | Web search as a tool, with citations |
| **Vector store MCPs** | RAG over your own corpus |

### Productivity / SaaS

| Server | One-liner |
|--------|-----------|
| **Slack MCP** | Post, search, summarise channels |
| **Notion / Confluence MCP** | Read/write pages, search the wiki |
| **Figma MCP** | Pull design components into code |
| **Jira / Linear MCP** | Triage, update, transition issues |

### Browser / UI automation

| Server | One-liner |
|--------|-----------|
| **Playwright MCP** | Drive a real browser — click, type, screenshot, scrape |
| **Computer-use MCP** | Control the whole desktop (experimental) |

### Patterns you'll notice

```
┌──────────────────────────────────────────────────────────────────┐
│   What kinds of things turn out to be great MCP servers?         │
│                                                                  │
│   1. APIs you'd otherwise hit with curl / SDK                    │
│      (GitHub, Azure, Jira, Slack…)                               │
│                                                                  │
│   2. CLIs you'd otherwise script                                 │
│      (git, kubectl, docker, az…)                                 │
│                                                                  │
│   3. Local resources with a security boundary                    │
│      (filesystem, browser, database)                             │
│                                                                  │
│   4. Internal company tools                                      │
│      (your service catalog, your secrets vault, your runbook DB) │
└──────────────────────────────────────────────────────────────────┘
```

If you find yourself writing "agent glue code" to call an API, that glue is a candidate to extract into an MCP server — and then everyone on your team gets it for free.

---

## Practice — Live demo of the built-in GitHub MCP

You already have this working. Let's prove it's a real MCP under the hood.

1. Launch Copilot CLI:
   ```bash
   copilot
   ```
2. Inspect installed MCPs:
   ```
   /mcp
   ```
   You should see `github` (or similar) listed.
3. Now ask a question that can only be answered by calling the GitHub MCP:
   ```
   List my 5 most recently updated repos and the open PR count for each.
   ```
4. Watch the tool calls fly by. That's MCP doing its job — Copilot picked the right tools, called them, parsed the responses.

Try one more — something with a side effect that demonstrates the agent picking the *right* tool:

```
What's the most recent issue in SARSOMA/workshops? Summarise it in one sentence.
```

> Notice you never told Copilot which tool to use. The model reads the tool descriptions advertised by the server and picks for itself. That's why **tool naming + descriptions are 90% of building a good MCP server** — we'll see this in §3.

---

## Q&A

### Question 1
A teammate built a clever script that hits your internal "deployments API" and posts to Slack. They're tired of being the only one who can run it. What's the right move?

A) Document the script in the wiki
B) Wrap the API in an MCP server, share it on the team — now anyone with an MCP-capable client can use it
C) Move the script to a chat bot
D) Schedule it as a cron job

<details><summary>Answer</summary>

**B.** That's exactly the M+N collapse: one MCP server, every team member's AI client benefits.

</details>

### Question 2
Why does the GitHub MCP work "automatically" in Copilot CLI when most MCP servers need to be added?

A) GitHub authored the MCP spec
B) Copilot CLI ships with GitHub MCP pre-configured — it's just an MCP server like any other, registered out of the box
C) The model is specifically trained on GitHub
D) Magic

<details><summary>Answer</summary>

**B.** It's not special — it's just pre-registered. You could remove it with `/mcp remove`.

</details>

---

## Next

→ [§3 — Build a local MCP: Repo Doctor](../03-Build-Local-MCP/README.md)
