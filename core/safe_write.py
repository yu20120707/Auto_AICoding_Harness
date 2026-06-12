from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


@dataclass(frozen=True)
class WriteResult:
    action: str
    path: Path
    backup_path: Path | None = None


def _backup_root(target_root: Path, timestamp: str) -> Path:
    return target_root / ".ai" / "backups" / timestamp


def _ensure_allowed_relative_path(relative_path: Path) -> None:
    if relative_path.is_absolute():
        raise ValueError(f"expected relative path, got absolute path: {relative_path}")

    parts = relative_path.parts
    if not parts:
        raise ValueError("empty relative path is not allowed")

    if parts[0] in {"src", "include", "tests", ".git"}:
        raise ValueError(f"refusing to write forbidden business path: {relative_path}")

    allowed = (
        relative_path in {Path("AGENTS.md"), Path("CLAUDE.md"), Path(".github") / "copilot-instructions.md"}
        or parts[0] == ".ai"
        or parts[0] == ".codex" and len(parts) > 1 and parts[1] == "agents"
        or parts[0] == "docs" and len(parts) > 1 and parts[1] == "ai"
        or parts[0] == "scripts" and parts[-1].startswith("ai_")
    )
    if not allowed:
        raise ValueError(f"refusing to write unmanaged path: {relative_path}")


def _resolve_target_path(target_root: Path, relative_path: Path) -> Path:
    root = target_root.resolve()
    target_path = target_root / relative_path
    resolved_target = target_path.resolve(strict=False)
    if not resolved_target.is_relative_to(root):
        raise ValueError(f"path escapes target root: {relative_path}")
    return target_path


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _atomic_write_bytes(target_path: Path, content: bytes) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        dir=str(target_path.parent),
        prefix=f".{target_path.name}.",
        suffix=".tmp",
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, target_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _append_backup_manifest(
    *,
    target_root: Path,
    timestamp: str,
    relative_path: Path,
    before_bytes: bytes,
    after_bytes: bytes,
    backup_path: Path,
) -> None:
    manifest_path = _backup_root(target_root, timestamp) / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"writes": []}

    manifest["writes"].append(
        {
            "operation": "force_overwrite",
            "path": relative_path.as_posix(),
            "action": "OVERWRITTEN",
            "sha256_before": _sha256_bytes(before_bytes),
            "sha256_after": _sha256_bytes(after_bytes),
            "backup_path": backup_path.relative_to(target_root).as_posix(),
        }
    )
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def safe_write_bytes(
    *,
    target_root: Path,
    relative_path: Path,
    content: bytes,
    force: bool,
    timestamp: str | None = None,
) -> WriteResult:
    _ensure_allowed_relative_path(relative_path)

    target_path = _resolve_target_path(target_root, relative_path)

    if not target_path.exists():
        _atomic_write_bytes(target_path, content)
        return WriteResult(action="CREATED", path=target_path)

    if not force:
        return WriteResult(action="SKIPPED", path=target_path)

    backup_timestamp = timestamp or datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    backup_path = _backup_root(target_root, backup_timestamp) / relative_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    before_bytes = target_path.read_bytes()
    shutil.copy2(target_path, backup_path)
    _atomic_write_bytes(target_path, content)
    _append_backup_manifest(
        target_root=target_root,
        timestamp=backup_timestamp,
        relative_path=relative_path,
        before_bytes=before_bytes,
        after_bytes=content,
        backup_path=backup_path,
    )
    return WriteResult(action="OVERWRITTEN", path=target_path, backup_path=backup_path)
