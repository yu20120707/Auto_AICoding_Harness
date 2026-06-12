from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class ProfileManifest:
    name: str
    display_name: str
    version: int
    languages: tuple[str, ...]
    domains: tuple[str, ...]
    risk_triggers: tuple[str, ...]
    verification: dict[str, str]
    root_path: Path
    manifest_path: Path


def profile_root(harness_root: Path, profile_name: str) -> Path:
    return harness_root / "profiles" / profile_name


def load_profile(harness_root: Path, profile_name: str) -> ProfileManifest:
    root = profile_root(harness_root, profile_name)
    manifest_path = root / "profile.yaml"
    if not manifest_path.exists():
        raise RuntimeError(f"missing profile manifest: {manifest_path}")

    payload = _load_manifest_payload(manifest_path)
    name = _require_str(payload, "name", manifest_path)
    if name != profile_name:
        raise RuntimeError(f"profile manifest name mismatch in {manifest_path}: {name} != {profile_name}")

    verification = payload.get("verification")
    if not isinstance(verification, dict):
        raise RuntimeError(f"profile manifest field 'verification' must be an object in {manifest_path}")
    normalized_verification = {
        key: _require_nested_str(verification, key, manifest_path)
        for key in ["build", "test", "sanitizer", "benchmark"]
    }

    return ProfileManifest(
        name=name,
        display_name=_require_str(payload, "display_name", manifest_path),
        version=_require_int(payload, "version", manifest_path),
        languages=tuple(_require_list(payload, "languages", manifest_path)),
        domains=tuple(_require_list(payload, "domains", manifest_path)),
        risk_triggers=tuple(_require_list(payload, "risk_triggers", manifest_path)),
        verification=normalized_verification,
        root_path=root,
        manifest_path=manifest_path,
    )


def _load_manifest_payload(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid profile manifest JSON/YAML in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"profile manifest must be an object in {path}")
    return payload


def _require_str(payload: dict[str, object], key: str, path: Path) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"profile manifest field '{key}' must be a non-empty string in {path}")
    return value


def _require_int(payload: dict[str, object], key: str, path: Path) -> int:
    value = payload.get(key)
    if not isinstance(value, int):
        raise RuntimeError(f"profile manifest field '{key}' must be an integer in {path}")
    return value


def _require_list(payload: dict[str, object], key: str, path: Path) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
        raise RuntimeError(f"profile manifest field '{key}' must be a non-empty string list in {path}")
    return value


def _require_nested_str(payload: dict[str, object], key: str, path: Path) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"profile manifest nested field '{key}' must be a non-empty string in {path}")
    return value
