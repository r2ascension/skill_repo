# Reusable helpers for per-cell-type group comparisons on single-cell violin plots.

.normalize_violin_df <- function(plot_df, expr_col = "expression", group_col = "group", celltype_col = "celltype") {
  required_cols <- c(expr_col, group_col, celltype_col)
  missing_cols <- setdiff(required_cols, colnames(plot_df))
  if (length(missing_cols) > 0) {
    stop(sprintf("Missing required columns: %s", paste(missing_cols, collapse = ", ")))
  }

  normalized <- data.frame(
    expression = plot_df[[expr_col]],
    group = plot_df[[group_col]],
    celltype = plot_df[[celltype_col]],
    stringsAsFactors = FALSE
  )
  normalized <- normalized[stats::complete.cases(normalized), , drop = FALSE]
  normalized
}

significance_stars <- function(p_values) {
  out <- rep("ns", length(p_values))
  out[!is.na(p_values) & p_values < 0.05] <- "*"
  out[!is.na(p_values) & p_values < 0.01] <- "**"
  out[!is.na(p_values) & p_values < 0.001] <- "***"
  out[!is.na(p_values) & p_values < 0.0001] <- "****"
  out
}

fetch_seurat_violin_data <- function(seurat_object, gene, group_col = "group", celltype_col = "celltype") {
  if (!requireNamespace("Seurat", quietly = TRUE)) {
    stop("Seurat must be installed to fetch data from a Seurat object.")
  }

  vars <- c(gene, group_col, celltype_col)
  plot_df <- Seurat::FetchData(seurat_object, vars = vars)
  colnames(plot_df) <- c("expression", "group", "celltype")
  plot_df
}

compute_violin_significance <- function(
  plot_df,
  expr_col = "expression",
  group_col = "group",
  celltype_col = "celltype",
  group_levels = NULL,
  adjust_method = "BH",
  star_by = c("p_adj", "p_value"),
  y_offset_fraction = 0.1
) {
  star_by <- match.arg(star_by)
  plot_df <- .normalize_violin_df(plot_df, expr_col, group_col, celltype_col)

  if (!is.null(group_levels)) {
    plot_df$group <- factor(plot_df$group, levels = group_levels)
  } else {
    plot_df$group <- factor(plot_df$group)
    group_levels <- levels(plot_df$group)
  }
  plot_df$celltype <- factor(plot_df$celltype, levels = unique(plot_df$celltype))

  split_df <- split(plot_df, plot_df$celltype, drop = TRUE)
  stats_list <- lapply(names(split_df), function(celltype_name) {
    subset_df <- split_df[[celltype_name]]
    observed_groups <- unique(as.character(subset_df$group[!is.na(subset_df$group)]))
    if (length(observed_groups) < 2) {
      return(data.frame(
        celltype = celltype_name,
        p_value = NA_real_,
        stringsAsFactors = FALSE
      ))
    }

    test_result <- stats::wilcox.test(expression ~ group, data = subset_df, exact = FALSE)
    rows <- list(
      celltype = celltype_name,
      p_value = unname(test_result$p.value)
    )

    for (group_name in group_levels) {
      expr_values <- subset_df$expression[subset_df$group == group_name]
      safe_group <- gsub("[^A-Za-z0-9]+", "_", as.character(group_name))
      rows[[paste0("n_", safe_group)]] <- sum(subset_df$group == group_name, na.rm = TRUE)
      rows[[paste0("median_", safe_group)]] <- if (length(expr_values) > 0) stats::median(expr_values, na.rm = TRUE) else NA_real_
      rows[[paste0("mean_", safe_group)]] <- if (length(expr_values) > 0) mean(expr_values, na.rm = TRUE) else NA_real_
    }

    as.data.frame(rows, stringsAsFactors = FALSE)
  })

  stats_df <- do.call(rbind, stats_list)
  valid_idx <- !is.na(stats_df$p_value)
  stats_df$p_adj <- NA_real_
  if (any(valid_idx)) {
    stats_df$p_adj[valid_idx] <- stats::p.adjust(stats_df$p_value[valid_idx], method = adjust_method)
  }
  stats_df$significance <- significance_stars(stats_df[[star_by]])

  summary_df <- do.call(rbind, lapply(split_df, function(subset_df) {
    expr_range <- range(subset_df$expression, na.rm = TRUE)
    data.frame(
      celltype = as.character(subset_df$celltype[1]),
      max_expr = expr_range[2],
      range_expr = diff(expr_range),
      stringsAsFactors = FALSE
    )
  }))
  summary_df$range_expr[is.na(summary_df$range_expr) | summary_df$range_expr <= 0] <- 1
  summary_df$y_pos <- summary_df$max_expr + summary_df$range_expr * y_offset_fraction

  annotation_df <- merge(stats_df, summary_df[, c("celltype", "y_pos")], by = "celltype", all.x = TRUE, sort = FALSE)

  list(
    plot_df = plot_df,
    stats_df = stats_df,
    annotation_df = annotation_df
  )
}

plot_significant_violin <- function(
  plot_df,
  expr_col = "expression",
  group_col = "group",
  celltype_col = "celltype",
  group_levels = NULL,
  fill_colors = NULL,
  add_boxplot = TRUE,
  add_jitter = FALSE,
  adjust_method = "BH",
  star_by = c("p_adj", "p_value"),
  title = NULL,
  x_label = "Cell type",
  y_label = "Gene expression"
) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 must be installed to build violin plots.")
  }

  star_by <- match.arg(star_by)
  computed <- compute_violin_significance(
    plot_df = plot_df,
    expr_col = expr_col,
    group_col = group_col,
    celltype_col = celltype_col,
    group_levels = group_levels,
    adjust_method = adjust_method,
    star_by = star_by
  )

  plot_df <- computed$plot_df
  annotation_df <- computed$annotation_df
  p <- ggplot2::ggplot(plot_df, ggplot2::aes(x = celltype, y = expression, fill = group)) +
    ggplot2::geom_violin(trim = TRUE, scale = "width", alpha = 0.7)

  if (add_boxplot) {
    p <- p + ggplot2::geom_boxplot(width = 0.12, outlier.size = 0.4, alpha = 0.7)
  }
  if (add_jitter) {
    p <- p + ggplot2::geom_jitter(
      ggplot2::aes(color = group),
      width = 0.18,
      size = 0.6,
      alpha = 0.45
    )
  }
  if (!is.null(fill_colors)) {
    p <- p + ggplot2::scale_fill_manual(values = fill_colors)
    if (add_jitter) {
      p <- p + ggplot2::scale_color_manual(values = fill_colors)
    }
  }

  annotation_df <- annotation_df[!is.na(annotation_df$y_pos), , drop = FALSE]
  if (nrow(annotation_df) > 0) {
    p <- p + ggplot2::geom_text(
      data = annotation_df,
      ggplot2::aes(x = celltype, y = y_pos, label = significance),
      inherit.aes = FALSE,
      vjust = -0.4,
      size = 4
    )
  }

  p <- p +
    ggplot2::scale_y_continuous(expand = ggplot2::expansion(mult = c(0.05, 0.15))) +
    ggplot2::labs(title = title, x = x_label, y = y_label) +
    ggplot2::theme_minimal() +
    ggplot2::theme(
      axis.text.x = ggplot2::element_text(angle = 45, hjust = 1, colour = "black"),
      axis.text.y = ggplot2::element_text(colour = "black"),
      axis.title = ggplot2::element_text(face = "bold", colour = "black"),
      plot.title = ggplot2::element_text(face = "bold", hjust = 0.5, colour = "black"),
      legend.position = "top"
    )

  list(
    plot = p,
    stats = computed$stats_df,
    data = plot_df
  )
}

batch_export_significant_violin <- function(
  seurat_object,
  genes,
  output_dir = ".",
  group_col = "group",
  celltype_col = "celltype",
  fill_colors = NULL,
  star_by = c("p_adj", "p_value"),
  width = 7,
  height = 5
) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 must be installed to save violin plots.")
  }

  star_by <- match.arg(star_by)
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }

  outputs <- lapply(genes, function(gene) {
    plot_df <- fetch_seurat_violin_data(
      seurat_object = seurat_object,
      gene = gene,
      group_col = group_col,
      celltype_col = celltype_col
    )
    result <- plot_significant_violin(
      plot_df = plot_df,
      fill_colors = fill_colors,
      title = gene,
      star_by = star_by
    )

    safe_gene <- gsub("[^A-Za-z0-9._-]+", "_", gene)
    pdf_path <- file.path(output_dir, paste0(safe_gene, ".geom_violin.pdf"))
    csv_path <- file.path(output_dir, paste0(safe_gene, ".wilcox_results.csv"))
    ggplot2::ggsave(filename = pdf_path, plot = result$plot, width = width, height = height)
    utils::write.csv(result$stats, file = csv_path, row.names = FALSE)

    data.frame(
      gene = gene,
      pdf_path = pdf_path,
      csv_path = csv_path,
      stringsAsFactors = FALSE
    )
  })

  do.call(rbind, outputs)
}
