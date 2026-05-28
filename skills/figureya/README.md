# FigureYa Skill Assets

This directory turns the local FigureYa compressed template collection into an on-demand content-level skill.

## Current Assets

- `SKILL.md`: workflow instructions for future agents
- `figureya_manifest.csv`: lightweight index of 833 extracted script and documentation files
- `tools/build_manifest.py`: rebuilds the content-aware manifest from extracted `FigureYa###*` template folders
- `tools/extract_all_templates.py`: expands all nested `FigureYa*.zip` files before indexing scripts
- `tools/search_figureya_templates.py`: keyword search over the manifest
- `tools/extract_figureya_template.py`: safely extracts one selected template ZIP
- `tools/test_figureya_tools.py`: unit tests for the helper tools

## Extract All Templates

```bash
python3 tools/extract_all_templates.py \
  /home/h2048/temp/FigureYa_unpacked_20260508/FigureYa-compressed-main \
  /home/h2048/temp/FigureYa_templates_extracted_20260509
```

## Rebuild Manifest

```bash
python3 tools/build_manifest.py \
  /home/h2048/temp/FigureYa_templates_extracted_20260509 \
  figureya_manifest.csv
```

The manifest reads file contents for `.Rmd`, `.R`, `.py`, `.ipynb`, `.sh`, `.java`, and `.md` files. It records each file's inferred purpose, packages, defined functions, input/output references, and upstream/downstream links so agents can understand the workflow chain before adapting a template.

## Verify Tools

```bash
python3 tools/test_figureya_tools.py
python3 tools/search_figureya_templates.py figureya_manifest.csv "single cell CNV" --limit 3
```

## Notes

The large extracted template payload remains outside the skill directory at `/home/h2048/temp/FigureYa_templates_extracted_20260509`. The skill stores only the content-aware manifest and helper tools so it stays lightweight.
