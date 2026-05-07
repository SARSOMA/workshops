# Part 2 Exercise: ADO Code Review Agent (Programmatic)

In Part 1 you built a code reviewer with a markdown file. It worked — but you had no control over how the PR was fetched, couldn't enforce a structured output, and couldn't add custom logic. This exercise builds the same code reviewer as a Copilot Extension, showing where custom code adds value.

**What this shows:** With a programmatic agent you control the entire pipeline — parse the PR URL, call the ADO MCP server programmatically, shape the prompt, and enforce structured output.

---

### Step 1 — Create the project

```bash
mkdir code-review-extension && cd code-review-extension
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install flask requests python-dotenv mcp
```

### Step 2 — Create the `.env` file

Create a `.env` file in your project directory to store configuration:

```env
ADO_PAT=your_ado_pat_here
ADO_ORG=msazure
```

> **Tip:** Never commit `.env` to source control — add it to `.gitignore`. The PAT is passed to the ADO MCP server subprocess automatically via the process environment.

### Step 3 — Write the agent

Create `app.py`:

```python
import json
import os
import re
import asyncio
import requests as http_client
from flask import Flask, request, Response
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

app = Flask(__name__)

ADO_ORG = os.environ.get("ADO_ORG", "msazure")


# --- SSE helpers ---

def sse_event(event_type: str, data: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

def create_ack_event() -> str:
    return sse_event("copilot_confirmation", {"type": "ack"})

def create_text_event(message: str) -> str:
    return sse_event("copilot_message", {"type": "content", "body": message})

def create_done_event() -> str:
    return sse_event("copilot_confirmation", {"type": "done"})


# --- ADO MCP helpers ---

async def _call_ado_tool(tool_name: str, arguments: dict) -> str:
    """Connect to the ADO MCP server and call a tool."""
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@azure-devops/mcp", ADO_ORG],
        env={k: v for k, v in os.environ.items()},
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            if result.isError:
                raise RuntimeError(
                    result.content[0].text if result.content else "Unknown MCP error"
                )
            return result.content[0].text


def call_ado_tool(tool_name: str, arguments: dict) -> str:
    """Synchronous wrapper around the async MCP tool call."""
    return asyncio.run(_call_ado_tool(tool_name, arguments))


def parse_ado_pr_url(text: str) -> dict | None:
    """Extract org, project, repo, and PR ID from an ADO pull request URL."""
    pattern = r"dev\.azure\.com/([^/]+)/([^/]+)/_git/([^/]+)/pullrequest/(\d+)"
    match = re.search(pattern, text)
    if not match:
        return None
    return {
        "org": match.group(1),
        "project": match.group(2),
        "repo": match.group(3),
        "pr_id": int(match.group(4)),
    }


def fetch_pr_details(project: str, repo: str, pr_id: int) -> dict:
    """Fetch PR metadata via the ADO MCP server."""
    raw = call_ado_tool("repo_get_pull_request_by_id", {
        "repositoryId": repo,
        "pullRequestId": pr_id,
        "project": project,
        "includeChangedFiles": True,
    })
    return json.loads(raw)


def fetch_pr_changes(project: str, repo: str, pr_id: int) -> list[dict]:
    """Fetch changed files via the ADO MCP server."""
    raw = call_ado_tool("repo_get_pull_request_changes", {
        "repositoryId": repo,
        "pullRequestId": pr_id,
        "project": project,
        "includeDiffs": False,
    })
    data = json.loads(raw)
    return data.get("changes", data.get("changeEntries", []))


REVIEW_SYSTEM_PROMPT = """You are a senior engineer performing a code review.
Review the PR changes below. For each file, categorize findings as:
- 🔴 Critical — must fix before merge
- 🟡 Warning — should address
- 🟢 Suggestion — nice to have

End with a summary: approve, request changes, or needs discussion.
Be specific — reference line numbers. Don't nitpick formatting."""


def call_copilot_model(prompt_text: str, github_token: str) -> str:
    """Send a prompt to the Copilot model and return the response."""
    resp = http_client.post(
        "https://api.githubcopilot.com/chat/completions",
        headers={
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
        },
        json={
            "messages": [
                {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text},
            ],
            "model": "gpt-4o",
        },
    )
    data = resp.json()
    return data["choices"][0]["message"]["content"]


# --- Main handler ---

@app.route("/", methods=["GET", "POST"])
def handler():
    if request.method == "GET":
        return "ok"

    payload = request.get_json(force=True)
    messages = payload.get("messages", [])
    user_message = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_message = msg.get("content", "")
            break

    github_token = request.headers.get("x-github-token", "")

    def generate():
        yield create_ack_event()

        # 1. Parse the ADO PR URL from the user's message
        pr_info = parse_ado_pr_url(user_message)
        if not pr_info:
            yield create_text_event(
                "I couldn't find an ADO pull request URL in your message.\n\n"
                "Please send a link like: "
                "`https://dev.azure.com/org/project/_git/repo/pullrequest/12345`"
            )
            yield create_done_event()
            return

        yield create_text_event(
            f"Fetching PR #{pr_info['pr_id']} from "
            f"**{pr_info['org']}/{pr_info['project']}** via MCP...\n\n"
        )

        # 2. Fetch PR details and changes via ADO MCP server
        try:
            pr = fetch_pr_details(pr_info["project"], pr_info["repo"], pr_info["pr_id"])
            changes = fetch_pr_changes(pr_info["project"], pr_info["repo"], pr_info["pr_id"])
        except Exception as e:
            yield create_text_event(f"Error fetching PR via ADO MCP server: {e}")
            yield create_done_event()
            return

        # 3. Build a prompt with the PR context
        file_summary = "\n".join(
            f"- {c.get('item', {}).get('path', 'unknown')} ({c.get('changeType', 'unknown')})"
            for c in changes[:30]  # cap at 30 files
        )
        review_prompt = (
            f"## PR: {pr.get('title', 'Untitled')}\n"
            f"**Author:** {pr.get('createdBy', {}).get('displayName', 'Unknown')}\n"
            f"**Description:** {pr.get('description', 'No description')}\n\n"
            f"### Changed files:\n{file_summary}\n\n"
            f"Please review these changes."
        )

        # 4. Call the Copilot model with the structured prompt
        review = call_copilot_model(review_prompt, github_token)

        yield create_text_event(review)
        yield create_done_event()

    return Response(generate(), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
```

### Step 4 — Start the server

```bash
python app.py
```

### Step 5 — Get a public URL

**If using Codespaces:**
1. In the Ports tab, right-click port 3000 → Port Visibility → Public
2. Copy the forwarded URL

**If using ngrok:**
```bash
ngrok http 3000
```

### Step 6 — Create a GitHub App

1. Go to [github.com/settings/apps/new](https://github.com/settings/apps/new)
2. Fill in:
   - **App name**: `code-review-extension-yourname`
   - **Homepage URL**: your public URL
   - **Webhook URL**: your public URL
3. Under **Permissions**: set **Copilot Chat** → Read-only
4. Under **Where can this GitHub App be installed?**: select "Only on this account"
5. Click **Create GitHub App**

### Step 7 — Enable the Copilot Agent

1. In your GitHub App settings, find **Copilot** in the sidebar
2. Set **App type** to **Agent**
3. Save

### Step 8 — Install and test

1. Click **Install App** → install on your account
2. In VS Code Copilot Chat, type `@code-review-extension` and paste a PR URL:

   ```
   @code-review-extension Review https://dev.azure.com/your-org/your-project/_git/your-repo/pullrequest/12345
   ```

---

## Comparing Part 1 vs Part 2

Both exercises built the same thing — an ADO code review agent. Here's how they compare:

| | Part 1: Markdown Agent | Part 2: Programmatic Agent |
|---|---|---|
| **Setup time** | ~2 minutes | ~20 minutes |
| **Code required** | 0 lines — just markdown | ~150 lines of Python |
| **ADO integration** | Via built-in MCP tools (agent calls them) | Via MCP Python SDK — same ADO MCP server, called programmatically |
| **Review logic** | Model decides based on your instructions | You build the prompt — can add custom rules, context, or pre-processing |
| **Output format** | Suggested in instructions, not enforced | You can parse, validate, or restructure the model's output before returning it |
| **Error handling** | Model handles errors (may hallucinate) | You catch API errors and return clear messages |
| **Distribution** | Shared via `.github/agents/` in your repo | Published as a GitHub App — installable org-wide |
| **Best for** | Personal/team use, quick iteration | Production tools, org-wide distribution, custom workflows |

**The takeaway:** Start with a markdown agent. When you need custom logic, structured output, or org-wide distribution, graduate to a programmatic extension.
