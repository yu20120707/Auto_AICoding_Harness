from __future__ import annotations

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
CAPABILITIES_PATH = REPO_ROOT / "docs" / "design" / "current-capabilities.md"
RELEASE_CHECKLIST_PATH = REPO_ROOT / "docs" / "release" / "v0.8-release-checklist.md"
USAGE_WALKTHROUGH_PATH = REPO_ROOT / "docs" / "usage" / "walkthrough.md"
TARGET_STRUCTURE_PATH = REPO_ROOT / "docs" / "usage" / "generated-target-structure.md"


class CurrentCapabilitiesManifestTest(unittest.TestCase):
    def test_command_entrypoints_exist(self) -> None:
        for command in [
            "ai-install-skills",
            "ai-init",
            "ai-upgrade",
            "ai-doctor",
            "ai-status",
            "ai-state",
            "ai-dispatch",
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
        self.assertTrue((REPO_ROOT / "docs" / "design" / "architecture.md").exists())
        self.assertTrue((REPO_ROOT / "docs" / "design" / "decision-records.md").exists())
        self.assertFalse((REPO_ROOT / "README.zh-CN.md").exists())

    def test_readme_exposes_phase16_command_surface(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        for command in [
            "ai-install-skills",
            "ai-init small",
            "ai-init medium",
            "ai-upgrade medium",
            "ai-upgrade large",
            "ai-status",
            "ai-doctor",
            "ai-state",
            "ai-dispatch",
            "ai-review spec / plan / diff / final",
            "ai-approve spec / plan / diff / final",
            "ai-reject spec / plan / diff / final",
            "ai-context-pack",
            "ai-handoff",
        ]:
            self.assertIn(command, readme)

    def test_unimplemented_capabilities_are_marked_not_implemented(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("仍未实现", readme)
        for command in [
            "subagent execution",
            "automatic third-party skill fetching",
        ]:
            self.assertIn(command, readme)

    def test_readme_and_capabilities_doc_expose_skill_consolidation_contract(self) -> None:
        combined = README_PATH.read_text(encoding="utf-8") + "\n" + CAPABILITIES_PATH.read_text(encoding="utf-8")
        self.assertIn("v1.7-optimization-hardening", combined)
        self.assertIn("ai-context-pack", combined)
        self.assertIn("ai-handoff", combined)
        self.assertIn("ai-state", combined)
        self.assertIn("ai-dispatch", combined)
        self.assertIn("workflow.md", combined)
        self.assertIn("verification.md", combined)
        self.assertIn("ai-review spec", combined)
        self.assertIn("ai-review plan", combined)
        self.assertIn("ai-review final", combined)
        self.assertIn("ai-approve spec", combined)
        self.assertIn("ai-reject final", combined)
        self.assertIn("supports `medium` as a bounded execution level", combined)
        self.assertIn("docs/ai/tasks/<task-id>/", combined)
        self.assertIn("does not advance state", combined)
        self.assertIn("enhancement templates", combined)
        self.assertIn("cpp-linux-backend-system", combined)
        self.assertIn("ai-install-skills", combined)
        self.assertIn("subagent role templates", combined)
        self.assertIn("global skills", combined)
        self.assertIn("global/AGENTS.md.template", combined)
        self.assertIn("repo-onboarding-analysis", combined)
        self.assertIn("maps large-mode subagent roles to recommended global skills", combined)
        self.assertIn("canonical dispatch log", combined)
        self.assertIn("subagent task packet", combined)
        self.assertIn(".ai/subagent-packets/", combined)
        self.assertIn("role-to-skill mapping", combined)
        self.assertIn("provenance", combined)
        self.assertIn("single Chinese", combined)
        self.assertIn("optimization-roadmap.md", combined)

    def test_readme_does_not_claim_subagent_or_skills_are_implemented(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertNotIn("subagent execution is implemented", readme)
        self.assertNotIn("automatic third-party skill fetching is implemented", readme)

    def test_subagent_templates_are_documented_as_optional(self) -> None:
        combined = README_PATH.read_text(encoding="utf-8") + "\n" + CAPABILITIES_PATH.read_text(encoding="utf-8")
        self.assertIn("small mode does not depend on subagents", combined)
        self.assertIn("If subagents are unavailable", combined)
        self.assertIn("prompt/context artifacts", combined)

    def test_global_skills_are_documented_as_explicit_installation(self) -> None:
        combined = (
            README_PATH.read_text(encoding="utf-8")
            + "\n"
            + CAPABILITIES_PATH.read_text(encoding="utf-8")
            + "\n"
            + TARGET_STRUCTURE_PATH.read_text(encoding="utf-8")
        )
        self.assertIn("small mode does not depend on skills at command runtime", combined)
        self.assertIn("If skills are not installed", combined)
        self.assertIn("portable skill", combined)
        self.assertIn("ai-install-skills", combined)

    def test_single_chinese_readme_exposes_current_baseline(self) -> None:
        content = README_PATH.read_text(encoding="utf-8")
        self.assertIn("v1.7-optimization-hardening", content)
        self.assertIn("skill 创建", content)
        self.assertIn("仍未实现", content)

    def test_bootstrap_and_adapter_docs_exist(self) -> None:
        for path in [
            "system/AGENTS.global.md",
            "global/AGENTS.md.template",
            "prompts/bootstrap-local-agent.md",
            "docs/install-targets.md",
            "docs/design/platform-adapters.md",
            "docs/design/task-levels-and-delegation.md",
            "docs/design/subagent-packets.md",
            "core/profile.py",
            "profiles/cpp-linux-backend-system/profile.yaml",
            "schemas/profile.schema.json",
        ]:
            self.assertTrue((REPO_ROOT / path).exists(), path)

        combined = "\n".join(
            (REPO_ROOT / path).read_text(encoding="utf-8")
            for path in [
                "system/AGENTS.global.md",
                "global/AGENTS.md.template",
                "prompts/bootstrap-local-agent.md",
                "docs/install-targets.md",
                "docs/design/platform-adapters.md",
                "docs/design/task-levels-and-delegation.md",
                "docs/design/subagent-packets.md",
            ]
        )
        self.assertIn("docs/ai/*", combined)
        self.assertIn("AGENTS.md", combined)
        self.assertIn("simple, medium, or complex", combined)
        self.assertIn("Subagent task packets", combined)



if __name__ == "__main__":
    unittest.main()
