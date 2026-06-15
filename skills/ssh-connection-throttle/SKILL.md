---
name: ssh-connection-throttle
description: Throttle SSH-family connections for the user's servers. Use whenever running `ssh`, `scp`, `sftp`, `rsync` over SSH, Git over SSH, or any command that opens a fresh SSH session. Keep connection starts below 5 per rolling 60 seconds and prefer waiting over bursts.
---

# SSH Connection Throttle

## Hard Rule

- Never start 5 or more SSH-family connections within any rolling 60-second window to the same server.
- Count `ssh`, `scp`, `sftp`, `rsync` over SSH, Git over SSH, and remote commands that open a new SSH session.
- Default to one active SSH-family connection at a time unless the user explicitly says otherwise.
- Prefer waiting over aggressive retries, parallel fan-out, or repeated probing.

## Operational Defaults

- Reuse a single SSH session for multiple remote commands whenever practical.
- If multiple fresh connections are unavoidable, space new connection starts at least 15 seconds apart.
- Do not launch SSH loops, background retries, or parallel workers that could exceed the limit.
- Before retrying after a failure, check whether a recent connection already happened and wait if needed.

## Execution Pattern

1. Plan the minimum number of fresh SSH sessions needed.
2. Prefer batching remote checks into one session.
3. Serialize transfers and remote commands by default.
4. If another new session is needed, wait long enough to stay below 5 starts per 60 seconds.

## Preferred Mindset

The user explicitly prefers slower, safer SSH access. If there is any doubt, reduce connection frequency and wait.
