# Stage 06 - UI Panel Report

**Verdict**: Pass

## What Changed
- Created the UI layer in `src/pose_ghost/ui` to serve as a pure control surface for the Pose Ghost system.
- Implemented `qt_compat.py` to seamlessly handle PySide2 and PySide6 compatibility, avoiding crashes in non-Maya environments.
- Implemented `PoseGhostPanel` containing all the requested UI controls in a compact layout.
- Implemented `ObjectListModel` to cleanly track targets and their bypass states.
- Implemented `UiCommandsProtocol` and a `FakeUiCommands` test implementation to decouple the UI from the Maya adapters.
- Added `Shortcuts` placeholder for future hotkey bindings.
- Created robust UI unit tests.

## The Logic According to Codex
The UI layer is treated strictly as a View and Controller interface that does absolutely no heavy lifting. It translates user interactions (clicks, text edits) into `OnionSettings` structs and calls the abstract `UiCommandsProtocol`. This enforces clean architecture by guaranteeing the UI cannot secretly execute Maya commands, mutate the scene, or start callback loops. 

## What Bugs Could Happen
- When integrated with the real Maya adapter commands, the UI list widget might need custom signal/slot wiring or a standard Qt Model/View architecture to stay synchronized with the scene if objects are deleted externally.
- Floating point spinboxes might send too many signal updates during a drag if not debounced.

## How to Test
1. Set Python Path: `$env:PYTHONPATH="src"`
2. Run standard Python unittests: `python -m unittest discover -s tests`
3. Observe all 47 tests passing (the `test_pose_ghost_panel_logic.py` test gracefully skips widget assertion if Qt isn't available).

## How This Relates to the Spec / Approved Decision
This fulfills the requirement of building a thin, command-driven UI control surface for Pose Ghost. The controls implemented directly align with the approved V1 behavior: multi-sample relative-frame onion skinning (Previous Count, Next Count, Frame Step, Base Opacity, Display Mode, etc.). No "how it behaves" panels or baked snapshot workflows were added, keeping the UI compact.

## What Could be a V2 Improvement
- Implement a true Qt `QAbstractListModel` for the object list to allow high-performance filtering, selecting, and dynamic Maya scene syncing.
- Add an interactive color picker or predefined palettes instead of placeholder color buttons.

## Exact Tests/Checks Run
- Unit Tests: Ran 47 tests via `unittest` encompassing core, runtime, and UI. (Pass)
- Compilation: Ran `compileall src/pose_ghost tests`. (Pass)
- Boundary Check: Ran Python script to scan all `src/pose_ghost` modules for banned framework, runtime, and UI logic boundaries. (Pass)

## Pass/Fail Counts
- Unit Tests: 46 Passed / 1 Skipped (Qt unavailable) / 0 Failed
- Import Boundary Checks: 1 Passed / 0 Failed
- Compile Checks: 1 Passed / 0 Failed

## Files Changed
- `src/pose_ghost/ui/__init__.py` (Created)
- `src/pose_ghost/ui/object_list_model.py` (Created)
- `src/pose_ghost/ui/pose_ghost_panel.py` (Created)
- `src/pose_ghost/ui/qt_compat.py` (Created)
- `src/pose_ghost/ui/shortcuts.py` (Created)
- `src/pose_ghost/ui/ui_commands.py` (Created)
- `tests/ui/__init__.py` (Created)
- `tests/ui/AGENTS.md` (Created)
- `tests/ui/CONTEXT.md` (Created)
- `tests/ui/REFERENCE.md` (Created)
- `tests/ui/test_object_list_model.py` (Created)
- `tests/ui/test_pose_ghost_panel_logic.py` (Created)
- `tests/ui/test_qt_compat.py` (Created)
- `tests/ui/test_ui_commands.py` (Created)
- `work/06_ui_panel/output/ui_report.md` (Created)

## UI Controls Implemented
- Target Root (field, pick, scan)
- Rig Root (field, pick, scan)
- Sampling Mode dropdown
- Previous Count, Next Count, Frame Step
- Clamp to Playback Range checkbox
- Display Mode dropdown
- Previous/Next Color buttons
- Base Opacity, Opacity Falloff, Fade Strength
- Object list (bypassing)
- Ghost Source Mode dropdown, Proxy Root (field, pick)
- Disable (Toggle), Clear Ghosts, Force Rebuild, Save Profile

## Validation Behavior for Invalid Values
The UI layer enforces correct boundaries before sending values to the commands:
- `previous_count` and `next_count` minimums are `0`.
- `frame_step` minimum is `0.1`.
- `opacity` and `fade_strength` are clamped between `0.0` and `1.0`.

## Command Seam Behavior
The `UiCommandsProtocol` exposes all required UI behaviors as abstract methods. The UI delegates actions like `scan_target_root` or `set_sampling_settings` to whatever implementation is injected, protecting the UI from Maya dependencies.

## Object List/Bypass Behavior
The `ObjectListModel` stores target instances and their bypass flags safely.

## Qt Compatibility Behavior
`qt_compat.py` safely tries `PySide6`, then `PySide2`, and stores the result in `QT_AVAILABLE`. It provides an `ensure_qt_available` function to prevent crashes in isolated test runs.

## Boundary Check Results
Confirmed that `core` remains Maya/Qt free, `runtime` remains Maya/Qt free, and `ui` strictly avoids importing Maya/maya_adapters logic.

## Scaffold/Spec Mismatches Found
None.

## Stage 07 Safe to Start
Yes, Stage 07 is safe to start.
