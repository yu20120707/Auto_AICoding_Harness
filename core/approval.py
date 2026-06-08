from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ApprovalGateConfig:
    gate: str
    review_path: Path
    approval_path: Path
    waiting_status: str
    approved_status: str
    rejected_status: str
    approval_title: str
    approve_notes: str
    reject_notes: str


GATE_CONFIGS: dict[str, ApprovalGateConfig] = {
    "spec": ApprovalGateConfig(
        gate="spec",
        review_path=Path(".ai") / "reviews" / "spec-review.md",
        approval_path=Path(".ai") / "approvals" / "spec-approval.md",
        waiting_status="WAITING_HUMAN_SPEC_APPROVAL",
        approved_status="SPEC_APPROVED",
        rejected_status="NEEDS_REPLAN",
        approval_title="Spec Approval",
        approve_notes="Human approved the spec review gate.",
        reject_notes="Human rejected the spec review gate. The task requires replanning before continuing.",
    ),
    "plan": ApprovalGateConfig(
        gate="plan",
        review_path=Path(".ai") / "reviews" / "plan-review.md",
        approval_path=Path(".ai") / "approvals" / "plan-approval.md",
        waiting_status="WAITING_HUMAN_PLAN_APPROVAL",
        approved_status="PLAN_APPROVED",
        rejected_status="NEEDS_REPLAN",
        approval_title="Plan Approval",
        approve_notes="Human approved the plan review gate.",
        reject_notes="Human rejected the plan review gate. The task requires replanning before continuing.",
    ),
    "diff": ApprovalGateConfig(
        gate="diff",
        review_path=Path(".ai") / "reviews" / "diff-review.md",
        approval_path=Path(".ai") / "approvals" / "diff-approval.md",
        waiting_status="WAITING_HUMAN_DIFF_APPROVAL",
        approved_status="DIFF_APPROVED",
        rejected_status="NEEDS_FIX",
        approval_title="Diff Approval",
        approve_notes="Human approved the diff review gate.",
        reject_notes="Human rejected the diff review gate. The task requires fixes before continuing.",
    ),
    "final": ApprovalGateConfig(
        gate="final",
        review_path=Path(".ai") / "reviews" / "final-review.md",
        approval_path=Path(".ai") / "approvals" / "final-approval.md",
        waiting_status="WAITING_HUMAN_FINAL_APPROVAL",
        approved_status="DONE",
        rejected_status="NEEDS_MORE_TESTS",
        approval_title="Final Approval",
        approve_notes="Human approved the final review gate.",
        reject_notes="Human rejected the final review gate. The task requires more verification before completion.",
    ),
}


def render_approval(*, config: ApprovalGateConfig, approved: bool) -> str:
    if approved:
        decision = "APPROVED"
        new_status = config.approved_status
        notes = config.approve_notes
    else:
        decision = "REJECTED"
        new_status = config.rejected_status
        notes = config.reject_notes

    return (
        f"# {config.approval_title}\n\n"
        "## Decision\n\n"
        f"{decision}\n\n"
        "## Gate\n\n"
        f"{config.gate}\n\n"
        "## Previous Status\n\n"
        f"{config.waiting_status}\n\n"
        "## New Status\n\n"
        f"{new_status}\n\n"
        "## Notes\n\n"
        f"{notes}\n"
    )
