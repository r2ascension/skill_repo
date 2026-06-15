#!/usr/bin/env python3
"""
check_tex.py - Heuristic LaTeX manuscript checker for statistical writing norms.

This script is intentionally lightweight: it uses regex + simple heuristics to flag
common issues in statistical manuscripts. It does not require LaTeX compilation.

Checks (heuristics)
- Abstract: sentence count (target 4-10; default 6-8), citations, math notation
- Keywords: alphabetical order, duplicates/redundancy, overlap with title terms
- Cross-referencing: duplicate labels, undefined refs, unused labels, label prefix convention
- Figures/tables: missing caption/label inside float blocks (best-effort)
- Review draft quality: line-number detection, raster image warnings
- Style annoyances: manual hard-coded "Figure 2" style refs, equation punctuation heuristic
- Writing cues: reproducibility/supplement statement presence
- Citation style hints: citep/citet usage balance
- English/unicode flags: "data is", significant wording, unicode minus/dash characters

Usage
  python check_tex.py path/to/main.tex

Exit codes
  0: no high-severity findings
  1: file/argument error
  2: high-severity findings detected
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Set


# --- regex helpers ---
COMMENT_RE = re.compile(r"(?<!\\)%.*$", re.MULTILINE)
INPUT_RE = re.compile(r"\\(input|include)\{([^}]+)\}")
TITLE_RE = re.compile(r"\\title\{([\s\S]*?)\}", re.MULTILINE)
ABSTRACT_ENV_RE = re.compile(r"\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}", re.MULTILINE)
ABSTRACT_CMD_RE = re.compile(r"\\abstract\{([\s\S]*?)\}", re.MULTILINE)
KEYWORDS_RE = re.compile(r"\\keywords\{([\s\S]*?)\}", re.MULTILINE)

CITE_CMD_RE = re.compile(
    r"""\\(cite[a-zA-Z*]*)\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}""",
    re.MULTILINE,
)

LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(ref|eqref|autoref|nameref)\{([^}]+)\}")

FIG_ENV_RE = re.compile(r"\\begin\{figure\*?\}([\s\S]*?)\\end\{figure\*?\}", re.MULTILINE)
TAB_ENV_RE = re.compile(r"\\begin\{table\*?\}([\s\S]*?)\\end\{table\*?\}", re.MULTILINE)
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")

LINENO_PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{lineno\}")
LINENO_ENABLE_RE = re.compile(r"\\linenumbers\*?(?:\[[^\]]*\])?")

MANUAL_REF_RE = re.compile(
    r"(?<!\\)(Figure|Table|Section|Equation|Eq\.)\s+\(?\d+(?:\.\d+)?\)?",
    re.IGNORECASE,
)

DISPLAY_EQ_RE = re.compile(
    r"(\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?|flalign\*?|alignat\*?)\}[\s\S]*?\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?|flalign\*?|alignat\*?)\}"
    r"|\\\[[\s\S]*?\\\]"
    r"|\$\$[\s\S]*?\$\$)",
    re.MULTILINE,
)

UNICODE_DASH_RE = re.compile(r"[\u2212\u2010\u2011\u2012\u2013\u2014]")

ALLOWED_PREFIXES = ("sec:", "fig:", "tab:", "eq:", "alg:", "app:")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
}


def strip_comments(tex: str) -> str:
    return re.sub(COMMENT_RE, "", tex)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def resolve_tex_path(root: Path, name: str) -> Path:
    p = Path(name)
    if p.is_absolute():
        if p.suffix == "":
            return p.with_suffix(".tex")
        return p
    if p.suffix == "":
        return (root / p).with_suffix(".tex")
    return root / p


def collect_tex_files(main_tex: Path, max_files: int = 300) -> List[Path]:
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


def extract_title(tex: str) -> str:
    m = TITLE_RE.search(tex)
    return m.group(1).strip() if m else ""


def extract_abstract(tex: str) -> str:
    m = ABSTRACT_ENV_RE.search(tex)
    if m:
        return m.group(1).strip()
    m = ABSTRACT_CMD_RE.search(tex)
    if m:
        return m.group(1).strip()
    return ""


def extract_keywords(tex: str) -> str:
    m = KEYWORDS_RE.search(tex)
    return m.group(1).strip() if m else ""


def split_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def analyze_abstract(abstract: str) -> List[str]:
    warnings: List[str] = []
    if not abstract:
        warnings.append("HIGH: No abstract found.")
        return warnings

    sents = split_sentences(abstract)
    n_sent = len(sents)
    if n_sent < 4:
        warnings.append(f"HIGH: Abstract too short ({n_sent} sentences). Target 4-10.")
    elif n_sent > 10:
        warnings.append(f"HIGH: Abstract too long ({n_sent} sentences). Target 4-10.")
    elif n_sent < 6 or n_sent > 8:
        warnings.append(f"LOW: Abstract has {n_sent} sentences (default sweet spot is 6-8).")

    if CITE_CMD_RE.search(abstract):
        warnings.append("HIGH: Abstract contains citation commands (remove citations from abstract).")
    if re.search(r"\$|\\\(|\\\)|\\\[|\\\]|\\begin\{equation", abstract):
        warnings.append("HIGH: Abstract appears to contain math notation (replace with words).")
    return warnings


def _keyword_parts(keywords: str) -> List[str]:
    return [kw.strip() for kw in re.split(r"[;,]", keywords) if kw.strip()]


def analyze_keywords(keywords: str, title: str) -> List[str]:
    warnings: List[str] = []
    if not keywords:
        warnings.append("MED: No \\keywords{...} found.")
        return warnings

    parts = _keyword_parts(keywords)
    if len(parts) < 6:
        warnings.append(f"MED: Only {len(parts)} keywords detected (recommended 6-10).")
    elif len(parts) > 10:
        warnings.append(f"MED: {len(parts)} keywords detected (recommended 6-10).")

    sorted_parts = sorted(parts, key=lambda s: s.lower())
    if parts != sorted_parts:
        warnings.append("MED: Keywords are not in alphabetical order.")

    lower_parts = [p.lower() for p in parts]
    dup_parts = sorted({p for p in lower_parts if lower_parts.count(p) > 1})
    if dup_parts:
        warnings.append("MED: Duplicate keywords detected: " + ", ".join(dup_parts))

    # overlap with title words
    title_words = set(re.sub(r"[^A-Za-z\\s]", " ", title).lower().split())
    overlaps: List[str] = []
    for kw in parts:
        for w in re.sub(r"[^A-Za-z\\s]", " ", kw).lower().split():
            if w in title_words and w not in STOP_WORDS:
                overlaps.append(kw)
                break
    if overlaps:
        warnings.append(
            "LOW: Some keywords overlap title terms (consider replacing): "
            + ", ".join(sorted(set(overlaps)))
        )

    # redundancy across keywords (same token repeated in 3+ phrases)
    token_counts: Dict[str, int] = {}
    for kw in parts:
        seen_in_kw: Set[str] = set()
        for tok in re.sub(r"[^A-Za-z\\s]", " ", kw).lower().split():
            if tok in STOP_WORDS:
                continue
            if tok not in seen_in_kw:
                token_counts[tok] = token_counts.get(tok, 0) + 1
                seen_in_kw.add(tok)
    repetitive = sorted([k for k, v in token_counts.items() if v >= 3])
    if repetitive:
        warnings.append(
            "LOW: Keyword set appears redundant; repeated token(s) in >=3 keywords: "
            + ", ".join(repetitive)
        )

    return warnings


def analyze_language(tex: str) -> List[str]:
    warnings: List[str] = []
    if re.search(r"\bdata\s+(is|was|has)\b", tex, re.IGNORECASE):
        warnings.append("LOW: 'data' appears used as singular (prefer 'data are').")

    for m in re.finditer(r"\bsignificant\b", tex, re.IGNORECASE):
        ctx = tex[max(0, m.start() - 40) : m.start()].lower()
        if "statistically" not in ctx:
            warnings.append(
                "LOW: 'significant' appears without 'statistically' nearby (confirm intended meaning)."
            )
            break

    bad_dash_chars = sorted(set(UNICODE_DASH_RE.findall(tex)))
    if bad_dash_chars:
        warnings.append(
            "LOW: Unicode minus/dash characters detected (use math mode for minus and ASCII hyphen where appropriate): "
            + " ".join(bad_dash_chars)
        )

    return warnings


def analyze_refs(tex: str) -> List[str]:
    warnings: List[str] = []
    labels = [m.group(1).strip() for m in LABEL_RE.finditer(tex)]
    refs = [m.group(2).strip() for m in REF_RE.finditer(tex)]

    counts: Dict[str, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    dups = sorted([k for k, v in counts.items() if v > 1])
    if dups:
        warnings.append("HIGH: Duplicate labels detected: " + ", ".join(dups[:50]) + (" ..." if len(dups) > 50 else ""))

    label_set = set(labels)
    ref_set = set(refs)

    undefined = sorted(ref_set - label_set)
    if undefined:
        warnings.append(
            "HIGH: References to undefined labels: "
            + ", ".join(undefined[:50])
            + (" ..." if len(undefined) > 50 else "")
        )

    unused = sorted(label_set - ref_set)
    if unused:
        warnings.append(
            "MED: Labels defined but never referenced: "
            + ", ".join(unused[:50])
            + (" ..." if len(unused) > 50 else "")
        )

    bad_prefix = sorted([label for label in label_set if not label.startswith(ALLOWED_PREFIXES)])
    if bad_prefix:
        warnings.append(
            "LOW: Labels not following prefix convention (sec:/fig:/tab:/eq:/alg:/app:): "
            + ", ".join(bad_prefix[:50])
            + (" ..." if len(bad_prefix) > 50 else "")
        )

    manual_refs = MANUAL_REF_RE.findall(tex)
    if manual_refs:
        warnings.append(
            "LOW: Hard-coded references like 'Figure 2' detected; prefer dynamic refs (Figure~\\ref{...})."
        )

    return warnings


def analyze_float_blocks(tex: str) -> List[str]:
    warnings: List[str] = []
    figs = FIG_ENV_RE.findall(tex)
    for i, body in enumerate(figs, start=1):
        if "\\caption" not in body:
            warnings.append(f"MED: Figure block {i} appears missing \\caption{{...}}.")
        if "\\label" not in body:
            warnings.append(f"MED: Figure block {i} appears missing \\label{{...}}.")

    tabs = TAB_ENV_RE.findall(tex)
    for i, body in enumerate(tabs, start=1):
        if "\\caption" not in body:
            warnings.append(f"MED: Table block {i} appears missing \\caption{{...}}.")
        if "\\label" not in body:
            warnings.append(f"MED: Table block {i} appears missing \\label{{...}}.")

    raster_hits: List[str] = []
    for m in INCLUDEGRAPHICS_RE.finditer(tex):
        path = m.group(1).strip()
        ext = Path(path).suffix.lower()
        if ext in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
            raster_hits.append(path)
    if raster_hits:
        uniq = sorted(set(raster_hits))
        warnings.append(
            "MED: Raster figure files detected (consider vector formats for line graphics): "
            + ", ".join(uniq[:20])
            + (" ..." if len(uniq) > 20 else "")
        )

    return warnings


def analyze_line_numbers(tex: str) -> List[str]:
    warnings: List[str] = []
    has_lineno_pkg = bool(LINENO_PACKAGE_RE.search(tex))
    has_lineno_cmd = bool(LINENO_ENABLE_RE.search(tex))

    if not has_lineno_pkg:
        warnings.append("MED: Line-number package not detected (recommended for review drafts).")
    elif not has_lineno_cmd:
        warnings.append("MED: 'lineno' package found, but line numbering command not detected.")

    return warnings


def analyze_reproducibility_cues(tex: str) -> List[str]:
    warnings: List[str] = []
    lower = tex.lower()
    cues = [
        "reproduc",
        "supplement",
        "supplementary",
        "code availability",
        "data availability",
        "github",
        "zenodo",
        "osf",
    ]
    if not any(c in lower for c in cues):
        warnings.append(
            "MED: No reproducibility/supplement cue detected (consider code/data/supplement availability statement)."
        )
    return warnings


def analyze_equation_punctuation(tex: str) -> List[str]:
    warnings: List[str] = []
    suspect_count = 0
    for m in DISPLAY_EQ_RE.finditer(tex):
        tail = tex[m.end() :]
        if not tail:
            continue
        stripped = tail.lstrip()
        if not stripped:
            continue
        first = stripped[0]
        if first not in ".,;:!?)]":
            # If the next token starts a command, this is still often punctuation-related,
            # but we only count clear word/digit starts to reduce false positives.
            if first.isalnum():
                suspect_count += 1
    if suspect_count:
        warnings.append(
            f"LOW: {suspect_count} displayed equation block(s) may be missing sentence punctuation after the equation."
        )
    return warnings


def analyze_citation_style(tex: str) -> List[str]:
    warnings: List[str] = []
    commands: List[str] = []
    total_keys = 0
    for m in CITE_CMD_RE.finditer(tex):
        commands.append(m.group(1).lower())
        total_keys += len([k for k in m.group(2).split(",") if k.strip()])

    if not commands:
        return warnings

    cmd_set = set(commands)
    uses_citep = any(c.startswith("citep") for c in cmd_set)
    uses_citet = any(c.startswith("citet") for c in cmd_set)
    uses_plain_cite = "cite" in cmd_set

    if uses_plain_cite and not (uses_citep or uses_citet):
        warnings.append("LOW: Only generic \\cite detected; consider explicit \\citep/\\citet for clearer narrative style.")

    if total_keys >= 5 and (uses_citep ^ uses_citet):
        warnings.append(
            "LOW: Citation style appears one-sided (mostly one of \\citep or \\citet); ensure textual vs parenthetical usage is intentional."
        )

    return warnings


def severity_rank(msg: str) -> int:
    if msg.startswith("HIGH:"):
        return 0
    if msg.startswith("MED:"):
        return 1
    if msg.startswith("LOW:"):
        return 2
    return 3


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python check_tex.py path/to/main.tex")
        return 1

    path = Path(sys.argv[1]).expanduser().resolve()
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    tex_files = collect_tex_files(path)
    combined = ""
    for p in tex_files:
        try:
            combined += "\n" + strip_comments(read_text(p))
        except Exception:
            continue

    title = extract_title(combined)
    abstract = extract_abstract(combined)
    keywords = extract_keywords(combined)

    findings: List[str] = []
    findings += analyze_abstract(abstract)
    findings += analyze_keywords(keywords, title)
    findings += analyze_refs(combined)
    findings += analyze_float_blocks(combined)
    findings += analyze_line_numbers(combined)
    findings += analyze_reproducibility_cues(combined)
    findings += analyze_equation_punctuation(combined)
    findings += analyze_citation_style(combined)
    findings += analyze_language(combined)

    print("check_tex report")
    print(f"  main: {path}")
    print(f"  scanned tex files: {len(tex_files)}")
    if title:
        print(f"  title: {title}")
    print()

    if not findings:
        print("OK: No issues detected by these heuristics.")
        return 0

    findings_sorted = sorted(findings, key=severity_rank)
    print("Findings:")
    for msg in findings_sorted:
        print(f"  - {msg}")
    print()

    high = any(msg.startswith("HIGH:") for msg in findings)
    return 2 if high else 0


if __name__ == "__main__":
    raise SystemExit(main())
