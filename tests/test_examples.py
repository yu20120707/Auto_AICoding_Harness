from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class ExamplesStructureTest(unittest.TestCase):
    def test_small_example_contains_expected_init_output(self) -> None:
        small = REPO_ROOT / "examples" / "small"
        for path in [
            "AGENTS.md",
            "CLAUDE.md",
            ".github/copilot-instructions.md",
            ".ai/state.json",
            ".ai/templates/README.md",
            "docs/ai/README.md",
            "docs/ai/workflow.md",
            "docs/ai/verification-matrix.md",
            "scripts/ai_check.sh",
        ]:
            self.assertTrue((small / path).exists(), path)

    def test_large_example_contains_expected_upgrade_output(self) -> None:
        large = REPO_ROOT / "examples" / "large"
        for path in [
            ".ai/epic.md",
            ".ai/spec.md",
            ".ai/implementation-plan.md",
            ".ai/verification.md",
            ".ai/reviews/README.md",
            ".ai/approvals/README.md",
            ".ai/subagent-packets/README.md",
            ".codex/agents/README.md",
        ]:
            self.assertTrue((large / path).exists(), path)

    def test_examples_do_not_include_runtime_noise(self) -> None:
        for example in [REPO_ROOT / "examples" / "small", REPO_ROOT / "examples" / "large"]:
            self.assertFalse((example / ".ai" / "backups").exists())
            self.assertFalse((example / ".ai" / "context-pack.md").exists())
            self.assertFalse((example / ".ai" / "handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
