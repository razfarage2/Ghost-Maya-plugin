# Known Bugs and Manual Validation Gaps

## 1. Graph Editor Tangent Manipulation
**Severity**: Low to Medium
**Description**: While standard keyframe translation edits successfully trigger the `KeyEditEvent` and rebuild the ghost correctly, manipulating tangent handles inside the Maya Graph Editor was not verified programmatically. Maya's `MAnimMessage.addAnimCurveEditedCallback` sometimes behaves inconsistently with tangent-only drags depending on Maya version.
**Reproduction Steps**:
1. Open Maya and start Pose Ghost on an animated object.
2. Open Graph Editor.
3. Select a key's tangent handle and drag it to alter the curve shape without moving the key's time/value.
4. Verify if the ghost automatically updates upon mouse release.
**Proposed Owner Decision**: If tangent edits fail to update ghosts, the user can press "Force Rebuild". For V2, a dedicated scriptJob for `undo/redo` or specific UI attribute changes might be necessary.

## 2. Referenced Node Deletion
**Severity**: Low
**Description**: `SceneProfileStore` saves targets by name string. If a referenced character is unloaded or its namespace changes drastically, the plugin may fail to locate the target upon scene reopen.
**Reproduction Steps**:
1. Reference a rig, set as target, save scene.
2. Unload reference.
3. Reopen scene.
**Proposed Owner Decision**: Maya adapter scanner gracefully drops missing nodes during generation, but UI may still display broken strings. Acceptable for V1.
