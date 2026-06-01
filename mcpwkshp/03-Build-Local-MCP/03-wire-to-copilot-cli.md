# 3.3 — Wire Repo Doctor into Copilot CLI

---

## Concept

Our server speaks stdio. To make Copilot CLI launch it, we add an entry to its
MCP config file:

| OS | Path |
|---|---|
| macOS / Linux | `~/.copilot/mcp-config.json` |
| Windows | `%USERPROFILE%\.copilot\mcp-config.json` |

Copilot CLI will spawn the command we specify, hand it stdio, and connect.

```
┌────────────────────┐    spawn (stdio)   ┌──────────────────────┐
│  Copilot CLI       │  ───────────────►  │  uv run server.py    │
│  (MCP client)      │  ◄───────────────  │  Repo Doctor server  │
└────────────────────┘     JSON-RPC       └──────────────────────┘
```

You can edit the config by hand, or use the built-in wizard. We'll do both, so
you know what the wizard writes.

> 🔬 **Want to see the actual JSON-RPC messages** that flow over that arrow?
> §4.4 (*The MCP handshake, on the wire*) walks through them line by line.

---

## Practice

### Step 1 — Find the absolute path to your project

**If you built the server yourself in §3.1 and §3.2,** use that folder.

**If you cloned this workshop repo and just want to run the finished server,** point at the prebuilt copy:

```bash
# from the workshop repo root
cd mcpwkshp/03-Build-Local-MCP/server
uv sync       # one-time: creates .venv and installs deps
```

Then grab the path to that `server` folder:

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
| Arguments | `run --directory <REPO_DOCTOR_PATH> python server.py` |
| Environment Variables | *(leave blank)* |
| Tools | `*` |

Press **Ctrl+S** (or **Cmd+S** on macOS) to save.

### Step 2 — Option B: edit the config file by hand

Open the MCP config file (`~/.copilot/mcp-config.json` on macOS/Linux, or
`%USERPROFILE%\.copilot\mcp-config.json` on Windows) and add a `repo-doctor`
entry under `mcpServers`:

```json
{
  "mcpServers": {
    "repo-doctor": {
      "type": "local",
      "command": "uv",
      "args": [
        "run",
        "--directory",
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
>
> 💡 **Why `--directory` (not `--project`)?** `--project` sets the project context but does **not** change the working directory. Copilot CLI spawns the server from your home directory (or wherever it was launched), so `python server.py` would fail to find the script. `--directory` sets both project *and* cwd → `server.py` resolves correctly.

If you already have other servers configured, just merge the `repo-doctor` key alongside them — don't replace the whole file.

### Step 3 — Verify

Restart Copilot CLI (exit and run `copilot` again). Then:

```
/mcp
```

You should see `repo-doctor` listed alongside any other servers, with a green
status indicator. A healthy entry looks like:

```
MCP servers
  repo-doctor          ✓ Ready    5 tools
  …your other servers…
```

If `repo-doctor` shows ✗ / `Connection closed` or is missing entirely, jump to
the **Troubleshooting** section below.

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

### `MCP error -32000: Connection closed` (the most common failure)

This means the child process exited *before* finishing the MCP `initialize` handshake — i.e., it never even said hello. **Always reproduce by running the exact command from your shell:**

```powershell
uv run --directory <REPO_DOCTOR_PATH> python server.py
```

You'll see one of:

| Output | Diagnosis | Fix |
|---|---|---|
| `'uv' is not recognized` / `command not found: uv` | `uv` isn't installed or isn't on PATH | Install it: `winget install --id=astral-sh.uv` (Windows) or `curl -LsSf https://astral.sh/uv/install.sh \| sh` (macOS/Linux). **Open a new shell**, then verify with `uv --version`. |
| `No such file or directory: server.py` | You used `--project` instead of `--directory`, so cwd isn't the project | Switch the flag to `--directory` (see Step 2). |
| Python traceback | Import error / syntax error in `server.py` | Fix the code; re-run `uv run mcp dev server.py` for the Inspector. |
| **Silent — just hangs** | ✅ **Success.** A healthy stdio MCP server waits for JSON-RPC on stdin. Press Ctrl+C — Copilot CLI will be able to talk to it. | (no action) |

### Other symptoms

| Symptom | Likely cause / fix |
|---------|--------------------|
| `repo-doctor` not in `/mcp` | Restart Copilot CLI; check that the MCP config file is valid JSON (no trailing commas) |
| Copilot CLI still says `Connection closed` after installing uv | You didn't restart Copilot CLI in a fresh shell that sees the new PATH. Quit, open a new terminal, run `copilot` again. |
| "command not found: uv" but `uv --version` works in your shell | Copilot CLI was launched from a session before `uv` was installed. Use the **absolute path** to `uv` (e.g., `C:\Users\<you>\.local\bin\uv.exe` on Windows, `/Users/<you>/.local/bin/uv` on macOS) in `command:`. |
| Tools listed but call hangs | Open the Inspector (`uv run mcp dev server.py`) and reproduce — likely a Python exception inside a tool. Logs print to stderr. |
| `run_build` times out at 120s on Windows with `python -m compileall` | Bare `"python"` from PATH resolved to the Microsoft Store stub (`%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe`), which can hang when stdin/stdout are piped. The reference `server.py` avoids this by invoking `sys.executable` instead of `"python"`. If you typed your own version, mirror that change. To verify the stub is the culprit: `Get-Command python` — if `Source` is under `WindowsApps`, that's the stub. |
| `run_lint` / `run_tests` say "not on PATH" after `uv tool install ruff pytest` | `uv tool install` drops binaries in `~/.local/bin`, which isn't on PATH by default. Run `uv tool update-shell`, then **close every terminal and Copilot CLI session** so the new PATH is inherited. |

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
After editing the MCP config file you don't see `repo-doctor` in `/mcp`. What's the first thing to do?

A) Reboot
B) Restart Copilot CLI — it loads MCP config on startup
C) Rebuild Python
D) Run `uv pip install` again

<details><summary>Answer</summary>

**B.** Copilot CLI reads the MCP config when it starts. Quit and relaunch.

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

You earned the break. ☕

Up next: **[§4 — Remote MCP on Azure](../04-Remote-MCP-on-Azure/README.md)** —
take the same JSON-RPC protocol, swap stdio for HTTP, and host it as a
Container App.

> 🔬 **Curious what just flowed over that stdio pipe?**
> [§4.4 — The MCP handshake](../04-Remote-MCP-on-Azure/04-mcp-handshake.md) walks
> through `initialize` → `tools/list` → `tools/call` byte-by-byte. The
> protocol is identical to what your local server just spoke; only the
> transport changes.

→ [§4 — Remote MCP on Azure](../04-Remote-MCP-on-Azure/README.md)
