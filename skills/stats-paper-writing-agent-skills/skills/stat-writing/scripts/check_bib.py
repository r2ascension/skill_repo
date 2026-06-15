#!/usr/bin/env python3
"""
check_bib.py - LaTeX citations <-> BibTeX consistency checker.

Features
- Extract citation keys from LaTeX source (natbib-style commands).
- Follow \\input{} and \\include{} recursively.
- Extract BibTeX entry keys and common fields from a .bib file.
- Report:
  1) cited-but-missing keys
  2) unused bib entries
  3) BibTeX hygiene warnings, including:
     - page ranges should use double dashes (110--118)
     - @article missing volume/pages
     - @book missing publisher/address (style-dependent)
     - duplicate DOI values across entries
     - author fields containing literal "et al."
     - capitalization-risk titles (acronym-like tokens without braces)

Usage
  python check_bib.py --tex main.tex --bib refs.bib

Exit codes
  0: no missing citations
  1: file/argument errors
  2: missing citations detected
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set


CITE_CMD_RE = re.compile(
    r"""\\cite[a-zA-Z*]*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}""",
    re.MULTILINE,
)
INPUT_RE = re.compile(r"""\\(input|include)\{([^}]+)\}""")
COMMENT_RE = re.compile(r"""(?<!\\)%.*$""", re.MULTILINE)


@dataclass
class BibEntry:
    key: str
    entry_type: str
    fields: Dict[str, str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(tex: str) -> str:
    return re.sub(COMMENT_RE, "", tex)


def resolve_tex_path(root: Path, name: str) -> Path:
    p = Path(name)
    candidates: List[Path] = []
    if p.is_absolute():
        candidates.append(p)
        if p.suffix == "":
            candidates.append(p.with_suffix(".tex"))
    else:
        candidates.append(root / p)
        if p.suffix == "":
            candidates.append((root / p).with_suffix(".tex"))

    for c in candidates:
        if c.exists() and c.is_file():
            return c

    return (root / p).with_suffix(".tex") if p.suffix == "" else (root / p)


def collect_tex_files(main_tex: Path, max_files: int = 200) -> List[Path]:
    visited: Set[Path] = set()
    stack: List[Path] = [main_tex]
    out: List[Path] = []

    while stack:
        path = stack.pop()
        if path in visited:
            continue
        visited.add(path)
        out.append(path)

        if len(out) >= max_files:
            break

        try:
            content = strip_comments(read_text(path))
        except Exception:
            continue

        for m in INPUT_RE.finditer(content):
            child = resolve_tex_path(path.parent, m.group(2).strip())
            if child.exists() and child.is_file() and child not in visited:
                stack.append(child)

    return out


def extract_cite_keys(tex: str) -> Set[str]:
    keys: Set[str] = set()
    for m in CITE_CMD_RE.finditer(tex):
        inside = m.group(1)
        for k in inside.split(","):
            k = k.strip()
            if k:
                keys.add(k)
    return keys


def parse_bib_entries(bib_text: str) -> Dict[str, BibEntry]:
    entries: Dict[str, BibEntry] = {}

    bib_text = re.sub(r"(?m)^\s*%.*$", "", bib_text)
    chunks = re.split(r"(?=@)", bib_text)

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk.startswith("@"):
            continue

        m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", chunk, re.IGNORECASE)
        if not m:
            continue

        entry_type = m.group(1).lower()
        key = m.group(2).strip()
        if entry_type in {"string", "preamble", "comment"}:
            continue

        fields: Dict[str, str] = {}
        for fm in re.finditer(r"(\w+)\s*=\s*(\{[^{}]*\}|\"[^\"]*\")\s*,?", chunk, re.IGNORECASE):
            fname = fm.group(1).lower().strip()
            raw = fm.group(2).strip()
            if raw.startswith("{") and raw.endswith("}"):
                raw = raw[1:-1]
            elif raw.startswith('"') and raw.endswith('"'):
                raw = raw[1:-1]
            fields[fname] = raw.strip()

        entries[key] = BibEntry(key=key, entry_type=entry_type, fields=fields)

    return entries


def _normalize_doi(doi: str) -> str:
    d = doi.strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    d = re.sub(r"^doi:\s*", "", d)
    d = d.strip()
    return d


def bib_hygiene_warnings(entries: Dict[str, BibEntry]) -> List[str]:
    warnings: List[str] = []

    doi_to_keys: Dict[str, List[str]] = {}

    for key, entry in entries.items():
        fields = entry.fields

        pages = fields.get("pages", "")
        if pages and "-" in pages and "--" not in pages:
            warnings.append(
                f"[{key}] pages appears to use a single dash: pages = {{{pages}}} (prefer 110--118)."
            )

        if entry.entry_type == "article":
            if not fields.get("volume"):
                warnings.append(f"[{key}] @article missing volume.")
            if not fields.get("pages"):
                warnings.append(f"[{key}] @article missing pages.")

        if entry.entry_type == "book":
            if not fields.get("publisher"):
                warnings.append(f"[{key}] @book missing publisher.")
            if not fields.get("address"):
                warnings.append(f"[{key}] @book missing address.")

        author = fields.get("author", "")
        if author and re.search(r"\bet\s+al\.?\b", author, re.IGNORECASE):
            warnings.append(f"[{key}] author field contains literal 'et al.' (list full authors in BibTeX).")

        title = fields.get("title", "")
        if title:
            if "{" not in title and re.search(r"\b[A-Z]{2,}\b", title):
                warnings.append(
                    f"[{key}] title contains acronym-like uppercase token(s) without braces; verify capitalization protection."
                )

        doi = fields.get("doi", "")
        if doi:
            normalized = _normalize_doi(doi)
            if normalized:
                doi_to_keys.setdefault(normalized, []).append(key)

    duplicate_dois = {d: ks for d, ks in doi_to_keys.items() if len(ks) > 1}
    for doi, keys in sorted(duplicate_dois.items()):
        warnings.append(f"Duplicate DOI detected ({doi}) across keys: {', '.join(sorted(keys))}.")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex", required=True, help="Path to main .tex file")
    parser.add_argument("--bib", required=True, help="Path to .bib file")
    args = parser.parse_args()

    main_tex = Path(args.tex).expanduser().resolve()
    bib_path = Path(args.bib).expanduser().resolve()

    if not main_tex.exists():
        print(f"ERROR: tex file not found: {main_tex}", file=sys.stderr)
        return 1
    if not bib_path.exists():
        print(f"ERROR: bib file not found: {bib_path}", file=sys.stderr)
        return 1

    tex_files = collect_tex_files(main_tex)
    all_tex = ""
    for p in tex_files:
        try:
            all_tex += "\n" + strip_comments(read_text(p))
        except Exception:
            continue

    cited_keys = extract_cite_keys(all_tex)
    bib_entries = parse_bib_entries(read_text(bib_path))
    bib_keys = set(bib_entries.keys())

    missing = sorted(cited_keys - bib_keys)
    unused = sorted(bib_keys - cited_keys)
    hygiene = bib_hygiene_warnings(bib_entries)

    print("check_bib report")
    print(f"  tex: {main_tex}")
    print(f"  bib: {bib_path}")
    print(f"  scanned tex files: {len(tex_files)}")
    print()

    print("CITED BUT MISSING FROM .bib")
    if missing:
        for k in missing:
            print(f"  - {k}")
    else:
        print("  OK: none")
    print()

    print("BIB ENTRIES NOT CITED")
    if unused:
        for k in unused[:200]:
            print(f"  - {k}")
        if len(unused) > 200:
            print(f"  ... ({len(unused) - 200} more)")
    else:
        print("  OK: none")
    print()

    print("BIB HYGIENE WARNINGS (heuristics)")
    if hygiene:
        for w in hygiene:
            print(f"  - {w}")
    else:
        print("  OK: none detected")
    print()

    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
