# AGENTS.md — tests

## Local role

You are working in test routing.

## Local rules

Keep core tests pure Python. Maya integration tests must be clearly separated and not run in normal pytest unless Maya environment is available.

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