# 3.2 — Add the Repo Doctor tools and resources

---

## Concept

Repo Doctor will expose:

**Tools (verbs)**
- `detect_stack(path)` — what kind of project is this?
- `run_lint(path)` — run the lint command, return summary + first errors
- `run_tests(path)` — run tests, return pass/fail counts where possible
- `run_build(path)` — run build, return exit code + tail of output
- `health_report(path)` — calls the above and writes `repo-doctor-report.md`

**Resources (nouns)**
- `repodoctor://template` — the markdown template used for the report
- `repodoctor://last-report` — the most recent `repo-doctor-report.md` from any path the user has diagnosed

### The teaching idea: context hygiene

A `pytest` run can dump thousands of lines. If you return that raw to the model, you blow up its context window for nothing.

**Rule of thumb for MCP tool authors:**

> Return what a human would *quote* from the output — not the whole output. Truncate to ~40 lines or 4 KB. Always include the exit code and the first error.

We'll bake this in.

---

## Practice

Replace `server.py` with the version below — this is the same code as the
reference implementation under [`server/server.py`](./server/). It's all in one
file so you can copy it as one block.

> 📁 If you'd rather just *use* the working server and skip ahead to wiring it
> into Copilot CLI, you can — see the **Quick start** in the [README](./README.md).
> The walk-through below is for attendees building it themselves.

### The full file

```python
# server.py
"""Repo Doctor — an MCP server that diagnoses the health of a local repo."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("repo-doctor")

# ---------- knobs ----------

DEFAULT_TIMEOUT = 120       # seconds — never let a subprocess run forever
MAX_OUTPUT_LINES = 40       # truncate so we don't burn LLM context
MAX_OUTPUT_CHARS = 4000

# Folders the python "build" step refuses to descend into. Vendored / cache
# trees can dwarf the real source and blow the timeout.
_BUILD_EXCLUDE_DIRS = {
    ".venv", "venv", ".env", "env",
    "__pycache__", ".git", ".hg", ".svn",
    "node_modules", "site-packages",
    ".tox", ".nox", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "dist", "build", ".eggs",
}
_BUILD_MAX_FILES = 500


# ---------- helpers ----------

def _truncate(text: str) -> str:
    """Trim subprocess output so we don't blow up the LLM context window."""
    lines = text.splitlines()
    if len(lines) > MAX_OUTPUT_LINES:
        head = lines[:MAX_OUTPUT_LINES]
        text = "\n".join(head) + f"\n… ({len(lines) - MAX_OUTPUT_LINES} more lines truncated)"
    if len(text) > MAX_OUTPUT_CHARS:
        text = text[:MAX_OUTPUT_CHARS] + "\n… (truncated)"
    return text


def _which(cmd: str) -> str | None:
    """Like ``shutil.which`` but also searches ``~/.local/bin`` (where
    ``uv tool install`` / ``pipx`` drop binaries). Lets a freshly-installed
    tool work even when the parent shell's PATH wasn't refreshed — a common
    Windows stumble after ``uv tool install``.
    """
    found = shutil.which(cmd)
    if found:
        return found
    for d in [Path.home() / ".local" / "bin"]:
        for ext in ("", ".exe", ".cmd", ".bat"):
            candidate = d / f"{cmd}{ext}"
            if candidate.is_file():
                return str(candidate)
    return None


def _run(cmd: list[str], cwd: Path) -> dict:
    """Run a command, return a structured result the LLM can reason about."""
    resolved = _which(cmd[0])
    if resolved is None:
        return {"ok": False, "skipped": True, "reason": f"{cmd[0]} not found on PATH"}
    cmd = [resolved, *cmd[1:]]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT,
            # Detach the child from the MCP server's stdio pipes. When this
            # server runs over stdio, our stdin is a pipe from the MCP client;
            # children inheriting it can hang on Windows.
            stdin=subprocess.DEVNULL,
        )
        return {
            "ok": proc.returncode == 0,
            "exit_code": proc.returncode,
            "command": " ".join(cmd),
            "stdout_tail": _truncate(proc.stdout or ""),
            "stderr_tail": _truncate(proc.stderr or ""),
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "timed_out": True, "command": " ".join(cmd)}


def _resolve(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"path does not exist: {p}")
    return p


def _collect_python_sources(root: Path) -> list[str]:
    """Walk `root` for .py files, skipping vendored / cache directories."""
    sources: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _BUILD_EXCLUDE_DIRS]
        for name in filenames:
            if name.endswith(".py"):
                rel = Path(dirpath, name).relative_to(root)
                sources.append(str(rel))
                if len(sources) >= _BUILD_MAX_FILES:
                    return sources
    return sources


def _detect(path: Path) -> dict:
    stacks: list[str] = []
    if (path / "package.json").exists():
        stacks.append("node")
    if (path / "pyproject.toml").exists() or (path / "requirements.txt").exists():
        stacks.append("python")
    if (path / "Cargo.toml").exists():
        stacks.append("rust")
    if (path / "go.mod").exists():
        stacks.append("go")
    if (
        any(path.glob("*.sln"))
        or any(path.glob("*.csproj"))
        or any(path.glob("*.fsproj"))
        or any(path.glob("*.vbproj"))
    ):
        stacks.append("dotnet")
    return {"path": str(path), "stacks": stacks or ["unknown"]}


# ---------- tools ----------

@mcp.tool()
def detect_stack(path: str = ".") -> dict:
    """Detect which ecosystem(s) a repo uses (node, python, rust, go, dotnet).

    Pass a path to a local directory; defaults to the current working directory.
    """
    return _detect(_resolve(path))


@mcp.tool()
def run_lint(path: str = ".") -> dict:
    """Run the lint step for the repo at `path` and return a truncated summary.

    Picks the lint command based on the detected stack. Skips gracefully if the
    required tool isn't installed.
    """
    p = _resolve(path)
    stacks = _detect(p)["stacks"]
    if "python" in stacks and _which("ruff"):
        return _run(["ruff", "check", "."], p)
    if "python" in stacks:
        return {"ok": True, "skipped": True,
                "reason": "python detected but `ruff` not on PATH — install with `uv tool install ruff`"}
    if "node" in stacks:
        return _run(["npm", "run", "lint", "--if-present"], p)
    if "rust" in stacks:
        return _run(["cargo", "clippy", "--no-deps", "-q"], p)
    if "go" in stacks:
        return _run(["go", "vet", "./..."], p)
    if "dotnet" in stacks and _which("dotnet"):
        return _run(["dotnet", "format", "--verify-no-changes", "--no-restore"], p)
    return {"ok": True, "skipped": True, "reason": f"no lint recipe for stacks={stacks}"}


@mcp.tool()
def run_tests(path: str = ".") -> dict:
    """Run the test suite for the repo at `path` and return a truncated summary."""
    p = _resolve(path)
    stacks = _detect(p)["stacks"]
    if "python" in stacks and _which("pytest"):
        result = _run(["pytest", "-q", "--maxfail=5"], p)
        # pytest exit code 5 = "no tests collected" — treat as skipped, not failed.
        if result.get("exit_code") == 5:
            return {"ok": True, "skipped": True,
                    "reason": "no tests collected (pytest exit 5)",
                    "command": result.get("command", "")}
        return result
    if "python" in stacks:
        return {"ok": True, "skipped": True,
                "reason": "python detected but `pytest` not on PATH — install with `uv tool install pytest`"}
    if "node" in stacks:
        return _run(["npm", "test", "--if-present"], p)
    if "rust" in stacks:
        return _run(["cargo", "test", "-q"], p)
    if "go" in stacks:
        return _run(["go", "test", "./..."], p)
    if "dotnet" in stacks and _which("dotnet"):
        return _run(["dotnet", "test", "--nologo", "--verbosity", "quiet"], p)
    return {"ok": True, "skipped": True, "reason": f"no test recipe for stacks={stacks}"}


@mcp.tool()
def run_build(path: str = ".") -> dict:
    """Run the build for the repo at `path` and return a truncated summary."""
    p = _resolve(path)
    stacks = _detect(p)["stacks"]
    if "node" in stacks:
        return _run(["npm", "run", "build", "--if-present"], p)
    if "rust" in stacks:
        return _run(["cargo", "build", "-q"], p)
    if "go" in stacks:
        return _run(["go", "build", "./..."], p)
    if "dotnet" in stacks and _which("dotnet"):
        return _run(["dotnet", "build", "--nologo", "--verbosity", "quiet"], p)
    if "python" in stacks:
        # Use `sys.executable` instead of bare "python" so we always invoke the
        # interpreter running this server — relying on PATH can hit the
        # Windows Store stub, which hangs subprocess calls.
        # Enumerate .py files explicitly (instead of `compileall -x <regex> .`)
        # so we never descend into massive vendored trees and trip the timeout.
        files = _collect_python_sources(p)
        if not files:
            return {"ok": True, "skipped": True, "reason": "no .py files found"}
        return _run([sys.executable, "-m", "compileall", "-q", *files], p)
    return {"ok": True, "skipped": True, "reason": f"no build recipe for stacks={stacks}"}


# ---------- report orchestrator ----------

REPORT_TEMPLATE = """# Repo Doctor Report

**Repo:** {path}
**Generated:** {ts}
**Detected stacks:** {stacks}
**Health score:** {score}/100

## Lint
- ok: {lint_ok}
- {lint_summary}

## Tests
- ok: {tests_ok}
- {tests_summary}

## Build
- ok: {build_ok}
- {build_summary}
"""


def _summary_line(result: dict) -> str:
    if result.get("skipped"):
        return f"skipped — {result.get('reason', 'n/a')}"
    if result.get("timed_out"):
        return f"timed out after {DEFAULT_TIMEOUT}s ({result.get('command', '')})"
    cmd = result.get("command", "")
    code = result.get("exit_code", "?")
    return f"`{cmd}` (exit {code})"


def _score(lint: dict, tests: dict, build: dict) -> int:
    parts = []
    for r in (lint, tests, build):
        if r.get("skipped"):
            parts.append(70)   # neutral
        elif r.get("ok"):
            parts.append(100)
        else:
            parts.append(0)
    return sum(parts) // len(parts)


@mcp.tool()
def health_report(path: str = ".") -> dict:
    """Run lint + tests + build on the repo at `path` and write a one-page markdown report.

    Writes `repo-doctor-report.md` inside the repo and returns its absolute path
    plus a short summary the assistant can read aloud.
    """
    p = _resolve(path)
    lint = run_lint(str(p))
    tests = run_tests(str(p))
    build = run_build(str(p))
    detected = _detect(p)

    content = REPORT_TEMPLATE.format(
        path=str(p),
        ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        stacks=", ".join(detected["stacks"]),
        score=_score(lint, tests, build),
        lint_ok=lint.get("ok"),
        lint_summary=_summary_line(lint),
        tests_ok=tests.get("ok"),
        tests_summary=_summary_line(tests),
        build_ok=build.get("ok"),
        build_summary=_summary_line(build),
    )
    out = p / "repo-doctor-report.md"
    out.write_text(content, encoding="utf-8")

    # Remember the path of the last report so the resource can serve it.
    state_dir = Path.home() / ".repo-doctor"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "last_report_path.txt").write_text(str(out), encoding="utf-8")

    return {
        "ok": all(r.get("ok") or r.get("skipped") for r in (lint, tests, build)),
        "score": _score(lint, tests, build),
        "report_path": str(out),
        "summary": _summary_line(lint) + " · " + _summary_line(tests) + " · " + _summary_line(build),
    }


# ---------- resources ----------

@mcp.resource("repodoctor://template")
def template() -> str:
    """The markdown template Repo Doctor uses to format reports."""
    return REPORT_TEMPLATE


@mcp.resource("repodoctor://last-report")
def last_report() -> str:
    """The most recent repo-doctor-report.md generated by this server."""
    marker = Path.home() / ".repo-doctor" / "last_report_path.txt"
    if not marker.exists():
        return "(no report generated yet — call health_report first)"
    p = Path(marker.read_text(encoding="utf-8").strip())
    if not p.exists():
        return f"(last report at {p} no longer exists)"
    return p.read_text(encoding="utf-8")


# ---------- entrypoint ----------

if __name__ == "__main__":
    mcp.run()
```

### What's new vs. §3.1

| Pattern | Where you see it | Why |
|---|---|---|
| **Subprocess + timeout** | `_run` | Never let a tool hang the agent |
| **Output truncation** | `_truncate` | Protect the model's context window |
| **`stdin=DEVNULL` on child** | `_run` | Children that inherit a piped stdin can hang on Windows |
| **Tool composition** | `health_report` calls `run_lint`/`run_tests`/`run_build` | One round-trip instead of four |
| **Resources** | `@mcp.resource("repodoctor://…")` | Read-only data the model can pull when it wants |
| **State across calls** | `~/.repo-doctor/last_report_path.txt` | `last-report` resource survives restarts |
| **`sys.executable` over bare `"python"`** | `run_build` | Avoids the Windows Store stub that silently hangs piped subprocesses |
| **Manual file enumeration for `compileall`** | `_collect_python_sources` | More deterministic than `compileall -x <regex>` and skips vendored trees |
| **Exit-code-aware result mapping** | `run_tests` (pytest `5` → skipped) | "No tests collected" isn't a failure |
| **PATH-tolerant tool lookup** | `_which` falls back to `~/.local/bin` | Lets `uv tool install ruff` "just work" without a shell restart |
| **"Tool not installed" hints** | `run_lint`, `run_tests` | Tells the user *how* to fix it instead of just "skipped" |

### Try it in the Inspector

```bash
uv run mcp dev server.py
```

In the Inspector:
1. Tools tab → `detect_stack` with `path: .` → see the stacks
2. Tools tab → `health_report` with `path: <path-to-a-repo-you-brought>` → confirm `repo-doctor-report.md` got written
3. Resources tab → click `repodoctor://last-report` → see the report contents

---

## Design discussion (4 min, instructor-led)

- **Why is `health_report` one tool and not "ask the LLM to chain the three"?**
  Both work. One tool means deterministic ordering and one round-trip. Chained tools give the LLM the ability to stop early or react to a failure. Trade-off: control vs. flexibility.
- **What happens if `pytest` isn't installed?**
  We return `skipped: true` with a `reason`. The LLM will mention it in its summary instead of crashing. (And if `pytest` *is* installed but the repo has no tests, we map exit code 5 → `skipped` for the same reason — "no tests" isn't a failure.)
- **Where should the report be written?**
  Inside the repo — discoverable, easy to commit if you want.

---

## Q&A

### Question 1
Why do we truncate stdout/stderr before returning?

A) To save disk space
B) Tool responses are sent back to the model as context — large outputs waste tokens and can crowd out the actual question
C) It's required by the MCP spec
D) For pretty printing

<details><summary>Answer</summary>

**B.** Context is the most precious resource your agent has. Truncate at the edge.

</details>

### Question 2
What's the difference between `repodoctor://template` (a resource) and `health_report` (a tool)?

A) None
B) Resources are read-only data the model can pull on demand; tools are actions the model calls to do work (potentially with side effects)
C) Resources are remote, tools are local
D) Tools are paid, resources are free

<details><summary>Answer</summary>

**B.** Resources = nouns, tools = verbs.

</details>

---

## Next

→ [3.3 — Wire Repo Doctor into Copilot CLI](./03-wire-to-copilot-cli.md)
