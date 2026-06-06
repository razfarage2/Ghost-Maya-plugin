# Pose Ghost Acceptance Tests v0.4

## 1. Core logic tests

### Relative frame sampling

```text
Given current frame 30, previous_count 3, next_count 3, step 1
Expect previous frames 29, 28, 27
Expect next frames 31, 32, 33
```

```text
Given current frame 30, previous_count 3, next_count 3, step 2
Expect previous frames 28, 26, 24
Expect next frames 32, 34, 36
```

### Range clamp

```text
Given playback range 1..40, current 2, previous_count 3, step 1, clamp true
Expect previous frames 1 only
```

### Display mode filtering

```text
Show Both: previous and next active
Show Previous: previous active, next hidden
Show Next: next active, previous hidden
```

### Opacity falloff

```text
base opacity 0.30, fade 0.65
index 1 = 0.30
index 2 = 0.195
index 3 = 0.12675
```

### Settings validation

Reject:

```text
negative counts
zero/negative frame step
opacity outside 0..1
fade_strength outside 0..1
unknown display mode
unknown sampling mode
```

## 2. Maya integration tests

### Group scanning

```text
User selects a group containing multiple skinned meshes.
Scan returns visible, non-intermediate mesh targets.
Pose Ghost generated nodes are excluded.
```

### Snapshot exact position

```text
Animated object moves along X over frames.
Current frame is 10.
Previous samples are generated at 9, 8, 7.
Each ghost appears at the evaluated world-space X position of its sample frame.
No offset is applied.
```

### Non-renderable ghosts

```text
Generated ghosts are visible in viewport.
Generated ghosts are hidden from final render visibility flags.
Original mesh render/material settings remain unchanged.
```

### Timeline update

```text
Scrub from frame 30 to 31.
Runtime receives time-change event.
Sample plan updates.
Ghosts rebuild once after debounce.
```

### Playback protection

```text
Start playback.
Runtime does not rebuild every frame.
Stop playback.
Runtime rebuilds once for the stopped frame.
```

### Key/graph edit dirty update

```text
Edit keyframe/tangent without changing frame.
Runtime receives animation edit event if supported.
Dirty flag is set.
Ghosts rebuild after debounce.
```

### Object bypass

```text
Bypass one object in target list.
Rebuild onion skins.
Bypassed object does not produce ghosts.
Other objects still produce ghosts.
Un-bypass restores it without rescanning.
```

### Scene profile persistence

```text
Create profile.
Save scene.
Reopen scene.
Profile loads and validates target objects.
UI state restores.
Auto-update resumes.
```

## 3. Non-destructive validation

Verify plugin never:

```text
keys source controls
edits animation curves
changes skinClusters
changes constraints
changes original materials
changes source hierarchy
writes into referenced rig files
makes ghosts renderable
```

## 4. Performance smoke tests

```text
Large mesh group with previous_count 3 and next_count 3.
Scrub timeline.
No rebuild storms.
No duplicate ghost accumulation.
Clear Ghosts deletes only Pose Ghost-owned nodes.
```

## 5. Definition of done

A stage is done only when:

```text
implementation report is written
exact tests run are listed
pass/fail counts are included
known bugs are documented
spec relationship is explained
V2 improvements are listed
```