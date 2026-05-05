# Part 1 Exercise: ADO Code Review Agent (Markdown)

In this exercise you'll build a code review agent using a `.agent.md` file. The agent uses the built-in ADO MCP tools to fetch pull request details and review the code — no custom server, no code to write.

**What this shows:** You can create a useful, specialized agent in under 5 minutes with just a markdown file and existing MCP tools.

---

## Step 1 — Create the agent file

Create `.github/agents/code-reviewer.agent.md` in your workspace:

~~~markdown
---
description: Reviews Azure DevOps pull requests for code quality, bugs, and best practices
tools: ['ado/*', 'search', 'read']
model: Claude Opus 4.7 (copilot)
---

# ADO Code Reviewer

You are a senior engineer performing code reviews on Azure DevOps pull requests.

## Workflow

1. When given an ADO pull request URL, use the ADO tools to fetch the PR details and file changes
2. Review each changed file for issues
3. Provide your review in the format below

## What to Check

- Logic errors and potential bugs
- Security issues (hardcoded secrets, injection, missing validation)
- Performance concerns (unnecessary loops, missing indexes, N+1 queries)
- Readability and naming
- Missing error handling

## Response Format

For each file with findings, use this structure:

### `<filename>`

- 🔴 **Critical** — must fix before merge
- 🟡 **Warning** — should address
- 🟢 **Suggestion** — nice to have

End with a brief summary: approve, request changes, or needs discussion.

## Rules

- Be specific — reference line numbers and show the problematic code
- Don't nitpick formatting if there's a formatter configured
- Acknowledge what's done well
- If the PR is clean, say so — don't manufacture issues
~~~

## Step 2 — Use the agent

### In VS Code Copilot Chat

1. Select **code-reviewer** from the agents dropdown
2. Paste an ADO pull request URL:

   ```
   Review this PR: https://dev.azure.com/your-org/your-project/_git/your-repo/pullrequest/12345
   ```

3. The agent will use the ADO MCP tools to fetch the PR diff and review it

### In Copilot CLI / Agency

```bash
# Interactive — select the code-reviewer agent
/agent

# Or by inference — Copilot picks the agent based on your prompt
Review the PR at https://dev.azure.com/your-org/your-project/_git/your-repo/pullrequest/12345

# Or programmatically
copilot --agent code-reviewer --prompt "Review https://dev.azure.com/your-org/your-project/_git/your-repo/pullrequest/12345"
```

---

## What You Just Built

| Aspect | What happened |
|--------|---------------|
| **Time to build** | ~2 minutes |
| **Lines of code** | 0 — just markdown |
| **How it works** | Your instructions are injected into the system prompt; the ADO MCP tools handle the API calls |
| **Limitations** | You can't customize the review logic, enforce a specific output format programmatically, or add pre/post-processing steps |

This is the strength of markdown agents: **fast to create, easy to iterate, zero infrastructure**. But you're limited to what the model and its tools can do — you can't add custom logic or enforce structure beyond what the instructions suggest.

> In Part 2, you'll build the same code reviewer as a programmatic extension and see where custom code adds value.

The programmatic mode (`--agent`) is especially useful for scripting and CI/CD pipelines.
