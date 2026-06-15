# Example wiring for single-cell-functional-activity helpers.
# Replace `seu` and file paths with project-specific inputs.

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

skill_root <- find_skill_root("single-cell-functional-activity")
source(file.path(skill_root, "R", "activity_common.R"))
source(file.path(skill_root, "R", "dorothea_viper.R"))
source(file.path(skill_root, "R", "progeny.R"))
source(file.path(skill_root, "R", "metabolism.R"))

# preflight_seurat_activity(seu, assay = "RNA", group_cols = c("celltype"))

# PROGENy example:
# seu <- run_progeny_activity(seu, assay_in = "RNA", organism = "Human", top = 500, perm = 1)
# seu <- scale_progeny_assay(seu)
# progeny_summary <- summarize_progeny_by_celltype(seu, celltype_col = "celltype")
# progeny_mat <- summary_to_activity_matrix(progeny_summary, feature_col = "pathway", group_col = "celltype", value_col = "mean")
# plot_activity_heatmap(progeny_mat, filename = "progeny_celltype_heatmap.pdf")

# Custom metabolism example:
# genesets <- read_pathway_gene_table("metabolic_pathways.csv", pathway_col = "pathway", gene_col = "gene")
# metab_scores <- run_metabolism_ssgsea(seu, genesets, assay = "RNA")
# seu <- attach_activity_assay(seu, metab_scores, assay_out = "METABOLISM", overwrite = TRUE)
