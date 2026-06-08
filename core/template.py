from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.safe_write import WriteResult, safe_write_bytes


@dataclass(frozen=True)
class TemplateFile:
    source_path: Path
    relative_path: Path


def gather_template_files(harness_root: Path, profile: str) -> list[TemplateFile]:
    return gather_template_files_for_stage(harness_root, profile, roots=["base/root", f"profiles/{profile}/root"])


def gather_template_files_for_stage(harness_root: Path, profile: str, roots: list[str]) -> list[TemplateFile]:
    merged_files: dict[Path, Path] = {}

    for template_root in _resolve_template_roots(harness_root, roots):
        if not template_root.exists():
            continue

        for source_path in sorted(path for path in template_root.rglob("*") if path.is_file()):
            relative_path = source_path.relative_to(template_root)
            merged_files[relative_path] = source_path

    return [
        TemplateFile(source_path=source_path, relative_path=relative_path)
        for relative_path, source_path in sorted(merged_files.items())
    ]


def materialize_templates(
    *,
    harness_root: Path,
    target_root: Path,
    profile: str,
    force: bool,
    timestamp: str,
) -> list[WriteResult]:
    return materialize_template_stage(
        harness_root=harness_root,
        target_root=target_root,
        profile=profile,
        force=force,
        timestamp=timestamp,
        roots=["base/root", f"profiles/{profile}/root"],
    )


def materialize_template_stage(
    *,
    harness_root: Path,
    target_root: Path,
    profile: str,
    force: bool,
    timestamp: str,
    roots: list[str],
) -> list[WriteResult]:
    results: list[WriteResult] = []

    for template_file in gather_template_files_for_stage(harness_root, profile, roots):
        results.append(
            safe_write_bytes(
                target_root=target_root,
                relative_path=template_file.relative_path,
                content=template_file.source_path.read_bytes(),
                force=force,
                timestamp=timestamp,
            )
        )

    return results


def _resolve_template_roots(harness_root: Path, roots: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for root in roots:
        root_path = Path(root)
        if root_path.parts and root_path.parts[0] == "profiles":
            resolved.append(harness_root / root_path)
        else:
            resolved.append(harness_root / "templates" / root_path)
    return resolved
