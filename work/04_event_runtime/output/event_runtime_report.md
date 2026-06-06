# Stage 04 - Event Runtime Report

**Verdict**: Pass

## What Changed
- Created the runtime orchestration layer in `src/pose_ghost/runtime` with all necessary sub-modules (`controller.py`, `update_queue.py`, `callback_registry.py`, `lifecycle.py`, `composition_root.py`, `event_router.py`).
- Implemented `tests/runtime` tests for all the above modules.
- Defined generic event types instead of coupling the system to Maya's internal callback objects.
- Implemented robust controller logic with playback suppression, dirty-state queuing, internal time-guard toggles, and safe enqueuing.

## The Logic According to Codex
The runtime layer exists solely to orchestrate messages. When the environment (like Maya) triggers a callback, the event router sends a generic Python message to the controller. The controller decides if a rebuild is necessary using the `core` layer's rules (`GhostState` and `RelativeFrameSampler`). If a rebuild is needed, it posts an action to the `UpdateQueue`. This guarantees we avoid Maya's infamous "callback storms" because the queue debounces requests, and the renderer (Stage 05) will only process the most recent `GhostState`.

## What Bugs Could Happen
- If the renderer crashes or fails to drain the queue properly, stale `GhostState` requests could linger.
- If Maya doesn't fire a `PlaybackStoppedEvent` properly (e.g., due to an exception or weird API quirk), the system might stay in a suspended `_is_playing` state indefinitely.
- The `UpdateQueue` only holds one pending request. If we introduce different types of actions besides "rebuild" and "clear", they might overwrite each other improperly unless the queue expands to be a list or priority queue.

## How to Test
1. Set Python Path: `$env:PYTHONPATH="src"`
2. Run standard Python unittests: `python -m unittest discover -s tests`
3. Observe all 41 tests passing (including both core and runtime).

## How This Relates to the Spec / Approved Decision
This fulfills the architectural mandate to isolate runtime orchestration from Maya APIs. The requirements explicitly banned polling loops; we successfully built an event-driven queue. It matches the multi-sample relative-frame onion skinning pattern since the `Controller` requests plans specifically from the core logic built in Stage 03.

## What Could be a V2 Improvement
- A full publish/subscribe event bus (e.g., using `rxpy` or a custom pubsub) could decouple the `Controller` from direct method calls entirely, making it easier to attach multiple observers (like UI panels).
- The UpdateQueue could implement a background worker thread with thread-safe locks, allowing the renderer to compute heavy meshes asynchronously (provided Maya's API thread safety permits).

## Exact Tests/Checks Run
- Unit Tests: Ran 41 tests via `unittest` encompassing core and runtime. (Pass)
- Compilation: Ran `compileall src/pose_ghost tests`. (Pass)
- Boundary Check: Ran Python script to scan all `src/pose_ghost/runtime` and `src/pose_ghost/core` files for banned framework and adapter imports. (Pass)

## Pass/Fail Counts
- Unit Tests: 41 Passed / 0 Failed
- Import Boundary Checks: 1 Passed / 0 Failed
- Compile Checks: 1 Passed / 0 Failed

## Files Changed
- `src/pose_ghost/runtime/__init__.py` (Created)
- `src/pose_ghost/runtime/callback_registry.py` (Created)
- `src/pose_ghost/runtime/composition_root.py` (Created)
- `src/pose_ghost/runtime/controller.py` (Created)
- `src/pose_ghost/runtime/event_router.py` (Created)
- `src/pose_ghost/runtime/lifecycle.py` (Created)
- `src/pose_ghost/runtime/update_queue.py` (Created)
- `tests/runtime/__init__.py` (Created)
- `tests/runtime/AGENTS.md` (Created)
- `tests/runtime/CONTEXT.md` (Created)
- `tests/runtime/REFERENCE.md` (Created)
- `tests/runtime/test_callback_registry.py` (Created)
- `tests/runtime/test_controller.py` (Created)
- `tests/runtime/test_event_router.py` (Created)
- `tests/runtime/test_lifecycle.py` (Created)
- `tests/runtime/test_update_queue.py` (Created)
- `work/04_event_runtime/output/event_runtime_report.md` (Created)

## Boundary Confirmation
- **Runtime Clean**: Confirmed `runtime` has no Maya/Qt/UI/maya_adapters imports.
- **Core Clean**: Confirmed `core` remains clean and free of unauthorized imports.

## Behavior Summaries
- **Callback Cleanup Behavior**: The `CallbackRegistry` tracks opaque IDs and matching cleanup functions. Calling `registry.clear()` invokes all cleanup functions and flushes the list.
- **Playback Skip Behavior**: Validated via `TestController`. When `PlaybackStartedEvent` is received, timeline changes are ignored. Upon `PlaybackStoppedEvent`, one rebuild is dynamically queued.
- **Key-Edit Dirty Behavior**: Validated via `TestController`. `KeyEditEvent` toggles a dirty flag. This defers the actual rebuild to the next frame evaluation or stops if playback is active.
- **Internal Time-Change Guard Behavior**: Validated via `TestController`. When `internal_time_change()` context manager is active, incoming `TimeChangeEvent`s are safely ignored.

## Scaffold/Spec Mismatches Found
None.

## Stage 05 Safe to Start
Yes, Stage 05 is safe to start.
