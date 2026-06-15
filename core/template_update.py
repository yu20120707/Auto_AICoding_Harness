from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from core.template import TemplateFile, gather_template_files_for_stage


TEMPLATE_HASH_MANIFEST_PATH = Path(".ai") / "template-hashes.json"
MIGRATIONS_ROOT = Path("docs") / "ai" / "migrations"
MIGRATIONS_INDEX_PATH = MIGRATIONS_ROOT / "index.md"


@dataclass(frozen=True)
class TemplateHashEntry:
    path: str
    sha256: str


@dataclass(frozen=True)
class TemplateUpdatePlanItem:
    path: str
    state: str
    action: str


def build_template_hash_manifest(harness_root: Path, profile: str, roots: list[str]) -> dict:
    entries = []
    for template_file in gather_template_files_for_stage(harness_root, profile, roots):
        entries.append(
            {
                "path": template_file.relative_path.as_posix(),
                "sha256": sha256_bytes(template_file.source_path.read_bytes()),
            }
        )
    return {"schema_version": 1, "profile": profile, "files": entries}


def render_template_hash_manifest(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=True) + "\n"


def load_template_hash_manifest(target_root: Path) -> dict | None:
    path = target_root / TEMPLATE_HASH_MANIFEST_PATH
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def plan_template_update(
    *,
    target_root: Path,
    template_files: list[TemplateFile],
    previous_manifest: dict | None,
) -> list[TemplateUpdatePlanItem]:
    previous_hashes = _previous_hashes(previous_manifest)
    items: list[TemplateUpdatePlanItem] = []
    for template_file in template_files:
        relative = template_file.relative_path
        path_text = relative.as_posix()
        target_path = target_root / relative
        old_hash = previous_hashes.get(path_text)
        new_hash = sha256_bytes(template_file.source_path.read_bytes())
        if not target_path.exists():
            if old_hash is None:
                items.append(TemplateUpdatePlanItem(path_text, "new", "create"))
            else:
                items.append(TemplateUpdatePlanItem(path_text, "user-deleted", "skip"))
            continue
        current_hash = sha256_bytes(target_path.read_bytes())
        if old_hash is None:
            items.append(TemplateUpdatePlanItem(path_text, "untracked", "skip"))
        elif current_hash == old_hash:
            items.append(TemplateUpdatePlanItem(path_text, "unchanged", "update" if current_hash != new_hash else "keep"))
        else:
            items.append(TemplateUpdatePlanItem(path_text, "user-modified", "conflict"))
    return items


def render_template_update_plan(items: list[TemplateUpdatePlanItem]) -> str:
    lines = ["# Template Update Plan", ""]
    for item in items:
        lines.append(f"- {item.path}: {item.state} -> {item.action}")
    return "\n".join(lines) + "\n"


def render_migrations_index() -> str:
    return (
        "# Migrations\n\n"
        "Migration declarations are optional hardening metadata for existing template updates.\n"
        "They must not change public directory semantics, introduce `.harness/`, or rename `small / medium / large`.\n"
    )


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _previous_hashes(previous_manifest: dict | None) -> dict[str, str]:
    if not previous_manifest:
        return {}
    files = previous_manifest.get("files", [])
    if not isinstance(files, list):
        return {}
    hashes: dict[str, str] = {}
    for item in files:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        sha256 = item.get("sha256")
        if isinstance(path, str) and isinstance(sha256, str):
            hashes[path] = sha256
    return hashes
