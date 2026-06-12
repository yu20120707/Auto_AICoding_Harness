from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import os
import shutil


@dataclass(frozen=True)
class SkillSource:
    name: str
    source_path: Path


@dataclass(frozen=True)
class SkillManifest:
    name: str
    scope: str
    version: int
    install_default: bool
    platforms: tuple[str, ...]
    summary: str
    triggers: tuple[str, ...]
    source_path: Path
    manifest_path: Path
    profile: str | None = None


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


def default_install_manifest_path() -> Path:
    return Path.home() / ".ai-harness" / "installed-skills.json"


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


def discover_skill_manifests(skills_root: Path) -> list[SkillManifest]:
    manifests: list[SkillManifest] = []
    names: set[str] = set()

    for source in discover_skill_sources(skills_root):
        manifest_path = source.source_path / "skill.yaml"
        if not manifest_path.exists():
            raise RuntimeError(f"missing skill manifest: {manifest_path}")

        payload = _parse_skill_manifest(manifest_path)
        name = _require_str(payload, "name", manifest_path)
        if name != source.name:
            raise RuntimeError(f"skill manifest name mismatch in {manifest_path}: {name} != {source.name}")
        if name in names:
            raise RuntimeError(f"duplicate skill name: {name}")
        names.add(name)

        scope = _require_str(payload, "scope", manifest_path)
        version = _require_int(payload, "version", manifest_path)
        install_default = _require_bool(payload, "install_default", manifest_path)
        platforms = tuple(_require_list(payload, "platforms", manifest_path))
        summary = _require_str(payload, "summary", manifest_path)
        triggers = tuple(_require_list(payload, "triggers", manifest_path))
        profile = payload.get("profile")
        if profile is not None and not isinstance(profile, str):
            raise RuntimeError(f"skill manifest field 'profile' must be a string in {manifest_path}")

        manifests.append(
            SkillManifest(
                name=name,
                scope=scope,
                version=version,
                install_default=install_default,
                platforms=platforms,
                summary=summary,
                triggers=triggers,
                source_path=source.source_path,
                manifest_path=manifest_path,
                profile=profile,
            )
        )

    return sorted(manifests, key=lambda manifest: manifest.name)


def select_skill_manifests(
    *,
    manifests: list[SkillManifest],
    platform: str,
    scopes: set[str] | None = None,
    profile: str | None = None,
) -> list[SkillManifest]:
    requested_scopes = scopes or set()
    selected: list[SkillManifest] = []

    for manifest in manifests:
        if platform not in manifest.platforms:
            continue

        include = False
        if not requested_scopes and profile is None:
            include = manifest.install_default
        else:
            if requested_scopes and manifest.scope in requested_scopes:
                include = True
            if profile is not None and manifest.profile == profile:
                include = True

        if include:
            selected.append(manifest)

    return selected


def install_all_skills(
    *,
    skills_root: Path,
    dest_root: Path,
    force: bool,
    platform: str = "codex",
    scopes: set[str] | None = None,
    profile: str | None = None,
    dry_run: bool = False,
    timestamp: str | None = None,
) -> list[SkillInstallResult]:
    install_timestamp = timestamp or datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    backup_root = dest_root.parent / "skill-backups" / install_timestamp
    selected = select_skill_manifests(
        manifests=discover_skill_manifests(skills_root),
        platform=platform,
        scopes=scopes,
        profile=profile,
    )
    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    results: list[SkillInstallResult] = []
    for manifest in selected:
        target = dest_root / manifest.name

        if not target.exists():
            if not dry_run:
                shutil.copytree(manifest.source_path, target)
            action = "WOULD_CREATE" if dry_run else "CREATED"
            results.append(SkillInstallResult(action=action, name=manifest.name, path=target))
            continue

        if not force:
            action = "WOULD_SKIP" if dry_run else "SKIPPED"
            results.append(SkillInstallResult(action=action, name=manifest.name, path=target))
            continue

        backup_path = backup_root / manifest.name
        if not dry_run:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            if target.is_dir():
                shutil.copytree(target, backup_path)
                shutil.rmtree(target)
            else:
                shutil.copy2(target, backup_path)
                target.unlink()

            shutil.copytree(manifest.source_path, target)
        action = "WOULD_OVERWRITE" if dry_run else "OVERWRITTEN"
        results.append(SkillInstallResult(action=action, name=manifest.name, path=target, backup_path=backup_path))

    return results


def write_install_manifest(
    *,
    manifest_path: Path,
    platform: str,
    installed_manifests: list[SkillManifest],
    dry_run: bool,
) -> Path:
    if dry_run:
        return manifest_path

    payload = {
        "platform": platform,
        "installed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "skills": [
            {
                "name": manifest.name,
                "scope": manifest.scope,
                "version": manifest.version,
                "profile": manifest.profile,
                "source": _relative_source(manifest.source_path),
            }
            for manifest in installed_manifests
        ],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def _relative_source(source_path: Path) -> str:
    parts = source_path.parts
    if "skills" in parts:
        index = parts.index("skills")
        return "/".join(parts[index:])
    return source_path.as_posix()


def _parse_skill_manifest(path: Path) -> dict[str, object]:
    payload: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            if current_list_key is None:
                raise RuntimeError(f"unexpected list item in {path}: {stripped}")
            payload.setdefault(current_list_key, [])
            payload[current_list_key].append(stripped[2:].strip())
            continue

        current_list_key = None
        key, sep, value = stripped.partition(":")
        if not sep:
            raise RuntimeError(f"invalid manifest line in {path}: {stripped}")
        key = key.strip()
        value = value.strip()
        if not value:
            payload[key] = []
            current_list_key = key
            continue
        if value in {"true", "false"}:
            payload[key] = value == "true"
        elif value.isdigit():
            payload[key] = int(value)
        else:
            payload[key] = value

    return payload


def _require_str(payload: dict[str, object], key: str, path: Path) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"skill manifest field '{key}' must be a non-empty string in {path}")
    return value


def _require_int(payload: dict[str, object], key: str, path: Path) -> int:
    value = payload.get(key)
    if not isinstance(value, int):
        raise RuntimeError(f"skill manifest field '{key}' must be an integer in {path}")
    return value


def _require_bool(payload: dict[str, object], key: str, path: Path) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        raise RuntimeError(f"skill manifest field '{key}' must be a boolean in {path}")
    return value


def _require_list(payload: dict[str, object], key: str, path: Path) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
        raise RuntimeError(f"skill manifest field '{key}' must be a non-empty string list in {path}")
    return value
