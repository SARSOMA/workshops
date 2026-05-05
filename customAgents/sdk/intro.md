# Part 2: Programmatic Custom Agents (GitHub Copilot Extensions SDK)

Part 1 covered markdown-based agents — static instruction files that steer the model. This part goes deeper: **Copilot Extensions** let you build a fully programmable agent that runs as a web service. Instead of injecting instructions into a system prompt, you intercept every message from the user and respond with exactly what your code produces.

This unlocks things that `.agent.md` files can't do:
- Query live databases, APIs, or internal services
- Run custom logic before and after calling the model
- Return structured data like citations, confirmations, and rich references
- Distribute your agent to others via GitHub Marketplace or your org

---

## What's Built-In

Before you build anything, you already have:

- **GitHub Copilot Chat** — the client that calls your extension via a webhook
- **The Copilot API** — Copilot proxies requests to your server and passes your responses back to the chat UI

You write a standard HTTP server. Copilot calls it.

---

## Architecture

```
┌────────────────────────┐       POST /       ┌─────────────────────────┐
│  GitHub Copilot Chat   │ ──────────────────► │  Your Extension Server  │
│  (VS Code, github.com) │                     │  (Python HTTP server)   │
│                        │ ◄────────────────── │                         │
│                        │    SSE stream        │  • Verify request       │
└────────────────────────┘                     │  • Parse payload        │
                                               │  • Call your APIs       │
                                               │  • Call Copilot model   │
                                               │  • Stream response      │
                                               └─────────────────────────┘
                                                         │
                                                  GitHub App
                                               (connects the two)
```

When a user messages your extension (`@your-agent hello`), Copilot sends an HTTP POST to your server. Your server verifies the request came from GitHub, processes the message, optionally calls the Copilot model, and streams the response back as Server-Sent Events (SSE).

---

## What's Best Suited For

Use the Copilot Extensions SDK when you need:

| Need | Why SDK > `.agent.md` |
|------|-----------------------|
| Live data (APIs, databases) | `.agent.md` only has static instructions; SDK can call any service at runtime |
| Custom response logic | SDK can transform, filter, or enrich responses before showing them |
| Team / org distribution | Publish to GitHub Marketplace or install org-wide as a GitHub App |
| Rich UI elements | SDK can send confirmations, citations, and reference cards the model can't generate on its own |
| Multi-step workflows with checkpoints | SDK has full control over the conversation loop |

If you just need a specialized persona with restricted tools, use `.agent.md`. If you need to integrate with external systems or distribute to others, use the SDK.

---

## Prerequisites

- Python 3.10 or later
- A GitHub account with Copilot Chat access
- A public HTTPS URL for your server — use one of:
  - **GitHub Codespaces** (easiest — ports can be made public with one click)
  - **ngrok** (`ngrok http 3000`) for local development

---

## Workshop Exercise

See the [exercise](exercise.md) for the full hands-on walkthrough of building and deploying a Hello World extension.

---

## Key Takeaways

- **Copilot Extensions = a GitHub App + an HTTP webhook endpoint** — Copilot calls your server, your server responds with SSE
- **The protocol is language-agnostic** — the exercise uses Python + Flask, but any language that can serve HTTP and stream SSE works
- **Always verify requests** in production — check the GitHub signature before trusting any payload
- **Use Codespaces or ngrok** to get a public URL during development
- **For production**, deploy your server anywhere (Azure, AWS, etc.) and update the webhook URL in your GitHub App settings

---

## Sources

| Resource | Link |
|----------|------|
| Copilot Extensions SDK (GitHub) | [copilot-extensions/preview-sdk.js](https://github.com/copilot-extensions/preview-sdk.js) |
| npm package | [@copilot-extensions/preview-sdk](https://www.npmjs.com/package/@copilot-extensions/preview-sdk) |
| Using Extensions in Copilot Chat | [GitHub Docs](https://docs.github.com/en/copilot/using-github-copilot/using-extensions-to-integrate-external-tools-with-copilot-chat) |
| SDK Examples | [examples/ in the repo](https://github.com/copilot-extensions/preview-sdk.js/tree/main/examples) |
