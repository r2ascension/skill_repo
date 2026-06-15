# Example single-gene GSEA workflow.

find_skill_root <- function(skill_name) {
	candidates <- c(
		file.path(Sys.getenv("HOME"), ".copilot", "skills", skill_name),
		normalizePath(file.path(getwd(), ".."), mustWork = FALSE),
		getwd()
	)
	hits <- candidates[file.exists(file.path(candidates, "SKILL.md")) & basename(candidates) == skill_name]
	if (!length(hits)) stop("Cannot locate skill root for ", skill_name, call. = FALSE)
	normalizePath(hits[[1]], mustWork = TRUE)
}

skill_root <- find_skill_root("single-gene-gsea-plotting")
source(file.path(skill_root, "R", "single_gene_gsea_plotting.R"))

# expr <- read.csv("expression_matrix.csv", row.names = 1, check.names = FALSE)
# term2gene <- clusterProfiler::read.gmt("c2.cp.kegg.v7.4.symbols.gmt")
# target_gene <- "YOUR_TARGET_GENE"
# gene_list <- single_gene_correlation_rank(expr, target_gene, method = "spearman")
# gsea <- run_clusterprofiler_gsea(gene_list, term2gene, pvalue_cutoff = 1)
# selected <- select_gsea_pathways_by_nes(gsea, n = 10, p_cutoff = 0.25, nes_decreasing = TRUE)
# p <- plot_gsea_curves_nes_matched(gsea, selected, color_by = "Description")
# dir.create("single_gene_gsea", showWarnings = FALSE)
# utils::write.csv(as.data.frame(gsea), "single_gene_gsea/gsea_full_results.csv", row.names = FALSE)
# utils::write.csv(selected, "single_gene_gsea/gsea_selected_nes_ordered.csv", row.names = FALSE)
# utils::write.csv(attr(p, "color_map"), "single_gene_gsea/gsea_color_map.csv", row.names = FALSE)
# ggplot2::ggsave("single_gene_gsea/gsea_curves_nes_matched.pdf", p, width = 10, height = 12, device = grDevices::cairo_pdf)
