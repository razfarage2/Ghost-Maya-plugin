# Pose Ghost UI Spec v0.4

## 1. UI principle

The UI is a compact control surface. The main product is the viewport onion-skin feedback.

The UI must not contain business logic, sample-planning logic, Maya mesh capture logic, or callback logic.

## 2. Main panel sections

```text
Pose Ghost / 3D Onion Skin

Target Setup
Sampling
Display
Appearance
Objects
Performance Source
Actions
```

## 3. Target Setup

Controls:

```text
Target Root / Group field
Pick Selected Target Group
Scan Targets
Result count: "N targets found"

Optional Rig / Control Root field
Pick Selected Rig Root
Scan Controls / Watch Keys
Result count: "N animated controls found"
```

Target root is for geometry scanning. Rig/control root is optional and used for animation edit tracking or future keyed-pose mode.

## 4. Sampling

Controls:

```text
Sampling Mode:
  Relative Frames (default)
  Keyed Poses (advanced placeholder or future mode)

Previous Count:
  integer, default 3, min 0

Next Count:
  integer, default 3, min 0

Frame Step:
  number/integer, default 1, min > 0

Clamp to Playback Range:
  boolean, default true
```

Step = 2 supports animation on twos.

## 5. Display

Mutually exclusive display mode controls:

```text
Show Both
Show Previous
Show Next
```

Behavior:

```text
Show Both: previous and next samples visible if available
Show Previous: previous samples only
Show Next: next samples only
```

## 6. Appearance

Controls:

```text
Previous Color: default blue
Next Color: default red
Base Opacity: default 0.30
Opacity Falloff: default enabled
Fade Strength: default 0.65
```

Farther samples should use lower opacity when falloff is enabled.

## 7. Objects / bypass list

The UI must include an object list or expandable section.

Each row:

```text
object display name
status: active / bypassed / missing
visibility or eye/bypass toggle
optional source/proxy indicator
```

Bypassed objects remain in the profile but are skipped during generation.

## 8. Performance Source

Controls:

```text
Ghost Source Mode:
  Original Mesh
  Proxy Mesh Group

Proxy Root / Group field
Pick Selected Proxy Group
Scan Proxy Objects
```

Decimation generation is not V1, but the UI may reserve a disabled/advanced placeholder if clearly marked as not implemented.

## 9. Actions

Controls:

```text
Enable / Disable
Clear Ghosts
Force Rebuild
Save Profile
Reload/Validate Profile
```

`Force Rebuild` is for recovery/debug. Normal operation remains automatic.

## 10. Shortcut / popup placeholder

The reference add-on supports a popup shortcut. Maya V1 may include a shelf/menu launcher first.

V2/polish placeholder:

```text
custom hotkey / popup panel
```

## 11. UI validation

UI must prevent obviously invalid values:

```text
previous_count < 0
next_count < 0
frame_step <= 0
opacity outside 0..1
fade_strength outside 0..1
missing target root when enabling
```

## 12. UI output to runtime

UI emits commands/intent only:

```text
set_target_root(path)
scan_targets()
set_sampling_settings(settings)
set_display_mode(mode)
set_appearance(settings)
set_object_bypass(object_id, bypassed)
clear_ghosts()
force_rebuild()
```

The runtime/controller decides what work to perform.