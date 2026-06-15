from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.safe_write import safe_write_bytes


class SafeWriteTest(unittest.TestCase):
    def test_parent_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            target_root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "parent path segments are not allowed"):
                safe_write_bytes(
                    target_root=target_root,
                    relative_path=Path("docs") / "ai" / ".." / ".." / ".." / "outside.txt",
                    content=b"bad\n",
                    force=False,
                )

    def test_allowlist_bypass_with_parent_segments_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            target_root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "parent path segments are not allowed"):
                safe_write_bytes(
                    target_root=target_root,
                    relative_path=Path("docs") / "ai" / ".." / ".." / "AGENTS.md",
                    content=b"bad\n",
                    force=False,
                )

    def test_force_overwrite_creates_backup_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            target_root = Path(tmp)
            relative_path = Path("AGENTS.md")

            safe_write_bytes(
                target_root=target_root,
                relative_path=relative_path,
                content=b"before\n",
                force=False,
            )
            result = safe_write_bytes(
                target_root=target_root,
                relative_path=relative_path,
                content=b"after\n",
                force=True,
                timestamp="20260612-120000",
            )

            self.assertEqual(result.action, "OVERWRITTEN")
            manifest_path = target_root / ".ai" / "backups" / "20260612-120000" / "manifest.json"
            self.assertTrue(manifest_path.exists())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            entries = manifest.get("writes") or manifest.get("entries") or []
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["path"], "AGENTS.md")

    def test_symlink_escape_is_rejected_when_supported(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            target_root = Path(tmp)
            outside_dir = target_root.parent / f"{target_root.name}-outside"
            outside_dir.mkdir(parents=True, exist_ok=True)
            link_path = target_root / "docs" / "ai"
            link_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                link_path.symlink_to(outside_dir, target_is_directory=True)
            except OSError:
                self.skipTest("symlink creation is not available in this environment")

            with self.assertRaisesRegex(ValueError, "path escapes target root"):
                safe_write_bytes(
                    target_root=target_root,
                    relative_path=Path("docs") / "ai" / "escaped.md",
                    content=b"bad\n",
                    force=False,
                )


if __name__ == "__main__":
    unittest.main()
