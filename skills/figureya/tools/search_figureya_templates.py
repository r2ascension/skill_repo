#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path


FIELDNAMES = [
    "template_id",
    "template_name",
    "template_dir",
    "script_role",
    "script_kind",
    "script_name",
    "script_relpath",
    "script_path",
    "script_size_bytes",
    "title",
    "requirement",
    "purpose",
    "method_summary",
    "packages",
    "functions_defined",
    "input_references",
    "output_references",
    "chain_position",
    "upstream_scripts",
    "downstream_scripts",
    "related_docs",
    "companion_html",
    "example_png",
    "install_dependencies_file",
    "input_file_count",
    "input_files_preview",
    "tags",
]

SYNONYMS = {
    "dimension": ["pca", "umap", "tsne", "dimension-reduction"],
    "reduction": ["pca", "umap", "tsne", "dimension-reduction"],
    "survival": ["surv", "cox", "risk", "prognosis"],
    "pathway": ["gsea", "kegg", "go", "enrichment"],
    "single": ["single-cell", "scrna", "sc"],
    "singlecell": ["single-cell", "scrna", "sc"],
    "cell": ["single-cell", "scrna", "sc"],
}


def weighted_terms(query: str) -> list[tuple[str, int]]:
    raw_terms = re.findall(r"[a-zA-Z0-9_+-]+", query.lower())
    weights: dict[str, int] = {}
    for term in raw_terms:
        weights[term] = max(weights.get(term, 0), 5)
        for synonym in SYNONYMS.get(term, []):
            weights[synonym] = max(weights.get(synonym, 0), 1)
    return list(weights.items())


def score_row(row: dict[str, str], query_terms: list[tuple[str, int]]) -> int:
    haystack = " ".join(
        [
            row.get("template_name", ""),
            row.get("template_dir", ""),
            row.get("script_role", ""),
            row.get("script_kind", ""),
            row.get("script_name", ""),
            row.get("script_relpath", ""),
            row.get("title", ""),
            row.get("requirement", ""),
            row.get("purpose", ""),
            row.get("method_summary", ""),
            row.get("packages", ""),
            row.get("functions_defined", ""),
            row.get("input_references", ""),
            row.get("output_references", ""),
            row.get("upstream_scripts", ""),
            row.get("downstream_scripts", ""),
            row.get("related_docs", ""),
            row.get("tags", ""),
        ]
    ).lower().replace("_", "-")
    tag_text = row.get("tags", "").lower()
    name_text = " ".join([row.get("template_name", ""), row.get("script_name", ""), row.get("title", "")]).lower()
    score = 0
    for term, weight in query_terms:
        if term in haystack:
            if term in tag_text:
                score += weight * 3
            elif term in name_text:
                score += weight * 2
            else:
                score += weight
    if row.get("script_role") == "tutorial":
        score += 2
    elif row.get("script_role") == "dependency":
        score -= 2
    return score


def search_manifest(manifest_path: Path, query: str, limit: int = 12) -> list[dict[str, str]]:
    query_terms = weighted_terms(query)
    with Path(manifest_path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    scored = [(score_row(row, query_terms), row) for row in rows]
    matches = [row for score, row in sorted(scored, key=lambda item: (-item[0], item[1].get("script_relpath", ""))) if score > 0]
    return matches[:limit]


def print_markdown(rows: list[dict[str, str]]) -> None:
    print("| ID | Template | Role | Script | Purpose | Tags |")
    print("|---|---|---|---|---|---|")
    for row in rows:
        tags = row.get("tags", "").replace(";", ", ")
        script = row.get("script_path") or row.get("script_relpath", "")
        purpose = row.get("purpose", "")[:160].replace("|", "/")
        print(
            f"| {row.get('template_id', '')} | {row.get('template_name', '')} | "
            f"{row.get('script_role', '')}/{row.get('script_kind', '')} | {script} | {purpose} | {tags} |"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Search a FigureYa script-level manifest.")
    parser.add_argument("manifest", type=Path, help="Path to figureya_manifest.csv")
    parser.add_argument("query", help="Keyword query, e.g. 'PCA', 'survival risk', or 'single-cell CNV'")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()
    print_markdown(search_manifest(args.manifest, args.query, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())