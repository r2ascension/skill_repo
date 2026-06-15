# Celltype-wise DEG and volcano plotting helpers.

.require_pkg <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) stop(sprintf("Package '%s' is required.", pkg), call. = FALSE)
  invisible(TRUE)
}

preflight_celltype_deg <- function(obj, celltype_col = "celltype", group_col = "group", ident_1, ident_2, sample_col = NULL, min_cells_per_group = 10) {
  .require_pkg("SeuratObject")
  if (!inherits(obj, "Seurat")) stop("Input must be a Seurat object.", call. = FALSE)
  missing <- setdiff(c(celltype_col, group_col), colnames(obj@meta.data))
  if (length(missing)) stop(sprintf("Missing metadata columns: %s", paste(missing, collapse = ", ")), call. = FALSE)
  if (!all(c(ident_1, ident_2) %in% unique(as.character(obj@meta.data[[group_col]])))) {
    stop("ident_1 and/or ident_2 not found in group_col.", call. = FALSE)
  }
  counts <- as.data.frame.matrix(table(obj@meta.data[[celltype_col]], obj@meta.data[[group_col]]))
  bad <- rownames(counts)[counts[[ident_1]] < min_cells_per_group | counts[[ident_2]] < min_cells_per_group]
  if (length(bad)) warning(sprintf("Skipping or warning for cell types with low cells: %s", paste(bad, collapse = ", ")), call. = FALSE)
  if (!is.null(sample_col) && sample_col %in% colnames(obj@meta.data)) {
    sample_counts <- table(obj@meta.data[[group_col]], obj@meta.data[[sample_col]])
    if (any(rowSums(sample_counts > 0) < 3)) warning("Fewer than 3 samples in at least one group; cell-level DEG should be considered exploratory.", call. = FALSE)
  }
  invisible(list(cell_counts = counts, low_celltypes = bad))
}

find_logfc_col <- function(df) {
  hits <- c("avg_log2FC", "avg_logFC", "log2FC", "logFC")
  hit <- hits[hits %in% names(df)][1]
  if (is.na(hit)) stop("Could not find a log fold-change column in DEG result.", call. = FALSE)
  hit
}

standardize_deg_table <- function(deg, celltype, group_1, group_2, method = "FindMarkers") {
  deg <- as.data.frame(deg)
  deg$gene <- rownames(deg)
  fc_col <- find_logfc_col(deg)
  out <- data.frame(
    gene = deg$gene,
    celltype = as.character(celltype),
    group_1 = as.character(group_1),
    group_2 = as.character(group_2),
    log2FC = as.numeric(deg[[fc_col]]),
    p_val = if ("p_val" %in% names(deg)) as.numeric(deg$p_val) else NA_real_,
    p_val_adj = if ("p_val_adj" %in% names(deg)) as.numeric(deg$p_val_adj) else NA_real_,
    pct.1 = if ("pct.1" %in% names(deg)) as.numeric(deg$pct.1) else NA_real_,
    pct.2 = if ("pct.2" %in% names(deg)) as.numeric(deg$pct.2) else NA_real_,
    method = method,
    stringsAsFactors = FALSE
  )
  out
}

run_celltype_findmarkers <- function(obj, celltype_col = "celltype", group_col = "group", ident_1, ident_2,
                                     assay = NULL, min_cells_per_group = 10, only_pos = FALSE, min_pct = 0.25,
                                     logfc_threshold = 0.25, test_use = "wilcox") {
  .require_pkg("Seurat")
  check <- preflight_celltype_deg(obj, celltype_col, group_col, ident_1, ident_2, min_cells_per_group = min_cells_per_group)
  celltypes <- setdiff(unique(as.character(obj@meta.data[[celltype_col]])), check$low_celltypes)
  out <- list()
  skipped <- data.frame(celltype = check$low_celltypes, reason = "low_cells", stringsAsFactors = FALSE)
  for (ct in celltypes) {
    deg <- tryCatch(
      Seurat::FindMarkers(
        obj,
        ident.1 = ident_1,
        ident.2 = ident_2,
        group.by = group_col,
        subset.ident = ct,
        assay = assay,
        only.pos = only_pos,
        min.pct = min_pct,
        logfc.threshold = logfc_threshold,
        test.use = test_use,
        verbose = FALSE
      ),
      error = function(e) e
    )
    if (inherits(deg, "error")) {
      skipped <- rbind(skipped, data.frame(celltype = ct, reason = deg$message, stringsAsFactors = FALSE))
      next
    }
    out[[ct]] <- standardize_deg_table(deg, ct, ident_1, ident_2, method = paste0("FindMarkers:", test_use))
  }
  deg_out <- if (length(out)) {
    do.call(rbind, out)
  } else {
    data.frame(
      gene = character(), celltype = character(), group_1 = character(), group_2 = character(),
      log2FC = numeric(), p_val = numeric(), p_val_adj = numeric(), pct.1 = numeric(), pct.2 = numeric(),
      method = character(), stringsAsFactors = FALSE
    )
  }
  list(deg = deg_out, skipped = skipped)
}

label_deg_thresholds <- function(deg, alpha = 0.05, logfc = 0.5) {
  deg$direction <- ifelse(is.finite(deg$log2FC) & deg$log2FC > logfc, "Up", ifelse(is.finite(deg$log2FC) & deg$log2FC < -logfc, "Down", "NS"))
  deg$significance <- ifelse(!is.na(deg$p_val_adj) & deg$p_val_adj < alpha & deg$direction != "NS", paste0(deg$direction, "_significant"), "Not_significant")
  deg
}

select_top_deg_labels <- function(deg, n = 5, alpha = 0.05, logfc = 0.5) {
  .require_pkg("dplyr")
  sig <- deg |>
    dplyr::filter(!is.na(.data$p_val_adj), .data$p_val_adj < alpha, abs(.data$log2FC) > logfc)
  up <- sig |> dplyr::filter(.data$log2FC > 0) |> dplyr::group_by(.data$celltype) |> dplyr::slice_max(order_by = .data$log2FC, n = n, with_ties = FALSE) |> dplyr::ungroup()
  down <- sig |> dplyr::filter(.data$log2FC < 0) |> dplyr::group_by(.data$celltype) |> dplyr::slice_min(order_by = .data$log2FC, n = n, with_ties = FALSE) |> dplyr::ungroup()
  rbind(up, down)
}

plot_multicluster_volcano <- function(deg, labels = NULL, celltype_col = "celltype") {
  .require_pkg("ggplot2")
  .require_pkg("ggrepel")
  plot_df <- deg
  plot_df$neg_log10_padj <- -log10(pmax(plot_df$p_val_adj, .Machine$double.xmin, na.rm = TRUE))
  if (requireNamespace("scRNAtoolVis", quietly = TRUE) && "cluster" %in% names(plot_df)) {
    # Keep fallback deterministic; callers may customize scRNAtoolVis directly if desired.
  }
  p <- ggplot2::ggplot(plot_df, ggplot2::aes(x = .data$log2FC, y = .data$neg_log10_padj, color = .data$significance)) +
    ggplot2::geom_point(size = 0.6, alpha = 0.75) +
    ggplot2::facet_wrap(stats::as.formula(paste("~", celltype_col)), scales = "free_y") +
    ggplot2::scale_color_manual(values = c(Up_significant = "#b2182b", Down_significant = "#2166ac", Not_significant = "grey75"), drop = FALSE) +
    ggplot2::theme_bw(base_size = 10) +
    ggplot2::labs(x = "log2 fold-change", y = "-log10 adjusted p-value", color = "Threshold")
  if (!is.null(labels) && nrow(labels)) {
    labels$neg_log10_padj <- -log10(pmax(labels$p_val_adj, .Machine$double.xmin, na.rm = TRUE))
    p <- p + ggrepel::geom_text_repel(data = labels, ggplot2::aes(label = .data$gene), size = 2.8, max.overlaps = Inf, show.legend = FALSE)
  }
  p
}
