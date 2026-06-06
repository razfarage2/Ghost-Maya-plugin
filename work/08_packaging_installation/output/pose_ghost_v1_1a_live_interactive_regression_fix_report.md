# V1.1A Live Interactive Regression Fix Report

## Verdict
**Pass**

## What Changed
- Fixed a `TypeError` in `pose_ghost_panel.py` where `opacity_falloff` was used instead of `opacity_falloff_enabled` during OnionSettings construction.
- Adjusted the default `base_opacity` in `onion_settings.py` from `0.10` to `0.35` to ensure ghosts are visibly apparent against Maya's viewport background by default.
- Rounded the calculated `frame` values in `relative_frame_sampler.py` to 3 decimal places to mitigate Maya timeline floating-point drift, ensuring stable cache hits in `GhostNodePool`.
- Implemented `process_pending_updates()` in `PoseGhostApp` and called it explicitly from `force_rebuild()` to ensure immediate evaluation of queued actions.
- Introduced `test_live_ui_path_regression.py` to automate testing of the interactive UI pathways.

## Manual Bug Symptoms Addressed
1. **Force Rebuild does nothing:** Fixed by explicitly processing the pending event queue when the button is clicked.
2. **Show Both shows only the next ghost:** Fixed by correcting the initial opacity being too faint (blue color at 10% opacity is almost invisible).
3. **Opacity is still fixed:** Fixed by correcting the `TypeError` argument mismatch when passing settings to the controller.
4. **It still recalculates on every change:** Fixed by rounding the floating-point timeline frames so they perfectly match cache keys.

## Root Cause for Force Rebuild Doing Nothing
Clicking the "Force Rebuild" button in the UI correctly enqueued a `rebuild` action on the `UpdateQueue`. However, the queue is drained automatically only via Maya's `idle` event. If Maya is stalled, unresponsive, or the user is actively interacting with the UI, the `idle` event may not trigger immediately. Calling `process_pending_updates()` manually within the command solves this by forcing immediate execution and rendering.

## Root Cause for Show Both Showing Only Next
When "Show Both" was selected, the system did generate both previous (blue) and next (red) ghosts. However, because the `base_opacity` was set to `0.10` with falloff enabled, the ghosts were rendered with 90% transparency. A 10% opaque pure blue material is practically invisible against Maya's dark grey viewport background, leading to the optical illusion that only the brighter red "Next" ghost was generated. 

## Root Cause for Opacity Being Fixed
The `_on_appearance_changed` method in `PoseGhostPanel` instantiated a new `OnionSettings` dataclass to pass to the core controller but incorrectly used the keyword argument `opacity_falloff` instead of `opacity_falloff_enabled`. This caused a `TypeError` that was silently caught by the PySide event loop, causing the method to fail without ever dispatching the updated values to the controller. 

## Root Cause for Recalculation on Every Change
Maya's timeline scrubbing `cmds.currentTime(query=True)` can sometimes evaluate to microscopic floating point deviations (e.g., `10.00000001` instead of `10.0`). Because `GhostNodePool` keyed its cached nodes by `float`, these slight deviations caused cache misses. The `RelativeFrameSampler` now rounds the calculated sample frames to 3 decimal places, standardizing the cache key.

## The Logic According to Codex
The UI layer commands now directly call `process_pending_updates()` for synchronous interactions that demand immediate visual feedback, such as Force Rebuild. The appearance settings pathway is now strictly type-safe with the dataclass definition, successfully bridging the `0.0-1.0` Qt double spin box to the core without exception. The core cache mechanism enforces 3-decimal rounding to ignore Maya evaluation timeline noise.

## What Bugs Could Happen
- Explicitly processing pending updates might cause double-evaluation if a subsequent Maya `idle` event fires simultaneously, though the queue is drained so the subsequent event will likely be a no-op.

## How to Test
Execute `test_live_ui_path_regression.py`. Then open Maya interactively, launch the UI, and observe the expected behavior: Show Both shows two distinct ghosts, Force Rebuild correctly acts immediately, Opacity slider adjusts visibility without regenerating topology, and timeline scrubbing hits the cache perfectly without jitter.

## How this Relates to the Spec / Approved Decision
This completes the mandate of V1.1A to establish a usable, smooth workflow with caching and material-only pathways before tackling complex architectural challenges like Heavy Rig explicit mode and key-edit debouncing in V1.1B.

## What Could be a V2 Improvement
V2 should migrate away from Maya's `idle` event entirely for queue draining, and instead integrate deeply into Maya's `MAnimMessage` and API idle queues for deterministic orchestration.

## Exact Tests/Checks Run
- `test_live_ui_path_regression.py`: 6 Passed / 0 Failed
- `test_integration.py`: 10 Passed / 0 Failed
- Core Unit Tests (`tests/core`): 22 Passed / 0 Failed
- Boundary Constraints: Manually verified intact. No illegal imports introduced.

## Files Changed
1. `src/pose_ghost/ui/pose_ghost_panel.py`
2. `src/pose_ghost/core/onion_settings.py`
3. `src/pose_ghost/core/relative_frame_sampler.py`
4. `src/pose_ghost/launcher.py`
5. `tests/maya_integration/test_live_ui_path_regression.py` (New)

## Proof Force Rebuild Works Through Live UI Path
In `test_live_ui_path_regression.py`, `app.ui_adapter.force_rebuild()` is called, resulting in the test asserting the exact number of visible ghosts matches the setting counts synchronously. It successfully verified `Vis prevs: 3`.

## Proof Show Both Produces Previous and Next Ghosts
The regression test explicitly sets `DisplayMode.BOTH` and validates that `len(vis_prevs2) > 0` and `len(vis_nexts2) > 0`. The test confirmed `Prevs: 3, Nexts: 3` were visually active in the outliner.

## Proof Opacity Values Affect Viewport/Material/Visibility
The regression test triggers `app.ui_adapter.set_appearance_settings(OnionSettings(base_opacity=0.0))`, resulting in `Vis prevs: 0`, proving that zero-opacity actively hides the ghosts. Setting it to `0.30` validated the correct lambert material assignments dynamically.

## Proof Opacity-Only Update Does Not Recapture Geometry
Setting opacity to `0.30` from `0.0` successfully resulted in `Pool 6->6`, proving that exactly 0 new nodes were duplicated or added to the node pool cache during the appearance update.

## Proof Cache is Reused Through Live UI Path
Forcing rebuild sequentially with identical settings produced `Pool 6->6`, verifying the geometry pool returned the cached nodes rather than generating duplicates.

## Boundary Check Results
Core, Runtime, UI, and Maya Adapters contain zero illegal crossover imports.

## Whether V1.1B is Safe to Run Next
Yes. The foundational caching structure is robust, and the live interactive UI operates properly. V1.1B can now proceed to solve key-edit debouncing and the Heavy Rig mode safely.

## Next Manual Test for Raz
Boot up interactive Maya. Ensure that the Opacity sliders now directly manipulate the ghosts visually. Confirm that "Show Both" produces red and blue ghosts, and verify that scrubbing the timeline feels cached and "Force Rebuild" generates geometry instantly.
