# V2 Recommendations

## 1. Viewport 2.0 / C++ Override Candidate
**Current Limitation**: V1 uses `cmds.duplicate` to capture geometry snapshots. While mathematically exact and safe, doing this multiple times per target object creates a large number of DAG nodes that impact scene evaluation and outliner cleanliness.
**V2 Improvement**: Transition `MeshSnapshotRenderer` to a pure Viewport 2.0 API implementation using `MUserRenderOperation` or `MPxSubSceneOverride`. Instead of duplicating meshes in the DAG, we can query the evaluated vertex data at `t=frame` and push it directly into the GPU buffer. This yields zero DAG footprint, zero scene pollution, and blazing fast interactive scrubbing.

## 2. Proxy/Decimation Improvements
**Current Limitation**: A heavy rig of 2 million polygons will produce 12 million polygons if `prev=3` and `next=3`.
**V2 Improvement**: If Viewport 2.0 rendering is not immediately feasible, introduce a `DecimationStrategy` inside the snapshot capture. We can temporarily apply `cmds.polyReduce` to the duplicated snapshot to keep the ghost mesh lightweight. Alternatively, rely heavily on the V1 `ProxySourceResolver` but automate proxy generation.

## 3. Playback Caching
**Current Limitation**: The V1 `Controller` smartly defers rebuilding ghosts *during* playback and generates them only when playback stops.
**V2 Improvement**: Pre-calculate and cache the GPU vertex buffers for the entire playback range so the ghosts can stream in real-time *during* playback without freezing Maya.

## 4. UI Enhancements
**Current Limitation**: The UI is a pure control panel. 
**V2 Improvement**: Implement an interactive timeline overlay. For example, draw small color-coded ticks in the Maya timeline UI (using Qt to paint over the time slider) to visually indicate where the onion samples are located.
