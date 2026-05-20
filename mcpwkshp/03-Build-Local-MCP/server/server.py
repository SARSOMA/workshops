"""Repo Doctor — an MCP server that diagnoses the health of a local repo.

Exposes tools that detect the project's stack and run lint / tests / build via
subprocess, plus a one-shot `health_report` tool that writes a markdown
summary. Subprocess output is truncated to keep the LLM's context window sane.

Run locally with `uv run python server.py` (stdio transport).
Use `uv run mcp dev server.py` to open the MCP Inspector.
"""
from __future__ import annotations

import shutil
import subprocess
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


def _which(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _run(cmd: list[str], cwd: Path) -> dict:
    if not _which(cmd[0]):
        return {"ok": False, "skipped": True, "reason": f"{cmd[0]} not found on PATH"}
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT,
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
    return {"path": str(path), "stacks": stacks or ["unknown"]}


@mcp.tool()
def detect_stack(path: str = ".") -> dict:
    """Detect which ecosystem(s) a repo uses (node, python, rust, go).

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
    if "node" in stacks:
        return _run(["npm", "run", "lint", "--if-present"], p)
    if "rust" in stacks:
        return _run(["cargo", "clippy", "--no-deps", "-q"], p)
    if "go" in stacks:
        return _run(["go", "vet", "./..."], p)
    return {"ok": True, "skipped": True, "reason": f"no lint recipe for stacks={stacks}"}


@mcp.tool()
def run_tests(path: str = ".") -> dict:
    """Run the test suite for the repo at `path` and return a truncated summary."""
    p = _resolve(path)
    stacks = _detect(p)["stacks"]
    if "python" in stacks and _which("pytest"):
        return _run(["pytest", "-q", "--maxfail=5"], p)
    if "node" in stacks:
        return _run(["npm", "test", "--if-present"], p)
    if "rust" in stacks:
        return _run(["cargo", "test", "-q"], p)
    if "go" in stacks:
        return _run(["go", "test", "./..."], p)
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
    if "python" in stacks and _which("python"):
        return _run(["python", "-m", "compileall", "-q", "."], p)
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
