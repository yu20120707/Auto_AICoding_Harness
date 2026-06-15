# Diff Review

## Status

WAITING_HUMAN_DIFF_APPROVAL

## Git Status

```text
 M bin/ai-status
?? .codegraph/
?? .reasonix/
?? core/task_state.py
?? docs/ai/
?? docs/design/trellis-inspired-v1.7-hardening.md
?? scripts/ai_check.sh
?? tests/test_task_state.py
```

## Diff Stat

```text
 bin/ai-status | 5 +++++
 1 file changed, 5 insertions(+)
```

## Changed Files

```text
bin/ai-status
```

## Diff

```diff
diff --git a/bin/ai-status b/bin/ai-status
index b9414bf..398c6f1 100644
--- a/bin/ai-status
+++ b/bin/ai-status
@@ -13,6 +13,7 @@ if str(REPO_ROOT) not in sys.path:
 from core.state import STATE_RELATIVE_PATH, load_state
 from core.state_machine import next_action_for_state, validate_state_dict
 from core.task_chain import task_dir_relative_path
+from core.task_state import load_active_task_supplement, summarize_task_supplement
 
 
 def present(path: Path) -> str:
@@ -79,6 +80,10 @@ def main() -> int:
                         else f"absent ({task_dir_relative_path(state).as_posix()})"
                     )
                 )
+                task_supplement = load_active_task_supplement(target_root, state)
+                if task_supplement is not None:
+                    for line in summarize_task_supplement(task_supplement):
+                        print(line)
         print(f"next_action: {next_action_for_state(state) if not validation_errors else 'Run ai-doctor to inspect the invalid state.'}")
         return 0
     except Exception as exc:
```

## Scope Check

* [ ] Only expected files changed
* [ ] No unrelated formatting
* [ ] No generated/runtime files accidentally committed
* [ ] No public API change unless approved
* [ ] No large hidden refactor

## C++ / System Risk Check

* [ ] Ownership/lifetime safe
* [ ] Error handling complete
* [ ] No data race introduced
* [ ] API/ABI compatibility checked
* [ ] Timeout/retry semantics unchanged or explained
* [ ] Tests updated or not required with reason

## Human Decision

* [ ] Approved
* [ ] Needs fix
* [ ] Needs replan
* [ ] Rejected

## Human Notes
