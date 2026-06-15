from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from core.approval import ApprovalGateConfig
from core.task_chain import task_id_for_state


RCA_FILE_NAME = "rca.md"
CHECK_RULES_ROOT = Path("docs") / "ai" / "check-rules"
DRAFTS_ROOT = CHECK_RULES_ROOT / "drafts"
INDEX_PATH = CHECK_RULES_ROOT / "index.md"


def rca_relative_path(state: dict[str, Any]) -> Path:
    return Path(".ai") / "tasks" / task_id_for_state(state) / RCA_FILE_NAME


def check_rule_draft_relative_path(state: dict[str, Any], gate: str) -> Path:
    return DRAFTS_ROOT / f"{task_id_for_state(state)}-{gate}.md"


def render_rca(*, state: dict[str, Any], config: ApprovalGateConfig, created_at: str | None = None) -> str:
    timestamp = created_at or datetime.now().astimezone().isoformat(timespec="seconds")
    return (
        "# RCA Draft\n\n"
        "## Status\n\n"
        "DRAFT\n\n"
        "## Trigger\n\n"
        f"- gate: {config.gate}\n"
        f"- rejected_status: {config.rejected_status}\n"
        f"- task_id: {task_id_for_state(state)}\n"
        f"- created_at: {timestamp}\n\n"
        "## Observed Failure\n\n"
        f"{config.reject_notes}\n\n"
        "## Likely Cause\n\n"
        "- To be completed by the implementer or reviewer before retrying the gate.\n\n"
        "## Corrective Action\n\n"
        f"- Address the rejected `{config.gate}` gate feedback.\n"
        f"- Rerun `ai-review {config.gate}` after the fix.\n\n"
        "## Follow-up Rule Candidate\n\n"
        "- See the generated check-rule draft. It is not enforced unless explicitly approved.\n"
    )


def render_check_rule_draft(*, state: dict[str, Any], config: ApprovalGateConfig, created_at: str | None = None) -> str:
    timestamp = created_at or datetime.now().astimezone().isoformat(timespec="seconds")
    return (
        "# Check Rule Draft\n\n"
        "## Status\n\n"
        "DRAFT_NOT_ENFORCED\n\n"
        "## Activation Policy\n\n"
        "This draft must not be added to `docs/ai/check-rules/index.md` automatically. "
        "It requires explicit human approval before becoming an enforced rule.\n\n"
        "## Trigger\n\n"
        f"- task_id: {task_id_for_state(state)}\n"
        f"- gate: {config.gate}\n"
        f"- created_at: {timestamp}\n\n"
        "## Candidate Rule\n\n"
        f"Before rerunning `{config.gate}` review, confirm the rejected issue is fixed and documented in `.ai/verification.md`.\n"
    )


def render_check_rules_index() -> str:
    return (
        "# Check Rules\n\n"
        "This directory may contain human-approved check rules and generated drafts.\n\n"
        "Generated drafts under `drafts/` are not enforced automatically. Move or reference a draft here "
        "only after explicit human approval.\n"
    )
