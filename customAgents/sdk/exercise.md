# Part 2 Exercise: ADO Code Review Agent (Programmatic)

In Part 1 you built a code reviewer with a markdown file. It worked — but you had no control over how the PR was fetched, couldn't enforce a structured output, and couldn't add custom logic. This exercise builds the same code reviewer as a standalone Python script, showing where custom code adds value.

**What this shows:** With a programmatic agent you control the entire pipeline — parse the PR URL, call the ADO MCP server programmatically, shape the prompt, enforce structured JSON output, and post **inline** review comments on specific files and lines back to ADO.

---

### Step 1 — Create the project

```bash
mkdir code-review-script && cd code-review-script
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install mcp github-copilot-sdk
```

### Step 2 — Create the `.env` file

Create a `.env` file in your project directory to store configuration:

```env
ADO_ORG=msazure
ADO_AUTH_MODE=interactive
```

**Auth mode options** (`ADO_AUTH_MODE`):
- `interactive` *(default)* — browser login prompt, works in local development
- `pat` — non-interactive PAT auth; also set `PERSONAL_ACCESS_TOKEN=base64('<email>:<pat>')`
- `envvar` — bearer token auth; also set `ADO_MCP_AUTH_TOKEN=<System.AccessToken>`

> **Tip:** Never commit `.env` to source control.
> The Copilot SDK reuses your local GitHub Copilot authentication (via the
> Copilot CLI / VS Code session), so no `GITHUB_TOKEN` is needed.

To load these variables into your shell before running:

```bash
set -a && source .env && set +a
```

### Step 3 — Write the script

Create `review_pr.py`:

```python
"""
ADO Code Review Script — Inline Comments Edition

Posts individual review comments inline on each file/line in an ADO PR,
rather than a single monolithic comment.

Usage:
    python review_pr.py https://dev.azure.com/msazure/one/_git/my-repo/pullrequest/12345
"""

import json
import os
import re
import sys
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from copilot import (
    CopilotClient,
    SessionConfig,
    MessageOptions,
    PermissionHandler,
)

ADO_ORG = os.environ.get("ADO_ORG", "msazure")
# Auth mode for the ADO MCP server: "envvar" (bearer token via ADO_MCP_AUTH_TOKEN),
# "pat" (PAT via PERSONAL_ACCESS_TOKEN), or "interactive" (browser login).
ADO_AUTH_MODE = os.environ.get("ADO_AUTH_MODE", "interactive")


# --- ADO MCP helpers ---

class AdoMcpClient:
    """Keeps a single MCP session open for multiple tool calls."""

    def __init__(self):
        self._session: ClientSession | None = None

    async def _ensure_session(self, stack):
        if self._session is None:
            server_params = StdioServerParameters(
                command="npx",
                args=["-y", "@azure-devops/mcp", ADO_ORG,
                      "--authentication", ADO_AUTH_MODE],
                env={k: v for k, v in os.environ.items()},
            )
            read, write = await stack.enter_async_context(
                stdio_client(server_params)
            )
            self._session = await stack.enter_async_context(
                ClientSession(read, write)
            )
            await self._session.initialize()

    async def call_tool(self, stack, tool_name: str, arguments: dict) -> str:
        await self._ensure_session(stack)
        result = await self._session.call_tool(tool_name, arguments)
        if result.isError:
            raise RuntimeError(
                result.content[0].text if result.content else "Unknown MCP error"
            )
        return result.content[0].text


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


# --- Copilot model (via Copilot SDK) ---

REVIEW_SYSTEM_PROMPT = """\
You are a senior engineer performing a code review.
You will receive a PR description and the full diff (with line numbers) for each changed file.

Return your review as a JSON object with two keys:

1. "comments" — an array of inline findings. Each element must have:
   - "filePath": the full path of the file (e.g. "/src/main.go")
   - "line": the line number in the NEW version of the file to attach the comment to
   - "severity": one of "critical", "warning", or "suggestion"
   - "body": your review comment in markdown (1-3 sentences, actionable)

2. "summary" — a short markdown paragraph summarising the overall review.
   End with one of: ✅ Approve, ⚠️ Request Changes, or 💬 Needs Discussion.

Rules:
- Only comment on meaningful issues — no formatting nits.
- Every comment MUST reference a real line that exists in the diff.
- Return ONLY valid JSON — no markdown fences, no extra text."""

SEVERITY_ICONS = {"critical": "🔴", "warning": "🟡", "suggestion": "🟢"}


async def call_copilot_model(system_prompt: str, user_prompt: str) -> str:
    """Send a prompt to Copilot via the Copilot SDK and return the response."""
    client = CopilotClient()
    await client.start()
    try:
        session = await client.create_session(SessionConfig(
            model="gpt-5",
            system_message={"content": system_prompt},
            on_permission_request=PermissionHandler.approve_all,
        ))
        response = await session.send_and_wait(MessageOptions(prompt=user_prompt))
        await session.destroy()
        if not response:
            raise RuntimeError("Copilot SDK returned no response")
        return response.data.content
    finally:
        await client.stop()


def parse_review_json(raw: str) -> dict:
    """Parse the model response as JSON, stripping markdown fences if present."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return json.loads(text)


# --- Diff helpers ---

def build_file_diffs(changes_data: dict) -> list[dict]:
    """Extract per-file diffs from the MCP changes response."""
    entries = changes_data.get("changes", changes_data.get("changeEntries", []))
    file_diffs = []
    for entry in entries:
        item = entry.get("item", {})
        path = item.get("path", "")
        change_type = entry.get("changeType", "unknown")
        # Skip folders
        if item.get("isFolder"):
            continue
        diff_text = entry.get("diff", "")
        file_diffs.append({
            "path": path,
            "changeType": change_type,
            "diff": diff_text,
        })
    return file_diffs


# --- Main ---

async def async_main():
    if len(sys.argv) != 2:
        print("Usage: python review_pr.py <ADO_PR_URL>", file=sys.stderr)
        sys.exit(1)

    pr_info = parse_ado_pr_url(sys.argv[1])
    if not pr_info:
        print("Error: Could not parse ADO PR URL.", file=sys.stderr)
        print(
            "Expected format: https://dev.azure.com/org/project/_git/repo/pullrequest/12345",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate ADO auth credentials based on the selected auth mode
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

    project, repo, pr_id = pr_info["project"], pr_info["repo"], pr_info["pr_id"]
    ado = AdoMcpClient()

    async with AsyncExitStack() as stack:
        # 1. Fetch PR metadata
        print(f"Fetching PR #{pr_id} from {pr_info['org']}/{project}...")
        pr_raw = await ado.call_tool(stack, "repo_get_pull_request_by_id", {
            "repositoryId": repo,
            "pullRequestId": pr_id,
            "project": project,
            "includeChangedFiles": True,
        })
        pr = json.loads(pr_raw)

        # 2. Fetch diffs with line content
        print("Fetching file diffs...")
        changes_raw = await ado.call_tool(stack, "repo_get_pull_request_changes", {
            "repositoryId": repo,
            "pullRequestId": pr_id,
            "project": project,
            "includeDiffs": True,
            "includeLineContent": True,
            "top": 30,
        })
        changes_data = json.loads(changes_raw)
        file_diffs = build_file_diffs(changes_data)

        # 3. Build review prompt with actual diffs
        diff_sections = []
        for fd in file_diffs:
            section = f"### {fd['path']} ({fd['changeType']})\n"
            if fd["diff"]:
                section += f"```diff\n{fd['diff']}\n```\n"
            else:
                section += "(binary or no diff available)\n"
            diff_sections.append(section)

        review_prompt = (
            f"## PR: {pr.get('title', 'Untitled')}\n"
            f"**Author:** {pr.get('createdBy', {}).get('displayName', 'Unknown')}\n"
            f"**Description:** {pr.get('description', 'No description')}\n\n"
            + "\n".join(diff_sections)
        )

        # 4. Generate structured review via the Copilot SDK
        print("Generating review...\n")
        raw_review = await call_copilot_model(REVIEW_SYSTEM_PROMPT, review_prompt)

        try:
            review = parse_review_json(raw_review)
        except json.JSONDecodeError:
            print("Model did not return valid JSON. Raw output:\n", file=sys.stderr)
            print(raw_review, file=sys.stderr)
            sys.exit(1)

        comments = review.get("comments", [])
        summary = review.get("summary", "No summary provided.")

        print(f"Got {len(comments)} inline comment(s).\n")
        print("--- Summary ---")
        print(summary)
        print()

        # 5. Post each comment as an inline thread
        for i, c in enumerate(comments, 1):
            file_path = c.get("filePath", "")
            line = c.get("line")
            severity = c.get("severity", "suggestion")
            icon = SEVERITY_ICONS.get(severity, "💬")
            body = f"{icon} **{severity.title()}**: {c.get('body', '')}"

            thread_args = {
                "repositoryId": repo,
                "pullRequestId": pr_id,
                "project": project,
                "content": body,
            }
            if file_path:
                thread_args["filePath"] = file_path
            if line and isinstance(line, int):
                thread_args["rightFileStartLine"] = line
                thread_args["rightFileStartOffset"] = 1
                thread_args["rightFileEndLine"] = line
                thread_args["rightFileEndOffset"] = 1

            print(f"  [{i}/{len(comments)}] {icon} {file_path}:{line or '?'}")
            try:
                await ado.call_tool(stack, "repo_create_pull_request_thread", thread_args)
            except RuntimeError as e:
                print(f"    ⚠ Failed to post: {e}", file=sys.stderr)

        # 6. Post the summary as a general (non-inline) thread
        print("\nPosting summary comment...")
        await ado.call_tool(stack, "repo_create_pull_request_thread", {
            "repositoryId": repo,
            "pullRequestId": pr_id,
            "project": project,
            "content": f"## Code Review Summary\n\n{summary}",
        })

    print("Done — all review comments posted to the PR.")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
```

### Step 4 — Run it

```bash
set -a && source .env && set +a
python review_pr.py https://dev.azure.com/msazure/one/_git/my-repo/pullrequest/12345
```

The script will:
1. Fetch the PR details and file diffs (with line content) via the ADO MCP server
2. Send the diffs to the Copilot model, which returns structured JSON with per-file findings
3. Post each finding as an **inline comment** on the specific file and line in the PR
4. Post an overall summary comment on the PR

---

## Comparing Part 1 vs Part 2

Both exercises built the same thing — an ADO code review agent. Here's how they compare:

| | Part 1: Markdown Agent | Part 2: Python Script |
|---|---|---|
| **Setup time** | ~2 minutes | ~10 minutes |
| **Code required** | 0 lines — just markdown | ~200 lines of Python |
| **How you run it** | Select agent in Copilot Chat, paste a PR URL | Run a script with the PR URL as an argument |
| **ADO integration** | Via built-in MCP tools (agent calls them) | Via MCP Python SDK — same ADO MCP server, called programmatically |
| **Review logic** | Model decides based on your instructions | You build the prompt — can add custom rules, context, or pre-processing |
| **Output format** | Free-form markdown | Structured JSON — you control severity labels, icons, and inline placement |
| **Posts comments** | Only if you ask it to | Automatically posts inline comments on each file/line + a summary |
| **Error handling** | Model handles errors (may hallucinate) | You catch API errors and return clear messages |
| **Automation** | Manual — you invoke it in chat | Scriptable — can run in CI/CD, cron, or batch over multiple PRs |
| **Best for** | Interactive, one-off reviews | Automated pipelines, batch reviews, custom workflows |

**The takeaway:** Start with a markdown agent. When you need automation, custom logic, or CI/CD integration, graduate to a script.
