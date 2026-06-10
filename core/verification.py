from __future__ import annotations

from pathlib import Path


VERIFICATION_PATH = Path(".ai") / "verification.md"


def verification_path(target_root: Path) -> Path:
    return target_root / VERIFICATION_PATH


def has_meaningful_verification(target_root: Path) -> bool:
    path = verification_path(target_root)
    if not path.exists():
        return False

    data = parse_verification(target_root)
    return any(item.get("command") and item.get("command") != "-" for item in data["ran"])


def parse_verification(target_root: Path) -> dict[str, list[dict[str, str]]]:
    path = verification_path(target_root)
    if not path.exists():
        return {"ran": [], "not_run": []}

    lines = path.read_text(encoding="utf-8").splitlines()
    section: str | None = None
    current: dict[str, str] | None = None
    ran: list[dict[str, str]] = []
    not_run: list[dict[str, str]] = []

    for raw in lines:
        line = raw.strip()
        if line == "## Ran":
            section = "ran"
            current = None
            continue
        if line == "## Not Run":
            section = "not_run"
            current = None
            continue
        if not section or not line.startswith("- "):
            continue

        key, _, value = line[2:].partition(":")
        key = key.strip().lower().replace(" ", "_")
        value = value.strip()

        if section == "ran":
            if key == "command":
                current = {"command": value, "result": "", "notes": ""}
                ran.append(current)
            elif current is not None and key in current:
                current[key] = value
        elif section == "not_run":
            if key == "item":
                current = {"item": value, "reason": "", "required_follow-up": ""}
                not_run.append(current)
            elif current is not None and key in current:
                current[key] = value

    return {"ran": ran, "not_run": not_run}


def render_verification_summary(target_root: Path) -> str:
    path = verification_path(target_root)
    if not path.exists():
        return "- verification.md: missing"

    data = parse_verification(target_root)
    lines = [f"- verification.md: present ({len(data['ran'])} ran, {len(data['not_run'])} not-run)"]
    for item in data["ran"][:2]:
        command = item.get("command") or "-"
        result = item.get("result") or "-"
        lines.append(f"- ran: {command} -> {result}")
    for item in data["not_run"][:2]:
        pending = item.get("item") or "-"
        reason = item.get("reason") or "-"
        lines.append(f"- not run: {pending} ({reason})")
    return "\n".join(lines)
