from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil


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

    forbidden_roots = {"src", "include", "tests"}
    if parts[0] in forbidden_roots:
        raise ValueError(f"refusing to write forbidden business path: {relative_path}")


def safe_write_bytes(
    *,
    target_root: Path,
    relative_path: Path,
    content: bytes,
    force: bool,
    timestamp: str | None = None,
) -> WriteResult:
    _ensure_allowed_relative_path(relative_path)

    target_path = target_root / relative_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if not target_path.exists():
        target_path.write_bytes(content)
        return WriteResult(action="CREATED", path=target_path)

    if not force:
        return WriteResult(action="SKIPPED", path=target_path)

    backup_timestamp = timestamp or datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    backup_path = _backup_root(target_root, backup_timestamp) / relative_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(target_path, backup_path)
    target_path.write_bytes(content)
    return WriteResult(action="OVERWRITTEN", path=target_path, backup_path=backup_path)

