---
name: opencli-local-check
description: Validate and use the locally installed `opencli` on this Windows machine. Use when the user asks whether Codex can call `opencli`, wants the resolved local entrypoint or version, needs a quick smoke test such as `opencli --help`, `opencli list`, or `opencli doctor`, or wants help separating PATH/startup issues from bridge, login, or site-specific failures.
---

# OpenCLI Local Check

## Quick Start

- Treat local CLI availability and remote bridge/login behavior as separate checks.
- Start with `Get-Command opencli | Select-Object Source,Definition,CommandType | Format-List`.
- Confirm the installed version with `opencli --version`.
- Use `opencli --help` as the minimum safe smoke test when the user only wants to know whether the CLI is callable.

## Verified Local Facts

- On 2026-06-13 in this Codex Windows environment, `Get-Command opencli` resolved to `C:\Users\simon\AppData\Roaming\npm\opencli.ps1`.
- On 2026-06-13, `opencli --version` returned `1.8.3`.
- On 2026-06-13, `opencli --help` returned normally and exposed core commands including `list`, `validate`, `verify`, `doctor`, `browser`, `plugin`, `adapter`, `profile`, `daemon`, and `external`.

## Workflow

1. Confirm the entrypoint/path.
2. Confirm the installed version.
3. Run the smallest safe smoke test that matches the user's request.
4. Escalate to a site-specific or bridge-specific command only after basic availability is confirmed.

## Smoke Test Choices

- Use `opencli --help` for basic launch verification.
- Use `opencli list` to inspect the exposed command surface.
- Use `opencli doctor` when the browser bridge or local connectivity is suspect.
- Use the user's exact target command only after the basic checks pass.

## Reporting Rules

- State clearly whether the problem is:
  - local command discovery,
  - local startup/runtime failure,
  - browser bridge/connectivity,
  - login/auth,
  - site-specific behavior.
- Do not claim Codex has a native OpenCLI integration just because the local CLI exists; only claim that shell invocation works once the checks above pass.

## Guardrails

- Prefer direct execution over theory when the user wants a real `opencli` check.
- Consult local `--help` output before browsing the web.
- Browse only when local help is insufficient or when current upstream documentation materially affects the answer.
