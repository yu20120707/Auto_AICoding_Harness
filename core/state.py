from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json

from core.safe_write import WriteResult, safe_write_bytes


STATE_RELATIVE_PATH = Path(".ai") / "state.json"


def default_state(profile: str, *, mode: str = "small") -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    if mode not in {"small", "medium", "large"}:
        raise ValueError(f"unsupported mode: {mode}")
    return {
        "schema_version": 1,
        "mode": mode,
        "profile": profile,
        "status": "INIT",
        "current_gate": None,
        "approved_gates": [],
        "created_by": "Auto_AICoding_Harness",
        "task_id": f"init-{mode}",
        "task_title": f"Initialize harness in {mode} mode",
        "updated_at": now,
    }


def upgrade_state_to_medium(existing_state: dict, profile: str) -> dict:
    return _upgrade_state(existing_state, profile, mode="medium")


def upgrade_state_to_large(existing_state: dict, profile: str) -> dict:
    return _upgrade_state(existing_state, profile, mode="large")


def _upgrade_state(existing_state: dict, profile: str, *, mode: str) -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    upgraded = dict(existing_state)
    upgraded.update(
        {
            "schema_version": 1,
            "mode": mode,
            "profile": profile,
            "status": "INIT",
            "current_gate": None,
            "approved_gates": [],
            "created_by": "Auto_AICoding_Harness",
            "task_id": f"init-{mode}",
            "task_title": f"Initialize harness in {mode} mode",
            "updated_at": now,
        }
    )
    return upgraded


def update_state_for_diff_review(existing_state: dict) -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    updated = dict(existing_state)
    updated.update(
        {
            "status": "WAITING_HUMAN_DIFF_APPROVAL",
            "current_gate": "diff",
            "updated_at": now,
        }
    )
    return updated


def update_state_for_waiting_gate(existing_state: dict, *, status: str, gate: str) -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    updated = dict(existing_state)
    updated.update(
        {
            "status": status,
            "current_gate": gate,
            "updated_at": now,
        }
    )
    return updated


def update_state_for_spec_review(existing_state: dict) -> dict:
    return update_state_for_waiting_gate(
        existing_state,
        status="WAITING_HUMAN_SPEC_APPROVAL",
        gate="spec",
    )


def update_state_for_plan_review(existing_state: dict) -> dict:
    return update_state_for_waiting_gate(
        existing_state,
        status="WAITING_HUMAN_PLAN_APPROVAL",
        gate="plan",
    )


def update_state_for_final_review(existing_state: dict) -> dict:
    return update_state_for_waiting_gate(
        existing_state,
        status="WAITING_HUMAN_FINAL_APPROVAL",
        gate="final",
    )


def update_state_for_gate_approved(existing_state: dict, *, gate: str, status: str) -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    updated = dict(existing_state)
    approved_gates = list(updated.get("approved_gates", []))
    if gate not in approved_gates:
        approved_gates.append(gate)

    updated.update(
        {
            "status": status,
            "current_gate": None,
            "approved_gates": approved_gates,
            "updated_at": now,
        }
    )
    return updated


def update_state_for_gate_rejected(existing_state: dict, *, gate: str, status: str) -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    updated = dict(existing_state)
    approved_gates = [existing_gate for existing_gate in updated.get("approved_gates", []) if existing_gate != gate]
    updated.update(
        {
            "status": status,
            "current_gate": None,
            "approved_gates": approved_gates,
            "updated_at": now,
        }
    )
    return updated


def update_state_for_spec_approved(existing_state: dict) -> dict:
    return update_state_for_gate_approved(existing_state, gate="spec", status="SPEC_APPROVED")


def update_state_for_plan_approved(existing_state: dict) -> dict:
    return update_state_for_gate_approved(existing_state, gate="plan", status="PLAN_APPROVED")


def update_state_for_diff_approved(existing_state: dict) -> dict:
    return update_state_for_gate_approved(existing_state, gate="diff", status="DIFF_APPROVED")


def update_state_for_final_approved(existing_state: dict) -> dict:
    return update_state_for_gate_approved(existing_state, gate="final", status="DONE")


def update_state_for_spec_rejected(existing_state: dict) -> dict:
    return update_state_for_gate_rejected(existing_state, gate="spec", status="NEEDS_REPLAN")


def update_state_for_plan_rejected(existing_state: dict) -> dict:
    return update_state_for_gate_rejected(existing_state, gate="plan", status="NEEDS_REPLAN")


def update_state_for_diff_rejected(existing_state: dict) -> dict:
    return update_state_for_gate_rejected(existing_state, gate="diff", status="NEEDS_FIX")


def update_state_for_final_rejected(existing_state: dict) -> dict:
    return update_state_for_gate_rejected(existing_state, gate="final", status="NEEDS_MORE_TESTS")


def write_state(
    *,
    target_root: Path,
    profile: str,
    mode: str = "small",
    force: bool,
    timestamp: str,
) -> WriteResult:
    payload = json.dumps(default_state(profile, mode=mode), indent=2, ensure_ascii=True) + "\n"
    return safe_write_bytes(
        target_root=target_root,
        relative_path=STATE_RELATIVE_PATH,
        content=payload.encode("utf-8"),
        force=force,
        timestamp=timestamp,
    )


def write_state_payload(
    *,
    target_root: Path,
    state: dict,
    force: bool,
    timestamp: str,
) -> WriteResult:
    payload = json.dumps(state, indent=2, ensure_ascii=True) + "\n"
    return safe_write_bytes(
        target_root=target_root,
        relative_path=STATE_RELATIVE_PATH,
        content=payload.encode("utf-8"),
        force=force,
        timestamp=timestamp,
    )


def load_state(target_root: Path) -> dict | None:
    state_path = target_root / STATE_RELATIVE_PATH
    if not state_path.exists():
        return None

    with state_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
