from __future__ import annotations

from pathlib import Path
import subprocess

from core.state import STATE_RELATIVE_PATH, load_state
from core.state_machine import next_action_for_state, validate_state_dict
from core.task_chain import required_large_task_artifacts, task_dir_relative_path


def collect_doctor_report(target_root: Path) -> dict:
    checks: list[dict[str, str]] = []
    state = load_state(target_root)

    def add(status: str, message: str, *, code: str) -> None:
        checks.append({"status": status, "message": message, "code": code})

    git_result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=target_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if git_result.returncode == 0 and git_result.stdout.strip() == "true":
        add("OK", "Git repository detected", code="git_repo")
        dirty_result = subprocess.run(
            ["git", "status", "--short"],
            cwd=target_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if dirty_result.returncode == 0:
            if dirty_result.stdout.strip():
                add("WARN", "working tree has uncommitted changes", code="git_dirty")
            else:
                add("OK", "working tree clean", code="git_clean")
    else:
        add("WARN", "current directory is not a git repository", code="git_missing")

    state_path = target_root / STATE_RELATIVE_PATH
    if not state_path.exists():
        add("FAIL", ".ai/state.json missing", code="state_missing")
        return {
            "checks": checks,
            "next_action": "Run ai-init small or ai-init medium to create the base harness files.",
            "has_failures": True,
        }

    add("OK", ".ai/state.json exists", code="state_exists")

    if state is None:
        add("FAIL", "state file could not be loaded", code="state_unreadable")
        return {
            "checks": checks,
            "next_action": "Repair .ai/state.json or reinitialize the target repository.",
            "has_failures": True,
        }

    state_errors = validate_state_dict(state)
    if state_errors:
        add("FAIL", "state schema invalid", code="state_invalid")
        for error in state_errors:
            add("FAIL", error, code="state_invalid_detail")
    else:
        add("OK", "state schema valid", code="state_valid")
        add("OK", f"mode: {state.get('mode')}", code="mode")
        add("OK", f"profile: {state.get('profile')}", code="profile")
        add("OK", f"status: {state.get('status')}", code="status")

    agents_path = target_root / "AGENTS.md"
    add(
        "OK" if agents_path.exists() else "FAIL",
        "AGENTS.md present" if agents_path.exists() else "AGENTS.md missing",
        code="agents",
    )

    docs_ai_path = target_root / "docs" / "ai"
    add(
        "OK" if docs_ai_path.exists() else "FAIL",
        "docs/ai present" if docs_ai_path.exists() else "docs/ai missing",
        code="docs_ai",
    )

    ai_check_path = target_root / "scripts" / "ai_check.sh"
    add(
        "OK" if ai_check_path.exists() else "FAIL",
        "scripts/ai_check.sh present" if ai_check_path.exists() else "scripts/ai_check.sh missing",
        code="ai_check",
    )

    if state is not None:
        mode = state.get("mode")
        medium_markers = [
            target_root / ".ai" / "implementation-plan.md",
            target_root / ".ai" / "run-trace.md",
            target_root / ".ai" / "verification.md",
        ]
        medium_present = all(path.exists() for path in medium_markers)
        stray_medium_present = any(path.exists() for path in medium_markers)
        large_markers = [
            target_root / ".ai" / "epic.md",
            target_root / ".ai" / "spec.md",
            target_root / ".ai" / "implementation-plan.md",
            target_root / ".ai" / "run-trace.md",
            target_root / ".ai" / "verification.md",
            target_root / ".ai" / "reviews",
            target_root / ".ai" / "approvals",
        ]
        large_present = all(path.exists() for path in large_markers)
        stray_large_present = any(path.exists() for path in large_markers)
        if mode == "small" and stray_medium_present:
            add("FAIL", "mode mismatch detected: state is small but medium-mode files are present", code="medium_mode_mismatch")
        elif mode == "medium" and not medium_present:
            add("FAIL", "medium mode state exists but medium-mode files are missing", code="medium_missing")
        elif mode == "medium":
            add("OK", "medium-mode files present", code="medium_present")
        if mode == "large" and not large_present:
            add("FAIL", "large mode state exists but large-mode files are missing", code="large_missing")
        elif mode == "small" and stray_large_present:
            add("FAIL", "mode mismatch detected: state is small but large-mode files are present", code="mode_mismatch")
        elif mode == "large":
            add("OK", "large-mode files present", code="large_present")
            task_dir = target_root / task_dir_relative_path(state)
            required_task_files = [target_root / path for path in required_large_task_artifacts(state)]
            if not task_dir.exists():
                add("FAIL", f"large task chain missing: {task_dir_relative_path(state).as_posix()}", code="large_task_chain_missing")
            elif not all(path.exists() for path in required_task_files):
                add("FAIL", "large task chain exists but required task evidence files are missing", code="large_task_chain_incomplete")
            else:
                add("OK", f"large task chain present: {task_dir_relative_path(state).as_posix()}", code="large_task_chain_present")

    has_failures = any(check["status"] == "FAIL" for check in checks)
    return {
        "checks": checks,
        "next_action": next_action_for_state(state) if not has_failures else "Fix the failed checks above, then rerun ai-doctor.",
        "has_failures": has_failures,
    }
