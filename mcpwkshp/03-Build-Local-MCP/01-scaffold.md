# 3.1 — Scaffold your MCP server

---

## Concept

We'll use [FastMCP](https://github.com/modelcontextprotocol/python-sdk) — the official Python SDK's high-level API. It turns Python functions into MCP tools with one decorator.

We'll use [uv](https://docs.astral.sh/uv/) for project + dependency management. It's much faster than pip and gives us a clean, isolated project.

The pattern you'll repeat for every MCP server you write:

```
1. uv init <project>
2. uv add "mcp[cli]"
3. Write server.py with `mcp = FastMCP("name")` and a tool
4. mcp dev server.py  ← MCP Inspector lets you click-test it
5. Wire into your MCP client (Copilot CLI, VS Code, …)
```

---

## Practice

### Step 1 — Create the project

> Pick a folder you don't mind keeping (e.g. `~/code/repo-doctor`). The path matters in §3.3, so write it down.

```bash
uv init repo-doctor
cd repo-doctor
uv add "mcp[cli]"
```

What just happened:
- `uv init` created `pyproject.toml`, `.python-version`, and a `hello.py` we'll replace
- `uv add "mcp[cli]"` installed the MCP Python SDK + the `mcp` CLI tool (used for the Inspector)

### Step 2 — Write the smallest possible MCP server

Replace the contents of `hello.py` (or create a new file `server.py` — we'll standardise on that name) with:

```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("repo-doctor")


@mcp.tool()
def ping() -> str:
    """Health check — returns 'pong' to prove the server is alive."""
    return "pong"


if __name__ == "__main__":
    mcp.run()
```

Things worth noticing:

| Line | What it does |
|------|--------------|
| `FastMCP("repo-doctor")` | The server's name — clients show this in lists |
| `@mcp.tool()` | Registers `ping` as an MCP tool |
| The **docstring** | This is what the LLM reads to decide whether to call the tool. Treat it as part of the API. |
| `mcp.run()` | Defaults to stdio transport — perfect for local |

### Step 3 — Verify with the MCP Inspector

The MCP Inspector is a built-in browser UI that lets you click-call your tools without wiring up Copilot yet.

```bash
uv run mcp dev server.py
```

This will:
- Start your server in dev mode
- Spawn the Inspector and print a URL like `http://localhost:6274`
- Open the URL in your browser

In the Inspector:
1. Click **Connect**
2. Go to the **Tools** tab — you should see `ping`
3. Click `ping` → **Run Tool** → you get back `"pong"`

🎉 You have a working MCP server.

> Leave the Inspector open in another tab while you work — it's the fastest feedback loop. Edit code, save, click **Reconnect**, test.

---

## Q&A

### Question 1
What does the `@mcp.tool()` decorator do?

A) Speeds up the function
B) Registers the function as an MCP tool and uses its signature + docstring as the tool's schema
C) Wraps the function in a try/except
D) Adds caching

<details><summary>Answer</summary>

**B.** FastMCP introspects the function's Python types and docstring to build the tool's MCP schema. Type hints aren't optional — they become the parameter schema the LLM sees.

</details>

### Question 2
Why does the docstring matter so much?

A) PEP 257 says it should
B) The LLM reads the docstring (along with the function/parameter names) to decide whether to call this tool. Vague docstring → tool ignored or misused.
C) It's used for log lines
D) It's not important

<details><summary>Answer</summary>

**B.** Tool selection is a "given the user's request and these tool descriptions, which tool fits?" problem. Your docstring is your sales pitch to the model.

</details>

---

## Next

→ [3.2 — Add the Repo Doctor tools and resources](./02-add-tools.md)
