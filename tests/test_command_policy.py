from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.command_policy import COMMAND_POLICIES, CommandPermission, get_command_policy


class CommandPolicyTest(unittest.TestCase):
    def test_known_command_policies_are_classified(self) -> None:
        self.assertEqual(get_command_policy("ai-status").permission, CommandPermission.READ_ONLY)
        self.assertEqual(get_command_policy("ai-doctor").permission, CommandPermission.READ_ONLY)
        self.assertEqual(get_command_policy("ai-context-pack").permission, CommandPermission.GENERATE_ARTIFACT)
        self.assertEqual(get_command_policy("ai-review").permission, CommandPermission.WORKFLOW_TRANSITION)
        self.assertEqual(get_command_policy("ai-upgrade").permission, CommandPermission.REQUIRES_USER_APPROVAL)
        self.assertEqual(get_command_policy("ai-approve").permission, CommandPermission.REQUIRES_USER_APPROVAL)

    def test_command_policy_table_has_unique_command_names(self) -> None:
        names = [policy.command for policy in COMMAND_POLICIES]
        self.assertEqual(len(names), len(set(names)))

    def test_system_global_agents_exists(self) -> None:
        path = REPO_ROOT / "system" / "AGENTS.global.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("Command Protocol", text)
        self.assertIn("ai-upgrade", text)


if __name__ == "__main__":
    unittest.main()
