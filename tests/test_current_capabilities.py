from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
CAPABILITIES_PATH = REPO_ROOT / "docs" / "design" / "current-capabilities.md"
RELEASE_CHECKLIST_PATH = REPO_ROOT / "docs" / "release" / "v0.8-release-checklist.md"
USAGE_WALKTHROUGH_PATH = REPO_ROOT / "docs" / "usage" / "walkthrough.md"
TARGET_STRUCTURE_PATH = REPO_ROOT / "docs" / "usage" / "generated-target-structure.md"
README_ZH_PATH = REPO_ROOT / "README.zh-CN.md"


class CurrentCapabilitiesManifestTest(unittest.TestCase):
    def test_command_entrypoints_exist(self) -> None:
        for command in [
            "ai-init",
            "ai-upgrade",
            "ai-status",
            "ai-review",
            "ai-approve",
            "ai-reject",
            "ai-context-pack",
            "ai-handoff",
        ]:
            self.assertTrue((REPO_ROOT / "bin" / command).exists(), command)

    def test_command_and_doc_entrypoints_exist(self) -> None:
        self.assertTrue(RELEASE_CHECKLIST_PATH.exists())
        self.assertTrue(USAGE_WALKTHROUGH_PATH.exists())
        self.assertTrue(TARGET_STRUCTURE_PATH.exists())
        self.assertTrue(README_ZH_PATH.exists())

    def test_readme_current_support_line_matches_phase13_surface(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        support_line = next(
            line for line in readme.splitlines() if line.startswith("Phase 13 currently supports ")
        )
        self.assertIn("ai-init small", support_line)
        self.assertIn("ai-upgrade large", support_line)
        self.assertIn("ai-status", support_line)
        self.assertIn("ai-review diff", support_line)
        self.assertIn("ai-review spec", support_line)
        self.assertIn("ai-review plan", support_line)
        self.assertIn("ai-review final", support_line)
        self.assertIn("ai-approve spec", support_line)
        self.assertIn("ai-approve plan", support_line)
        self.assertIn("ai-approve diff", support_line)
        self.assertIn("ai-approve final", support_line)
        self.assertIn("ai-reject spec", support_line)
        self.assertIn("ai-reject plan", support_line)
        self.assertIn("ai-reject diff", support_line)
        self.assertIn("ai-reject final", support_line)
        self.assertIn("ai-context-pack", support_line)
        self.assertIn("ai-handoff", support_line)

    def test_unimplemented_capabilities_are_marked_not_implemented(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        for command in [
            "subagent execution",
            "skills installation",
            "automatic third-party skill fetching",
        ]:
            self.assertTrue(
                any(command in line and "not implemented" in line for line in readme.splitlines()),
                command,
            )

    def test_readme_and_capabilities_doc_expose_skill_consolidation_contract(self) -> None:
        combined = README_PATH.read_text(encoding="utf-8") + "\n" + CAPABILITIES_PATH.read_text(encoding="utf-8")
        self.assertIn("v1.3-skill-creator-zh-readme", combined)
        self.assertIn("ai-context-pack", combined)
        self.assertIn("ai-handoff", combined)
        self.assertIn("ai-review spec", combined)
        self.assertIn("ai-review plan", combined)
        self.assertIn("ai-review final", combined)
        self.assertIn("ai-approve spec", combined)
        self.assertIn("ai-reject final", combined)
        self.assertIn("does not advance state", combined)
        self.assertIn("enhancement layers", combined)
        self.assertIn("cpp-linux-backend-system", combined)
        self.assertIn("No new CLI commands", combined)
        self.assertIn("subagent role templates", combined)
        self.assertIn("skills templates", combined)
        self.assertIn("maps subagent roles to recommended local skills", combined)
        self.assertIn("provenance", combined)
        self.assertIn("Chinese README", combined)

    def test_readme_does_not_claim_subagent_or_skills_are_implemented(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertNotIn("subagent execution is implemented", readme)
        self.assertNotIn("skills installation is implemented", readme)
        self.assertNotIn("automatic third-party skill fetching is implemented", readme)

    def test_subagent_templates_are_documented_as_optional(self) -> None:
        combined = README_PATH.read_text(encoding="utf-8") + "\n" + CAPABILITIES_PATH.read_text(encoding="utf-8")
        self.assertIn("small mode does not depend on subagents", combined)
        self.assertIn("If subagents are unavailable", combined)

    def test_skill_templates_are_documented_as_optional_local_enhancements(self) -> None:
        combined = (
            README_PATH.read_text(encoding="utf-8")
            + "\n"
            + CAPABILITIES_PATH.read_text(encoding="utf-8")
            + "\n"
            + TARGET_STRUCTURE_PATH.read_text(encoding="utf-8")
        )
        self.assertIn("small mode does not depend on skills", combined)
        self.assertIn("If skills are unavailable", combined)
        self.assertIn("local project-level enhancement templates", combined)
        self.assertIn(".agents/skills/", combined)

    def test_chinese_readme_exposes_current_baseline(self) -> None:
        content = README_ZH_PATH.read_text(encoding="utf-8")
        self.assertIn("v1.3-skill-creator-zh-readme", content)
        self.assertIn("skill-creator", content)
        self.assertIn("仍未实现", content)



if __name__ == "__main__":
    unittest.main()
