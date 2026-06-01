# Tutorial 1.3 — Effects on the Context Window

---

## Concept

Connecting MCP servers changes the math of what fits in the model's context window. There's a **good side** (MCP lets the agent fetch *just-in-time*, instead of stuffing everything in up-front) and a **bad side** (every connected server costs tokens, even when idle). Knowing both helps you design servers — and pick which ones to enable — without surprises.

### ✅ The positive side — MCP *saves* context tokens

Before MCP, the standard pattern for "give the agent more knowledge" was: dump huge blobs of data into the prompt and hope the model finds the right bits. MCP flips that.

| Pattern | Without MCP | With MCP |
|---|---|---|
| **Just-in-time fetch** | Paste 50KB of docs/logs/SQL results into the prompt up front | Expose a `search_docs` / `query_db` tool; the model calls it only when needed |
| **Fresh data** | Re-paste the latest snapshot each turn | Tool returns live data — no stale copies, no duplication across turns |
| **Structured results** | Free-form text the model has to re-parse | JSON schemas → compact, deterministic, easier for the model to reuse |
| **Resources (read-only)** | All context loaded into the chat | The client can list resources cheaply and only `read` the ones it needs |
| **Reusable across tools** | Every new capability = bigger system prompt | One MCP server, used by Copilot CLI + VS Code + Claude with **no extra prompt tokens** |
| **Side-effects in one place** | "Here's a script… copy it into your terminal… paste the output back" | One tool call, one structured result — no round-tripping through the chat |

Net effect: a well-designed MCP server **replaces N turns of paste-and-reason with 1 tool call + a small structured response.** Often a *big* token win.

### ⚠️ The negative side — MCP *spends* context tokens

```
┌───────────────────────────────────────────────────────────────────┐
│  THE MODEL'S CONTEXT WINDOW (e.g. 200K tokens for Claude Opus)    │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  System prompt + agent instructions               ~2K        │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │  📡 MCP TOOL SCHEMAS (every connected server!)               │ │
│  │     • tool name + description + JSON-schema per tool         │ │
│  │     • can be 100s of tokens per tool                         │ │
│  │     • paid every single turn, even when not used        ~8K  │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │  Conversation history                            ~grows      │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │  📥 TOOL CALL RESULTS  ← biggest risk                        │ │
│  │     • subprocess output, API responses                       │ │
│  │     • one unbounded `npm test` can eat 50K tokens!           │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

Two budgets to watch:

| Cost | When you pay | Mitigation |
|------|--------------|------------|
| **Tool schema cost** | Every single model call, for every MCP server you have connected | Disconnect MCP servers you're not using. Use `tools: ["specific_tool"]` instead of `["*"]` to narrow exposure. |
| **Tool result cost** | Each time a tool returns | **Truncate in the server.** Limit subprocess output, paginate large lists, summarise before returning. |

### Why this matters in practice

- A typical MCP server exposes **5–30 tools**. Each tool's name + description + parameter schema can be **100–500 tokens**.
- The Azure MCP server exposes ~40 tools. That's **~8K tokens** before you've said anything.
- Connect three "kitchen-sink" servers (Azure, GitHub, Filesystem) and you're paying ~20K tokens per turn just to *know* the tools exist.
- A single unbounded `cat large.log` can blow your remaining budget in one tool call.

### The trade-off in one sentence

> 🎯 **MCP shifts context from "always loaded" to "loaded on demand" — but you pay a small fixed schema tax for every server you connect.** A server is a net win when *(savings per call) × (calls per session) > (schema tokens × turns)*.

### What Repo Doctor does about it (preview of §3)

The server you'll build has explicit guardrails:

```python
MAX_OUTPUT_LINES = 40
MAX_OUTPUT_CHARS = 4000

def _truncate(text: str) -> str:
    # keep the first 40 lines, then cap at 4000 chars,
    # and add a "… (truncated)" marker so the model knows
    ...
```

Every subprocess (`npm test`, `cargo build`, `pytest`) gets piped through `_truncate` before it goes back to the model. That's why a Repo Doctor `health_report` returns ~1K tokens instead of 50K.

### Three habits of a context-window-friendly MCP server

1. **Write tight tool descriptions.** Every word costs tokens *every turn*. Skip the marketing copy.
2. **Truncate by default, full output on request.** Return summaries; expose a separate tool/resource for the full blob if needed.
3. **Prefer resources over tools** when the data is read-only and the client can decide whether to fetch it. Resources aren't auto-loaded into the schema the same way.

---

## Q&A

### Question 1
You connected an MCP server with 30 tools but didn't call any of them this turn. How many tool-schema tokens did you spend?

A) Zero — schemas only count when called
B) All 30 tools' worth — schemas are sent every turn
C) Only the ones the model "considered"
D) Depends on the transport

<details><summary>Answer</summary>

**B.** Tool schemas are part of the system message on every model call, regardless of whether they get used. That's why connecting lots of MCPs has a real, ongoing cost.

</details>

### Question 2
Your MCP server wraps `kubectl logs`. A user asks for logs of a noisy pod. What should the tool return?

A) The full unbounded stream
B) A truncated tail (e.g. last 40 lines + total line count) and a separate tool to fetch more
C) Refuse to run if output looks long
D) Stream it directly to the LLM

<details><summary>Answer</summary>

**B.** Return enough for the model to reason, plus a way to ask for more. This is the *context hygiene* pattern you'll build into Repo Doctor in §3.

</details>

---

## Next

→ [§2 — Transports & Topology](../02-Transports-And-Topology/README.md)
