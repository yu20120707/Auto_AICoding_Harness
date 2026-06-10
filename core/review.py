from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from core.verification import VERIFICATION_PATH


@dataclass(frozen=True)
class GitDiffData:
    status_short: str
    diff_stat: str
    changed_files: str
    diff_text: str


@dataclass(frozen=True)
class ReviewArtifact:
    relative_path: Path
    content: str
    skipped_message: str
    update_state: str


def ensure_git_repo(target_root: Path) -> None:
    result = _run_git(target_root, "rev-parse", "--is-inside-work-tree")
    if result.returncode != 0 or result.stdout.strip() != "true":
        message = result.stderr.strip() or "current directory is not a git repository"
        raise RuntimeError(message)


def collect_git_diff_data(target_root: Path) -> GitDiffData:
    commands = {
        "status_short": ("status", "--short"),
        "diff_stat": ("diff", "--stat"),
        "changed_files": ("diff", "--name-only"),
        "diff_text": ("diff",),
    }

    outputs: dict[str, str] = {}
    for key, args in commands.items():
        result = _run_git(target_root, *args)
        if result.returncode != 0:
            message = result.stderr.strip() or f"git {' '.join(args)} failed"
            raise RuntimeError(message)
        outputs[key] = result.stdout

    if not outputs["diff_text"].strip():
        raise RuntimeError("no git diff to review")

    return GitDiffData(
        status_short=outputs["status_short"],
        diff_stat=outputs["diff_stat"],
        changed_files=outputs["changed_files"],
        diff_text=outputs["diff_text"],
    )


def render_diff_review(data: GitDiffData) -> str:
    return (
        "# Diff Review\n\n"
        "## Status\n\n"
        "WAITING_HUMAN_DIFF_APPROVAL\n\n"
        "## Git Status\n\n"
        "```text\n"
        f"{data.status_short.rstrip()}\n"
        "```\n\n"
        "## Diff Stat\n\n"
        "```text\n"
        f"{data.diff_stat.rstrip()}\n"
        "```\n\n"
        "## Changed Files\n\n"
        "```text\n"
        f"{data.changed_files.rstrip()}\n"
        "```\n\n"
        "## Diff\n\n"
        "```diff\n"
        f"{data.diff_text.rstrip()}\n"
        "```\n\n"
        "## Scope Check\n\n"
        "* [ ] Only expected files changed\n"
        "* [ ] No unrelated formatting\n"
        "* [ ] No generated/runtime files accidentally committed\n"
        "* [ ] No public API change unless approved\n"
        "* [ ] No large hidden refactor\n\n"
        "## C++ / System Risk Check\n\n"
        "* [ ] Ownership/lifetime safe\n"
        "* [ ] Error handling complete\n"
        "* [ ] No data race introduced\n"
        "* [ ] API/ABI compatibility checked\n"
        "* [ ] Timeout/retry semantics unchanged or explained\n"
        "* [ ] Tests updated or not required with reason\n\n"
        "## Human Decision\n\n"
        "* [ ] Approved\n"
        "* [ ] Needs fix\n"
        "* [ ] Needs replan\n"
        "* [ ] Rejected\n\n"
        "## Human Notes\n"
    )


def build_spec_review() -> ReviewArtifact:
    source = Path(".ai") / "spec.md"
    return ReviewArtifact(
        relative_path=Path(".ai") / "reviews" / "spec-review.md",
        content=render_spec_review(source.read_text(encoding="utf-8")),
        skipped_message="state unchanged; use --force to regenerate spec review",
        update_state="spec",
    )


def build_plan_review() -> ReviewArtifact:
    source = Path(".ai") / "implementation-plan.md"
    return ReviewArtifact(
        relative_path=Path(".ai") / "reviews" / "plan-review.md",
        content=render_plan_review(source.read_text(encoding="utf-8")),
        skipped_message="state unchanged; use --force to regenerate plan review",
        update_state="plan",
    )


def build_final_review(target_root: Path) -> ReviewArtifact:
    return ReviewArtifact(
        relative_path=Path(".ai") / "reviews" / "final-review.md",
        content=render_final_review(target_root),
        skipped_message="state unchanged; use --force to regenerate final review",
        update_state="final",
    )


def render_spec_review(spec_text: str) -> str:
    return (
        "# Spec Review\n\n"
        "## Status\n\n"
        "WAITING_HUMAN_SPEC_APPROVAL\n\n"
        "## Source\n\n"
        ".ai/spec.md\n\n"
        "## Spec Summary\n\n"
        "```text\n"
        f"{_excerpt(spec_text)}\n"
        "```\n\n"
        "## Scope Check\n\n"
        "- [ ] Goal is clear\n"
        "- [ ] Non-goals are explicit\n"
        "- [ ] Allowed files / modules are clear\n"
        "- [ ] Forbidden changes are clear\n"
        "- [ ] Required validation is defined\n\n"
        "## Risk Check\n\n"
        "- [ ] API / ABI risk considered\n"
        "- [ ] Data / persistence risk considered\n"
        "- [ ] Concurrency / IPC / network risk considered\n"
        "- [ ] Performance risk considered\n"
        "- [ ] Rollback or recovery considered\n\n"
        "## Human Decision\n\n"
        "- [ ] Approved\n"
        "- [ ] Needs replan\n"
        "- [ ] Rejected\n\n"
        "## Human Notes\n"
    )


def render_plan_review(plan_text: str) -> str:
    return (
        "# Plan Review\n\n"
        "## Status\n\n"
        "WAITING_HUMAN_PLAN_APPROVAL\n\n"
        "## Source\n\n"
        ".ai/implementation-plan.md\n\n"
        "## Plan Summary\n\n"
        "```text\n"
        f"{_excerpt(plan_text)}\n"
        "```\n\n"
        "## Implementation Check\n\n"
        "- [ ] Call chain is identified\n"
        "- [ ] Affected files are listed\n"
        "- [ ] Change scope is minimal\n"
        "- [ ] Validation commands are defined\n"
        "- [ ] Rollback or fallback is considered\n\n"
        "## C++ / System Check\n\n"
        "- [ ] Resource lifetime considered\n"
        "- [ ] Error propagation considered\n"
        "- [ ] Concurrency and locking considered\n"
        "- [ ] API / ABI compatibility considered\n"
        "- [ ] Performance impact considered\n\n"
        "## Human Decision\n\n"
        "- [ ] Approved\n"
        "- [ ] Needs replan\n"
        "- [ ] Rejected\n\n"
        "## Human Notes\n"
    )


def render_final_review(target_root: Path) -> str:
    sources = [
        VERIFICATION_PATH,
        Path(".ai") / "evaluation.md",
        Path(".ai") / "context-pack.md",
        Path(".ai") / "handoff.md",
        Path(".ai") / "reviews" / "diff-review.md",
        Path(".ai") / "approvals" / "diff-approval.md",
    ]
    present_sources = [path for path in sources if (target_root / path).exists()]
    source_lines = "\n".join(f"- {path.as_posix()}" for path in present_sources) or "- none"
    evidence_sections = []
    for path in present_sources:
        evidence_sections.append(
            f"### {path.as_posix()}\n\n"
            "```text\n"
            f"{_excerpt((target_root / path).read_text(encoding='utf-8'))}\n"
            "```"
        )
    evidence_text = "\n\n".join(evidence_sections) or "No review evidence found."
    return (
        "# Final Review\n\n"
        "## Status\n\n"
        "WAITING_HUMAN_FINAL_APPROVAL\n\n"
        "## Sources\n\n"
        f"{source_lines}\n\n"
        "## Final Evidence Summary\n\n"
        f"{evidence_text}\n\n"
        "## Completion Check\n\n"
        "- [ ] Requested scope completed\n"
        "- [ ] Diff reviewed\n"
        "- [ ] Required validation completed\n"
        "- [ ] Known issues documented\n"
        "- [ ] No blocked human gate remains\n"
        "- [ ] Handoff/context available if needed\n\n"
        "## Human Decision\n\n"
        "- [ ] Approved\n"
        "- [ ] Needs fix\n"
        "- [ ] Rejected\n\n"
        "## Human Notes\n"
    )


def require_review_input_exists(target_root: Path, review_type: str) -> None:
    required_by_type = {
        "spec": [Path(".ai") / "spec.md"],
        "plan": [Path(".ai") / "implementation-plan.md"],
    }
    if review_type in required_by_type:
        required = required_by_type[review_type][0]
        if not (target_root / required).exists():
            raise RuntimeError(f"missing required review input: {required.as_posix()}")
        return

    if review_type == "final":
        candidates = [
            VERIFICATION_PATH,
            Path(".ai") / "evaluation.md",
            Path(".ai") / "context-pack.md",
            Path(".ai") / "handoff.md",
        ]
        if not any((target_root / path).exists() for path in candidates):
            joined = ", ".join(path.as_posix() for path in candidates)
            raise RuntimeError(f"missing required final review input: one of {joined}")


def _excerpt(text: str, *, max_chars: int = 4000) -> str:
    stripped = text.strip()
    if not stripped:
        return "(empty)"
    if len(stripped) <= max_chars:
        return stripped
    return stripped[:max_chars].rstrip() + "\n...[truncated]"


def _run_git(target_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=target_root,
        capture_output=True,
        text=True,
        check=False,
    )
