#!/usr/bin/env python3
import argparse
import csv
import json
import re
from collections import defaultdict
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

SCRIPT_KINDS = {
    ".rmd": "Rmd",
    ".r": "R",
    ".py": "Python",
    ".ipynb": "Notebook",
    ".sh": "Shell",
    ".java": "Java",
    ".jl": "Julia",
    ".md": "Markdown",
}

TAG_RULES = [
    ("pca", "pca;dimension-reduction;omics"),
    ("umap", "umap;dimension-reduction;single-cell"),
    ("tsne", "tsne;dimension-reduction;single-cell"),
    ("roc", "roc;diagnostic;model-evaluation"),
    ("gsea", "gsea;pathway;enrichment;omics"),
    ("fgsea", "gsea;pathway;enrichment;omics"),
    ("kegg", "kegg;pathway;enrichment;omics"),
    ("go", "go;pathway;enrichment;omics"),
    ("wgcna", "wgcna;network;coexpression;omics"),
    ("heatmap", "heatmap;matrix;omics"),
    ("volcano", "volcano;differential-expression;omics"),
    ("surv", "survival;clinical;prognosis"),
    ("cox", "survival;clinical;cox"),
    ("risk", "survival;clinical;risk-model"),
    ("nomogram", "nomogram;clinical;prediction"),
    ("mutation", "mutation;cancer-genomics;omics"),
    ("mutsig", "mutation;cancer-genomics;omics"),
    ("oncoplot", "mutation;cancer-genomics;omics"),
    ("cnv", "cnv;cancer-genomics;omics"),
    ("atac", "atac;epigenomics;omics"),
    ("chip", "chip-seq;epigenomics;omics"),
    ("methyl", "methylation;epigenomics;omics"),
    ("meth", "methylation;epigenomics;omics"),
    ("single", "single-cell;omics"),
    ("scrna", "single-cell;scrna-seq;omics"),
    ("sc", "single-cell;omics"),
    ("immune", "immunology;tumor-microenvironment;omics"),
    ("immuno", "immunology;tumor-microenvironment;omics"),
    ("tme", "tumor-microenvironment;immunology;omics"),
    ("gdsc", "drug-response;pharmacogenomics;cancer"),
    ("cmap", "drug-response;connectivity-map;cancer"),
    ("box", "boxplot;distribution;visualization"),
    ("violin", "violin;distribution;visualization"),
    ("bubble", "bubble;visualization"),
    ("circos", "circos;genomics;visualization"),
    ("venn", "venn;set;visualization"),
    ("lollipop", "lollipop;mutation;visualization"),
    ("forest", "forest;clinical;visualization"),
    ("cor", "correlation;statistics;visualization"),
]

REFERENCE_EXTENSIONS = (
    ".csv",
    ".txt",
    ".tsv",
    ".xlsx",
    ".xls",
    ".rds",
    ".rda",
    ".rdata",
    ".gmt",
    ".gct",
    ".cls",
    ".grp",
    ".bed",
    ".bedgraph",
    ".mtx",
    ".h5ad",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".html",
    ".r",
    ".rmd",
    ".py",
    ".ipynb",
    ".sh",
    ".java",
)


def unique_join(values: list[str]) -> str:
    normalized = []
    for value in values:
        value = value.strip()
        if value and value not in normalized:
            normalized.append(value)
    return ";".join(normalized)


def parse_template_dir(template_dir: Path) -> tuple[str, str]:
    match = re.match(r"FigureYa(\d+)(.+)$", template_dir.name)
    if not match:
        return "", template_dir.name
    template_id, raw_name = match.groups()
    return template_id, raw_name.strip("_- ") or template_dir.name


def script_kind(path: Path) -> str:
    return SCRIPT_KINDS.get(path.suffix.lower(), "")


def script_role(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if suffix == ".md":
        return "documentation"
    if name == "install_dependencies.r":
        return "dependency"
    if suffix in {".rmd", ".ipynb"}:
        return "tutorial"
    if suffix == ".sh":
        return "shell"
    return "helper"


def read_text_excerpt(path: Path, max_bytes: int = 262144) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
    except OSError:
        return ""
    return data.decode("utf-8", errors="ignore")


def notebook_text(path: Path) -> str:
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return ""
    chunks = []
    for cell in notebook.get("cells", [])[:60]:
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        chunks.append(source)
    return "\n".join(chunks)


def script_text(path: Path) -> str:
    if path.suffix.lower() == ".ipynb":
        return notebook_text(path)
    return read_text_excerpt(path)


def extract_title(path: Path, text: str, template_name: str) -> str:
    match = re.search(r"(?im)^title:\s*[\"']?([^\"'\n]+)", text)
    if match:
        return match.group(1).strip()
    markdown_heading = re.search(r"(?m)^#\s+(.+)$", text)
    if markdown_heading:
        return markdown_heading.group(1).strip().strip("`*")
    roxygen_title = re.search(r"(?m)^#'\s*@title\s+(.+)$", text)
    if roxygen_title:
        return roxygen_title.group(1).strip()
    return f"FigureYa {template_name}" if template_name else path.stem


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip().strip("#").strip("/* ").strip()).strip()


def first_paragraph(text: str, skip_title: bool = True) -> str:
    collected = []
    for raw_line in text.splitlines():
        line = clean_line(raw_line)
        if not line or line in {"---", "```"}:
            if collected:
                break
            continue
        if skip_title and line.lower().startswith("title:"):
            continue
        if skip_title and raw_line.lstrip().startswith("#"):
            continue
        if line.startswith("!") or line.startswith("["):
            continue
        collected.append(line)
        if len(" ".join(collected)) > 300:
            break
    return " ".join(collected)[:500]


def extract_requirement(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        lowered = line.lower()
        if "需求描述" in line or "requirement" in lowered:
            collected = []
            for next_line in lines[index + 1 : index + 16]:
                stripped = clean_line(next_line)
                if not stripped:
                    continue
                if stripped.startswith("---") or stripped.startswith("```"):
                    break
                if stripped.startswith("##") and collected:
                    break
                collected.append(stripped)
            return " ".join(collected)[:700]
    return ""


def extract_packages(path: Path, text: str) -> list[str]:
    packages = []
    suffix = path.suffix.lower()
    if suffix in {".r", ".rmd"}:
        packages.extend(re.findall(r"\b(?:library|require)\s*\(\s*[\"']?([A-Za-z][\w.]*)", text))
        packages.extend(re.findall(r"\b([A-Za-z][\w.]*)::", text))
        packages.extend(re.findall(r"install\.packages\s*\(\s*[\"']([^\"']+)", text))
    elif suffix == ".py":
        packages.extend(re.findall(r"(?m)^\s*import\s+([A-Za-z_][\w.]*)", text))
        packages.extend(re.findall(r"(?m)^\s*from\s+([A-Za-z_][\w.]*)\s+import", text))
    elif suffix == ".ipynb":
        packages.extend(re.findall(r"\b(?:library|require)\s*\(\s*[\"']?([A-Za-z][\w.]*)", text))
        packages.extend(re.findall(r"(?m)^\s*import\s+([A-Za-z_][\w.]*)", text))
        packages.extend(re.findall(r"(?m)^\s*from\s+([A-Za-z_][\w.]*)\s+import", text))
    elif suffix == ".java":
        packages.extend(re.findall(r"(?m)^\s*import\s+([A-Za-z_][\w.]*);", text))
    return [package.split(".")[0] for package in packages]


def extract_functions(path: Path, text: str) -> list[str]:
    suffix = path.suffix.lower()
    functions = []
    if suffix in {".r", ".rmd"}:
        functions.extend(re.findall(r"(?m)^\s*([A-Za-z.][\w.]*)\s*(?:<-|=)\s*function\s*\(", text))
    elif suffix in {".py", ".ipynb"}:
        functions.extend(re.findall(r"(?m)^\s*def\s+([A-Za-z_][\w]*)\s*\(", text))
    elif suffix == ".sh":
        functions.extend(re.findall(r"(?m)^\s*([A-Za-z_][\w.-]*)\s*\(\)\s*\{", text))
    elif suffix == ".java":
        functions.extend(re.findall(r"(?m)\bclass\s+([A-Za-z_][\w]*)", text))
    return functions


def quoted_file_candidates(text: str) -> list[str]:
    candidates = []
    for quoted in re.findall(r"[\"']([^\"']+)[\"']", text):
        lowered = quoted.lower()
        if lowered.endswith(REFERENCE_EXTENSIONS) or Path(quoted).name.lower().startswith(("easy_input", "input_", "output_")):
            candidates.append(quoted)
    return candidates


def extract_io_references(text: str) -> tuple[list[str], list[str]]:
    inputs = []
    outputs = []
    input_patterns = [
        r"\b(?:read\.csv|read\.table|read\.delim|read_tsv|read_csv|fread|readRDS|read_excel|load|source)\s*\([^\n]*?[\"']([^\"']+)[\"']",
        r"\b(?:scanpy\.read|sc\.read|open)\s*\([^\n]*?[\"']([^\"']+)[\"']",
    ]
    output_patterns = [
        r"\b(?:write\.csv|write\.table|write_tsv|write_csv|writeLines|saveRDS|save|ggsave|pdf|png|jpeg|tiff|sink)\s*\([^\n]*?[\"']([^\"']+)[\"']",
        r"\b(?:to_csv|savefig|write_h5ad)\s*\([^\n]*?[\"']([^\"']+)[\"']",
    ]
    for pattern in input_patterns:
        inputs.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    for pattern in output_patterns:
        outputs.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    for candidate in quoted_file_candidates(text):
        basename = Path(candidate).name.lower()
        if candidate not in outputs and (basename.startswith(("output_", "result_")) or basename.endswith((".pdf", ".png", ".jpg", ".jpeg", ".html"))):
            outputs.append(candidate)
        elif candidate not in inputs and candidate not in outputs:
            inputs.append(candidate)
    return inputs, outputs


def chain_position(path: Path) -> str:
    text = str(path).lower()
    match = re.search(r"(?:step|part|stage|s)[_-]?(\d+)", text)
    if match:
        return str(int(match.group(1)))
    return ""


def first_existing(candidates: list[Path]) -> str:
    for candidate in candidates:
        if candidate.exists():
            return str(candidate.resolve())
    return ""


def companion_html_for(script_path: Path, template_dir: Path) -> str:
    same_stem = script_path.with_suffix(".html")
    if same_stem.exists():
        return str(same_stem.resolve())
    html_files = sorted(template_dir.rglob("*.html"), key=lambda path: (len(path.parts), str(path)))
    return str(html_files[0].resolve()) if html_files else ""


def template_companions(template_dir: Path) -> tuple[str, str, list[str], list[Path]]:
    example_png = first_existing([template_dir / "example.png"])
    if not example_png:
        png_files = sorted(template_dir.rglob("*.png"), key=lambda path: (len(path.parts), str(path)))
        example_png = str(png_files[0].resolve()) if png_files else ""
    install_dependencies = first_existing([template_dir / "install_dependencies.R"])
    input_files = sorted(
        [
            path
            for path in template_dir.rglob("*")
            if path.is_file() and path.name.lower().startswith(("easy_input", "input_", "example_input"))
        ],
        key=lambda path: str(path),
    )
    docs = sorted([path for path in template_dir.rglob("*.md") if path.is_file()], key=lambda path: str(path))
    return example_png, install_dependencies, [str(path.resolve()) for path in input_files], docs


def build_tags(template_name: str, script_relpath: str, title: str, requirement: str, purpose: str, packages: str) -> str:
    haystack = " ".join([template_name, script_relpath, title, requirement, purpose, packages]).lower()
    tags = {"figureya"}
    for needle, tag_string in TAG_RULES:
        if needle in haystack:
            tags.update(tag_string.split(";"))
    return ";".join(sorted(tags))


def iter_template_dirs(root: Path) -> list[Path]:
    return sorted([path for path in Path(root).iterdir() if path.is_dir() and path.name.startswith("FigureYa")], key=lambda path: path.name.lower())


def iter_script_files(template_dir: Path) -> list[Path]:
    return sorted(
        [path for path in template_dir.rglob("*") if path.is_file() and path.suffix.lower() in SCRIPT_KINDS],
        key=lambda path: str(path.relative_to(template_dir)).lower(),
    )


def infer_purpose(role: str, title: str, requirement: str, paragraph: str, functions: str, packages: str) -> str:
    if role == "documentation":
        return paragraph or title
    if requirement:
        return requirement
    if role == "dependency":
        return f"Install dependency packages: {packages}" if packages else "Install dependency packages for the template."
    if functions:
        return f"Helper script defining functions: {functions}"
    return paragraph or title


def method_summary(packages: str, functions: str, inputs: str, outputs: str) -> str:
    parts = []
    if packages:
        parts.append(f"packages={packages}")
    if functions:
        parts.append(f"functions={functions}")
    if inputs:
        parts.append(f"inputs={inputs}")
    if outputs:
        parts.append(f"outputs={outputs}")
    return " | ".join(parts)[:1000]


def add_chain_links(records: list[dict[str, str]]) -> None:
    by_template: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in records:
        by_template[record["template_dir"]].append(record)

    for template_records in by_template.values():
        relpath_to_record = {record["script_relpath"]: record for record in template_records}
        output_to_scripts: dict[str, set[str]] = defaultdict(set)
        script_basenames: dict[str, set[str]] = defaultdict(set)
        for record in template_records:
            basename = Path(record["script_relpath"]).name
            script_basenames[basename].add(record["script_relpath"])
            for output_ref in record["output_references"].split(";"):
                if output_ref:
                    output_to_scripts[Path(output_ref).name].add(record["script_relpath"])

        upstream: dict[str, set[str]] = defaultdict(set)
        downstream: dict[str, set[str]] = defaultdict(set)
        for record in template_records:
            current = record["script_relpath"]
            for input_ref in record["input_references"].split(";"):
                if not input_ref:
                    continue
                ref_name = Path(input_ref).name
                for producer in output_to_scripts.get(ref_name, set()):
                    if producer != current:
                        upstream[current].add(producer)
                        downstream[producer].add(current)
                for source_script in script_basenames.get(ref_name, set()):
                    if source_script != current:
                        upstream[current].add(source_script)
                        downstream[source_script].add(current)

        by_position: dict[int, list[dict[str, str]]] = defaultdict(list)
        for record in template_records:
            if record["chain_position"].isdigit() and record["script_role"] not in {"documentation", "dependency"}:
                by_position[int(record["chain_position"])].append(record)
        positions = sorted(by_position)
        for previous_position, following_position in zip(positions, positions[1:]):
            if following_position <= previous_position:
                continue
            for previous in by_position[previous_position]:
                previous_path = previous["script_relpath"]
                for following in by_position[following_position]:
                    following_path = following["script_relpath"]
                    if previous_path != following_path:
                        downstream[previous_path].add(following_path)
                        upstream[following_path].add(previous_path)

        doc_paths = [record["script_relpath"] for record in template_records if record["script_role"] == "documentation"]
        for record in template_records:
            relpath = record["script_relpath"]
            record["upstream_scripts"] = unique_join(sorted(upstream.get(relpath, set())))
            record["downstream_scripts"] = unique_join(sorted(downstream.get(relpath, set())))
            if record["script_role"] != "documentation":
                record["related_docs"] = unique_join(doc_paths)
            relpath_to_record[relpath] = record


def scan_extracted_scripts(root: Path) -> list[dict[str, str]]:
    root = Path(root)
    records = []
    for template_dir in iter_template_dirs(root):
        template_id, template_name = parse_template_dir(template_dir)
        example_png, install_dependencies, input_files, docs = template_companions(template_dir)
        doc_relpaths = [str(path.relative_to(root)) for path in docs]
        for script_path in iter_script_files(template_dir):
            text = script_text(script_path)
            relpath = str(script_path.relative_to(root))
            title = extract_title(script_path, text, template_name)
            requirement = extract_requirement(text)
            packages = unique_join(sorted(set(extract_packages(script_path, text))))
            functions = unique_join(sorted(set(extract_functions(script_path, text))))
            inputs, outputs = extract_io_references(text)
            input_refs = unique_join(inputs)
            output_refs = unique_join(outputs)
            role = script_role(script_path)
            paragraph = first_paragraph(text)
            purpose = infer_purpose(role, title, requirement, paragraph, functions, packages)
            record = {
                "template_id": template_id,
                "template_name": template_name,
                "template_dir": template_dir.name,
                "script_role": role,
                "script_kind": script_kind(script_path),
                "script_name": script_path.name,
                "script_relpath": relpath,
                "script_path": str(script_path.resolve()),
                "script_size_bytes": str(script_path.stat().st_size),
                "title": title,
                "requirement": requirement,
                "purpose": purpose,
                "method_summary": method_summary(packages, functions, input_refs, output_refs),
                "packages": packages,
                "functions_defined": functions,
                "input_references": input_refs,
                "output_references": output_refs,
                "chain_position": chain_position(script_path),
                "upstream_scripts": "",
                "downstream_scripts": "",
                "related_docs": unique_join(doc_relpaths) if role != "documentation" else "",
                "companion_html": companion_html_for(script_path, template_dir),
                "example_png": example_png,
                "install_dependencies_file": install_dependencies,
                "input_file_count": str(len(input_files)),
                "input_files_preview": "|".join(input_files[:12]),
                "tags": "",
            }
            record["tags"] = build_tags(template_name, relpath, title, requirement, purpose, packages)
            records.append(record)
    add_chain_links(records)
    return records


def write_manifest(records: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a content-aware FigureYa manifest from extracted template directories.")
    parser.add_argument("root", type=Path, help="Directory containing extracted FigureYa### template directories")
    parser.add_argument("output", type=Path, help="CSV manifest output path")
    args = parser.parse_args()
    records = scan_extracted_scripts(args.root)
    write_manifest(records, args.output)
    print(f"Wrote {len(records)} content-aware records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())