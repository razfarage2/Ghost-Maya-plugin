# Pose Ghost V1.1A Cache, Pool, and Opacity Optimization Report

## Verdict
**Pass**

## What Changed
- Created `TargetScanCache` to cache hierarchy scanning results, preventing redundant rescans during normal timeline scrubbing.
- Created `GhostNodePool` to maintain an MRU pool of evaluated ghost snapshots keyed by `(target_mesh, frame)`. Ghosts are no longer blindly deleted during scrubbing; unused ghosts are simply hidden.
- Modified `MeshSnapshotRenderer` to integrate with `GhostNodePool` for geometry generation and material assignment. Re-uses existing geometry instead of triggering expensive `cmds.duplicate` evaluations if the sample frame already has a generated geometry.
- Introduced a dedicated `apply_appearance_only` pathway in `MeshSnapshotRenderer` that allows real-time updating of materials and transparency without initiating a full geometry recapture.
- Updated `GhostState` and `Controller` logic so that opacity and other purely visual changes trigger `action: appearance` on the queue rather than `action: rebuild`.
- Updated `launcher.py` to correctly map the `appearance` action to the new `apply_appearance_only` function.
- Added `test_cache_optimization.py` and updated existing integration tests (`test_integration.py`) to align with the new caching strategies and object naming conventions.

## Root Cause of Repeated Recalculation
In V1.0, `MeshSnapshotRenderer.render` began by calling `DisplayLayerManager.clear_all()`, which deleted all existing ghost DAG nodes. It then re-ran `EvaluatedSnapshotCapture.capture_snapshot(target, sample.frame)` to duplicate the meshes for every single requested frame in the sample plan, even if the timeline had only advanced by one frame and most of the previous samples were still identical.

## Root Cause of Interactive Opacity Not Updating
Opacity slider updates triggered a `SettingsChangedEvent`, which forced a full recalculation. This was too heavy to compute smoothly in real-time, resulting in lag. Furthermore, deleting and rebuilding meshes during a slider drag broke the Maya evaluation loop or created extreme jank, causing it to feel "broken".

## The Logic According to Codex
The system uses the new `GhostNodePool` to abstract away geometry management.
When `MeshSnapshotRenderer` requests a ghost for `(cube, frame=10)`, the pool checks if `Ghost_cube_10` exists. If it does, we return it immediately and skip the Maya evaluation capture. We then parent it to the correct group and run the material update.
When `GhostState` detects that only visual parameters (like `base_opacity`) changed, it returns `True` for `requires_appearance_update` and `False` for `requires_rebuild`.
The `Controller` enqueues an `appearance` job, bypassing the `SamplePlan` evaluation and skipping geometry generation.

## What Bugs Could Happen
- If a rigger changes the mesh topology (e.g. skinning weights or blendshapes) without scrubbing the timeline to invalidate the cache, the ghost pool might serve up an outdated "cached" geometry.
- If the `MAX_SIZE` (currently 100) on `GhostNodePool` is reached rapidly during scrubbing, old nodes will be `cmds.delete`'d, which may trigger a slight latency spike on frame changes.

## How to Test
Execute `test_cache_optimization.py` to ensure all four optimization behaviors behave perfectly (Target scan caching, snapshot caching, material-only updates, and skipped evaluation on opacity=0.0). Run the rest of the integration tests (`test_integration.py`, etc.) to confirm regressions are avoided. Load it in Maya and scrub the timeline / adjust opacity while watching the Outliner and Script Editor to confirm smooth behavior.

## How this Relates to the Spec / Approved Decision
This fulfills the approved V1.1A requirement to provide "Ghost snapshot/node reuse foundation so timeline movement reuses existing ghost data where safe instead of full delete/recreate behavior."

## What Could be a V2 Improvement
V2 could entirely migrate off `cmds.duplicate` and `cmds.parent` and move to an OpenGL or Viewport 2.0 `MPxSubSceneOverride` rendering approach, completely eliminating DAG node clutter, avoiding outliner interference, and solving the topology caching issue entirely.

## Exact Tests/Checks Run
- `test_cache_optimization.py`: 4 Passed / 0 Failed
- `test_ux_hotfixes.py`: 1 Passed / 0 Failed
- `test_ui_scan_wiring.py`: 1 Passed / 0 Failed
- `test_renderer.py`: 1 Passed / 0 Failed
- `test_integration.py`: 10 Passed / 0 Failed
- Python Unit Tests (core): 48 Passed / 0 Failed
- Boundary Checks: Passed (No illegal cross-boundary imports)

## Files Changed
1. `src/pose_ghost/maya_adapters/target_scan_cache.py` (New)
2. `src/pose_ghost/maya_adapters/ghost_node_pool.py` (New)
3. `src/pose_ghost/maya_adapters/mesh_snapshot_renderer.py` (Modified)
4. `src/pose_ghost/core/ghost_state.py` (Modified)
5. `src/pose_ghost/runtime/controller.py` (Modified)
6. `src/pose_ghost/launcher.py` (Modified)
7. `work/07_integration_validation/test_integration.py` (Modified)
8. `tests/maya_integration/test_cache_optimization.py` (New)

## Cache Strategy Chosen
**Ghost Geometry Reuse via LRU Pool**: The `GhostNodePool` manages actual Maya DAG nodes using a dictionary acting as an LRU cache (backed by `collections.OrderedDict`). Nodes are keyed by a tuple of `(target_path, frame)`. Nodes are hidden (visibility=0) instead of being deleted when they exit the current sample plan. Unused nodes are evicted only when the pool hits its `MAX_SIZE` threshold (100). This safely caches the `cmds.duplicate(rr=True)` output while keeping the node count bounded and maintaining Maya DG non-destructive workflows.

## Target Scan Cache Behavior
`TargetScanCache` stores the resolved array of mesh targets mapped to a root transform path. The cache only executes `cmds.listRelatives` when: a new root is picked, an explicit force rescan is requested, or when an internal validation check finds one of the cached DAG nodes was deleted (in which case it prunes the dead node and serves the rest).

## Snapshot/Ghost Cache Behavior
During playback/scrubbing, `RelativeFrameSampler` outputs the new target frames. `MeshSnapshotRenderer` requests the corresponding `(target_path, frame)` tuples. `GhostNodePool` matches them to previously duplicated meshes. The matching nodes are revealed (`cmds.setAttr(..., visibility, 1)`), re-parented to the correct group, and recolored via MaterialManager. Any previously visible nodes not requested in the new frame are hidden, skipping full destruction/creation cycles.

## Material-only Update Behavior
When UI slider tweaks change `base_opacity` or `fade_strength`, the `Controller` enqueues an `appearance` job. `MeshSnapshotRenderer.apply_appearance_only()` is triggered, which iterates through all currently active ghosts and ONLY runs `MaterialManager.assign_per_sample_material()`. Geometry duplication is entirely bypassed.

## Cache Invalidation Rules
- `TargetScanCache`: Invalidated explicitly by UI interactions (Scan Target) or if `GhostNodePool.clear()` is called. 
- `GhostNodePool`: Invalidated completely via `clear()` (e.g., when the user clicks 'Clear Ghosts'). Evicts oldest frames automatically on cache max.

## Proof Opacity Changes No Longer Recapture Geometry
In `test_cache_optimization.py -> test_material_only_update()`, generating the initial frame yields `pool_size=2`. Adjusting the opacity slider from 0.1 to 0.3 queues an `appearance` job. Verifying the pool size afterward confirms it remains exactly 2, and no new `EvaluatedSnapshotCapture` commands are logged.

## Proof Cached Frames Are Reused
In `test_cache_optimization.py -> test_snapshot_reuse()`, moving the timeline from frame 10 to frame 11 only generates new missing overlapping geometry at the edge of the sampling bounds. The pool growth remains precisely bounded rather than duplicating new copies of overlapping frames.

## Proof Existing Tests Still Pass
All regression tests passed successfully in Maya headless batch mode without breaking existing hotfixes (Selection preservation, hideInOutliner, etc.).

## Boundary Check Results
Core, Runtime, UI, and Maya Adapters contain zero illegal crossover imports. The system remains clean.

## Whether V1.1B Should Proceed Next
Yes. The foundational caching structure is robust. V1.1B can now proceed to solve key-edit debouncing and the Heavy Rig mode safely.

## Next Manual Test for Raz
Boot up interactive Maya. Scan the target root, and scrub the timeline on a rigged character. Validate that scrubbing feels significantly lighter and less jittery than V1.0. Next, drag the Opacity and Falloff sliders; confirm that the ghosts update smoothly and instantaneously in the viewport without flickering or triggering Maya hangs.
