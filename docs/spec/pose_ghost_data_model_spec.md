# Pose Ghost Data Model Spec v0.4

## 1. Purpose

This spec defines core data models. These models belong in `src/pose_ghost/core/` and must not depend on Maya APIs.

## 2. OnionSettings

```python
@dataclass(frozen=True)
class OnionSettings:
    sampling_mode: SamplingMode
    previous_count: int
    next_count: int
    frame_step: float
    clamp_to_playback_range: bool
    display_mode: DisplayMode
    previous_color: tuple[float, float, float]
    next_color: tuple[float, float, float]
    base_opacity: float
    opacity_falloff_enabled: bool
    fade_strength: float
```

Validation:

```text
previous_count >= 0
next_count >= 0
frame_step > 0
base_opacity between 0 and 1
fade_strength between 0 and 1
```

## 3. OnionSample

```python
@dataclass(frozen=True)
class OnionSample:
    frame: float
    side: SampleSide   # previous | next
    index: int         # 1 is nearest to current frame
    opacity: float
    color: tuple[float, float, float]
```

## 4. SamplePlan

```python
@dataclass(frozen=True)
class SamplePlan:
    current_frame: float
    previous: tuple[OnionSample, ...]
    next: tuple[OnionSample, ...]
```

The sample plan is the renderer input. The renderer must not decide sampling policy.

## 5. DisplayMode

```python
class DisplayMode(Enum):
    BOTH = 'both'
    PREVIOUS = 'previous'
    NEXT = 'next'
```

Display mode filters which sample lists are active.

## 6. SamplingMode

```python
class SamplingMode(Enum):
    RELATIVE_FRAMES = 'relative_frames'
    KEYED_POSES = 'keyed_poses'
```

`RELATIVE_FRAMES` is V1 default.

## 7. TargetObject

```python
@dataclass(frozen=True)
class TargetObject:
    object_id: str
    display_name: str
    dag_path: str
    source_mode: SourceMode
    bypassed: bool
    missing: bool = False
```

`object_id` should be stable where possible. Maya adapter decides whether to use UUID, DAG path, or hybrid identity.

## 8. GhostState

```python
@dataclass(frozen=True)
class GhostState:
    profile_id: str
    sample_plan: SamplePlan
    target_signature: str
    appearance_signature: str
    display_mode: DisplayMode
```

Purpose:

```text
compare desired state against last rendered state
avoid unnecessary rebuilds
```

## 9. Scene profile schema

Current schema version: 2

```json
{
  "schema_version": 2,
  "profile_id": "uuid",
  "profile_name": "Character",
  "target_root": "|CHARACTER_MESH_GRP",
  "rig_root": "|CHARACTER_RIG_GRP",
  "target_objects": [],
  "bypassed_objects": [],
  "sampling_mode": "relative_frames",
  "previous_count": 3,
  "next_count": 3,
  "frame_step": 1,
  "clamp_to_playback_range": true,
  "display_mode": "both",
  "previous_color": [0.1, 0.35, 1.0],
  "next_color": [1.0, 0.1, 0.05],
  "base_opacity": 0.3,
  "opacity_falloff_enabled": true,
  "fade_strength": 0.65,
  "ghost_source_mode": "original",
  "proxy_target_root": null,
  "enabled": true
}
```

## 10. Opacity falloff

Default formula:

```python
opacity = base_opacity * (fade_strength ** (index - 1))
```

When falloff is disabled:

```python
opacity = base_opacity
```

## 11. Relative frame sample planner

Pseudo-code:

```python
def build_relative_sample_plan(current_frame, settings, playback_range=None):
    previous = []
    next_ = []

    for index in range(1, settings.previous_count + 1):
        frame = current_frame - index * settings.frame_step
        if settings.clamp_to_playback_range and playback_range and frame < playback_range.start:
            continue
        previous.append(make_sample(frame, 'previous', index, settings))

    for index in range(1, settings.next_count + 1):
        frame = current_frame + index * settings.frame_step
        if settings.clamp_to_playback_range and playback_range and frame > playback_range.end:
            continue
        next_.append(make_sample(frame, 'next', index, settings))

    return SamplePlan(current_frame=current_frame, previous=tuple(previous), next=tuple(next_))
```