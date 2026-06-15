from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from core.task_chain import task_dir_relative_path


CONTEXT_MANIFEST_FILE_NAME = "context.jsonl"

ALLOWED_REFERENCE_PREFIXES = (
    "docs/ai/tasks/",
    "docs/ai/specs/",
    "docs/ai/profiles/",
    "docs/ai/workflow/",
    "docs/ai/check-rules/",
    ".ai/spec.md",
    ".ai/implementation-plan.md",
    ".ai/tech-design.md",
    ".ai/risk-and-rollback.md",
    ".ai/verification.md",
    ".ai/context-pack.md",
    ".ai/handoff.md",
    ".ai/tasks/",
    ".ai/context/packs/",
)

DISALLOWED_REFERENCE_PREFIXES = (
    "src/",
    "include/",
    "tests/",
    "core/",
    "bin/",
    "templates/",
    ".git/",
)


@dataclass(frozen=True)
class ContextManifestEntry:
    path: str
    reason: str
    phase: str

    def to_json_line(self) -> str:
        return json.dumps(
            {"path": self.path, "reason": self.reason, "phase": self.phase},
            ensure_ascii=True,
        )


@dataclass(frozen=True)
class ContextManifestLoadResult:
    path: Path
    exists: bool
    entries: list[ContextManifestEntry]
    errors: list[str]

    @property
    def valid(self) -> bool:
        return self.exists and not self.errors


def context_manifest_relative_path(state: dict[str, Any]) -> Path:
    return Path(".ai") / "tasks" / str(state.get("task_id") or "current-task") / CONTEXT_MANIFEST_FILE_NAME


def build_default_context_manifest_entries(target_root: Path, state: dict[str, Any]) -> list[ContextManifestEntry]:
    candidates = [
        ContextManifestEntry(".ai/spec.md", "Large-mode requirement source", "implement"),
        ContextManifestEntry(".ai/implementation-plan.md", "Large-mode implementation plan", "implement"),
        ContextManifestEntry(".ai/tech-design.md", "Large-mode technical design", "implement"),
        ContextManifestEntry(".ai/risk-and-rollback.md", "Rollback and risk guardrails", "review"),
        ContextManifestEntry(".ai/verification.md", "Verification evidence", "review"),
        ContextManifestEntry(".ai/handoff.md", "Cross-session handoff summary", "handoff"),
        ContextManifestEntry(
            (task_dir_relative_path(state) / "01-spec.md").as_posix(),
            "Durable task spec evidence",
            "implement",
        ),
        ContextManifestEntry(
            (task_dir_relative_path(state) / "03-implementation-plan.md").as_posix(),
            "Durable task implementation plan evidence",
            "implement",
        ),
        ContextManifestEntry(
            (task_dir_relative_path(state) / "05-verification.md").as_posix(),
            "Durable task verification evidence",
            "review",
        ),
    ]
    return [entry for entry in candidates if (target_root / entry.path).exists()]


def render_context_manifest(entries: list[ContextManifestEntry]) -> str:
    return "\n".join(entry.to_json_line() for entry in entries) + ("\n" if entries else "")


def load_context_manifest(target_root: Path, state: dict[str, Any]) -> ContextManifestLoadResult:
    relative_path = context_manifest_relative_path(state)
    path = target_root / relative_path
    if not path.exists():
        return ContextManifestLoadResult(path=relative_path, exists=False, entries=[], errors=[])

    entries: list[ContextManifestEntry] = []
    errors: list[str] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
            continue
        entry_errors = validate_context_manifest_payload(payload)
        if entry_errors:
            errors.extend(f"line {line_number}: {error}" for error in entry_errors)
            continue
        entries.append(
            ContextManifestEntry(
                path=payload["path"],
                reason=payload["reason"],
                phase=payload["phase"],
            )
        )
    return ContextManifestLoadResult(path=relative_path, exists=True, entries=entries, errors=errors)


def validate_context_manifest_payload(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return ["entry must be an object"]
    errors: list[str] = []
    for key in ("path", "reason", "phase"):
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} must be a non-empty string")
    path = payload.get("path")
    if isinstance(path, str) and path.strip():
        normalized = path.replace("\\", "/").lstrip("/")
        if ".." in Path(normalized).parts:
            errors.append(f"path escapes allowed scope: {path}")
        if normalized != path:
            errors.append(f"path must be normalized relative posix: {path}")
        if normalized.startswith(DISALLOWED_REFERENCE_PREFIXES):
            errors.append(f"path is disallowed by default: {path}")
        if not _is_allowed_reference(normalized):
            errors.append(f"path is outside allowed context manifest scope: {path}")
    return errors


def summarize_context_manifest(result: ContextManifestLoadResult, *, max_entries: int = 8) -> str:
    if not result.exists:
        return "- context manifest: missing"
    lines = [f"- context manifest: present ({result.path.as_posix()})"]
    lines.append(f"- context manifest valid: {'yes' if not result.errors else 'no'}")
    lines.append(f"- context manifest entries: {len(result.entries)}")
    for entry in result.entries[:max_entries]:
        lines.append(f"  - {entry.path} [{entry.phase}]: {entry.reason}")
    if len(result.entries) > max_entries:
        lines.append(f"  - ... {len(result.entries) - max_entries} more")
    if result.errors:
        lines.append(f"- context manifest errors: {' | '.join(result.errors)}")
    return "\n".join(lines)


def _is_allowed_reference(path: str) -> bool:
    return path.startswith(ALLOWED_REFERENCE_PREFIXES)
