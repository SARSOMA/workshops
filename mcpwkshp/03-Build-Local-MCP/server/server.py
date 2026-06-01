"""Repo Doctor — an MCP server that diagnoses the health of a local repo.

Exposes tools that detect the project's stack and run lint / tests / build via
subprocess, plus a one-shot `health_report` tool that writes a markdown
summary. Subprocess output is truncated to keep the LLM's context window sane.

Run locally with `uv run python server.py` (stdio transport).
Use `uv run mcp dev server.py` to open the MCP Inspector.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("repo-doctor")

DEFAULT_TIMEOUT = 120
MAX_OUTPUT_LINES = 40
MAX_OUTPUT_CHARS = 4000


def _truncate(text: str) -> str:
    lines = text.splitlines()
    if len(lines) > MAX_OUTPUT_LINES:
        head = lines[:MAX_OUTPUT_LINES]
        text = "\n".join(head) + f"\n… ({len(lines) - MAX_OUTPUT_LINES} more lines truncated)"
    if len(text) > MAX_OUTPUT_CHARS:
        text = text[:MAX_OUTPUT_CHARS] + "\n… (truncated)"
    return text


def _which(cmd: str) -> str | None:
    """Locate an executable on PATH, falling back to well-known per-user tool dirs.

    Returns the absolute path or None. Behaves like ``shutil.which`` but also
    searches the directories ``uv tool install`` / ``pipx`` deposit binaries
    into — so a freshly-installed tool works even when PATH wasn't refreshed
    in the parent shell (a common stumble on Windows after ``uv tool install``).
    """
    found = shutil.which(cmd)
    if found:
        return found
    extra_dirs = [Path.home() / ".local" / "bin"]
    for d in extra_dirs:
        for ext in ("", ".exe", ".cmd", ".bat"):
            candidate = d / f"{cmd}{ext}"
            if candidate.is_file():
                return str(candidate)
    return None


def _run(cmd: list[str], cwd: Path) -> dict:
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
            # server runs over stdio transport, our stdin is a pipe to the
            # client; children inheriting it can hang on Windows.
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


_BUILD_EXCLUDE_DIRS = {
    ".venv", "venv", ".env", "env",
    "__pycache__", ".git", ".hg", ".svn",
    "node_modules", "site-packages",
    ".tox", ".nox", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "dist", "build", ".eggs",
}
_BUILD_MAX_FILES = 500


def _collect_python_sources(root: Path) -> list[str]:
    """Walk `root` for .py files, skipping vendored / cache directories.

    Returns paths relative to `root` (suitable for passing on the command
    line with cwd=root). Capped at _BUILD_MAX_FILES so the build step always
    completes in bounded time regardless of repo size.
    """
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
        return {"ok": True, "skipped": True, "reason": "python detected but `ruff` not on PATH — install with `uv tool install ruff`"}
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
            return {
                "ok": True,
                "skipped": True,
                "reason": "no tests collected (pytest exit 5)",
                "command": result.get("command", ""),
            }
        return result
    if "python" in stacks:
        return {"ok": True, "skipped": True, "reason": "python detected but `pytest` not on PATH — install with `uv tool install pytest`"}
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
        # Use sys.executable instead of bare "python" so we always invoke the
        # interpreter running this server. Relying on PATH can resolve to the
        # Windows Store stub (or another broken shim), which hangs subprocess
        # calls and trips the build timeout.
        # Enumerate .py files ourselves and pass them to compileall. This is
        # more deterministic than `compileall -x <regex> .` (whose regex is
        # matched against full paths and is easy to get subtly wrong on
        # Windows) and avoids descending into massive vendored trees.
        files = _collect_python_sources(p)
        if not files:
            return {"ok": True, "skipped": True, "reason": "no .py files found"}
        return _run(
            [sys.executable, "-m", "compileall", "-q", *files],
            p,
        )
    return {"ok": True, "skipped": True, "reason": f"no build recipe for stacks={stacks}"}


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
            parts.append(70)
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

    state_dir = Path.home() / ".repo-doctor"
    state_dir.mkdir(exist_ok=True)
    (state_dir / "last_report_path.txt").write_text(str(out), encoding="utf-8")

    return {
        "ok": all(r.get("ok") or r.get("skipped") for r in (lint, tests, build)),
        "score": _score(lint, tests, build),
        "report_path": str(out),
        "summary": _summary_line(lint) + " · " + _summary_line(tests) + " · " + _summary_line(build),
    }


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


if __name__ == "__main__":
    mcp.run()
