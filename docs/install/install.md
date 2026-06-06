# Pose Ghost Installation Guide

## Maya Version Tested
- **Maya 2024** (Python 3 / PySide6 / PySide2)

## 1. Add the Module Path
Pose Ghost uses Maya's standard module system (`.mod` files).
1. Locate the `PoseGhost.mod` file in the root of this downloaded repository.
2. Edit `PoseGhost.mod` if necessary. By default, it uses a relative path `.` assuming the `.mod` file stays in the repository root. If you move the `.mod` file to your Maya modules directory, update the path inside the `.mod` file to point to the repository root.
3. Copy or Symlink `PoseGhost.mod` into your Maya modules directory.
   - **Windows**: `C:\Users\<username>\Documents\maya\modules`
   - **macOS**: `~/Library/Preferences/Autodesk/maya/modules`
   - **Linux**: `~/maya/modules`

## 2. Launching the Tool
Once installed, you can launch Pose Ghost by creating a shelf button.
1. Open Maya.
2. Open the Script Editor (Python tab).
3. Paste the following code:
```python
import pose_ghost.launcher as pg
pg.show()
```
4. Highlight the text and middle-mouse drag it to your custom shelf.

## 3. Verify it Loaded
- Click the shelf button.
- The Pose Ghost UI panel should appear.
- The Script Editor should show no import errors.

## 4. Where Reports and Tests Live
- **Automated Tests**: Located in the `tests/` directory and can be run using standard `unittest` via `$env:PYTHONPATH="src"; python -m unittest discover -s tests`.
- **Validation Reports**: Located in the `work/` directory split by stage (e.g. `work/07_integration_validation/output/`).

## 5. Known Manual Validation Gaps
- **Graph Editor Tangent Handles**: Due to limitations in automated Maya batch testing, manipulating tangent handles in the Graph Editor without moving the key value was not programmatically verified. If ghosts fail to automatically update after a tangent edit, use the "Force Rebuild" button in the UI.
