from __future__ import annotations

VALID_MODES = {"small", "medium", "large"}
VALID_GATES = ("spec", "plan", "diff", "final")

WAITING_STATUS_BY_GATE = {
    "spec": "WAITING_HUMAN_SPEC_APPROVAL",
    "plan": "WAITING_HUMAN_PLAN_APPROVAL",
    "diff": "WAITING_HUMAN_DIFF_APPROVAL",
    "final": "WAITING_HUMAN_FINAL_APPROVAL",
}

APPROVED_STATUS_BY_GATE = {
    "spec": "SPEC_APPROVED",
    "plan": "PLAN_APPROVED",
    "diff": "DIFF_APPROVED",
    "final": "DONE",
}

REJECTED_STATUS_BY_GATE = {
    "spec": "NEEDS_REPLAN",
    "plan": "NEEDS_REPLAN",
    "diff": "NEEDS_FIX",
    "final": "NEEDS_MORE_TESTS",
}

VALID_STATUSES = {
    "INIT",
    *WAITING_STATUS_BY_GATE.values(),
    *APPROVED_STATUS_BY_GATE.values(),
    *REJECTED_STATUS_BY_GATE.values(),
}

REQUIRED_STATE_KEYS = {
    "schema_version",
    "mode",
    "profile",
    "status",
    "current_gate",
    "approved_gates",
    "created_by",
    "task_id",
    "task_title",
    "updated_at",
}


def validate_state_dict(state: dict) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_STATE_KEYS - set(state))
    if missing:
        errors.append(f"missing required keys: {', '.join(missing)}")

    mode = state.get("mode")
    if mode not in VALID_MODES:
        errors.append(f"invalid mode: {mode}")

    status = state.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"invalid status: {status}")

    current_gate = state.get("current_gate")
    if current_gate is not None and current_gate not in VALID_GATES:
        errors.append(f"invalid current_gate: {current_gate}")

    approved_gates = state.get("approved_gates")
    if not isinstance(approved_gates, list):
        errors.append("approved_gates must be a list")
    else:
        for gate in approved_gates:
            if gate not in VALID_GATES:
                errors.append(f"invalid approved gate: {gate}")

    waiting_gate = gate_for_waiting_status(status)
    if waiting_gate is not None and current_gate != waiting_gate:
        errors.append(
            f"status {status} requires current_gate={waiting_gate}, got {current_gate}"
        )

    if waiting_gate is None and current_gate is not None:
        errors.append(f"status {status} does not allow current_gate={current_gate}")

    if status == "SPEC_APPROVED" and "spec" not in state.get("approved_gates", []):
        errors.append("SPEC_APPROVED requires spec in approved_gates")
    if status == "PLAN_APPROVED" and "plan" not in state.get("approved_gates", []):
        errors.append("PLAN_APPROVED requires plan in approved_gates")
    if status == "DIFF_APPROVED" and "diff" not in state.get("approved_gates", []):
        errors.append("DIFF_APPROVED requires diff in approved_gates")
    if status == "DONE" and "final" not in state.get("approved_gates", []):
        errors.append("DONE requires final in approved_gates")

    return errors


def assert_valid_state(state: dict) -> None:
    errors = validate_state_dict(state)
    if errors:
        raise RuntimeError("invalid state.json: " + "; ".join(errors))


def gate_for_waiting_status(status: str | None) -> str | None:
    for gate, waiting_status in WAITING_STATUS_BY_GATE.items():
        if status == waiting_status:
            return gate
    return None


def assert_review_allowed(state: dict, gate: str) -> None:
    assert_valid_state(state)

    if gate not in VALID_GATES:
        raise RuntimeError(f"unsupported review gate: {gate}")

    status = state["status"]
    mode = state["mode"]
    approved = set(state.get("approved_gates", []))
    waiting_gate = gate_for_waiting_status(status)
    if waiting_gate is not None:
        raise RuntimeError(
            f"cannot enter {gate} review while waiting for human decision on {waiting_gate}"
        )

    if mode in {"small", "medium"}:
        return

    if gate == "spec":
        if status not in {"INIT", "NEEDS_REPLAN"}:
            raise RuntimeError(f"spec review not allowed from status {status}")
        return

    if gate == "plan":
        if "spec" not in approved:
            raise RuntimeError("plan review requires spec approval first")
        if status not in {"SPEC_APPROVED", "NEEDS_REPLAN"}:
            raise RuntimeError(f"plan review not allowed from status {status}")
        return

    if gate == "diff":
        if "plan" not in approved:
            raise RuntimeError("diff review requires plan approval first")
        if status not in {"PLAN_APPROVED", "NEEDS_FIX"}:
            raise RuntimeError(f"diff review not allowed from status {status}")
        return

    if "diff" not in approved:
        raise RuntimeError("final review requires diff approval first")
    if status not in {"DIFF_APPROVED", "NEEDS_MORE_TESTS"}:
        raise RuntimeError(f"final review not allowed from status {status}")


def assert_waiting_gate_for_decision(state: dict, gate: str, *, action: str) -> None:
    assert_valid_state(state)

    if gate not in VALID_GATES:
        raise RuntimeError(f"unsupported {action} gate: {gate}")

    expected_status = WAITING_STATUS_BY_GATE[gate]
    if state.get("status") != expected_status:
        raise RuntimeError(
            f"current status does not allow {gate} {action}: {state.get('status')}"
        )
    if state.get("current_gate") != gate:
        raise RuntimeError(
            f"current gate does not allow {gate} {action}: {state.get('current_gate')}"
        )


def next_action_for_state(state: dict | None) -> str:
    if state is None:
        return "Run ai-init small or ai-init medium to create the base harness files."

    status = state.get("status")
    mode = state.get("mode")

    if status == "INIT":
        if mode == "large":
            return "Run ai-review spec to start the large-mode gate chain."
        if mode == "medium":
            return "Fill .ai/implementation-plan.md, keep .ai/run-trace.md current, then make the scoped change and run ai-review diff."
        return "Make the scoped change, then run ai-review diff when a diff exists."
    if status == "SPEC_APPROVED":
        return "Run ai-review plan."
    if status == "PLAN_APPROVED":
        return "Implement the plan, then run ai-review diff."
    if status == "DIFF_APPROVED":
        if mode == "medium":
            return "Record verification in .ai/verification.md and summarize the outcome, or run ai-review final if you want a formal final gate."
        return "Record verification in .ai/verification.md, then run ai-review final."
    if status == "DONE":
        return "Workflow complete."
    if status == "NEEDS_REPLAN":
        return "Revise the spec or plan, then rerun the appropriate review gate."
    if status == "NEEDS_FIX":
        return "Fix the implementation, then rerun ai-review diff."
    if status == "NEEDS_MORE_TESTS":
        return "Add verification evidence in .ai/verification.md, then rerun ai-review final."

    gate = gate_for_waiting_status(status)
    if gate is not None:
        return f"Human decision required: run ai-approve {gate} or ai-reject {gate}."

    return "State is present but not fully understood; run ai-doctor for diagnostics."
