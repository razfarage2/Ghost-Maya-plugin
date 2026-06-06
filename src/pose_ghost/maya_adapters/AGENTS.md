# AGENTS.md — maya_adapters

## Local role

You are working in the Maya API boundary layer.

## Local rules

Maya API calls belong here. Keep Maya details out of core. Do not mutate source rig/mesh/materials.

## Required report

Any change in this folder must report:

- what changed
- the logic according to Codex
- what bugs could happen
- how to test
- how this relates to the spec / approved decision
- what could be a v2 improvement
- exact tests run
- pass/fail counts