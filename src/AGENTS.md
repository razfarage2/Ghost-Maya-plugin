# AGENTS.md — src

## Local role

You are working in the source tree router.

## Local rules

Do not implement behavior directly in `src/`. Route work into `src/pose_ghost/` and local package folders.

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