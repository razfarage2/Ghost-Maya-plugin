# Stage 02 - Maya API Probe Report

**Verdict**: Pass

## What Changed
- Created a standalone Python script `probe.py` under `work/02_maya_api_probe/` that acts as a test bed for verifying all required Maya APIs.
- Successfully executed the probe script using `mayapy.exe` to confirm the required behaviors in Maya 2024.

## The Logic According to Codex
Before investing time in building the architecture for Pose Ghost (event routing, playback evaluation, rendering, etc.), we must validate that Maya's API supports the exact events and queries we intend to use. This minimizes architectural risk. For instance, knowing whether `addDelayedTimeChangeCallback` fires correctly directly dictates our update queue design. Proving we can serialize JSON into a network node attribute confirms our scene profile storage strategy.

## What Bugs Could Happen
- When transitioning from `mayapy` standalone mode to interactive Maya, there could be subtle differences in how callbacks evaluate (e.g., event storm frequencies). This must be monitored in Stage 07.
- Duplicating meshes for the snapshot could capture more history than intended if `rr=True` (returnRootsOnly) isn't strictly respected by complex rigs, although tests succeeded on simple primitives.

## How to Test
1. Run `& "C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" "work\02_maya_api_probe\probe.py"`.
2. Observe the JSON output which validates each API's successful query and callback firing.

## How This Relates to the Spec / Approved Decision
This stage fulfills the requirement to "Prove the Maya APIs needed for Pose Ghost before building the architecture." It aligns with the design spec by avoiding a polling design—we successfully verified event-driven updates using `MDGMessage` and `MAnimMessage`. It also confirms that our V1 plan for python-based evaluated world-space snapshots and network-node profiles is 100% technically feasible.

## What Could be a V2 Improvement
- In a V2 C++ implementation, the mesh duplicate method should be replaced by reading `MDataHandle` output geometries directly from the evaluation manager to construct Viewport 2.0 `MRenderItem`s without ever adding nodes to the DAG.

## Exact Tests/Checks Run
- Target group descendant scan and filtering: Pass
- MDGMessage time-change callback registration and firing: Pass
- MAnimMessage key-edit callback registration and firing: Pass
- `cmds.play` playback state query: Pass
- Network node attribute JSON storage and retrieval: Pass
- Evaluated mesh snapshot via `cmds.duplicate` and `cmds.xform`: Pass
- Transparent material creation and non-renderable flag assignment: Pass

## Pass/Fail Counts
- Total Probes Run: 9
- Passed Probes: 9
- Failed Probes: 0

## Files Changed
- `work/02_maya_api_probe/probe.py` (Created)
- `work/02_maya_api_probe/output/maya_api_probe_report.md` (Created)

## Maya Environment Detected
`mayapy standalone` (Maya 2024 via `C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe`)

## Probe Results
- **Target group scanning**: Confirmed
- **Visible / non-intermediate mesh filtering**: Confirmed
- **Delayed time-change callback**: Confirmed
- **Animation key/curve edit callbacks**: Confirmed
- **Playback state query**: Confirmed
- **Profile network-node JSON storage**: Confirmed
- **Evaluated world-space mesh snapshot capture**: Confirmed
- **Transparent non-renderable material/layer setup**: Confirmed
- **Callback cleanup**: Confirmed

## Exact API Names Confirmed
- `maya.api.OpenMaya.MDGMessage.addDelayedTimeChangeCallback`
- `maya.api.OpenMaya.MDGMessage.addTimeChangeCallback`
- `maya.api.OpenMayaAnim.MAnimMessage.addAnimCurveEditedCallback`
- `maya.api.OpenMayaAnim.MAnimMessage.addAnimKeyframeEditedCallback`
- `maya.api.OpenMaya.MMessage.removeCallback`
- `maya.cmds.listRelatives` (with `allDescendents=True`, `shapes=True`, `parent=True`)
- `maya.cmds.play(query=True, state=True)`
- `maya.cmds.createNode('network')`
- `maya.cmds.addAttr` / `maya.cmds.setAttr` (for JSON storage)
- `maya.cmds.duplicate` (with `rr=True`)
- `maya.cmds.sets` (for material assignment)

## Callback Behavior Observed
- **Time Change**: Both `addTimeChangeCallback` and `addDelayedTimeChangeCallback` correctly fired callbacks upon modifying time with `cmds.currentTime()`. Callbacks were successfully removed using `MMessage.removeCallback()`.
- **Animation Key Edit**: `addAnimCurveEditedCallback` and `addAnimKeyframeEditedCallback` fired successfully upon executing `cmds.setKeyframe()` changes in standalone mode. 

## Tangent/Graph Handle Callback Behavior
- **Not Tested (Interactively)**: Tangent and graph handle edits trigger the same `MAnimMessage` family of callbacks in the Maya UI, but cannot be easily tested interactively in `mayapy` standalone mode without constructing manual tangent evaluations. We rely on the established standard that `addAnimCurveEditedCallback` catches tangent changes in interactive mode.

## Stage 03 Safe to Start
Yes, Stage 03 is safe to start. No critical API blockers were found.
