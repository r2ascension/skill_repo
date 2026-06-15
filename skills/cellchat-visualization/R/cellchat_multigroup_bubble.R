# CellChat multi-group bubble plotting helpers.

.require_pkg <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) stop(sprintf("Package '%s' is required.", pkg), call. = FALSE)
  invisible(TRUE)
}

`%||%` <- function(x, y) if (is.null(x) || length(x) == 0 || is.na(x)) y else x

standard_empty_cellchat_table <- function(group = NA_character_) {
  data.frame(
    source = character(), target = character(), interaction_name = character(), pathway_name = character(),
    prob = numeric(), pval = numeric(), source_target = character(), group = character(), stringsAsFactors = FALSE
  )
}

extract_cellchat_bubble_data <- function(cellchat_obj, target_celltype, role = c("source", "target"), group = NULL, remove_isolate = FALSE) {
  role <- match.arg(role)
  .require_pkg("CellChat")
  if (!inherits(cellchat_obj, "CellChat")) stop("cellchat_obj must inherit from 'CellChat'.", call. = FALSE)
  idents <- tryCatch(as.character(unique(cellchat_obj@idents)), error = function(e) character())
  if (length(idents) && !target_celltype %in% idents) {
    warning(sprintf("Target cell type '%s' not found in group '%s'.", target_celltype, group %||% "unknown"), call. = FALSE)
    return(standard_empty_cellchat_table(group = group))
  }
  res <- if (role == "source") {
    CellChat::netVisual_bubble(cellchat_obj, sources.use = target_celltype, remove.isolate = remove_isolate, return.data = TRUE)
  } else {
    CellChat::netVisual_bubble(cellchat_obj, targets.use = target_celltype, remove.isolate = remove_isolate, return.data = TRUE)
  }
  df <- if (is.list(res) && "communication" %in% names(res)) res$communication else res
  standardize_cellchat_communication(df, group = group)
}

standardize_cellchat_communication <- function(df, group = NULL) {
  if (is.null(df) || !nrow(df)) return(standard_empty_cellchat_table(group = group))
  df <- as.data.frame(df, stringsAsFactors = FALSE)
  aliases <- list(
    source = c("source", "sources", "sender"),
    target = c("target", "targets", "receiver"),
    interaction_name = c("interaction_name", "interaction_name_2", "ligand.receptor", "pairLR"),
    pathway_name = c("pathway_name", "pathway", "pathway_name_2"),
    prob = c("prob", "weight", "value", "communication_probability"),
    pval = c("pval", "p.value", "p_val", "p_value")
  )
  pick <- function(keys) keys[keys %in% names(df)][1]
  out <- data.frame(stringsAsFactors = FALSE)
  for (nm in names(aliases)) {
    hit <- pick(aliases[[nm]])
    out[[nm]] <- if (!is.na(hit)) df[[hit]] else if (nm %in% c("prob", "pval")) NA_real_ else NA_character_
  }
  out$prob <- suppressWarnings(as.numeric(out$prob))
  out$pval <- suppressWarnings(as.numeric(out$pval))
  out$source_target <- paste0(out$source, " -> ", out$target)
  out$group <- as.character(group %||% "group")
  out <- out[!is.na(out$source) & !is.na(out$target) & !is.na(out$interaction_name), , drop = FALSE]
  out
}

merge_cellchat_bubble_tables <- function(named_tables) {
  .require_pkg("data.table")
  data.table::rbindlist(named_tables, fill = TRUE, use.names = TRUE)
}

filter_cellchat_bubble_data <- function(df, top_pathways = 20, manual_pathways = character(), top_n_per_group = 30,
                                        min_prob = 0, pval_cutoff = NULL) {
  .require_pkg("data.table")
  dt <- data.table::as.data.table(df)
  dt <- dt[is.finite(prob) & prob > min_prob]
  if (!is.null(pval_cutoff) && "pval" %in% names(dt)) dt <- dt[is.na(pval) | pval <= pval_cutoff]
  pathway_rank <- dt[, .(mean_prob = mean(prob, na.rm = TRUE)), by = pathway_name][order(-mean_prob, pathway_name)]
  keep_pathways <- unique(c(head(pathway_rank$pathway_name, top_pathways), manual_pathways))
  dt <- dt[pathway_name %in% keep_pathways]
  dt <- dt[order(group, -prob, interaction_name), head(.SD, top_n_per_group), by = group]
  attr(dt, "pathway_rank") <- pathway_rank
  dt[]
}

order_cellchat_axes <- function(df) {
  .require_pkg("data.table")
  dt <- data.table::as.data.table(df)
  interaction_order <- dt[, .(mean_prob = mean(prob, na.rm = TRUE)), by = interaction_name][order(-mean_prob, interaction_name)]$interaction_name
  x_order <- dt[, .(max_prob = max(prob, na.rm = TRUE)), by = source_target][order(-max_prob, source_target)]$source_target
  list(interaction_order = interaction_order, source_target_order = x_order)
}

plot_multigroup_cellchat_bubble <- function(df, group_levels = NULL, color_values = NULL, size_range = c(1.5, 9)) {
  .require_pkg("ggplot2")
  axes <- order_cellchat_axes(df)
  plot_df <- as.data.frame(df)
  if (!is.null(group_levels)) plot_df$group <- factor(plot_df$group, levels = group_levels)
  plot_df$interaction_name <- factor(plot_df$interaction_name, levels = rev(axes$interaction_order))
  plot_df$source_target <- factor(plot_df$source_target, levels = axes$source_target_order)

  p <- ggplot2::ggplot(plot_df, ggplot2::aes(x = source_target, y = interaction_name, size = prob, color = group)) +
    ggplot2::geom_point(alpha = 0.85) +
    ggplot2::scale_size_continuous(range = size_range, name = "Communication probability") +
    ggplot2::facet_grid(. ~ group, scales = "free_x", space = "free_x") +
    ggplot2::theme_bw(base_size = 11) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 45, hjust = 1, vjust = 1), strip.text = ggplot2::element_text(face = "bold")) +
    ggplot2::labs(x = "Sender -> Receiver", y = "Ligand-receptor interaction", color = "Group")
  if (!is.null(color_values)) p <- p + ggplot2::scale_color_manual(values = color_values)
  p
}

save_cellchat_bubble_artifacts <- function(df, out_dir, prefix = "cellchat_bubble") {
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  utils::write.table(df, file = file.path(out_dir, paste0(prefix, "_merged_communication.tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  axes <- order_cellchat_axes(df)
  utils::write.table(data.frame(interaction_name = axes$interaction_order), file = file.path(out_dir, paste0(prefix, "_interaction_order.tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  utils::write.table(data.frame(source_target = axes$source_target_order), file = file.path(out_dir, paste0(prefix, "_source_target_order.tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  invisible(out_dir)
}
