# Stage 03 - Core Logic Report

**Verdict**: Pass

## What Changed
- Implemented pure Python core business logic for Pose Ghost, focusing strictly on deterministic onion-skin sample planning.
- Added data models: `OnionSettings`, `DisplayMode`, `OnionSample`, `SamplePlan`, `TargetObject`, `GhostState`.
- Added logic components: `RelativeFrameSampler`, `OpacityFalloff`, and a placeholder for `KeyedPoseSampler`.
- Created a clean `__init__.py` to export the public core API cleanly.
- Wrote unit tests for all components under `tests/core/`.

## The Logic According to Codex
The core package serves as the "policy" in clean architecture. It knows nothing about Maya or Qt. It only answers questions like "Given current frame 30 and these settings, what frames do we need ghosts for, and what should their opacities be?" `RelativeFrameSampler` implements the math for calculating these frames based on step, count, and display mode parameters. `GhostState` provides a safe boundary to check if new settings/time changes actually warrant a heavy rebuild. The core does not execute rebuilds; it only defines when they are logically necessary.

## What Bugs Could Happen
- If invalid settings bypass the dataclass `__post_init__` normalization (e.g., direct mutation without property setters), negative frame counts or invalid frame steps could cause unexpected looping behavior or empty plans.
- Float comparison for frames might hit precision issues if sub-frame sampling logic is introduced without appropriate `math.isclose` checks. Currently, standard floats are used for frame numbers.

## How to Test
1. Set Python Path: `$env:PYTHONPATH="src"`
2. Run standard Python unittests: `python -m unittest discover -s tests/core`
3. Observe all 22 tests passing.

## How This Relates to the Spec / Approved Decision
This enforces the clean architecture policy (core logic must remain independent of external frameworks). The tests prove the core can run in standard Python. This also directly follows the Superhive reference behavior, supporting multi-sample relative-frame onion skinning (previous/next counts, variable frame steps, clamp, and opacity falloff).

## What Could be a V2 Improvement
- In a V2 C++ integration, we might want to mirror this logic struct in C++ or use a robust Python C-API wrapper to evaluate frames directly within the DAG evaluation cycle.
- Add strict type enforcement (e.g., Pydantic) to `OnionSettings` to prevent invalid states via direct attribute mutation.

## Exact Tests/Checks Run
- Unit Tests: Ran 22 tests via `unittest`. (Pass)
- Compilation: Ran `compileall src/pose_ghost tests`. (Pass)
- Boundary Check: Ran Python script to scan all `src/pose_ghost/core` files for `maya`, `maya.cmds`, `maya.api`, `PySide2/6`, `Qt`, `pose_ghost.maya_adapters`, `pose_ghost.runtime`, `pose_ghost.ui`. (Pass)

## Pass/Fail Counts
- Unit Tests: 22 Passed / 0 Failed
- Import Boundary Checks: 1/1 Passed
- Compile Checks: 1/1 Passed

## Files Changed
- `src/pose_ghost/core/__init__.py` (Updated)
- `src/pose_ghost/core/display_mode.py` (Created)
- `src/pose_ghost/core/ghost_state.py` (Created)
- `src/pose_ghost/core/keyed_pose_sampler.py` (Created)
- `src/pose_ghost/core/onion_sample.py` (Created)
- `src/pose_ghost/core/onion_settings.py` (Created)
- `src/pose_ghost/core/opacity_falloff.py` (Created)
- `src/pose_ghost/core/relative_frame_sampler.py` (Created)
- `src/pose_ghost/core/sample_plan.py` (Created)
- `src/pose_ghost/core/target_object.py` (Created)
- `tests/core/test_display_mode.py` (Created)
- `tests/core/test_ghost_state.py` (Created)
- `tests/core/test_opacity_falloff.py` (Created)
- `tests/core/test_relative_frame_sampler.py` (Created)
- `tests/core/test_sample_plan.py` (Created)
- `work/03_core_logic/output/core_logic_report.md` (Created)

## Confirmation of No Unauthorized Imports
Confirmed. An automated script scanned all python files in `src/pose_ghost/core` and found zero imports from Maya, Qt, runtime, or other non-core components.

## Scaffold/Spec Mismatches Found
None. The required implementation aligned perfectly with the product target. The "keyed pose" behavior remains a simple placeholder as explicitly required, with the "relative frame" being the primary V1 behavior.

## Stage 04 Safe to Start
Yes, Stage 04 is safe to start.
