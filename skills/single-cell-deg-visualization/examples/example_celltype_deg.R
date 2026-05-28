# Example celltype-wise DEG workflow.

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

skill_root <- find_skill_root("single-cell-deg-visualization")
source(file.path(skill_root, "R", "celltype_deg_volcano.R"))

# result <- run_celltype_findmarkers(
#   obj = seurat_object,
#   celltype_col = "celltype",
#   group_col = "group",
#   ident_1 = "group1",
#   ident_2 = "group2",
#   min_cells_per_group = 20,
#   test_use = "wilcox"
# )
# deg <- label_deg_thresholds(result$deg, alpha = 0.05, logfc = 0.5)
# labels <- select_top_deg_labels(deg, n = 5)
# p <- plot_multicluster_volcano(deg, labels = labels)
# dir.create("celltype_deg", showWarnings = FALSE)
# utils::write.csv(deg, "celltype_deg/deg_merged.csv", row.names = FALSE)
# utils::write.csv(result$skipped, "celltype_deg/skipped_celltypes.csv", row.names = FALSE)
# ggplot2::ggsave("celltype_deg/multicluster_volcano.pdf", p, width = 12, height = 8, device = grDevices::cairo_pdf)
