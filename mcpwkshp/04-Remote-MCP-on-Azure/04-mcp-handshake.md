# 4.4 — The MCP handshake, on the wire

You've seen Copilot CLI call your remote server in §4.3. Now let's pop the hood
and watch the **actual HTTP/JSON-RPC traffic** Copilot CLI sends. This is the
"there's no magic here" page.

If you understand these four requests, you can write an MCP client in any
language in ~30 lines of code.

---

## Concept

Every MCP-over-HTTP session is four ordered messages from the client:

```
┌────────────┐                                          ┌──────────────────┐
│  Client    │                                          │  MCP Server      │
│ (any tool) │                                          │  (your ACA app)  │
└─────┬──────┘                                          └────────┬─────────┘
      │                                                          │
      │  ① POST /  initialize                                    │
      │  ───────────────────────────────────────────────────────►│
      │   ◄──── 200 OK   mcp-session-id: abc…                    │
      │        data: { serverInfo, capabilities, … }             │
      │                                                          │
      │  ② POST /  notifications/initialized   (+session id)     │
      │  ───────────────────────────────────────────────────────►│
      │   ◄──── 202 Accepted   (empty body)                      │
      │                                                          │
      │  ③ POST /  tools/list                  (+session id)     │
      │  ───────────────────────────────────────────────────────►│
      │   ◄──── 200 OK                                           │
      │        data: { tools: [ {name, inputSchema}, … ] }       │
      │                                                          │
      │  ④ POST /  tools/call                  (+session id)     │
      │  ───────────────────────────────────────────────────────►│
      │   ◄──── 200 OK                                           │
      │        data: { result: { content: [ … ] } }              │
      │                                                          │
```

A few non-obvious rules:

| Rule | Why |
|---|---|
| **Same URL for every call** — the FQDN root (`/`), not `/mcp` | MCP-over-HTTP is "one endpoint, JSON-RPC method names". `/mcp` is a common wrong guess that returns 404. |
| Always send `Accept: application/json, text/event-stream` | The server replies as SSE (`event: message\ndata: {…json…}`), even for a single response. |
| Capture `mcp-session-id` from the **initialize** *response headers* | Required on every subsequent call. Without it the next call would be treated as a brand-new session. |
| Always send `notifications/initialized` **before** any `tools/*` call | The server uses this to flip the session from "handshaking" to "ready". |
| Messages with `id` expect a response. Messages without `id` are notifications → server returns `202 Accepted`, no body. | Standard JSON-RPC. |
| Parse the `data:` line of the SSE response — the JSON-RPC payload is inside it | Don't try to `JSON.parse(responseBody)` directly. |

---

## Practice — talk to your server with raw HTTP

Set this once (use the FQDN you printed in §4.2):

```bash
BASE=https://<your-aca-fqdn>/
```

### ① `initialize` — open the session

```bash
curl -s -i "$BASE" -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{
    "jsonrpc":"2.0","id":1,"method":"initialize",
    "params":{
      "protocolVersion":"2025-06-18",
      "capabilities":{},
      "clientInfo":{"name":"workshop-curl","version":"1.0"}
    }
  }'
```

Expected response — note three things in particular:

```
HTTP/1.1 200 OK
mcp-session-id: OshGFZLD-Wwz8dgDp5BABA      ← capture this
content-type: text/event-stream              ← SSE, not application/json
server: Kestrel

event: message
data: {"result":{"protocolVersion":"2025-06-18",
                  "capabilities":{"logging":{},"tools":{}},
                  "serverInfo":{"name":"Azure MCP Server","version":"3.0.0-beta.15"},
                  "instructions":"…"},
       "id":1,"jsonrpc":"2.0"}
```

Capture the session id into a shell var:

```bash
SID=OshGFZLD-Wwz8dgDp5BABA   # paste yours from the response header
```

### ② `notifications/initialized` — say "ready"

```bash
curl -s -i "$BASE" -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "mcp-session-id: $SID" \
  --data '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

Expected: `HTTP/1.1 202 Accepted`, empty body.

> Notice: no `"id"` field → notification → 202 with no payload. If you forget
> this step, subsequent `tools/*` calls error out.

### ③ `tools/list` — discover what's available

```bash
curl -s "$BASE" -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "mcp-session-id: $SID" \
  --data '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

You'll get an SSE response containing an array of tools — name + description +
JSON schema. With `--namespace subscription --namespace group` set in §4.2 you'll
see ~3–4 tools. Without those filters, you'd see ~60.

### ④ `tools/call` — invoke one

```bash
curl -s "$BASE" -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "mcp-session-id: $SID" \
  --data '{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{"name":"subscription_list","arguments":{}}
  }'
```

Inside the `data:` payload you'll find:

```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"status\":200,\"message\":\"Success\",\"results\":{\"subscriptions\":[{\"subscriptionId\":\"…\",\"displayName\":\"…\",\"state\":\"Enabled\",\"tenantId\":\"…\"}]}}"
      }
    ],
    "isError": false
  },
  "id": 3,
  "jsonrpc": "2.0"
}
```

The inner `text` is a *JSON string* (Azure MCP packages structured results that
way). Real clients parse it once more.

---

## PowerShell version (Windows attendees)

Same flow, idiomatic for Windows boxes — useful if `curl` isn't installed:

```powershell
$base = "https://<your-aca-fqdn>/"
$headers = @{
  "Content-Type" = "application/json"
  "Accept"       = "application/json, text/event-stream"
}

# ① initialize
$init = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"workshop-ps","version":"1.0"}}}'
$resp = Invoke-WebRequest -Uri $base -Method Post -Headers $headers -Body $init
$sid  = $resp.Headers["mcp-session-id"]; if ($sid -is [array]) { $sid = $sid[0] }
Write-Host "session: $sid"

# ② notifications/initialized
$h2 = $headers.Clone(); $h2["mcp-session-id"] = $sid
Invoke-WebRequest -Uri $base -Method Post -Headers $h2 `
  -Body '{"jsonrpc":"2.0","method":"notifications/initialized"}' | Out-Null

# ③ tools/list
$list = Invoke-WebRequest -Uri $base -Method Post -Headers $h2 `
  -Body '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
$listJson = (($list.Content -split "`n") | Where-Object { $_ -like "data: *" } |
             Select-Object -First 1).Substring(6) | ConvertFrom-Json
"Server advertises {0} tools" -f $listJson.result.tools.Count

# ④ tools/call → subscription_list
$callBody = '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"subscription_list","arguments":{}}}'
$call = Invoke-WebRequest -Uri $base -Method Post -Headers $h2 -Body $callBody
$callJson = (($call.Content -split "`n") | Where-Object { $_ -like "data: *" } |
             Select-Object -First 1).Substring(6) | ConvertFrom-Json
$inner = $callJson.result.content[0].text | ConvertFrom-Json
$inner.results.subscriptions | Format-Table displayName, subscriptionId
```

---

## What Copilot CLI does internally

That's it. When you type "List my Azure subscriptions" in Copilot CLI:

1. CLI does the **initialize + initialized** dance on startup (once per session).
2. The LLM sees the **tools/list** schema as part of its tool catalog.
3. The LLM emits a tool-call → CLI sends **tools/call** with the chosen tool + arguments.
4. CLI feeds the result back into the LLM context for the next turn.

The MCP server doesn't know or care that an LLM is on the other side — it's
just answering JSON-RPC. That's what makes it portable across Copilot CLI,
Foundry, Claude Desktop, Copilot Studio, and anything else that speaks MCP.

---

## Q&A

### Question 1
What's special about the response to `initialize`?

A) It returns the user's OAuth token
B) It returns a `mcp-session-id` header that must be echoed on every subsequent call
C) It opens a WebSocket
D) Nothing — it's just an HTTP 200

<details><summary>Answer</summary>

**B.** Without the header on subsequent requests, the server treats each call as a brand-new (un-initialized) session and rejects it.

</details>

### Question 2
Why does the server reply with `text/event-stream` instead of `application/json`?

A) It's faster
B) MCP-over-HTTP uses Server-Sent Events as its response format so a single call can stream multiple JSON-RPC messages back (progress updates, partial results, the final result)
C) Required by HTTPS
D) Bug in the implementation

<details><summary>Answer</summary>

**B.** Even when there's only one message, the framing is still SSE — clients have to parse `data:` lines.

</details>

### Question 3
You send `tools/call` and get `HTTP 400` with body "session not initialized". What did you forget?

A) The `Authorization` header
B) The `notifications/initialized` POST between `initialize` and `tools/call`
C) `--read-only`
D) The CORS preflight

<details><summary>Answer</summary>

**B.** Handshake is **initialize → initialized → tools/***. The middle step has no `id` so it returns 202 with no body — it's easy to skip.

</details>

---

## Next

→ [4.5 — Auth deep-dive: incoming vs outgoing, OAuth 2.1, OBO](./05-auth-deep-dive.md)
→ [§5 — Wrap-up](../05-Wrap-Up/README.md)
