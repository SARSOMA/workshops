# Part 2 Exercise: ADO Code Review Agent (Programmatic)

In Part 1 you built a code reviewer with a markdown file. It worked — but you had no control over how the PR was fetched, couldn't enforce a structured output, and couldn't add custom logic. This exercise builds the same code reviewer as a standalone Python script, showing where custom code adds value.

**What this shows:** With a programmatic agent you control the entire pipeline — parse the PR URL, configure a Copilot SDK session with the ADO MCP server, let the model drive all tool calls to fetch the PR and post **inline** review comments directly, all within a single 90-second session.

---

### Step 1 — Create the project

```bash
mkdir code-review-script && cd code-review-script
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install github-copilot-sdk
```

### Step 2 — Create the `.env` file

Create a `.env` file in your project directory to store configuration:

```env
GITHUB_TOKEN=<your-github-token>
ADO_ORG=msazure
ADO_AUTH_MODE=interactive
```

**Auth mode options** (`ADO_AUTH_MODE`):
- `interactive` *(default)* — browser login prompt, works in local development
- `pat` — non-interactive PAT auth; also set `PERSONAL_ACCESS_TOKEN=base64('<email>:<pat>')`
- `envvar` — bearer token auth; also set `ADO_MCP_AUTH_TOKEN=<System.AccessToken>`

> **Tip:** Never commit `.env` to source control.
> The `GITHUB_TOKEN` authenticates the Copilot SDK — use a classic GitHub token with
> `read:org` scope (same as `gh auth token`).

To load these variables into your shell before running:

```bash
set -a && source .env && set +a
```

### Step 3 — Write the script

Create `review_pr.py`:

```python
"""
ADO Code Review Script — Inline Comments Edition

Uses the Copilot SDK with the ADO MCP server to review a PR and post
individual inline comments on each changed file/line.

Usage:
    python review_pr.py https://dev.azure.com/msazure/one/_git/my-repo/pullrequest/12345
"""

import os
import re
import sys
import asyncio
from copilot import (
    CopilotClient,
    SessionConfig,
    MessageOptions,
    MCPLocalServerConfig,
)
from copilot.generated.session_events import SessionEventType

ADO_ORG = os.environ.get("ADO_ORG", "msazure")
# Auth mode for the ADO MCP server: "envvar" (bearer token via ADO_MCP_AUTH_TOKEN),
# "pat" (PAT via PERSONAL_ACCESS_TOKEN), or "interactive" (browser login).
ADO_AUTH_MODE = os.environ.get("ADO_AUTH_MODE", "interactive")
# GitHub token for Copilot SDK authentication.
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def parse_ado_pr_url(url: str) -> dict | None:
    """Extract org, project, repo, and PR ID from an ADO pull request URL."""
    pattern = r"dev\.azure\.com/([^/]+)/([^/]+)/_git/([^/]+)/pullrequest/(\d+)"
    match = re.search(pattern, url)
    if not match:
        return None
    return {
        "org": match.group(1),
        "project": match.group(2),
        "repo": match.group(3),
        "pr_id": int(match.group(4)),
    }


REVIEW_SYSTEM_PROMPT = """\
You are a senior engineer performing a code review using the ADO MCP tools available to you.

Given a PR URL, you must complete the review in EXACTLY 3 steps with NO additional tool calls:

STEP 1: Call ado-repo_get_pull_request_by_id once to read the PR title and description.

STEP 2: Call ado-repo_get_pull_request_changes ONCE with (top=10, includeDiffs=true,
        includeLineContent=true). Do not paginate — review only what is returned.

STEP 3: For each meaningful finding in the diff, call ado-repo_create_pull_request_thread
        to post ONE inline comment per issue:
        - filePath: the file path
        - rightFileStartLine / rightFileEndLine: the line number in the new file
        - rightFileStartOffset / rightFileEndOffset: 1
        - content: prefix with severity icon:
            🔴 **Critical**: <message>   — must fix before merge
            🟡 **Warning**: <message>    — should address
            🟢 **Suggestion**: <message> — nice to have
        Post one final summary thread (no filePath) titled "## Code Review Summary"
        with overall verdict: ✅ Approve, ⚠️ Request Changes, or 💬 Needs Discussion.

Rules:
- Only comment on meaningful issues — no formatting nits.
- Post at most 5 inline comments + 1 summary.
- Do not call any tool more than once.
- Do not fetch individual file contents.
- Respond with "Review complete." after all tool calls are done."""


def _log_event(event) -> None:
    """Print notable session events for progress visibility."""
    t = event.type
    if t == SessionEventType.TOOL_EXECUTION_START:
        name = getattr(event.data, "mcp_tool_name", None) or getattr(event.data, "tool_name", "?")
        print(f"  🔧 Tool: {name}")
    elif t == SessionEventType.SESSION_IDLE:
        print("  💬 Session idle")
    elif t == SessionEventType.SESSION_ERROR:
        print(f"  ❌ Error: {event.data}")


async def run_review(pr_url: str) -> None:
    """Create a Copilot session with ADO MCP and let the model drive the review."""
    client_opts = {"github_token": GITHUB_TOKEN} if GITHUB_TOKEN else {}
    client = CopilotClient(client_opts)
    await client.start()
    try:
        session = await client.create_session(SessionConfig(
            model="gpt-5",
            system_message={"content": REVIEW_SYSTEM_PROMPT},
            available_tools=[
                "ado-repo_get_pull_request_by_id",
                "ado-repo_get_pull_request_changes",
                "ado-repo_create_pull_request_thread",
            ],
            mcp_servers={
                "ado": MCPLocalServerConfig(
                    command="npx",
                    args=["-y", "@azure-devops/mcp", ADO_ORG,
                          "--authentication", ADO_AUTH_MODE],
                    env={k: v for k, v in os.environ.items()},
                    tools=["*"],
                ),
            },
        ))
        session.on(_log_event)
        response = await session.send_and_wait(
            MessageOptions(prompt=f"Review this PR and post inline comments: {pr_url}"),
            timeout=90,
        )
        await session.destroy()
        if response:
            print(f"\n{response.data.content}")
    except asyncio.TimeoutError:
        print("\n⚠ Timeout reached — any comments posted so far remain on the PR.")
    finally:
        await client.stop()


async def async_main():
    if len(sys.argv) != 2:
        print("Usage: python review_pr.py <ADO_PR_URL>", file=sys.stderr)
        sys.exit(1)

    if ADO_AUTH_MODE == "envvar" and not os.environ.get("ADO_MCP_AUTH_TOKEN"):
        print(
            "Error: ADO_MCP_AUTH_TOKEN environment variable is not set.\n"
            "Required when ADO_AUTH_MODE=envvar. Set it to a bearer token (e.g. System.AccessToken).",
            file=sys.stderr,
        )
        sys.exit(1)
    elif ADO_AUTH_MODE == "pat" and not os.environ.get("PERSONAL_ACCESS_TOKEN"):
        print(
            "Error: PERSONAL_ACCESS_TOKEN environment variable is not set.\n"
            "Required when ADO_AUTH_MODE=pat. Set it to base64('<email>:<pat>').",
            file=sys.stderr,
        )
        sys.exit(1)

    pr_url = sys.argv[1]
    if not parse_ado_pr_url(pr_url):
        print("Error: Could not parse ADO PR URL.", file=sys.stderr)
        print(
            "Expected format: https://dev.azure.com/org/project/_git/repo/pullrequest/12345",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Starting review: {pr_url}")
    await run_review(pr_url)
    print("Done.")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
```

### Step 4 — Run it

```bash
cd code-review-script && set -a && source .env && set +a && .venv/bin/python3 review_pr.py "https://dev.azure.com/org/project/_git/repo/pullrequest/12345"
```

The script will:
1. Open a Copilot SDK session with the ADO MCP server attached
2. Let the Copilot model drive all tool calls: fetch PR, fetch diffs, post inline comments
3. Print each tool call as it happens so you can follow the agent's progress
4. Post up to 5 inline review comments + a summary directly on the PR

---

## Comparing Part 1 vs Part 2

Both exercises built the same thing — an ADO code review agent. Here's how they compare:

| | Part 1: Markdown Agent | Part 2: Python Script |
|---|---|---|
| **Setup time** | ~2 minutes | ~10 minutes |
| **Code required** | 0 lines — just markdown | ~150 lines of Python |
| **How you run it** | Select agent in Copilot Chat, paste a PR URL | Run a script with the PR URL as an argument |
| **ADO integration** | Via built-in MCP tools (agent calls them) | Via Copilot SDK + ADO MCP server configured in session |
| **Review logic** | Model decides based on your instructions | You shape the prompt, restrict tools, and control tool call budget |
| **Output format** | Free-form markdown | Inline comments on specific files and lines + summary thread |
| **Posts comments** | Only if you ask it to | Automatically posts inline comments on each file/line + a summary |
| **Error handling** | Model handles errors (may hallucinate) | You catch API errors and return clear messages |
| **Automation** | Manual — you invoke it in chat | Scriptable — can run in CI/CD, cron, or batch over multiple PRs |
| **Best for** | Interactive, one-off reviews | Automated pipelines, batch reviews, custom workflows |

**The takeaway:** Start with a markdown agent. When you need automation, custom logic, or CI/CD integration, graduate to a script.

