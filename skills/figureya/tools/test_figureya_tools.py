import csv
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


class FigureYaToolTests(unittest.TestCase):
    def _write_zip(self, directory: Path, name: str, members: dict[str, str]) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        zip_path = directory / f"{name}.zip"
        with zipfile.ZipFile(zip_path, "w") as archive:
            for member_name, content in members.items():
                archive.writestr(member_name, content)
        return zip_path

    def test_extract_all_archives_expands_nested_template_zips(self):
        import extract_all_templates

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "zips"
            destination = root / "templates"
            self._write_zip(source, "FigureYa101PCA", {"FigureYa101PCA/FigureYa101PCA.Rmd": "# PCA\n"})
            self._write_zip(source, "FigureYa102ROC", {"FigureYa102ROC/FigureYa102ROC.Rmd": "# ROC\n"})

            extracted = extract_all_templates.extract_all(source, destination)

            self.assertEqual(len(extracted), 2)
            self.assertTrue((destination / "FigureYa101PCA" / "FigureYa101PCA.Rmd").exists())
            self.assertTrue((destination / "FigureYa102ROC" / "FigureYa102ROC.Rmd").exists())

    def test_scan_extracted_scripts_extracts_script_metadata(self):
        import build_manifest

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template = root / "FigureYa101PCA"
            template.mkdir()
            (template / "FigureYa101PCA.Rmd").write_text(
                "---\n"
                "title: \"FigureYa101PCA\"\n"
                "---\n"
                "## 需求描述 Requirement description\n"
                "RNA-seq PCA plot for grouped samples.\n"
                "```{r}\nlibrary(ggplot2)\n```\n",
                encoding="utf-8",
            )
            (template / "FigureYa101PCA.html").write_text("<h1>PCA</h1>", encoding="utf-8")
            (template / "example.png").write_text("png", encoding="utf-8")
            (template / "install_dependencies.R").write_text("install.packages('ggplot2')", encoding="utf-8")
            (template / "easy_input_expr.csv").write_text("gene,s1\nA,1\n", encoding="utf-8")

            records = build_manifest.scan_extracted_scripts(root)

        tutorial_records = [row for row in records if row["script_role"] == "tutorial"]
        self.assertEqual(len(tutorial_records), 1)
        record = tutorial_records[0]
        self.assertEqual(record["template_id"], "101")
        self.assertEqual(record["template_name"], "PCA")
        self.assertEqual(record["script_kind"], "Rmd")
        self.assertEqual(record["script_relpath"], "FigureYa101PCA/FigureYa101PCA.Rmd")
        self.assertTrue(record["script_path"].endswith("FigureYa101PCA/FigureYa101PCA.Rmd"))
        self.assertEqual(record["title"], "FigureYa101PCA")
        self.assertIn("RNA-seq PCA", record["requirement"])
        self.assertTrue(record["companion_html"].endswith("FigureYa101PCA.html"))
        self.assertTrue(record["example_png"].endswith("example.png"))
        self.assertTrue(record["install_dependencies_file"].endswith("install_dependencies.R"))
        self.assertEqual(record["input_file_count"], "1")
        self.assertIn("pca", record["tags"])

    def test_scan_extracted_scripts_reads_docs_and_builds_chain(self):
        import build_manifest

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template = root / "FigureYa999Chain"
            template.mkdir()
            (template / "README.md").write_text(
                "# Chain demo\n\nThis module first computes PCA scores, then plots them.\n",
                encoding="utf-8",
            )
            (template / "FigureYa999Chain_step1.Rmd").write_text(
                "---\ntitle: \"Chain step 1\"\n---\n"
                "## 需求描述 Requirement description\n"
                "Compute PCA scores from expression data.\n"
                "```{r}\n"
                "library(ggplot2)\n"
                "expr <- read.csv('easy_input_expr.csv')\n"
                "write.csv(expr, 'pca_scores.csv')\n"
                "```\n",
                encoding="utf-8",
            )
            (template / "FigureYa999Chain_step2.R").write_text(
                "library(ggplot2)\n"
                "plot_scores <- function(path) {\n"
                "  scores <- read.csv('pca_scores.csv')\n"
                "  ggsave('pca_plot.pdf')\n"
                "}\n",
                encoding="utf-8",
            )
            (template / "easy_input_expr.csv").write_text("gene,s1\nA,1\n", encoding="utf-8")

            records = build_manifest.scan_extracted_scripts(root)

        by_relpath = {row["script_relpath"]: row for row in records}
        doc = by_relpath["FigureYa999Chain/README.md"]
        step1 = by_relpath["FigureYa999Chain/FigureYa999Chain_step1.Rmd"]
        step2 = by_relpath["FigureYa999Chain/FigureYa999Chain_step2.R"]

        self.assertEqual(doc["script_role"], "documentation")
        self.assertIn("first computes PCA", doc["purpose"])
        self.assertIn("Compute PCA scores", step1["purpose"])
        self.assertIn("ggplot2", step1["packages"])
        self.assertIn("easy_input_expr.csv", step1["input_references"])
        self.assertIn("pca_scores.csv", step1["output_references"])
        self.assertIn("plot_scores", step2["functions_defined"])
        self.assertIn("pca_scores.csv", step2["input_references"])
        self.assertIn("pca_plot.pdf", step2["output_references"])
        self.assertIn("FigureYa999Chain/FigureYa999Chain_step2.R", step1["downstream_scripts"])
        self.assertIn("FigureYa999Chain/FigureYa999Chain_step1.Rmd", step2["upstream_scripts"])
        self.assertEqual(step1["chain_position"], "1")
        self.assertEqual(step2["chain_position"], "2")
        self.assertIn("FigureYa999Chain/README.md", step1["related_docs"])

    def test_search_manifest_matches_script_paths_and_tags(self):
        import build_manifest
        import search_figureya_templates

        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.csv"
            with manifest_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=build_manifest.FIELDNAMES)
                writer.writeheader()
                writer.writerow(
                    {
                        "template_id": "101",
                        "template_name": "PCA",
                        "template_dir": "FigureYa101PCA",
                        "script_role": "tutorial",
                        "script_kind": "Rmd",
                        "script_name": "FigureYa101PCA.Rmd",
                        "script_relpath": "FigureYa101PCA/FigureYa101PCA.Rmd",
                        "script_path": "/tmp/FigureYa101PCA/FigureYa101PCA.Rmd",
                        "script_size_bytes": "100",
                        "title": "FigureYa101PCA",
                        "requirement": "RNA-seq PCA plot for grouped samples",
                        "companion_html": "/tmp/FigureYa101PCA/FigureYa101PCA.html",
                        "example_png": "/tmp/FigureYa101PCA/example.png",
                        "install_dependencies_file": "/tmp/FigureYa101PCA/install_dependencies.R",
                        "input_file_count": "1",
                        "input_files_preview": "/tmp/FigureYa101PCA/easy_input_expr.csv",
                        "tags": "pca;dimension-reduction;omics;figureya",
                    }
                )

            matches = search_figureya_templates.search_manifest(manifest_path, "dimension reduction")

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["template_id"], "101")
        self.assertEqual(matches[0]["script_relpath"], "FigureYa101PCA/FigureYa101PCA.Rmd")

    def test_search_manifest_prioritizes_specific_query_terms(self):
        import build_manifest
        import search_figureya_templates

        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.csv"
            with manifest_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=build_manifest.FIELDNAMES)
                writer.writeheader()
                base = {
                    "template_dir": "",
                    "script_role": "tutorial",
                    "script_kind": "Rmd",
                    "script_name": "x.Rmd",
                    "script_size_bytes": "100",
                    "title": "",
                    "requirement": "",
                    "companion_html": "",
                    "example_png": "",
                    "install_dependencies_file": "",
                    "input_file_count": "0",
                    "input_files_preview": "",
                }
                writer.writerow(
                    {
                        **base,
                        "template_id": "226",
                        "template_name": "scRNA_cNMF",
                        "script_relpath": "FigureYa226scRNA_cNMF/scripts/s3-vis_cNMF.Rmd",
                        "script_path": "/tmp/FigureYa226scRNA_cNMF/scripts/s3-vis_cNMF.Rmd",
                        "tags": "figureya;omics;scrna-seq;single-cell",
                    }
                )
                writer.writerow(
                    {
                        **base,
                        "template_id": "166",
                        "template_name": "scCNV",
                        "script_relpath": "FigureYa166scCNV/FigureYa166scCNV.Rmd",
                        "script_path": "/tmp/FigureYa166scCNV/FigureYa166scCNV.Rmd",
                        "tags": "cancer-genomics;cnv;figureya;omics;single-cell",
                    }
                )

            matches = search_figureya_templates.search_manifest(manifest_path, "single cell CNV")

        self.assertGreaterEqual(len(matches), 2)
        self.assertEqual(matches[0]["template_name"], "scCNV")


if __name__ == "__main__":
    unittest.main()