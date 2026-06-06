# V2.0A Probe Hotfix 01: Plugin-Loaded Check Report

## Verdict: PASS

The false "Plugin not loaded" error in the interactive proof runner is fixed. Visual interactive validation is now unblocked.

## What Changed

1. **`probe_viewport_backend.py`**:
   - Added constant `PLUGIN_NAME = "probe_viewport_backend"`.
   - Added `is_probe_plugin_loaded()` helper to query the actual plugin registry.
   - Updated `run_cube_proof()` to auto-load the plugin via `__file__` if it detects it is not loaded.
   - Fixed a `UnicodeEncodeError` by replacing the `→` character with `->` in print statements.
2. **`test_v2_probe_interactive_load_path.py`** [NEW]:
   - Added a targeted regression test that exactly mirrors the manual UI import/load path.
3. **`probe_interactive_steps.md`**:
   - Updated the manual steps to reflect the clean import path.

## Root Cause of False "Plugin Not Loaded"

`run_cube_proof()` was previously doing this:
```python
cmds.pluginInfo(LOCATOR_TYPE_NAME, query=True, loaded=True)
```
Where `LOCATOR_TYPE_NAME` was `"PoseGhostProbeLocator"`. This is the name of the *node type* the plugin registers, not the name of the *plugin itself* (which is `"probe_viewport_backend"`). Maya's plugin registry returned `False`, causing the script to exit prematurely even though the plugin was successfully loaded.

## The Logic According to Codex

The script now queries `cmds.pluginInfo("probe_viewport_backend")`. Additionally, to make the developer experience smoother, `run_cube_proof()` will attempt to automatically call `cmds.loadPlugin(__file__)` if it finds the plugin isn't loaded but the module has been imported, eliminating a manual step.

## What Bugs Could Happen

- If the file is renamed from `probe_viewport_backend.py` to something else, the hardcoded `PLUGIN_NAME` will mismatch.
- If the module is imported in a way where `__file__` is not resolvable to an absolute path, the auto-load might fail (though the manual load fallback message is preserved).

## How to Test

Run the new automated test:
```bash
mayapy tests/maya_integration/test_v2_probe_interactive_load_path.py
```

## How This Relates to the V2 Probe / Spec

It unblocks the required manual verification step for the V2 Viewport Backend Spike, as defined in the acceptance criteria.

## What Could Be a V2/V3 Improvement

A centralized plugin loader/manager inside `launcher.py` or a dedicated `plugin_manager.py` that handles `loadPlugin` / `unloadPlugin` / `pluginInfo` robustly for the entire Pose Ghost tool, rather than ad-hoc checks in individual files.

## Exact Tests/Checks Run

| Test | Result |
|------|--------|
| `test_v2_probe_interactive_load_path.py` | 3 Pass |
| `probe_api_availability.py` | Pass |
| `test_v2_viewport_backend_probe.py` | 9 Pass |
| `tests/core/` (unittest) | 28 Pass |
| Compile Check | All Pass |
| Boundary Check | No violations |

## Pass/Fail Counts

- **Total Checked**: 40+ Pass / 0 Fail.

## Files Changed (Count: 3)

1. `work/09_v2_viewport_backend_probe/probe_viewport_backend.py` [MODIFIED]
2. `tests/maya_integration/test_v2_probe_interactive_load_path.py` [NEW]
3. `work/09_v2_viewport_backend_probe/probe_interactive_steps.md` [MODIFIED]

## Exact Interactive Command Raz Should Run Next

Copy and paste this directly into the Maya Python Script Editor:

```python
import sys
import maya.cmds as cmds
sys.path.insert(0, r"G:\maya-plugins\Ghost-Maya-plugin")
from work._09_v2_viewport_backend_probe import probe_viewport_backend as pvb
pvb.run_cube_proof()
```

*(Note: The auto-load feature added in this hotfix means you no longer need a separate `cmds.loadPlugin` step — `run_cube_proof()` handles it.)*

## Blockers Status

**Visual interactive validation is UNBLOCKED.**

## Should Stage 10 Wait?

**YES.** Stage 10 (Full V2 Implementation) should continue to wait for Raz’s interactive visual check. The automated tests prove the architecture (nodes, buffers, API calls), but only interactive testing can prove the shaders actually render correctly to the human eye in the Maya viewport.
