from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from core.approval import ApprovalGateConfig
from core.review import ReviewArtifact
from core.task_chain import task_id_for_state


TASK_REVIEW_FILE_NAME = "review.md"
TASK_APPROVAL_FILE_NAME = "approval.json"


@dataclass(frozen=True)
class ReviewGateRecord:
    review_type: str
    status: str
    created_at: str
    review_summary: str
    risk_level: str
    required_action: str


def task_runtime_dir(state: dict[str, Any]) -> Path:
    return Path(".ai") / "tasks" / task_id_for_state(state)


def task_review_relative_path(state: dict[str, Any]) -> Path:
    return task_runtime_dir(state) / TASK_REVIEW_FILE_NAME


def task_approval_relative_path(state: dict[str, Any]) -> Path:
    return task_runtime_dir(state) / TASK_APPROVAL_FILE_NAME


def render_task_review(*, review_type: str, source_path: Path, review_text: str) -> str:
    return (
        "# Task Review Supplement\n\n"
        f"## Review Type\n\n{review_type}\n\n"
        f"## Source\n\n{source_path.as_posix()}\n\n"
        "## Summary\n\n"
        f"{_excerpt(review_text)}\n"
    )


def render_waiting_approval_json(*, review_type: str, review_text: str, created_at: str | None = None) -> str:
    record = ReviewGateRecord(
        review_type=review_type,
        status="waiting",
        created_at=created_at or datetime.now().astimezone().isoformat(timespec="seconds"),
        review_summary=_one_line_summary(review_text),
        risk_level="medium",
        required_action="ai-approve or ai-reject",
    )
    return json.dumps(record.__dict__, indent=2, ensure_ascii=True) + "\n"


def render_decision_approval_json(
    *,
    config: ApprovalGateConfig,
    approved: bool,
    created_at: str | None = None,
) -> str:
    status = "approved" if approved else "rejected"
    required_action = "continue" if approved else "fix and rerun review"
    payload = {
        "status": status,
        "review_type": config.gate,
        "created_at": created_at or datetime.now().astimezone().isoformat(timespec="seconds"),
        "review_summary": config.approve_notes if approved else config.reject_notes,
        "risk_level": "medium",
        "required_action": required_action,
    }
    return json.dumps(payload, indent=2, ensure_ascii=True) + "\n"


def task_status_for_review_gate(review_type: str) -> str:
    return "waiting_approval"


def task_status_for_decision(*, gate: str, approved: bool) -> str:
    if approved:
        return "completed" if gate == "final" else "finalizing"
    if gate == "final":
        return "finalizing"
    return "needs_fix" if gate == "diff" else "planning"


def update_task_payload_status(payload: dict[str, Any], *, status: str, updated_at: str | None = None) -> dict[str, Any]:
    updated = dict(payload)
    updated["status"] = status
    updated["updated_at"] = updated_at or datetime.now().astimezone().isoformat(timespec="seconds")
    return updated


def _one_line_summary(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("```")]
    summary = " ".join(lines[:3]) or "review generated"
    if len(summary) > 240:
        summary = summary[:237].rstrip() + "..."
    return summary


def _excerpt(text: str, *, max_chars: int = 2000) -> str:
    stripped = text.strip()
    if not stripped:
        return "(empty)"
    if len(stripped) <= max_chars:
        return stripped
    return stripped[:max_chars].rstrip() + "\n...[truncated]"
