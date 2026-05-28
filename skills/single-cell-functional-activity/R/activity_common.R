# Shared helpers for single-cell functional activity workflows.
# These skeletons are intentionally conservative: they validate inputs, avoid
# unnecessary dense conversion, and return plain R objects for downstream use.

.require_pkg <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    stop(sprintf("Package '%s' is required but not installed.", pkg), call. = FALSE)
  }
  invisible(TRUE)
}

preflight_seurat_activity <- function(obj, assay = "RNA", group_cols = character(), min_cells = 1) {
  .require_pkg("SeuratObject")
  if (!inherits(obj, "Seurat")) {
    stop("Input must be a Seurat object.", call. = FALSE)
  }
  if (!assay %in% SeuratObject::Assays(obj)) {
    stop(sprintf("Assay '%s' not found. Available assays: %s", assay, paste(SeuratObject::Assays(obj), collapse = ", ")), call. = FALSE)
  }
  missing_cols <- setdiff(group_cols, colnames(obj@meta.data))
  if (length(missing_cols)) {
    stop(sprintf("Missing metadata columns: %s", paste(missing_cols, collapse = ", ")), call. = FALSE)
  }
  if (ncol(obj) < min_cells) {
    stop(sprintf("Object has %s cells, below min_cells=%s.", ncol(obj), min_cells), call. = FALSE)
  }
  invisible(TRUE)
}

safe_get_assay_matrix <- function(obj, assay = "RNA", slot_try = c("data", "counts", "scale.data"), dense = FALSE, dense_max_gb = 8) {
  .require_pkg("SeuratObject")
  if (!inherits(obj, "Seurat")) stop("Input must be a Seurat object.", call. = FALSE)
  if (!assay %in% SeuratObject::Assays(obj)) stop(sprintf("Assay '%s' not found.", assay), call. = FALSE)

  mat <- NULL
  used_slot <- NULL
  for (slot in slot_try) {
    mat <- tryCatch(
      SeuratObject::GetAssayData(obj, assay = assay, slot = slot),
      error = function(e) NULL
    )
    if (!is.null(mat) && length(dim(mat)) == 2 && nrow(mat) > 0 && ncol(mat) > 0) {
      used_slot <- slot
      break
    }
  }
  if (is.null(mat)) stop(sprintf("No usable assay matrix found for assay '%s'.", assay), call. = FALSE)

  attr(mat, "assay") <- assay
  attr(mat, "slot") <- used_slot
  if (dense) {
    est_gb <- as.numeric(nrow(mat)) * as.numeric(ncol(mat)) * 8 / 1024^3
    if (est_gb > dense_max_gb) {
      stop(sprintf("Dense conversion would require ~%.1f GB, above dense_max_gb=%.1f.", est_gb, dense_max_gb), call. = FALSE)
    }
    mat <- as.matrix(mat)
    attr(mat, "dense_est_gb") <- est_gb
  }
  mat
}

check_feature_overlap <- function(features, universe, min_overlap_fraction = 0.2, label = "feature set") {
  features <- unique(stats::na.omit(as.character(features)))
  universe <- unique(stats::na.omit(as.character(universe)))
  overlap <- intersect(features, universe)
  frac <- if (length(features)) length(overlap) / length(features) else 0
  out <- list(
    label = label,
    n_features = length(features),
    n_universe = length(universe),
    n_overlap = length(overlap),
    overlap_fraction = frac,
    overlap = overlap,
    missing = setdiff(features, universe)
  )
  if (frac < min_overlap_fraction) {
    warning(sprintf("Low overlap for %s: %s/%s (%.1f%%).", label, length(overlap), length(features), 100 * frac), call. = FALSE)
  }
  out
}

activity_matrix_to_long <- function(activity_matrix, metadata = NULL, cell_col = "cell", feature_col = "feature", score_col = "score",
                                    include_zeros = TRUE, max_dense_entries = 5e7) {
  .require_pkg("data.table")
  if (is.null(rownames(activity_matrix)) || is.null(colnames(activity_matrix))) {
    stop("activity_matrix must have rownames(features) and colnames(cells).", call. = FALSE)
  }

  n_entries <- as.numeric(nrow(activity_matrix)) * as.numeric(ncol(activity_matrix))
  if (inherits(activity_matrix, "sparseMatrix") && !include_zeros) {
    .require_pkg("Matrix")
    warning("Returning only non-zero sparse entries; downstream summaries will ignore implicit zeros unless handled separately.", call. = FALSE)
    trip <- Matrix::summary(activity_matrix)
    dt <- data.table::data.table(
      feature = rownames(activity_matrix)[trip$i],
      cell = colnames(activity_matrix)[trip$j],
      score = as.numeric(trip$x)
    )
    data.table::setnames(dt, c("feature", "cell", "score"), c(feature_col, cell_col, score_col))
  } else {
    if (n_entries > max_dense_entries) {
      stop(sprintf(
        "Long table expansion would create %.1f million rows. Summarize first, increase max_dense_entries, or set include_zeros=FALSE for sparse non-zero output.",
        n_entries / 1e6
      ), call. = FALSE)
    }
    dt <- data.table::as.data.table(as.table(as.matrix(activity_matrix)))
    data.table::setnames(dt, c(feature_col, cell_col, score_col))
    dt[[score_col]] <- as.numeric(dt[[score_col]])
  }
  dt[[feature_col]] <- as.character(dt[[feature_col]])
  dt[[cell_col]] <- as.character(dt[[cell_col]])

  if (!is.null(metadata)) {
    meta <- data.table::as.data.table(metadata, keep.rownames = cell_col)
    meta[[cell_col]] <- as.character(meta[[cell_col]])
    dt <- merge(dt, meta, by = cell_col, all.x = TRUE, sort = FALSE)
  }
  dt[]
}

summarize_activity_by_group <- function(activity_long, group_col, feature_col = "feature", score_col = "score", min_cells = 1) {
  .require_pkg("data.table")
  dt <- data.table::as.data.table(activity_long)
  required <- c(feature_col, group_col, score_col)
  missing <- setdiff(required, names(dt))
  if (length(missing)) stop(sprintf("Missing columns: %s", paste(missing, collapse = ", ")), call. = FALSE)
  out <- dt[is.finite(get(score_col)), .(
    mean = mean(get(score_col), na.rm = TRUE),
    sd = stats::sd(get(score_col), na.rm = TRUE),
    n = .N,
    sem = stats::sd(get(score_col), na.rm = TRUE) / sqrt(.N)
  ), by = c(feature_col, group_col)]
  out <- out[n >= min_cells]
  out[]
}

summary_to_activity_matrix <- function(summary_table, feature_col = "feature", group_col = "group", value_col = "mean", fill = NA_real_) {
  .require_pkg("data.table")
  dt <- data.table::as.data.table(summary_table)
  dup <- dt[, .N, by = c(feature_col, group_col)][N > 1]
  if (nrow(dup)) {
    stop("summary_table contains duplicated feature/group combinations; aggregate before casting.", call. = FALSE)
  }
  wide <- data.table::dcast(dt, stats::as.formula(paste(feature_col, "~", group_col)), value.var = value_col, fill = fill)
  mat <- as.matrix(wide[, -1, with = FALSE])
  rownames(mat) <- wide[[feature_col]]
  mat
}

symmetric_breaks <- function(mat, n = 101, cap_quantile = NULL) {
  x <- as.numeric(mat)
  x <- x[is.finite(x)]
  if (!length(x)) return(seq(-1, 1, length.out = n))
  if (!is.null(cap_quantile)) {
    lim <- stats::quantile(abs(x), probs = cap_quantile, na.rm = TRUE, names = FALSE)
  } else {
    lim <- max(abs(x), na.rm = TRUE)
  }
  if (!is.finite(lim) || lim == 0) lim <- 1
  seq(-lim, lim, length.out = n)
}

plot_activity_heatmap <- function(mat, scale_rows = TRUE, palette = c("#2166ac", "white", "#b2182b"), filename = NULL, width = 7, height = 8) {
  .require_pkg("pheatmap")
  plot_mat <- as.matrix(mat)
  if (scale_rows) {
    row_sd <- apply(plot_mat, 1, stats::sd, na.rm = TRUE)
    keep <- is.finite(row_sd) & row_sd > 0
    plot_mat <- plot_mat[keep, , drop = FALSE]
    plot_mat <- t(scale(t(plot_mat)))
  }
  breaks <- symmetric_breaks(plot_mat, n = 101, cap_quantile = 0.99)
  colors <- grDevices::colorRampPalette(palette)(length(breaks) - 1)
  p <- pheatmap::pheatmap(plot_mat, color = colors, breaks = breaks, border_color = NA, silent = !is.null(filename))
  if (!is.null(filename)) {
    grDevices::pdf(filename, width = width, height = height, useDingbats = FALSE)
    grid::grid.newpage(); grid::grid.draw(p$gtable)
    grDevices::dev.off()
  }
  invisible(p)
}

write_session_info <- function(file) {
  dir.create(dirname(file), recursive = TRUE, showWarnings = FALSE)
  capture.output(utils::sessionInfo(), file = file)
  invisible(file)
}
