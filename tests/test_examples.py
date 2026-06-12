from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class ExamplesStructureTest(unittest.TestCase):
    def test_examples_readme_mentions_all_supported_example_types(self) -> None:
        content = (REPO_ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        for item in [
            "small/",
            "large/",
            "cpp-linux-backend-mini/",
            "injected-output-sample/",
        ]:
            self.assertIn(item, content)

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
            ".ai/tech-design.md",
            ".ai/implementation-plan.md",
            ".ai/verification.md",
            ".ai/risk-and-rollback.md",
            ".ai/reviews/README.md",
            ".ai/approvals/README.md",
            ".ai/subagent-packets/README.md",
            ".codex/agents/README.md",
            "docs/ai/tasks/README.md",
            "docs/ai/tasks/init-large/00-prd.md",
            "docs/ai/tasks/init-large/01-spec.md",
            "docs/ai/tasks/init-large/02-tech-design.md",
            "docs/ai/tasks/init-large/03-implementation-plan.md",
        ]:
            self.assertTrue((large / path).exists(), path)

    def test_cpp_linux_backend_mini_contains_expected_business_files(self) -> None:
        sample = REPO_ROOT / "examples" / "cpp-linux-backend-mini"
        for path in [
            "README.md",
            "CMakeLists.txt",
            "include/echo_server.h",
            "src/echo_server.cpp",
            "src/main.cpp",
            "tests/test_echo_server.cpp",
        ]:
            self.assertTrue((sample / path).exists(), path)

    def test_injected_output_sample_contains_expected_post_injection_files(self) -> None:
        sample = REPO_ROOT / "examples" / "injected-output-sample"
        for path in [
            "AGENTS.md",
            "CLAUDE.md",
            ".github/copilot-instructions.md",
            ".ai/state.json",
            ".ai/spec.md",
            ".ai/tech-design.md",
            ".ai/implementation-plan.md",
            ".ai/verification.md",
            ".ai/risk-and-rollback.md",
            "include/server.h",
            "src/server.cpp",
            "tests/test_server.cpp",
            "docs/ai/tasks/README.md",
            "docs/ai/tasks/sample-server-hardening/00-prd.md",
            "docs/ai/tasks/sample-server-hardening/01-spec.md",
            "docs/ai/tasks/sample-server-hardening/02-tech-design.md",
            "docs/ai/tasks/sample-server-hardening/03-implementation-plan.md",
            "docs/ai/tasks/sample-server-hardening/04-diff-review.md",
            "docs/ai/tasks/sample-server-hardening/05-verification.md",
            "docs/ai/tasks/sample-server-hardening/06-risk-and-rollback.md",
            "docs/ai/tasks/sample-server-hardening/07-handoff.md",
        ]:
            self.assertTrue((sample / path).exists(), path)

        state = (sample / ".ai" / "state.json").read_text(encoding="utf-8")
        self.assertIn('"task_id": "sample-server-hardening"', state)
        self.assertIn('"mode": "large"', state)

    def test_examples_do_not_include_runtime_noise(self) -> None:
        for example in [
            REPO_ROOT / "examples" / "small",
            REPO_ROOT / "examples" / "large",
            REPO_ROOT / "examples" / "injected-output-sample",
        ]:
            self.assertFalse((example / ".ai" / "backups").exists())
            self.assertFalse((example / ".ai" / "context-pack.md").exists())
            self.assertFalse((example / ".ai" / "handoff.md").exists())

    def test_injected_output_sample_does_not_contain_copy_artifacts(self) -> None:
        sample = REPO_ROOT / "examples" / "injected-output-sample"
        for path in [
            ".github/.github",
            ".ai/templates/templates",
            "docs/ai/ai",
            "scripts/scripts",
            "docs/ai/tasks/init-large",
        ]:
            self.assertFalse((sample / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
