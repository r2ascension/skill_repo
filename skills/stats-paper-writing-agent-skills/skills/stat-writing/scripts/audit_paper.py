#!/usr/bin/env python3
"""audit_paper.py - Combined audit runner for LaTeX statistical manuscripts.

This is a convenience wrapper around the bundled scripts:

  - check_tex.py: structure/writing heuristics (abstract/keywords/labels/floats/line numbers/
    raster figures/manual refs/equation punctuation/reproducibility cues/citation style/English)
  - check_bib.py: citation <-> BibTeX consistency + BibTeX hygiene warnings

The goal is to provide one command you can run before submission to catch common issues.

Usage:
  python audit_paper.py --tex path/to/main.tex [--bib path/to/refs.bib]

Exit codes:
  0: no HIGH findings from check_tex and no missing citations from check_bib (if provided)
  1: file/argument errors
  2: HIGH findings and/or missing citations

Notes:
- This does not compile LaTeX.
- No network access required.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def run(cmd: List[str]) -> Tuple[int, str]:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.returncode, proc.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", required=True, help="Path to main .tex file")
    ap.add_argument("--bib", required=False, help="Optional path to .bib file")
    args = ap.parse_args()

    tex = Path(args.tex).expanduser().resolve()
    bib = Path(args.bib).expanduser().resolve() if args.bib else None

    if not tex.exists():
        print(f"ERROR: tex file not found: {tex}", file=sys.stderr)
        return 1
    if bib is not None and not bib.exists():
        print(f"ERROR: bib file not found: {bib}", file=sys.stderr)
        return 1

    script_dir = Path(__file__).parent
    check_tex = script_dir / "check_tex.py"
    check_bib = script_dir / "check_bib.py"

    if not check_tex.exists():
        print(f"ERROR: missing script: {check_tex}", file=sys.stderr)
        return 1
    if bib is not None and not check_bib.exists():
        print(f"ERROR: missing script: {check_bib}", file=sys.stderr)
        return 1

    print("=== audit_paper: check_tex ===")
    rc_tex, out_tex = run([sys.executable, str(check_tex), str(tex)])
    print(out_tex.rstrip())
    print()

    rc_bib = 0
    if bib is not None:
        print("=== audit_paper: check_bib ===")
        rc_bib, out_bib = run([sys.executable, str(check_bib), "--tex", str(tex), "--bib", str(bib)])
        print(out_bib.rstrip())
        print()

    issues = (rc_tex == 2) or (rc_bib == 2)
    print("=== audit_paper: summary ===")
    if issues:
        if rc_tex == 2:
            print("- HIGH findings detected by check_tex.")
            print("  Note: MED/LOW findings may also be present and should be reviewed.")
        if bib is not None and rc_bib == 2:
            print("- Missing citations detected by check_bib (cited-but-missing keys).")
            print("  Note: check_bib output can also include non-blocking hygiene warnings.")
        print("Action: fix HIGH issues first, then address MED/LOW hygiene findings and rerun.")
        return 2

    print("OK: No HIGH findings (and no missing citations, if a .bib was provided).")
    print("Review MED/LOW findings from the report for final quality polish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
