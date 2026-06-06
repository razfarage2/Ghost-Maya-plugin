# Pose Ghost Runtime Spec v0.4

## 1. Runtime goal

The runtime reacts to Maya scene/timeline changes and keeps onion skins current without polling.

## 2. No polling

Polling means repeatedly checking timeline state on a timer. This is forbidden as the normal runtime design.

Required approach:

```text
Maya event/callback backend
+ debounce queue
+ dirty-state tracking
+ playback protection
```

## 3. Runtime components

```text
runtime/controller.py
  Owns high-level runtime decisions.

runtime/event_router.py
  Receives Maya time/key/playback events and forwards intent.

runtime/update_queue.py
  Debounces heavy work and keeps only the latest desired state.

runtime/callback_registry.py
  Stores callback IDs and removes them safely.

runtime/lifecycle.py
  Startup/shutdown, scene-open/scene-close handling.

runtime/composition_root.py
  Wires core logic and concrete Maya adapters.
```

## 4. Time-change flow

```text
User changes current frame
↓
Maya delayed time-change callback fires
↓
event_router receives time event
↓
if internal time-change guard is active: ignore
↓
if playback is active: mark pending update but do not rebuild now
↓
controller builds desired SamplePlan
↓
controller compares SamplePlan against last rendered GhostState
↓
if unchanged: do nothing
↓
if changed: enqueue rebuild
```

## 5. Playback behavior

The runtime must avoid rebuilding on every playback frame.

Behavior:

```text
During playback:
  keep existing ghosts visible
  do not rebuild every frame
  record that rebuild may be needed

When playback stops:
  rebuild once for the final/current frame
```

Maya playback state should be queried by a Maya adapter, not by core logic.

## 6. Animation edit flow

The reference behavior requires auto-update when keys or graph handles are edited.

Maya runtime behavior:

```text
User edits keys / tangents / graph handles
↓
MAnimMessage callback fires if supported by current Maya version
↓
controller marks onion state dirty
↓
update queue schedules rebuild for current frame
↓
renderer captures new samples
```

If exact graph-handle/tangent callback behavior differs by Maya version, the API probe must document it and propose the cleanest fallback.

## 7. Sample plan build flow

```text
current frame
previous count
next count
frame step
range clamp
playback start/end
sampling mode
```

These produce:

```text
SamplePlan:
  previous: list[OnionSample]
  next: list[OnionSample]
```

The renderer only receives a sample plan. It does not decide which frames to sample.

## 8. Debounce queue

Scrubbing can fire many frame updates quickly.

Required behavior:

```text
only latest requested SamplePlan matters
older pending plans are discarded
heavy rebuild is deferred until Maya is safe/idle if needed
no concurrent rebuilds
```

State fields:

```text
pending_plan
is_rebuild_running
is_dirty
last_rendered_state
last_request_time
```

## 9. Internal time-change guard

Snapshot capture may temporarily set Maya time to each sample frame.

This can trigger time callbacks, so runtime must guard internal time changes:

```python
is_internal_time_change = True
try:
    capture_samples()
finally:
    restore_original_time()
    is_internal_time_change = False
```

Any time callback received during internal capture must be ignored.

## 10. Rebuild conditions

Rebuild required when:

```text
sample frames change
display mode changes
sample count changes
frame step changes
opacity/color/falloff changes
target list changes
bypass list changes
source mode changes
proxy root changes
animation edit callback marks dirty
profile is loaded/reloaded
ghosts were cleared
```

No rebuild required when:

```text
current frame changes but resulting SamplePlan and visual settings are identical
playback is currently running
```

## 11. Callback lifecycle

All callback IDs must be registered and removed on shutdown/scene unload/plugin unload.

Required pattern:

```python
callback_id = add_callback(...)
callback_registry.register(callback_id)

# shutdown
callback_registry.clear()
```

Unremoved Maya callbacks can cause crashes or stale callback behavior.

## 12. Error handling

Runtime must fail safe:

```text
if profile missing: do nothing
if target missing: mark profile invalid and do not mutate scene
if renderer fails: clear partial ghosts it owns and write/report error
if callback registration fails: disable auto-update and report fallback need
if current scene changes: validate profile before rebuilding
```

## 13. Runtime reports

Each runtime implementation task must report:

```text
callbacks registered
debounce behavior implemented
playback skip behavior implemented
internal time-change guard implemented
cleanup path implemented
tests run
known Maya-version risks
```