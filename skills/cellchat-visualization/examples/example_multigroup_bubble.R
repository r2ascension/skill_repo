# Example multi-group CellChat bubble workflow.

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

skill_root <- find_skill_root("cellchat-visualization")
source(file.path(skill_root, "R", "cellchat_multigroup_bubble.R"))

# cellchat_list <- list(
#   Control = readRDS("Group_Control/Cellchat.rds"),
#   Treatment1 = readRDS("Group_Treatment1/Cellchat.rds"),
#   Treatment2 = readRDS("Group_Treatment2/Cellchat.rds")
# )
# target_celltype <- "CellType_A"
# role <- "source" # or "target"
# tables <- Map(function(obj, nm) extract_cellchat_bubble_data(obj, target_celltype, role = role, group = nm), cellchat_list, names(cellchat_list))
# merged <- merge_cellchat_bubble_tables(tables)
# filtered <- filter_cellchat_bubble_data(merged, top_pathways = 20, manual_pathways = c(), top_n_per_group = 30)
# p <- plot_multigroup_cellchat_bubble(filtered, group_levels = names(cellchat_list))
# dir.create("cellchat_multigroup", showWarnings = FALSE)
# save_cellchat_bubble_artifacts(filtered, "cellchat_multigroup", prefix = paste0("cellchat_", role))
# ggplot2::ggsave(file.path("cellchat_multigroup", paste0("cellchat_", role, "_bubble.pdf")), p, width = 12, height = 10, device = grDevices::cairo_pdf)
