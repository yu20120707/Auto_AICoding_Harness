from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import os
import shutil


@dataclass(frozen=True)
class SkillSource:
    name: str
    source_path: Path


@dataclass(frozen=True)
class SkillInstallResult:
    action: str
    name: str
    path: Path
    backup_path: Path | None = None


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def default_skills_dest() -> Path:
    return default_codex_home() / "skills"


def discover_skill_sources(skills_root: Path) -> list[SkillSource]:
    if not skills_root.exists():
        raise FileNotFoundError(f"skills source directory does not exist: {skills_root}")

    sources: dict[str, Path] = {}
    for skill_file in sorted(skills_root.rglob("SKILL.md")):
        skill_dir = skill_file.parent
        name = skill_dir.name
        if name in sources:
            raise ValueError(f"duplicate skill name: {name}")
        sources[name] = skill_dir

    if not sources:
        raise RuntimeError(f"no SKILL.md files found under {skills_root}")

    return [SkillSource(name=name, source_path=path) for name, path in sorted(sources.items())]


def install_all_skills(
    *,
    skills_root: Path,
    dest_root: Path,
    force: bool,
    dry_run: bool = False,
    timestamp: str | None = None,
) -> list[SkillInstallResult]:
    install_timestamp = timestamp or datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    backup_root = dest_root.parent / "skill-backups" / install_timestamp
    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    results: list[SkillInstallResult] = []
    for source in discover_skill_sources(skills_root):
        target = dest_root / source.name

        if not target.exists():
            if not dry_run:
                shutil.copytree(source.source_path, target)
            action = "WOULD_CREATE" if dry_run else "CREATED"
            results.append(SkillInstallResult(action=action, name=source.name, path=target))
            continue

        if not force:
            action = "WOULD_SKIP" if dry_run else "SKIPPED"
            results.append(SkillInstallResult(action=action, name=source.name, path=target))
            continue

        backup_path = backup_root / source.name
        if not dry_run:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            if target.is_dir():
                shutil.copytree(target, backup_path)
                shutil.rmtree(target)
            else:
                shutil.copy2(target, backup_path)
                target.unlink()

            shutil.copytree(source.source_path, target)
        action = "WOULD_OVERWRITE" if dry_run else "OVERWRITTEN"
        results.append(SkillInstallResult(action=action, name=source.name, path=target, backup_path=backup_path))

    return results
