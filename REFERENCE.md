# REFERENCE.md — Pose Ghost Root Reference

## Project Vocabulary

| Term | Meaning |
|---|---|
| Onion skin | A translucent visual sample of the animated object at another frame |
| Previous sample | A sampled frame lower than current frame, colored blue by default |
| Next sample | A sampled frame higher than current frame, colored red by default |
| Sample plan | The full list of previous/next frames to capture for the current frame |
| Target object | Mesh/object selected for onion skin generation |
| Bypassed object | Target object kept in the profile but excluded from current onion generation |
| Snapshot | Standalone geometry captured from an evaluated source mesh at a sample frame |
| Exact world-space pose | The ghost appears where the object actually evaluated at that sample frame |
| Relative frames | Sampling by fixed frame step around current frame |
| Keyed poses | Optional advanced sampling by nearby keyed frames |

## External Behavior Reference

- Primary UX/behavior reference: `docs/references/superhive_3d_onion_skinning_reference.md`
- Do not copy code or assets from the reference add-on.
- The reference is Blender-specific and GPL licensed. This project should use it only as behavior/UX inspiration.

## Policy Reference

- ICM: `docs/references/icm.pdf`
- Clean Code: `docs/policies/clean_code.md`
- Clean Architecture: `docs/policies/clean_architecture.md`

## Maya Runtime Reference

- Maya Python command layer: `maya.cmds`
- Maya API 2.0: `maya.api.OpenMaya`
- Maya animation API: `maya.api.OpenMayaAnim`
- UI: Qt/PySide compatibility adapter
- V2 renderer possibility: C++ Viewport 2.0 draw backend