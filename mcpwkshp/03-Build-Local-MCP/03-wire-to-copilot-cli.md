# 3.3 — Wire Repo Doctor into Copilot CLI

---

## Concept

Our server speaks stdio. To make Copilot CLI launch it, we add an entry to:

```
~/.copilot/mcp-config.json
```

Copilot CLI will spawn the command we specify, hand it stdio, and connect.

```
┌────────────────────┐    spawn (stdio)   ┌──────────────────────┐
│  Copilot CLI       │  ───────────────►  │  uv run server.py    │
│  (MCP client)      │  ◄───────────────  │  Repo Doctor server  │
└────────────────────┘     JSON-RPC       └──────────────────────┘
```

You can edit `mcp-config.json` by hand, or use the built-in wizard. We'll do both, so you know what the wizard writes.

---

## Practice

### Step 1 — Find the absolute path to your project

In the `repo-doctor` directory you created in §3.1:

```bash
# macOS / Linux
pwd

# Windows PowerShell
(Get-Location).Path
```

Copy it — you'll paste it in the next step. Below we'll call it `<REPO_DOCTOR_PATH>`.

### Step 2 — Option A: use the `/mcp add` wizard

Inside a Copilot CLI session:

```
/mcp add
```

Fill in:

| Field | Value |
|-------|-------|
| Server Name | `repo-doctor` |
| Server Type | `1` (Local) |
| Command | `uv` |
| Arguments | `run --project <REPO_DOCTOR_PATH> python server.py` |
| Environment Variables | *(leave blank)* |
| Tools | `*` |

Press **Ctrl+S** (or **Cmd+S** on macOS) to save.

### Step 2 — Option B: edit `mcp-config.json` by hand

Open `~/.copilot/mcp-config.json` and add a `repo-doctor` entry under `mcpServers`:

```json
{
  "mcpServers": {
    "repo-doctor": {
      "type": "local",
      "command": "uv",
      "args": [
        "run",
        "--project",
        "<REPO_DOCTOR_PATH>",
        "python",
        "server.py"
      ],
      "tools": ["*"]
    }
  }
}
```

> Don't forget to expand `<REPO_DOCTOR_PATH>` to the absolute path you grabbed in Step 1.

If you already have other servers configured, just merge the `repo-doctor` key alongside them — don't replace the whole file.

### Step 3 — Verify

Restart Copilot CLI (exit and run `copilot` again). Then:

```
/mcp
```

You should see `repo-doctor` listed alongside any other servers. If not, run:

```
/mcp help
```

…and double-check the path and command.

### Step 4 — Drive it from natural language

Now the fun part. Inside the Copilot CLI session, **`cd` into one of your real repos first**, then try these:

```
Run a health check on this repo.
```

```
What's wrong with the build right now?
```

```
Show me the last repo-doctor report.
```

```
This repo failed lint — what should I fix first?
```

Watch which tools Copilot picks. Notice that you never named a tool — the model read your docstrings and chose.

### Step 5 — Observe the report

After `health_report` runs, you should have a fresh `repo-doctor-report.md` in the repo you diagnosed. Open it.

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---------|--------------------|
| `repo-doctor` not in `/mcp` | Restart Copilot CLI; check `~/.copilot/mcp-config.json` is valid JSON |
| "command not found: uv" | Copilot CLI doesn't see `uv` on PATH. Use the **absolute path** to `uv` (e.g. `~/.local/bin/uv`) in `command:` |
| "No such file or directory: server.py" | The `--project <path>` argument must be the **absolute path** to the repo-doctor folder, and `server.py` must live there |
| Tools listed but call hangs | Open the Inspector (`uv run mcp dev server.py`) and reproduce — likely a Python exception inside a tool. Logs print to stderr. |

---

## What we built

```
┌──────────────────────────────────────────────────────────────────┐
│                  REPO DOCTOR — END-TO-END                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User:  "Run a health check on this repo"                        │
│            │                                                     │
│  Copilot CLI  ─── picks tool: `health_report` ───►               │
│            │                                                     │
│            ▼  JSON-RPC over stdio                                │
│  Repo Doctor (Python)                                            │
│    │                                                             │
│    ├─► subprocess: ruff check / pytest / npm test / cargo …      │
│    ├─► truncate output                                           │
│    ├─► write repo-doctor-report.md                               │
│    └─► return { score, report_path, summary }                    │
│            │                                                     │
│            ▼                                                     │
│  Copilot CLI: "Score 78/100. Lint passed, 2 test failures…"      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

You now have a real MCP server that's useful, opinionated, and ~250 lines of Python.

---

## Q&A

### Question 1
After editing `~/.copilot/mcp-config.json` you don't see `repo-doctor` in `/mcp`. What's the first thing to do?

A) Reboot
B) Restart Copilot CLI — it loads MCP config on startup
C) Rebuild Python
D) Run `uv pip install` again

<details><summary>Answer</summary>

**B.** Copilot CLI reads `mcp-config.json` when it starts. Quit and relaunch.

</details>

### Question 2
Why use absolute paths in `args`?

A) Performance
B) The MCP server is spawned with the home directory as cwd (or whatever Copilot picks) — relative paths break
C) Required by JSON
D) Stylistic preference

<details><summary>Answer</summary>

**B.** Always pin paths in process-spawn configs.

</details>

---

## Next

You earned the break. ☕  See you in §4 for the remote MCP demo on Azure.

→ [§4 — Remote MCP on Azure](../04-Remote-MCP-on-Azure/README.md)
