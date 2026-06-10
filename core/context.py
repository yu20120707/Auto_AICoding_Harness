from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from core.verification import render_verification_summary


REVIEW_PATH = Path(".ai") / "reviews" / "diff-review.md"
APPROVAL_PATH = Path(".ai") / "approvals" / "diff-approval.md"
CONTEXT_PACK_PATH = Path(".ai") / "context-pack.md"
HANDOFF_PATH = Path(".ai") / "handoff.md"


@dataclass(frozen=True)
class GitSummary:
    is_repo: bool
    status_short: str
    diff_stat: str
    changed_files: str


def collect_optional_git_summary(target_root: Path) -> GitSummary:
    probe = _run_git(target_root, "rev-parse", "--is-inside-work-tree")
    if probe.returncode != 0 or probe.stdout.strip() != "true":
        return GitSummary(
            is_repo=False,
            status_short="git: not a git repository",
            diff_stat="unavailable",
            changed_files="unavailable",
        )

    status_short = _run_git_text(target_root, "status", "--short") or "empty"
    diff_stat = _run_git_text(target_root, "diff", "--stat") or "empty"
    changed_files = _run_git_text(target_root, "diff", "--name-only") or "empty"
    return GitSummary(
        is_repo=True,
        status_short=status_short,
        diff_stat=diff_stat,
        changed_files=changed_files,
    )


def render_context_pack(target_root: Path, state: dict, git_summary: GitSummary) -> str:
    return (
        "# Context Pack\n\n"
        "## Harness State\n\n"
        f"- mode: {state.get('mode', '-')}\n"
        f"- profile: {state.get('profile', '-')}\n"
        f"- status: {state.get('status', '-')}\n"
        f"- current_gate: {_display_gate(state.get('current_gate'))}\n"
        f"- approved_gates: {', '.join(state.get('approved_gates', [])) or 'none'}\n\n"
        "## Important Files\n\n"
        f"- AGENTS.md: {_present(target_root / 'AGENTS.md')}\n"
        f"- docs/ai/: {_present(target_root / 'docs' / 'ai')}\n"
        f"- scripts/ai_check.sh: {_present(target_root / 'scripts' / 'ai_check.sh')}\n"
        f"- .ai/verification.md: {_present(target_root / Path('.ai') / 'verification.md')}\n"
        f"- .ai/reviews/diff-review.md: {_present(target_root / REVIEW_PATH)}\n"
        f"- .ai/approvals/diff-approval.md: {_present(target_root / APPROVAL_PATH)}\n\n"
        "## Git Summary\n\n"
        "```text\n"
        f"{git_summary.status_short.rstrip()}\n"
        "```\n\n"
        "## Diff Stat\n\n"
        "```text\n"
        f"{git_summary.diff_stat.rstrip()}\n"
        "```\n\n"
        "## Changed Files\n\n"
        "```text\n"
        f"{git_summary.changed_files.rstrip()}\n"
        "```\n\n"
        "## Recent Review\n\n"
        f"{_recent_review_summary(target_root)}\n\n"
        "## Recent Approval\n\n"
        f"{_recent_approval_summary(target_root)}\n\n"
        "## Plan Snapshot\n\n"
        f"{_artifact_excerpt_summary(target_root, Path('.ai') / 'spec.md', label='spec')}\n"
        f"{_artifact_excerpt_summary(target_root, Path('.ai') / 'implementation-plan.md', label='plan')}\n"
        f"{_artifact_excerpt_summary(target_root, Path('.ai') / 'affected-files.md', label='affected-files')}\n\n"
        "## Verification Snapshot\n\n"
        f"{render_verification_summary(target_root)}\n\n"
        "## Next Suggested Action\n\n"
        f"{_next_suggested_action(state)}\n"
    )


def render_handoff(target_root: Path, state: dict, git_summary: GitSummary) -> str:
    return (
        "# Handoff\n\n"
        "## Current State\n\n"
        f"- mode: {state.get('mode', '-')}\n"
        f"- profile: {state.get('profile', '-')}\n"
        f"- status: {state.get('status', '-')}\n"
        f"- current_gate: {_display_gate(state.get('current_gate'))}\n"
        f"- approved_gates: {', '.join(state.get('approved_gates', [])) or 'none'}\n\n"
        "## What Has Been Done\n\n"
        f"{_what_has_been_done(target_root, state)}\n\n"
        "## Modified / Relevant Files\n\n"
        "```text\n"
        f"{git_summary.status_short.rstrip()}\n"
        "```\n\n"
        "## Validation / Review Artifacts\n\n"
        f"{_artifact_list(target_root)}\n\n"
        "## Plan Snapshot\n\n"
        f"{_artifact_excerpt_summary(target_root, Path('.ai') / 'spec.md', label='spec')}\n"
        f"{_artifact_excerpt_summary(target_root, Path('.ai') / 'implementation-plan.md', label='plan')}\n"
        f"{_artifact_excerpt_summary(target_root, Path('.ai') / 'affected-files.md', label='affected-files')}\n\n"
        "## Verification Snapshot\n\n"
        f"{render_verification_summary(target_root)}\n\n"
        "## Current Blocker / Gate\n\n"
        f"{_current_blocker(state)}\n\n"
        "## Next Action\n\n"
        f"{_next_suggested_action(state)}\n\n"
        "## Do Not Do\n\n"
        "- Do not implement out-of-scope features.\n"
        "- Do not bypass human review gates.\n"
        "- Do not overwrite existing harness files without `--force`.\n"
        "- Do not introduce third-party dependencies.\n"
    )


def _recent_review_summary(target_root: Path) -> str:
    review_path = target_root / REVIEW_PATH
    if not review_path.exists():
        return "- unavailable"
    status = _markdown_value(review_path, "## Status") or "unknown"
    return f"- {REVIEW_PATH.as_posix()} ({status})"


def _recent_approval_summary(target_root: Path) -> str:
    approval_path = target_root / APPROVAL_PATH
    if not approval_path.exists():
        return "- unavailable"
    decision = _markdown_value(approval_path, "## Decision") or "unknown"
    return f"- {APPROVAL_PATH.as_posix()} ({decision})"


def _what_has_been_done(target_root: Path, state: dict) -> str:
    items: list[str] = []
    if (target_root / "AGENTS.md").exists():
        items.append("- initialized small")
    if state.get("mode") == "large" or (target_root / ".ai" / "epic.md").exists():
        items.append("- upgraded large")
    if (target_root / REVIEW_PATH).exists():
        items.append("- diff review generated")
    if (target_root / (Path(".ai") / "reviews" / "spec-review.md")).exists():
        items.append("- spec review generated")
    if (target_root / (Path(".ai") / "reviews" / "plan-review.md")).exists():
        items.append("- plan review generated")
    if (target_root / (Path(".ai") / "reviews" / "final-review.md")).exists():
        items.append("- final review generated")
    if "spec" in state.get("approved_gates", []):
        items.append("- spec approved")
    if "plan" in state.get("approved_gates", []):
        items.append("- plan approved")
    if state.get("status") == "DIFF_APPROVED":
        items.append("- diff approved")
    if state.get("status") == "NEEDS_FIX":
        items.append("- diff rejected")
    if "final" in state.get("approved_gates", []):
        items.append("- final approved")
    return "\n".join(items) or "- no recorded progress"


def _artifact_list(target_root: Path) -> str:
    artifacts = [
        REVIEW_PATH,
        APPROVAL_PATH,
        CONTEXT_PACK_PATH,
        Path(".ai") / "run-trace.md",
        Path(".ai") / "verification.md",
        Path(".ai") / "evaluation.md",
    ]
    lines = []
    for artifact in artifacts:
        lines.append(f"- {artifact.as_posix()}: {_present(target_root / artifact)}")
    return "\n".join(lines)


def _current_blocker(state: dict) -> str:
    status = state.get("status")
    gate = state.get("current_gate")
    if gate is not None:
        return f"Blocked on human gate `{gate}` with status `{status}`."
    return f"No active human gate. Current status is `{status}`."


def _next_suggested_action(state: dict) -> str:
    status = state.get("status")
    if status == "WAITING_HUMAN_DIFF_APPROVAL":
        return "- Run `ai-approve diff` or `ai-reject diff`."
    if status == "DIFF_APPROVED":
        return "- Continue implementation or generate final validation artifacts."
    if status == "WAITING_HUMAN_FINAL_APPROVAL":
        return "- Review .ai/verification.md, then run `ai-approve final` or `ai-reject final`."
    if status == "PLAN_APPROVED":
        return "- Execute the plan, keep .ai/run-trace.md current, and record validation in .ai/verification.md."
    if status == "SPEC_APPROVED":
        return "- Refine .ai/implementation-plan.md and run `ai-review plan`."
    if status == "NEEDS_MORE_TESTS":
        return "- Add missing verification evidence in .ai/verification.md and rerun `ai-review final`."
    if status == "NEEDS_FIX":
        return "- Fix issues and rerun `ai-review diff`."
    if status == "INIT":
        return "- Start a task or run `ai-review diff` after changes."
    return f"- Continue from status `{status}` with the smallest safe next step."


def _artifact_excerpt_summary(target_root: Path, artifact: Path, *, label: str) -> str:
    path = target_root / artifact
    if not path.exists():
        return f"- {label}: missing"

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return f"- {label}: empty"

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    summary = " ".join(lines[:2])
    if len(summary) > 160:
        summary = summary[:157].rstrip() + "..."
    return f"- {label}: {summary}"


def _markdown_value(path: Path, header: str) -> str | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if line.strip() == header:
            for candidate in lines[index + 1 :]:
                stripped = candidate.strip()
                if stripped:
                    return stripped
    return None


def _run_git(target_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=target_root,
        capture_output=True,
        text=True,
        check=False,
    )


def _run_git_text(target_root: Path, *args: str) -> str:
    result = _run_git(target_root, *args)
    if result.returncode != 0:
        return "unavailable"
    return result.stdout.strip()


def _present(path: Path) -> str:
    return "present" if path.exists() else "missing"


def _display_gate(gate: object) -> str:
    return "none" if gate in (None, "", "none") else str(gate)
