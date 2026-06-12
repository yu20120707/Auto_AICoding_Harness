from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from core.safe_write import WriteResult, safe_write_bytes


TASKS_ROOT = Path("docs") / "ai" / "tasks"
TASKS_README_PATH = TASKS_ROOT / "README.md"


@dataclass(frozen=True)
class TaskArtifactSpec:
    file_name: str
    source_path: Path
    fallback_content: str


TASK_ARTIFACT_SPECS: tuple[TaskArtifactSpec, ...] = (
    TaskArtifactSpec(
        file_name="00-prd.md",
        source_path=Path(".ai") / "epic.md",
        fallback_content=(
            "# PRD / Problem Statement\n\n"
            "Capture the task background, goals, non-goals, constraints, and acceptance criteria.\n"
        ),
    ),
    TaskArtifactSpec(
        file_name="01-spec.md",
        source_path=Path(".ai") / "spec.md",
        fallback_content="# Spec\n\nDescribe the executable engineering spec for this task.\n",
    ),
    TaskArtifactSpec(
        file_name="02-tech-design.md",
        source_path=Path(".ai") / "tech-design.md",
        fallback_content="# Tech Design\n\nDescribe modules, call paths, data flow, and risk boundaries.\n",
    ),
    TaskArtifactSpec(
        file_name="03-implementation-plan.md",
        source_path=Path(".ai") / "implementation-plan.md",
        fallback_content=(
            "# Implementation Plan\n\n"
            "Capture the concrete execution plan, file scope, and verification checkpoints.\n"
        ),
    ),
    TaskArtifactSpec(
        file_name="04-diff-review.md",
        source_path=Path(".ai") / "reviews" / "diff-review.md",
        fallback_content="# Diff Review\n\nDiff review has not been generated yet.\n",
    ),
    TaskArtifactSpec(
        file_name="05-verification.md",
        source_path=Path(".ai") / "verification.md",
        fallback_content="# Verification\n\nRecord concrete validation evidence for this task.\n",
    ),
    TaskArtifactSpec(
        file_name="06-risk-and-rollback.md",
        source_path=Path(".ai") / "risk-and-rollback.md",
        fallback_content=(
            "# Risk And Rollback\n\n"
            "Capture residual risk, rollback steps, and required follow-up before release.\n"
        ),
    ),
    TaskArtifactSpec(
        file_name="07-handoff.md",
        source_path=Path(".ai") / "handoff.md",
        fallback_content="# Handoff\n\nSummarize the current task state for the next session or reviewer.\n",
    ),
)


def task_id_for_state(state: dict) -> str:
    raw_task_id = str(state.get("task_id") or "current-task").strip()
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "-", raw_task_id).strip("-")
    return sanitized or "current-task"


def task_dir_relative_path(state: dict) -> Path:
    return TASKS_ROOT / task_id_for_state(state)


def task_artifact_relative_path(state: dict, file_name: str) -> Path:
    return task_dir_relative_path(state) / file_name


def required_large_task_artifacts(state: dict) -> list[Path]:
    return [
        task_artifact_relative_path(state, "00-prd.md"),
        task_artifact_relative_path(state, "01-spec.md"),
        task_artifact_relative_path(state, "02-tech-design.md"),
        task_artifact_relative_path(state, "03-implementation-plan.md"),
    ]


def sync_large_task_chain(
    *,
    target_root: Path,
    state: dict,
    force: bool,
    timestamp: str,
    file_names: list[str] | None = None,
) -> list[WriteResult]:
    if state.get("mode") != "large":
        return []

    selected = {
        spec.file_name: spec
        for spec in TASK_ARTIFACT_SPECS
        if file_names is None or spec.file_name in file_names
    }
    results = [
        safe_write_bytes(
            target_root=target_root,
            relative_path=TASKS_README_PATH,
            content=render_tasks_readme().encode("utf-8"),
            force=force,
            timestamp=timestamp,
        )
    ]
    for file_name in file_names or [spec.file_name for spec in TASK_ARTIFACT_SPECS]:
        spec = selected[file_name]
        source = target_root / spec.source_path
        content = source.read_text(encoding="utf-8") if source.exists() else spec.fallback_content
        if not content.endswith("\n"):
            content += "\n"
        results.append(
            safe_write_bytes(
                target_root=target_root,
                relative_path=task_artifact_relative_path(state, spec.file_name),
                content=content.encode("utf-8"),
                force=force,
                timestamp=timestamp,
            )
        )
    return results


def render_tasks_readme() -> str:
    return (
        "# Task Evidence Chain\n\n"
        "Each subdirectory under `docs/ai/tasks/` represents one large-mode task keyed by `.ai/state.json::task_id`.\n\n"
        "Expected files:\n\n"
        "- `00-prd.md`\n"
        "- `01-spec.md`\n"
        "- `02-tech-design.md`\n"
        "- `03-implementation-plan.md`\n"
        "- `04-diff-review.md`\n"
        "- `05-verification.md`\n"
        "- `06-risk-and-rollback.md`\n"
        "- `07-handoff.md`\n"
    )
