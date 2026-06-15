from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.template import TemplateFile  # noqa: E402
from core.template_update import (  # noqa: E402
    build_template_hash_manifest,
    plan_template_update,
    render_template_update_plan,
    sha256_bytes,
)


class TemplateUpdateUnitTest(unittest.TestCase):
    def test_plan_detects_unchanged_user_modified_and_deleted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            root = Path(tmp)
            source_dir = root / "source"
            target_dir = root / "target"
            source_dir.mkdir()
            target_dir.mkdir()
            unchanged_source = source_dir / "AGENTS.md"
            modified_source = source_dir / "CLAUDE.md"
            deleted_source = source_dir / "scripts" / "ai_check.sh"
            deleted_source.parent.mkdir()
            unchanged_source.write_bytes(b"new agents\n")
            modified_source.write_bytes(b"new claude\n")
            deleted_source.write_bytes(b"new check\n")
            (target_dir / "AGENTS.md").write_bytes(b"old agents\n")
            (target_dir / "CLAUDE.md").write_bytes(b"user modified\n")
            (target_dir / "scripts").mkdir()
            previous = {
                "files": [
                    {"path": "AGENTS.md", "sha256": sha256_bytes(b"old agents\n")},
                    {"path": "CLAUDE.md", "sha256": sha256_bytes(b"old claude\n")},
                    {"path": "scripts/ai_check.sh", "sha256": sha256_bytes(b"old check\n")},
                ]
            }
            template_files = [
                TemplateFile(unchanged_source, Path("AGENTS.md")),
                TemplateFile(modified_source, Path("CLAUDE.md")),
                TemplateFile(deleted_source, Path("scripts") / "ai_check.sh"),
            ]

            plan = plan_template_update(target_root=target_dir, template_files=template_files, previous_manifest=previous)

            states = {item.path: (item.state, item.action) for item in plan}
            self.assertEqual(states["AGENTS.md"], ("unchanged", "update"))
            self.assertEqual(states["CLAUDE.md"], ("user-modified", "conflict"))
            self.assertEqual(states["scripts/ai_check.sh"], ("user-deleted", "skip"))
            self.assertIn("CLAUDE.md: user-modified -> conflict", render_template_update_plan(plan))


class TemplateHashIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([PYTHON, *args], cwd=tmpdir, capture_output=True, text=True, check=False)

    def test_ai_init_writes_template_hash_and_migration_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((tmpdir / ".ai" / "template-hashes.json").exists())
            self.assertTrue((tmpdir / "docs" / "ai" / "migrations" / "index.md").exists())
            self.assertIn(".ai/template-hashes.json", result.stdout)
            self.assertIn("docs/ai/migrations/index.md", result.stdout)

    def test_manifest_builder_hashes_templates(self) -> None:
        manifest = build_template_hash_manifest(REPO_ROOT, "cpp-linux-backend-system", ["base/root"])

        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["profile"], "cpp-linux-backend-system")
        self.assertTrue(manifest["files"])
        self.assertTrue(all("sha256" in item for item in manifest["files"]))


if __name__ == "__main__":
    unittest.main()
