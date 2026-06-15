from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from core.task_chain import task_id_for_state


TASK_SUPPLEMENT_ROOT = Path(".ai") / "tasks"
TASK_SUPPLEMENT_FILE_NAME = "task.json"

SUPPORTED_SCHEMA_VERSION = 1
SUPPORTED_TASK_MODES = {"large"}
SUPPORTED_TASK_STATUSES = {
    "planning",
    "ready",
    "implementing",
    "reviewing",
    "waiting_approval",
    "approved",
    "rejected",
    "needs_fix",
    "finalizing",
    "completed",
    "blocked",
}

REQUIRED_TASK_KEYS = {
    "schema_version",
    "id",
    "mode",
    "status",
    "source",
    "scope",
    "created_at",
    "updated_at",
    "artifacts",
}

REQUIRED_SOURCE_KEYS = {"epic", "spec", "plan"}
REQUIRED_ARTIFACT_KEYS = {"context_manifest", "review", "rca", "final"}

LEGAL_TRANSITIONS: dict[str, set[str]] = {
    "planning": {"ready", "implementing", "blocked"},
    "ready": {"implementing", "blocked"},
    "implementing": {"reviewing", "blocked"},
    "reviewing": {"waiting_approval", "needs_fix", "blocked"},
    "waiting_approval": {"approved", "rejected", "blocked"},
    "approved": {"finalizing"},
    "rejected": {"needs_fix"},
    "needs_fix": {"implementing", "blocked"},
    "finalizing": {"completed", "blocked"},
    "completed": set(),
    "blocked": {"planning", "implementing"},
}

ALLOWED_TASK_STATUSES_BY_WORKFLOW_STATUS: dict[str, set[str]] = {
    "INIT": {"planning"},
    "WAITING_HUMAN_SPEC_APPROVAL": {"waiting_approval"},
    "SPEC_APPROVED": {"planning"},
    "WAITING_HUMAN_PLAN_APPROVAL": {"waiting_approval"},
    "PLAN_APPROVED": {"implementing"},
    "WAITING_HUMAN_DIFF_APPROVAL": {"waiting_approval"},
    "DIFF_APPROVED": {"finalizing"},
    "WAITING_HUMAN_FINAL_APPROVAL": {"waiting_approval"},
    "DONE": {"completed"},
    "NEEDS_REPLAN": {"planning"},
    "NEEDS_FIX": {"implementing"},
    "NEEDS_MORE_TESTS": {"finalizing"},
}


@dataclass(frozen=True)
class TaskSupplementLoadResult:
    path: Path
    exists: bool
    payload: dict[str, Any] | None
    errors: list[str]

    @property
    def valid(self) -> bool:
        return self.exists and not self.errors


def task_supplement_relative_path(task_id: str) -> Path:
    return TASK_SUPPLEMENT_ROOT / task_id / TASK_SUPPLEMENT_FILE_NAME


def active_task_supplement_relative_path(state: dict[str, Any]) -> Path:
    return task_supplement_relative_path(task_id_for_state(state))


def validate_task_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["task supplement must be a JSON object"]

    missing = sorted(REQUIRED_TASK_KEYS - set(payload))
    if missing:
        errors.append(f"missing required keys: {', '.join(missing)}")

    schema_version = payload.get("schema_version")
    if schema_version != SUPPORTED_SCHEMA_VERSION:
        errors.append(f"unsupported schema_version: {schema_version}")

    task_id = payload.get("id")
    if not isinstance(task_id, str) or not task_id.strip():
        errors.append("id must be a non-empty string")

    mode = payload.get("mode")
    if mode not in SUPPORTED_TASK_MODES:
        errors.append(f"invalid mode for task supplement: {mode}")

    status = payload.get("status")
    if status not in SUPPORTED_TASK_STATUSES:
        errors.append(f"invalid status: {status}")

    source = payload.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        _validate_string_mapping(source, REQUIRED_SOURCE_KEYS, "source", errors)

    scope = payload.get("scope")
    if not isinstance(scope, list):
        errors.append("scope must be a list")
    elif not all(isinstance(item, str) for item in scope):
        errors.append("scope entries must be strings")

    for key in ("created_at", "updated_at"):
        value = payload.get(key)
        if not isinstance(value, str):
            errors.append(f"{key} must be a string")

    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
    else:
        _validate_string_mapping(artifacts, REQUIRED_ARTIFACT_KEYS, "artifacts", errors)

    review = payload.get("review")
    if review is not None and not isinstance(review, dict):
        errors.append("review must be an object when present")

    approval = payload.get("approval")
    if approval is not None and not isinstance(approval, dict):
        errors.append("approval must be an object when present")

    return errors


def assert_valid_task_payload(payload: Any) -> None:
    errors = validate_task_payload(payload)
    if errors:
        raise ValueError("invalid task supplement: " + "; ".join(errors))


def validate_transition(current_status: str, next_status: str) -> list[str]:
    errors: list[str] = []
    if current_status not in SUPPORTED_TASK_STATUSES:
        errors.append(f"invalid current status: {current_status}")
    if next_status not in SUPPORTED_TASK_STATUSES:
        errors.append(f"invalid next status: {next_status}")
    if errors:
        return errors

    allowed = LEGAL_TRANSITIONS[current_status]
    if next_status not in allowed:
        allowed_text = ", ".join(sorted(allowed)) or "none"
        errors.append(
            f"illegal task transition: {current_status} -> {next_status}; allowed: {allowed_text}"
        )
    return errors


def assert_valid_transition(current_status: str, next_status: str) -> None:
    errors = validate_transition(current_status, next_status)
    if errors:
        raise ValueError("; ".join(errors))


def validate_task_status_consistency(payload: dict[str, Any], state: dict[str, Any]) -> list[str]:
    workflow_status = state.get("status")
    task_status = payload.get("status")
    allowed = ALLOWED_TASK_STATUSES_BY_WORKFLOW_STATUS.get(str(workflow_status))
    if allowed is None:
        return [f"cannot validate task supplement status against unknown workflow status: {workflow_status}"]
    if task_status not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        return [
            "task supplement status conflicts with canonical workflow state: "
            f"state status {workflow_status} allows {allowed_text}, got {task_status}"
        ]
    return []


def load_active_task_supplement(target_root: Path, state: dict[str, Any] | None) -> TaskSupplementLoadResult | None:
    if state is None or state.get("mode") != "large":
        return None

    relative_path = active_task_supplement_relative_path(state)
    path = target_root / relative_path
    if not path.exists():
        return TaskSupplementLoadResult(path=relative_path, exists=False, payload=None, errors=[])

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return TaskSupplementLoadResult(
            path=relative_path,
            exists=True,
            payload=None,
            errors=[f"invalid JSON: {exc.msg}"],
        )

    errors = validate_task_payload(payload)
    state_task_id = str(state.get("task_id") or "").strip()
    if isinstance(payload, dict):
        if state_task_id and payload.get("id") != state_task_id:
            errors.append(f"task id mismatch: state has {state_task_id}, task.json has {payload.get('id')}")
        errors.extend(validate_task_status_consistency(payload, state))
    return TaskSupplementLoadResult(path=relative_path, exists=True, payload=payload, errors=errors)


def summarize_task_supplement(result: TaskSupplementLoadResult) -> list[str]:
    if not result.exists:
        return []

    lines = [f"task_supplement: present ({result.path.as_posix()})"]
    if result.payload is not None:
        lines.append(f"task_supplement_id: {result.payload.get('id', '-')}")
        lines.append(f"task_supplement_status: {result.payload.get('status', '-')}")
    lines.append(f"task_supplement_valid: {'yes' if not result.errors else 'no'}")
    if result.errors:
        lines.append(f"task_supplement_errors: {' | '.join(result.errors)}")
    return lines


def _validate_string_mapping(
    mapping: dict[Any, Any],
    required_keys: set[str],
    field_name: str,
    errors: list[str],
) -> None:
    missing = sorted(required_keys - set(mapping))
    if missing:
        errors.append(f"{field_name} missing required keys: {', '.join(missing)}")
    for key in sorted(required_keys & set(mapping)):
        value = mapping.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name}.{key} must be a non-empty string")
