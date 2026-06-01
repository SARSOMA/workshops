# Tutorial 2.1 — Transports & the Transport × Locality Matrix

---

## Concept

Now that you know what an MCP server *is*, the next question is **where it runs** and **how the host talks to it**. Two independent dimensions:

- **Locality** — is the server on **your laptop** or **somewhere else (cloud)**?
- **Transport** — does the host talk to it via **stdio** (a pipe, locally) or **HTTP** (a network call)?

> 🧠 **stdio** = standard input / standard output. The two text "pipes" every Unix-ish program has. Two programs running on the same machine can exchange messages by one writing to its stdout and the other reading from its stdin — no network, no ports, no auth.

> 🌐 **Streamable HTTP** = a single HTTP endpoint that speaks JSON-RPC, with optional server-sent events for streaming. Replaces the older "HTTP+SSE" transport in the 2025 spec.

Three of the four squares are valid — the only impossible one is stdio over a network (pipes don't traverse sockets).

```
                       LOCAL (your laptop)            REMOTE (cloud / shared host)
                  ┌────────────────────────────┬────────────────────────────────┐
   stdio          │  ✅ default for local      │  ❌ impossible                 │
                  │  child-process pipes       │     (no pipe over network)     │
                  │  Our Repo Doctor (§3)      │                                │
                  ├────────────────────────────┼────────────────────────────────┤
   Streamable     │  ✅ totally legal          │  ✅ the only remote option     │
   HTTP           │  e.g. localhost:8080       │  Bearer auth + TLS             │
                  │  shared by many clients    │  Our Azure MCP on ACA (§4)     │
                  └────────────────────────────┴────────────────────────────────┘
```

What changes square-to-square:

| Aspect | local-stdio | local-HTTP | remote-HTTP |
|---|---|---|---|
| Wire | stdin/stdout pipe | TCP on `localhost:<port>` | HTTPS on a public FQDN |
| Trust source | OS user (process trust) | OS user **if** bound to `127.0.0.1` | Bearer token (OAuth 2.1) |
| Auth on the wire | none (no wire) | none on `127.0.0.1`; required on `0.0.0.0` | required (token) |
| Server lifecycle | spawned per client | one daemon, many clients | one deployment, many users |
| Outgoing creds | reads your `~/.azure/`, `~/.aws/`, etc. | same as stdio | managed identity / OBO |
| When to pick | default for personal use | shared local state, multi-client, parity with prod | any time the server isn't on your laptop |

> 🔒 **Local HTTP gotcha:** binding to `0.0.0.0` exposes the unauthenticated server to your whole network. Stick to `127.0.0.1` unless you've explicitly added auth.

### How to pick

1. **You're the only consumer, on one machine** → **local stdio**. Zero ceremony, fastest, safest. *(This is §3.)*
2. **Multiple clients on the same machine should share state, or you want to debug with `curl`, or you want the same artifact you'll deploy to prod** → **local HTTP** on `127.0.0.1`.
3. **The server lives in a container / VM / Azure / SaaS** → **remote HTTP**. You now need real auth. *(This is §4 + the auth deep-dive.)*

The MCP protocol itself is identical across all three squares — same JSON-RPC 2.0, same `tools/call`, `resources/list`, `prompts/get`. **Only the transport changes.**

---

## Q&A

### Question 1
You want one MCP server shared by your whole team. Which transport do you pick?

A) stdio
B) Streamable HTTP

<details><summary>Answer</summary>

**B.** stdio servers are subprocesses of the local host — not shareable. HTTP MCP servers can be deployed once and used by many clients.

</details>

### Question 2
Which square of the transport × locality matrix is **impossible**?

A) Local + stdio
B) Local + HTTP
C) Remote + stdio
D) Remote + HTTP

<details><summary>Answer</summary>

**C.** stdio is child-process pipes between host and server — it can't cross a network. The other three squares are all valid; the workshop uses the local-stdio square in §3 and the remote-HTTP square in §4.

</details>

---

## Next

→ [How the client talks to the server](./02-client-talks-to-server.md)
