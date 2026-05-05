# Part 3: Enterprise Agents (Microsoft 365 Copilot)

Parts 1 and 2 covered developer-facing agents — markdown files that steer the model and programmatic extensions that run as web services. This part covers the **enterprise side**: agents built inside the Microsoft 365 Copilot platform, designed for business users and distributed through the org.

These agents live in the M365 ecosystem. They appear inside Microsoft 365 Copilot Chat, Teams, Word, and PowerPoint — right where your users already work. They can be grounded in SharePoint documents, Outlook emails, Teams chats, and external data via Copilot connectors.

---

## What's Built-In

Before any customization, Microsoft 365 Copilot already has:

- **M365 Copilot Chat** — the general-purpose chat experience at [m365.cloud.microsoft/chat](https://m365.cloud.microsoft/chat)
- **In-app Copilot** — Copilot inside Word, PowerPoint, Excel, Teams, Outlook
- **Microsoft Graph grounding** — Copilot can reason over your org's files, emails, calendar, and people
- **Copilot connectors** — pre-built integrations that bring external data into Copilot's reach

Custom agents extend this by focusing Copilot on a specific task, knowledge domain, or workflow.

---

## Two Types of M365 Agents

| Type | What It Is | Best For |
|------|-----------|----------|
| **Declarative Agent** | A customized version of M365 Copilot — you declare instructions, knowledge sources, and capabilities. Runs on the same Copilot orchestrator and models. | Business scenarios that leverage existing M365 data — IT help desks, onboarding bots, policy Q&A, project assistants |
| **Custom Engine Agent** | A fully custom agent that uses your own AI model (Azure OpenAI, etc.) but surfaces inside the M365 Copilot UI. | Advanced scenarios where you need a different model, custom RAG pipeline, or external AI service |

For this workshop we'll focus on **declarative agents** — they're the most accessible and cover the majority of enterprise use cases.

---

## What's Best Suited For

Use M365 declarative agents when:

| Need | Why M365 > `.agent.md` or SDK |
|------|---------------------------------|
| **Enterprise distribution** | Agents are published through the Microsoft 365 admin center — IT controls who gets them |
| **M365 data grounding** | SharePoint sites, OneDrive files, Outlook emails, Teams chats — all available as knowledge sources |
| **No-code / low-code** | Agent Builder lets anyone create agents with natural language — no IDE or coding required |
| **Copilot connectors** | Bring external data (ServiceNow, Jira, Salesforce, etc.) into your agent via pre-built connectors |
| **Familiar UI** | Agents appear inside the apps your users already use — M365 Copilot Chat, Teams, Word, PowerPoint |
| **Security & compliance** | Inherits M365 data protections, admin controls, and Responsible AI guardrails |

If your audience is developers working in code, use `.agent.md` or the SDK. If your audience is the broader org, use M365 agents.

---

## Three Ways to Build a Declarative Agent

| Tool | Best For | Requires Coding? |
|------|----------|-------------------|
| **Agent Builder** (in M365 Copilot) | Quick agents built with natural language — anyone can do it | No |
| **Copilot Studio** | Advanced agents with custom topics, triggers, and multi-turn flows | Low-code |

---

## Prerequisites

- A **Microsoft 365 Copilot license** (all workshop attendees should already have this)
- Access to [m365.cloud.microsoft/chat](https://m365.cloud.microsoft/chat)

---

## Workshop Exercise: Build a Declarative Agent

### Agent Builder

This uses the built-in Agent Builder right inside Microsoft 365 Copilot.

#### Step 1 — Open Agent Builder

1. Go to [m365.cloud.microsoft/chat](https://m365.cloud.microsoft/chat)
2. Click **New agent** (in the left sidebar or the chat area)

#### Step 2 — Describe your agent with natural language

In the **Describe** tab, tell Copilot what agent you want to build. For example:

> "Create an agent that helps new team members onboard. It should answer questions about our team's processes, coding standards, and project setup. It should be friendly and concise."

Agent Builder will automatically generate:
- A **name** and **description**
- **Instructions** for the agent
- **Starter prompts** (suggested questions users can ask)

#### Step 3 — Add knowledge sources

You can add knowledge in two ways:
- **In the Describe tab**: Use the **+** button in the chat box to attach SharePoint sites, folders, or files
- **In the Configure tab**: Manually add up to 20 knowledge sources

For this exercise, add a SharePoint site or folder that contains team documentation (or any site you have access to).

#### Step 4 — Review the configuration

Switch to the **Configure** tab to review what Agent Builder generated:

| Field | Description |
|-------|-------------|
| **Name** | Display name (max 30 characters) |
| **Description** | Helps the LLM identify when to use this agent (max 1,000 characters) |
| **Instructions** | Detailed behavior instructions for the agent (max 8,000 characters) |
| **Knowledge** | SharePoint sites, files, Copilot connectors, or personal data sources |
| **Capabilities** | Optional: code interpreter, image generator |
| **Starter Prompts** | Suggested questions shown to users |

Edit any fields you want to refine.

#### Step 5 — Test it

Switch to the **Try it** tab. Ask your agent a question related to the knowledge sources you added. Verify it responds appropriately and uses the right data.

#### Step 6 — Share it

Once you're happy with the agent:
1. Click **Share** or **Publish**
2. Choose who can access it — just you, specific people, or your whole org
3. The agent appears in the M365 Copilot sidebar for anyone you've shared it with

---

## Key Takeaways

- **M365 declarative agents** customize Copilot for business scenarios — no new infrastructure needed
- **Agent Builder** (no-code) lets anyone build an agent with natural language in minutes
- **Knowledge sources** (SharePoint, Copilot connectors, personal data) are what make M365 agents powerful — they ground responses in your org's actual data
- **Enterprise controls** — agents are managed through the Microsoft 365 admin center, with built-in security and compliance
- **Declarative agents** run on the same Copilot orchestrator and models — you're customizing behavior, not hosting infrastructure

---

## Sources

| Resource | Link |
|----------|------|
| M365 Copilot Extensibility Overview | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/) |
| Declarative Agents Overview | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-declarative-agent) |
| Build Agents with Agent Builder | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-build-agents) |
| Write Effective Instructions | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/declarative-agent-instructions) |
| Agents Overview (Declarative vs Custom Engine) | [Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview) |
