from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CommandPermission(Enum):
    READ_ONLY = "read_only"
    GENERATE_ARTIFACT = "generate_artifact"
    WORKFLOW_TRANSITION = "workflow_transition"
    REQUIRES_USER_APPROVAL = "requires_user_approval"
    DESTRUCTIVE = "destructive"


@dataclass(frozen=True)
class CommandPolicy:
    command: str
    permission: CommandPermission
    summary: str


COMMAND_POLICIES: tuple[CommandPolicy, ...] = (
    CommandPolicy("ai-status", CommandPermission.READ_ONLY, "Show the human-readable workflow status."),
    CommandPolicy("ai-state", CommandPermission.READ_ONLY, "Show the machine-readable workflow state."),
    CommandPolicy("ai-doctor", CommandPermission.READ_ONLY, "Diagnose state and generated-file consistency."),
    CommandPolicy("ai-context-pack", CommandPermission.GENERATE_ARTIFACT, "Create a resumable context summary."),
    CommandPolicy("ai-handoff", CommandPermission.GENERATE_ARTIFACT, "Create a next-session handoff artifact."),
    CommandPolicy("ai-review", CommandPermission.WORKFLOW_TRANSITION, "Generate review artifacts and enter a waiting gate."),
    CommandPolicy("ai-upgrade", CommandPermission.REQUIRES_USER_APPROVAL, "Increase workflow control strength."),
    CommandPolicy("ai-approve", CommandPermission.REQUIRES_USER_APPROVAL, "Record a human approval decision."),
    CommandPolicy("ai-reject", CommandPermission.REQUIRES_USER_APPROVAL, "Record a human rejection decision."),
    CommandPolicy("ai-install-skills", CommandPermission.REQUIRES_USER_APPROVAL, "Write selected global skills for Codex."),
)


def get_command_policy(command: str) -> CommandPolicy:
    for policy in COMMAND_POLICIES:
        if policy.command == command:
            return policy
    raise KeyError(command)
