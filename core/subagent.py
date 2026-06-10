from __future__ import annotations

from datetime import datetime
from pathlib import Path


RUN_TRACE_PATH = Path(".ai") / "run-trace.md"
PACKET_DIR = Path(".ai") / "subagent-packets"
ROLES = ("planner", "explorer", "implementer", "reviewer", "evaluator")


def packet_path(target_root: Path, role: str) -> Path:
    if role not in ROLES:
        raise ValueError(f"unsupported role: {role}")
    return target_root / PACKET_DIR / f"{role}.md"


def parse_skill_sections(target_root: Path, role: str) -> tuple[list[str], list[str]]:
    path = packet_path(target_root, role)
    if not path.exists():
        raise RuntimeError(f"missing subagent packet: {PACKET_DIR.as_posix()}/{role}.md")

    required: list[str] = []
    optional: list[str] = []
    section: str | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "## Required Skills":
            section = "required"
            continue
        if stripped == "## Optional Skills":
            section = "optional"
            continue
        if stripped.startswith("## "):
            section = None
            continue
        if section is None or not stripped.startswith("- "):
            continue

        skill = stripped[2:].strip().strip("`")
        if not skill:
            continue
        if section == "required":
            required.append(skill)
        else:
            optional.append(skill)

    if not required:
        raise RuntimeError(f"packet is missing required skills: {PACKET_DIR.as_posix()}/{role}.md")

    return required, optional


def render_dispatch_record(
    *,
    role: str,
    scope: str,
    required_skills: list[str],
    optional_skills: list[str],
    objective: str,
    expected_output: str,
    result_location: str,
) -> str:
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    optional_text = ", ".join(optional_skills) if optional_skills else "none"
    return (
        f"## Dispatch {timestamp}\n\n"
        f"- role: {role}\n"
        f"- scope: {scope}\n"
        f"- required_skills: {', '.join(required_skills)}\n"
        f"- optional_skills: {optional_text}\n"
        f"- objective: {objective}\n"
        f"- expected_output: {expected_output}\n"
        f"- result_location: {result_location}\n"
    )


def append_dispatch_record(target_root: Path, record: str) -> Path:
    run_trace_path = target_root / RUN_TRACE_PATH
    if not run_trace_path.exists():
        raise RuntimeError(f"missing run trace: {RUN_TRACE_PATH.as_posix()}")

    existing = run_trace_path.read_text(encoding="utf-8")
    if existing.endswith("\n\n"):
        separator = ""
    elif existing.endswith("\n"):
        separator = "\n"
    else:
        separator = "\n\n"

    run_trace_path.write_text(existing + separator + record, encoding="utf-8")
    return run_trace_path
