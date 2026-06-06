# AGENTS.md — Devir Root Router
# דְּבִיר — Local Identity and Secrets Vault

> You are working on **Devir** — a standalone, local, encrypted vault
> service. Devir is part of the H.I.R.A.M. ecosystem but is its own
> repository. It is not a feature of HIRAM. HIRAM is one of its clients.

---

For any file search or grep in the current git-indexed directory, use `fff` tools.

---

## What Is Devir

Devir protects the owner's sensitive data — passwords, identity fields,
API keys, documents, contacts, SSH keys, secure notes. It releases the
minimum needed, to authorized callers only, with a full audit trail.

The approved specification is the source of truth for architectural
and security decisions. Read it before touching code:

```text
docs/spec/devir_spec_v4.md
```

If a prompt, module doc, or older report references `docs/spec/devir_spec_v3.md`,
check whether the repo contains `devir_spec_v4.md`. If v3/v4 paths disagree,
flag the mismatch in the report. Do not silently invent a spec change.

Before you start anything first read the docs/policies folder with
- clean_architecture.md
- clean_code.md
and then continue, make sure the code is following these policies.

---

## Repo Map — Where To Go

| You need to work on... | Go to |
|---|---|
| The core Rust daemon: crypto, storage, policy, sessions, API, CLI | `daemon/` |
| The Mishneh hot standby daemon | `standby/` |
| The desktop tray app (Tauri) | `tray-app/` |
| The browser extension | `browser-extension/` |
| The Android app | `android/` |
| Specs, decisions, architecture docs, reports | `docs/` |
| Encryption / key derivation | `daemon/src/vault_core/` |
| OS key storage (DPAPI / Keystore) | `daemon/src/key_adapter/` |
| Access control and approval rules | `daemon/src/policy_engine/` |
| Building time-limited data packages | `daemon/src/capsule_builder/` |
| Owner approval flow | `daemon/src/approval_gate/` |
| Append-only event log | `daemon/src/audit_ledger/` |
| HTTP API (localhost:7777) | `daemon/src/http_api/` |
| Agent-facing CLI tool | `daemon/src/cli/` |
| Shared unlock/session claim | `daemon/src/vault_service/`, `daemon/src/http_api/` |
| Travel Mode policy and controls | `daemon/src/policy_engine/`, `daemon/src/vault_service/`, `daemon/src/http_api/`, `tray-app/`, `android/` |
| Benaiah service-principal capsule flow | `daemon/src/policy_engine/`, `daemon/src/vault_service/`, `daemon/src/http_api/` |
| Autofill Core backend | `daemon/src/vault_service/`, `daemon/src/http_api/`, `daemon/src/audit_ledger/` |
| Android Autofill adapter | `android/` |

Each major folder has local routing/context docs. Before changing a folder,
read the folder's `AGENTS.md`, `CLAUDE.md` if present, `CONTEXT.md`, and
`REFERENCE.md`.

---

## Current Implementation Reality

Devir is no longer an empty scaffold. The repo contains active daemon,
tray, Android, browser-extension handoff, Benaiah, Travel Mode, shared
unlock, and Autofill Core code.

Do not use old root text saying "no production code exists" or "Android /
browser-extension are placeholders only" as truth. Use the current module
`CONTEXT.md` / `REFERENCE.md` files and latest reports.

Phase labels are historical planning labels. Phase 1 is not closed until
owner live validation signs off the relevant Definition of Done, but several
approved cross-phase surfaces already exist because Raz approved them:

- Android Travel Mode status/disable and shared unlock resume.
- Browser-extension support through tray handoff broker.
- Benaiah service-principal capsule contract.
- Backend Autofill Core.

Do not expand those surfaces without a narrowly scoped prompt.

---

## Non-Negotiable Rules

1. **The spec is the source of truth.** `docs/spec/devir_spec_v4.md`
   is the current tracked authority when present. If code and spec disagree,
   flag the deviation. Do not silently resolve it in code's favor.

2. **Read local docs before changing code.** Use the relevant `AGENTS.md`,
   `CLAUDE.md` if present, `CONTEXT.md`, and `REFERENCE.md` for the module.

3. **No plaintext secrets ever.** Do not log secret values. Do not return
   raw secrets from API endpoints. Do not store keys next to data. Do not
   put passwords, TOTP secrets, bearer tokens, Hotam proofs, biometric proofs,
   AUK, VEK, or device secrets in logs, UI, reports, or tests.

4. **Rust for all security-critical code.** The daemon and standby are Rust.
   TypeScript is for tray/browser UI shells. Kotlin is for Android clients.

5. **No delete — only archive.** Vault items are never deleted. The audit
   ledger is append-only.

6. **actor is required on every audit event.** Every event must carry a
   non-null, non-empty actor. Silent or anonymous operations do not exist.

7. **Owner-level actions need the approved owner-auth surface.** Protocol
   Hotam gates owner-level actions unless an explicit approved decision says
   otherwise. Current approved exception: tray/local-PC Travel Mode disable
   uses a valid unlocked owner session and does not require a fresh Windows
   Hello prompt; Android Travel Mode disable remains biometric-backed.

8. **Brokers are not owners.** Benaiah and autofillers are broker clients.
   They may receive narrowly scoped continuity/capability flows, but they
   never become owner sessions and never browse the vault.

9. **The LLM/HIRAM never receives raw vault data.** It receives approved
   capability capsules only.

10. **If unsure, stop and flag it.** Do not guess at security decisions.
    Do not fill gaps with assumptions.

---

## Locked / Approved Current Contracts

### Shared unlock / session claim

- Vault unlock state is daemon-wide.
- Bearer sessions are per client and are never shared across clients.
- Trusted resume window is one hour from successful owner unlock.
- `POST /lock` clears daemon-wide unlock state and invalidates owner/browser sessions.
- Tray/local owner and Android phone claim their own fresh sessions.
- Benaiah/service-principal tokens cannot claim owner sessions.

### Travel Mode

- Fresh/default Travel Mode state is OFF.
- Explicit owner enable persists ON until disabled.
- Tray can show status and disable Travel Mode without extra Windows Hello.
- Android can show status and disable Travel Mode only with biometric/fingerprint.
- Travel Mode blocks/tightens sensitive paths except Benaiah.
- Benaiah remains under its normal strict rules while Travel Mode is ON.

### Benaiah

- Benaiah polls deferred capsule status using `data.request_id`.
- `approval_request_id` is owner-approval metadata, not Benaiah's polling id.
- Benaiah specific allowed identity fields require approval/deferred capsule.
- Benaiah full identity bundle is blocked always.
- Benaiah forbidden fields remain blocked.
- Benaiah does not become owner and cannot claim owner sessions.

### Autofill Core

- Autofillers are brokers.
- Backend Autofill Core exists for match/fill/save-candidate.
- Match returns safe metadata only.
- Fill uses a minimum login capsule for matched login targets.
- Locked/resume states are structured continuation states, not silent failures.
- Travel Mode blocks/tightens autofill. Do not copy Benaiah's Travel Mode
  exception to autofill.
- Android/browser/PC platform adapters are separate passes.

---

## Current Build Discipline

Every Codex task must be narrow. Do not bundle daemon, Android, browser,
and PC-wide work unless the prompt explicitly approves that scope.

Every Codex task must write a report including:

- what changed
- the logic according to Codex
- what bugs could happen
- how to test
- how this relates to the spec / approved decision
- what could be a v2 improvement
- exact tests run
- pass/fail counts

Passing tests are not final proof. Raz's live logs are the validation layer.

---

## Phase Status

| Area | Current status | Notes |
|---|---|---|
| Daemon | Active implementation | Vault, policy, sessions, Travel Mode, Benaiah, Autofill Core are implemented in code/tests. |
| Tray app | Active implementation | Includes Travel Mode status/disable and shared unlock auto-claim. |
| Android app | Active implementation | Includes Travel Mode biometric disable and shared unlock resume. Android Autofill adapter is the next scoped pass. |
| Browser extension | Partial implementation | Shared unlock support currently through tray handoff broker; direct daemon claim remains deferred. |
| Standby / Mishneh | Planned/partial depending on repo state | Check module docs before changing. |
| Benaiah | Active broker integration | Service-principal capsule flow implemented; full identity bundle remains blocked. |
| Autofill | Backend Core implemented | Android/browser/PC adapters remain separate passes. |
| Windows Credential Provider | Future work | Do not implement unless explicitly prompted. |

---

## Naming Reference

| Name | Hebrew | Role |
|---|---|---|
| Devir | דְּבִיר | The vault — Holy of Holies |
| Otzar | אוֹצָר | Dumb encrypted blob store / sync relay |
| Mishneh | מִשְׁנֶה | Full hot standby |
| Hotam | חוֹתָם | Biometric owner verification protocol |
| Benaiah | בְּנָיָהוּ | Broker for deletion/identity capsule workflows |
