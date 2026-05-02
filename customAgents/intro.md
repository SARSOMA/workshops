# Custom AI Agents Workshop

## Let's Get Started

Make sure you've completed the [prerequisites](prerequisites.md) — you should have at least VS Code Copilot Chat and one CLI option (Copilot CLI or Agency) authenticated with your Microsoft corp GitHub account.

## What Are Custom Agents?

Every AI assistant ships with general-purpose behavior. Custom agents let you **shape that behavior** — giving the AI a persona, domain expertise, specific tools, and guardrails tailored to your work.

Think of it this way: out-of-the-box Copilot is a brilliant generalist. A custom agent is a brilliant **specialist** — a security reviewer who knows your threat model, a documentation writer who follows your style guide, or a DevOps expert who knows your pipeline.

### How Do Custom Agents Actually Work?

Custom agents don't retrain or fine-tune the underlying model. The model itself stays the same. What changes is the **context** that gets sent to it.

Every time you interact with an AI model, your message is wrapped in a larger context that the model sees before generating a response. This context includes a **system prompt** — instructions that tell the model how to behave, what role to play, what rules to follow, and what tools it can use. Custom agents work by injecting your specialized instructions into that system prompt.

```
┌──────────────────────────────────────────────────┐
│  What the model actually receives:               │
│                                                  │
│  ┌──────────────────────────────────────────┐    │
│  │  System Prompt (invisible to you)        │    │
│  │  ├── Platform instructions (from GitHub) │    │
│  │  ├── YOUR agent instructions ◄───────────│──── This is what you control
│  │  ├── Tool definitions                    │    │
│  │  └── Custom instructions files           │    │
│  ├──────────────────────────────────────────┤    │
│  │  Conversation history                    │    │
│  ├──────────────────────────────────────────┤    │
│  │  Your current message                    │    │
│  └──────────────────────────────────────────┘    │
└──────────────────────────────────────────────────┘
```

So when you create a custom agent that says "You are a security reviewer — check for SQL injection, XSS, and hardcoded credentials," you're not teaching the model new knowledge. You're **steering** it — telling it which part of its existing knowledge to focus on, what format to respond in, and what standards to enforce.

This is also why custom agents can restrict which **tools** the model has access to. A documentation agent might only need file read/write, while a DevOps agent might need shell access and Git. Limiting tools keeps the agent focused and reduces the chance of unintended side effects.

The key insight: **you're not changing what the model knows — you're changing what it pays attention to.**

> **Sources:**
> - [Customization concepts (VS Code docs)](https://code.visualstudio.com/docs/copilot/concepts/customization) — "AI models have broad general knowledge but don't know your codebase or team practices. Customization is how you share that context."
> - [About customizing GitHub Copilot responses (GitHub docs)](https://docs.github.com/en/copilot/concepts/prompting/response-customization) — "You can create custom instructions that automatically add this information for you. The additional information is not displayed, but is available to Copilot to allow it to generate higher quality responses."

### Why Custom Agents Matter

- **Consistency** — Encode your team's conventions once; every interaction follows them automatically
- **Specialization** — Domain-specific agents outperform generic prompts because they carry persistent context
- **Efficiency** — Skip the repeated "act as a..." preamble — agents remember their role
- **Shareability** — Check agent definitions into your repo and your entire team benefits
- **Scalability** — From a single markdown file to a full server-side extension to enterprise-wide M365 agents, the approach scales with your needs

---

## About This Workshop

This is an **interactive, hands-on workshop**. Each section has a short information segment followed by a workshop exercise where you'll build something yourself. Come with questions — interrupt, ask, experiment.

### Structure

| Part | Topic | Info | Exercise |
|------|-------|------|----------|
| **1** | Markdown-based agents (VS Code Chat / Copilot CLI / Agency) | ~15 min | ~10 min |
| **2** | Programmatic agents (GitHub Copilot Extensions SDK) | ~15 min | ~10 min |
| **3** | Enterprise agents (Microsoft 365 Copilot) | ~15 min | ~10 min |

Each part follows the same rhythm:
1. **What's built-in** — what you get for free before any customization
2. **What's best suited** — when and why to use this approach
3. **Build one together** — a simple custom agent you'll create and test live

---

## Why I Recommend Having Both VS Code Copilot Chat and Copilot CLI

You'll see me use both throughout this workshop, and I'd encourage you to have both set up. They have different strengths:

- **VS Code Copilot Chat** has a rich UI — inline diffs, file references, one-click apply, and easy back-and-forth. It's best for **involved tasks** that need your guidance, manual input, or iterative refinement. When you need to steer the agent, review changes visually, or have a conversation, this is where you want to be.

- **Copilot CLI** (or Agency) is best for **well-defined tasks** that probably don't need intervention. Write a clear prompt, let it run, come back when it's done. The key advantage: you can run **multiple CLI instances in parallel** — each in its own terminal, each working on a separate task independently. One can be writing tests, another refactoring a module, a third generating documentation — all at the same time.

The workflow I use: kick off CLI sessions with well-scoped tasks (if I have multiple to do), then work in VS Code Chat on whatever needs the most hands-on attention.
