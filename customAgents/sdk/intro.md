# Part 2: Programmatic Custom Agents (GitHub Copilot Extensions SDK)

Part 1 covered markdown-based agents — static instruction files that steer the model. This part goes deeper: **Copilot SDK** let you build a fully programmable agent. This brings the power of calling agentic AI from inside your own code.

This unlocks things that `.agent.md` files can't do:
- Ability to package agentic AI execution into an executable or pipeline
- Run custom logic before and after calling the model
- Query live databases, APIs, or internal services
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
│  GitHub Copilot Chat   │ ──────────────────► │  Your Copilot SDK App   │
│  (VS Code, github.com) │                     │                         │
│                        │ ◄────────────────── │                         │
│                        │    SSE stream        │                         │
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
| Custom response logic | SDK can transform, filter, or enrich responses before showing them |
| Live data (APIs, databases) | `.agent.md` only has static instructions; SDK can call any service at runtime |
| Team / org distribution | Publish to GitHub Marketplace or install org-wide as a GitHub App |
| Multi-step workflows with checkpoints | SDK has full control over the conversation loop |

If you just need a specialized persona with restricted tools, use `.agent.md`. If you need to integrate with external systems or distribute to others, use the SDK..

---

## Demos

**hello_world.py** — calls the Copilot model with a system prompt and prints the response:

```bash
set -a && source customAgents/sdk/.env && set +a
python customAgents/sdk/hello_world.py
```

**code-review-script** — reviews an ADO pull request and posts comments:

```bash
set -a && source .env && set +a
python review_pr.py https://dev.azure.com/msazure/one/_git/my-repo/pullrequest/12345
```

**code-review-script from ADO Pipeline** — reviews an ADO pull request and posts comments, but from a pipeline

---

## Prerequisites

- Python 3.10 or later
- A GitHub account with Copilot Chat access

---

## Workshop Exercise

See the [exercise](exercise.md) for the full hands-on walkthrough of building and deploying a Hello World extension.

---

## Key Takeaways

- **The protocol is language-agnostic** — the exercise uses Python, but any language that can work
- **Always verify requests** in production — check the GitHub signature before trusting any payload
- **For production**, deploy your server anywhere (Azure, AWS, etc.) and update the webhook URL in your GitHub App settings

---

## Sources

| Resource | Link |
|----------|------|
| Copilot Extensions SDK (GitHub) | [copilot-extensions/preview-sdk.js](https://github.com/copilot-extensions/preview-sdk.js) |
| npm package | [@copilot-extensions/preview-sdk](https://www.npmjs.com/package/@copilot-extensions/preview-sdk) |
| Using Extensions in Copilot Chat | [GitHub Docs](https://docs.github.com/en/copilot/using-github-copilot/using-extensions-to-integrate-external-tools-with-copilot-chat) |
| SDK Examples | [examples/ in the repo](https://github.com/copilot-extensions/preview-sdk.js/tree/main/examples) |
