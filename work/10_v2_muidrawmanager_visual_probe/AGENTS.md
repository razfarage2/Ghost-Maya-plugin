# AGENTS.md — MUIDrawManager Visual Probe

This folder contains an isolated visual probe to verify if `MPxDrawOverride` + `MUIDrawManager` can draw 3D onion skin ghost geometry in Maya 2026.

## Current Goal
Prove `MUIDrawManager.mesh()` can draw blue/red transparent proxies without DAG node duplicates or batch-mode Python crashes.

## Next Step
If this probe succeeds, it will become the basis for the Stage 10B production renderer.
