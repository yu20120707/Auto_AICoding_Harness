from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class SubagentTemplatesIntegrationTest(unittest.TestCase):
    def run_cmd(self, tmpdir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, *args],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            check=False,
        )

    def prepare_large(self, tmpdir: Path) -> None:
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-init"), "small").returncode, 0)
        self.assertEqual(self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large").returncode, 0)

    def test_large_mode_generates_subagent_role_templates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            for path in [
                ".codex/agents/README.md",
                ".codex/agents/planner.md",
                ".codex/agents/explorer.md",
                ".codex/agents/implementer.md",
                ".codex/agents/reviewer.md",
                ".codex/agents/evaluator.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

    def test_large_mode_generates_subagent_packet_templates(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            for path in [
                ".ai/subagent-packets/README.md",
                ".ai/subagent-packets/planner.md",
                ".ai/subagent-packets/explorer.md",
                ".ai/subagent-packets/implementer.md",
                ".ai/subagent-packets/reviewer.md",
                ".ai/subagent-packets/evaluator.md",
            ]:
                self.assertTrue((tmpdir / path).exists(), path)

    def test_role_templates_contain_key_terms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            self.assertTrue(
                "spec" in (tmpdir / ".codex/agents/planner.md").read_text(encoding="utf-8").lower()
                or "scope" in (tmpdir / ".codex/agents/planner.md").read_text(encoding="utf-8").lower()
            )
            explorer_text = (tmpdir / ".codex/agents/explorer.md").read_text(encoding="utf-8").lower()
            self.assertTrue("call chain" in explorer_text or "affected-files" in explorer_text or "affected files" in explorer_text)
            implementer_text = (tmpdir / ".codex/agents/implementer.md").read_text(encoding="utf-8").lower()
            self.assertTrue("minimal" in implementer_text or "scope" in implementer_text)
            reviewer_text = (tmpdir / ".codex/agents/reviewer.md").read_text(encoding="utf-8").lower()
            self.assertTrue("diff" in reviewer_text or "api/abi" in reviewer_text)
            evaluator_text = (tmpdir / ".codex/agents/evaluator.md").read_text(encoding="utf-8").lower()
            self.assertTrue("test" in evaluator_text or "verification" in evaluator_text)
            readme_text = (tmpdir / ".codex/agents/README.md").read_text(encoding="utf-8").lower()
            self.assertTrue("optional" in readme_text or "enhancement" in readme_text)

    def test_packet_templates_contain_context_and_skill_terms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            expectations = {
                "planner.md": ["Required Context", "task-contract-and-leveling", "Return Format"],
                "explorer.md": ["Required Context", "context-engineering", "Stop Conditions"],
                "implementer.md": ["Forbidden Actions", "verification-before-completion", "cpp-linux-system-engineering"],
                "reviewer.md": ["Expected Output", "code-review-and-quality", "verification_gaps"],
                "evaluator.md": ["recommended_final_claim", "verification-before-completion", "performance-analysis"],
            }

            for filename, terms in expectations.items():
                content = (tmpdir / ".ai" / "subagent-packets" / filename).read_text(encoding="utf-8")
                for term in terms:
                    self.assertIn(term, content, filename)

    def test_default_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            planner = tmpdir / ".codex" / "agents" / "planner.md"
            planner.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ALREADY_LARGE", result.stdout)
            self.assertIn("SKIPPED .codex/agents/planner.md", result.stdout)
            self.assertEqual(planner.read_text(encoding="utf-8"), "user modified\n")

    def test_packet_templates_default_do_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            packet = tmpdir / ".ai" / "subagent-packets" / "planner.md"
            packet.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ALREADY_LARGE", result.stdout)
            self.assertIn("SKIPPED .ai/subagent-packets/planner.md", result.stdout)
            self.assertEqual(packet.read_text(encoding="utf-8"), "user modified\n")

    def test_force_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            reviewer = tmpdir / ".codex" / "agents" / "reviewer.md"
            reviewer.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .codex/agents/reviewer.md", result.stdout)

            backups = [
                path
                for path in (tmpdir / ".ai" / "backups").rglob("reviewer.md")
                if ".codex" in path.parts and "agents" in path.parts
            ]
            self.assertTrue(backups, "expected reviewer template backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))

    def test_packet_force_backs_up_and_overwrites(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)
            packet = tmpdir / ".ai" / "subagent-packets" / "reviewer.md"
            packet.write_text("user modified\n", encoding="utf-8")

            result = self.run_cmd(tmpdir, str(REPO_ROOT / "bin" / "ai-upgrade"), "large", "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("OVERWRITTEN .ai/subagent-packets/reviewer.md", result.stdout)

            backups = [
                path
                for path in (tmpdir / ".ai" / "backups").rglob("reviewer.md")
                if "subagent-packets" in path.parts
            ]
            self.assertTrue(backups, "expected packet backup")
            self.assertIn("user modified", backups[0].read_text(encoding="utf-8"))
            self.assertIn("Reviewer Packet", packet.read_text(encoding="utf-8"))

    def test_current_capabilities_are_synced(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        capabilities = (REPO_ROOT / "docs/design/current-capabilities.md").read_text(encoding="utf-8")
        combined = readme + "\n" + capabilities

        self.assertIn("v1.6-subagent-packets", combined)
        self.assertIn("subagent role templates", combined)
        self.assertIn("subagent task packet", combined)
        self.assertIn("subagent execution", combined)

    def test_role_templates_reference_global_skill_guidance_without_hard_dependency(self) -> None:
        with tempfile.TemporaryDirectory(prefix="auto-ai-harness-") as tmp:
            tmpdir = Path(tmp)
            self.prepare_large(tmpdir)

            expectations = {
                "planner.md": ["karpathy-guidelines", "task-contract-and-leveling", "context-engineering"],
                "explorer.md": ["context-engineering", "systematic-debugging"],
                "implementer.md": ["karpathy-guidelines", "cpp-linux-system-engineering", "verification-before-completion"],
                "reviewer.md": ["code-review-and-quality", "cpp-linux-system-engineering"],
                "evaluator.md": ["verification-before-completion", "performance-analysis"],
            }

            for filename, skills in expectations.items():
                content = (tmpdir / ".codex" / "agents" / filename).read_text(encoding="utf-8")
                self.assertIn("Skill Guidance", content)
                self.assertIn("Skills are globally installed advisory guidance", content)
                self.assertIn("If skills are unavailable", content)
                for skill in skills:
                    self.assertIn(skill, content, filename)


if __name__ == "__main__":
    unittest.main()
