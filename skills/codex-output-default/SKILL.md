---
name: codex-output-default
description: Set and enforce a default local output directory for Codex on Windows, including path normalization, persistent PowerShell profile setup, preference file updates, and optional memory note updates. Use when users ask to change default output location, fix path format issues such as E;/codex/, or make output defaults persistent across sessions.
---

# Codex Output Default

Normalize paths to Windows absolute form, apply persistent defaults, and verify behavior in a fresh shell.

## Workflow

1. Normalize the requested path.
- Convert separators to backslashes.
- Ensure drive-letter format such as `E:\codex\`.
- Reject malformed style such as `E;/codex/`.

2. Apply the default with the bundled script.
- Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\apply_output_default.ps1 -OutputDir "E:\codex"
```

3. Verify persistence.
- Check `E:\codex\codex_output_preference.txt`.
- Open a fresh PowerShell process and confirm `$env:CODEX_OUTPUT_DIR`.
- Confirm alias `codex-out` returns the same path.

## Expected Artifacts

- Preference file: `E:\codex\codex_output_preference.txt`
- PowerShell profile update: `C:\Users\<user>\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
- Memory note: `C:\Users\<user>\.codex\memories\extensions\ad_hoc\notes\YYYYMMDD-HHMM-codex-output-default.md`
