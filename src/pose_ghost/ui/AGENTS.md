# AGENTS.md — ui

## Local role

You are working in the compact UI layer.

## Local rules

UI must call controller commands only. Do not implement sampling, callbacks, or mesh capture here.

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