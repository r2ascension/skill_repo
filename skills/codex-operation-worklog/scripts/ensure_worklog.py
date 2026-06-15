#!/usr/bin/env python3
"""
Create or extend a repository-level WORKLOG.md for substantive local Codex work.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


HEADER = """# Repository Worklog

## Rule

- This file records substantive local Codex operations in this repository.
- Reuse a task-specific worklog when one already governs the active thread.
- Otherwise append entries here instead of leaving changes undocumented.
"""


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "worklog_step"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def build_entry(step: str, author: str) -> str:
    timestamp = now_iso()
    return f"""### {timestamp} | {slugify(step)}

- Operation:
- Goal:
- Process:
- Modified files:
- Commands:
  ```bash
  ...
  ```
- Decisions:
- Verification:
- Result:
- Next step:
- Time:
  - {timestamp}
- Author:
  - {author}
"""


def ensure_worklog(path: Path) -> None:
    if path.exists():
        return
    path.write_text(HEADER + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ensure a repository-level WORKLOG.md exists and optionally append a scaffold entry."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root used when --worklog is omitted.")
    parser.add_argument("--worklog", help="Explicit target worklog path.")
    parser.add_argument("--step", default="worklog-update", help="Short step name for the entry title.")
    parser.add_argument("--author", default="Codex", help="Author name written into the scaffold.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append the scaffold to the worklog instead of printing it only.",
    )
    args = parser.parse_args()

    worklog = Path(args.worklog).resolve() if args.worklog else Path(args.repo_root).resolve() / "WORKLOG.md"
    ensure_worklog(worklog)
    entry = build_entry(args.step, args.author)

    if args.append:
        with worklog.open("a", encoding="utf-8", newline="\n") as handle:
            if worklog.stat().st_size > 0:
                handle.write("\n")
            handle.write(entry)
        print(worklog)
    else:
        print(entry)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
