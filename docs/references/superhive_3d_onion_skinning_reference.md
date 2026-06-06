# Superhive 3D Onion Skinning Reference

URL: https://superhivemarket.com/products/3d-onion-skinning

## Purpose of this reference

This file captures the approved behavior target for Pose Ghost. The Superhive add-on is a Blender product, not a Maya product. Use this file as UX and behavior reference only.

Do not copy code, assets, UI graphics, text, or implementation from the reference add-on.

## Behavior details to mirror in Maya

The reference add-on describes these capabilities:

- Relative frame baking: display frames before and after the current frame.
- Customizable frame counts and colors.
- Useful for analyzing timing and spacing.
- Auto-update when frame changes through keyboard arrows or timeline scrubbing.
- Avoids updating repeatedly during playback, while keeping animation viewable.
- Auto-update when keyframes or graph handles are added, removed, translated, or edited.
- Translucent materials with customizable colors, fading, and opacity.
- Object flexibility.
- Works with linked/library-style data in Blender; Maya equivalent should be reference-safe.
- Supports targeted geometry areas in Blender; Maya V2 should consider component/vertex-set masking.
- Supports bypassing specific objects while keeping them available in the object list.
- Uses decimated/simple source objects for performance.
- Compact UI, optional popup access, tooltips, object list management, and shortcuts.
- Good for animation on twos and reducing bake overload over wider ranges.

## Maya translation

| Reference behavior | Maya Pose Ghost translation |
|---|---|
| Relative frame baking | Build `SamplePlan` using current frame, previous count, next count, and frame step |
| Frame counts and colors | UI controls and scene profile fields |
| Auto-update on frame change | `MDGMessage` time-change callback + debounce |
| Auto-update on key/handle edits | `MAnimMessage` animation edit callbacks + dirty rebuild |
| Avoid playback update storm | Query playback state and defer rebuild until playback stops |
| Translucent materials | Maya ghost materials with opacity/falloff |
| Object flexibility | Target adapter seam; V1 meshes, V2 curves/surfaces/instances |
| Linked data | Reference-safe scene profile and snapshot generation |
| Vertex group support | V2 component/vertex-set masking seam |
| Object bypass | Object bypass store and UI list |
| Decimated sources | Proxy source resolver and V2 decimation provider seam |
| Compact UI | Minimal Maya panel + optional popup/hotkey |

## Legal/build constraint

The Superhive add-on is GPL licensed according to the product page. This project must not copy implementation code or assets unless the project intentionally accepts the license consequences. Current decision: behavior reference only.