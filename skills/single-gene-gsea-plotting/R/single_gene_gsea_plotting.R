# Single-gene GSEA and NES-consistent plotting helpers.

.require_pkg <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) stop(sprintf("Package '%s' is required.", pkg), call. = FALSE)
  invisible(TRUE)
}

validate_expression_matrix <- function(expr, target_gene) {
  if (!is.matrix(expr) && !is.data.frame(expr)) stop("expr must be a matrix/data.frame with genes as rows.", call. = FALSE)
  expr <- as.matrix(expr)
  if (is.null(rownames(expr))) stop("expr must have gene rownames.", call. = FALSE)
  hits <- which(rownames(expr) == target_gene)
  if (!length(hits)) stop(sprintf("Target gene '%s' not found.", target_gene), call. = FALSE)
  if (length(hits) > 1) stop(sprintf("Target gene '%s' appears multiple times; disambiguate first.", target_gene), call. = FALSE)
  na_before <- sum(is.na(expr))
  expr_num <- suppressWarnings(apply(expr, 2, as.numeric))
  rownames(expr_num) <- rownames(expr)
  colnames(expr_num) <- colnames(expr)
  na_after <- sum(is.na(expr_num))
  if (na_after > na_before) {
    stop("Expression matrix contains non-numeric values that would be coerced to NA. Remove annotation columns before ranking.", call. = FALSE)
  }
  expr <- expr_num
  storage.mode(expr) <- "numeric"
  expr
}

single_gene_correlation_rank <- function(expr, target_gene, method = c("spearman", "pearson"), min_sd = 0) {
  method <- match.arg(method)
  expr <- validate_expression_matrix(expr, target_gene)
  target <- as.numeric(expr[target_gene, ])
  keep <- rownames(expr) != target_gene
  sds <- apply(expr, 1, stats::sd, na.rm = TRUE)
  keep <- keep & is.finite(sds) & sds > min_sd
  x <- expr[keep, , drop = FALSE]
  cors <- apply(x, 1, function(g) suppressWarnings(stats::cor(g, target, method = method, use = "pairwise.complete.obs")))
  cors <- cors[is.finite(cors)]
  sort(cors, decreasing = TRUE)
}

run_clusterprofiler_gsea <- function(gene_list, term2gene, pvalue_cutoff = 1, p_adjust_method = "BH", seed = 1, ...) {
  .require_pkg("clusterProfiler")
  if (!is.numeric(gene_list) || is.null(names(gene_list))) stop("gene_list must be a named numeric vector.", call. = FALSE)
  gene_list <- sort(gene_list[is.finite(gene_list)], decreasing = TRUE)
  if (!is.data.frame(term2gene) || ncol(term2gene) < 2) stop("term2gene must be a data.frame with at least two columns.", call. = FALSE)
  set.seed(seed)
  clusterProfiler::GSEA(geneList = gene_list, TERM2GENE = term2gene, pvalueCutoff = pvalue_cutoff, pAdjustMethod = p_adjust_method, ...)
}

select_gsea_pathways_by_nes <- function(gsea_result, descriptions = NULL, ids = NULL, n = NULL, p_col = "p.adjust", p_cutoff = 0.25,
                                        nes_decreasing = TRUE) {
  res <- as.data.frame(gsea_result)
  if (!nrow(res)) stop("GSEA result is empty.", call. = FALSE)
  if (!is.null(descriptions)) res <- res[res$Description %in% descriptions, , drop = FALSE]
  if (!is.null(ids)) res <- res[res$ID %in% ids, , drop = FALSE]
  if (p_col %in% names(res) && !is.null(p_cutoff)) res <- res[is.na(res[[p_col]]) | res[[p_col]] <= p_cutoff, , drop = FALSE]
  res <- res[order(if (nes_decreasing) -res$NES else res$NES, res$Description), , drop = FALSE]
  if (!is.null(n)) res <- head(res, n)
  res
}

make_named_gsea_colors <- function(labels, palette = NULL) {
  labels <- as.character(labels)
  n <- length(labels)
  if (is.null(palette)) {
    if (requireNamespace("viridis", quietly = TRUE)) {
      cols <- viridis::viridis(n, option = "D")
    } else {
      cols <- grDevices::hcl.colors(n, palette = "Dark 3")
    }
  } else if (length(palette) < n) {
    cols <- grDevices::colorRampPalette(palette)(n)
  } else {
    cols <- palette[seq_len(n)]
  }
  stats::setNames(cols, labels)
}

plot_gsea_curves_nes_matched <- function(gsea_result, selected, color_by = c("Description", "ID"), subplots = 1:3,
                                         ncol = 1, legend_title = "Pathway") {
  color_by <- match.arg(color_by)
  .require_pkg("enrichplot")
  .require_pkg("ggplot2")
  .require_pkg("patchwork")
  .require_pkg("cowplot")
  selected <- as.data.frame(selected)
  if (!nrow(selected)) stop("selected pathway table is empty.", call. = FALSE)
  labels <- selected[[color_by]]
  ids <- selected$ID
  colors <- make_named_gsea_colors(labels)

  plots <- lapply(seq_along(ids), function(i) {
    p <- enrichplot::gseaplot2(
      gsea_result,
      geneSetID = ids[i],
      subplots = subplots,
      pvalue_table = FALSE,
      ES_geom = "line",
      color = unname(colors[i])
    )
    if (inherits(p, "list")) p <- patchwork::wrap_plots(p, ncol = 1)
    p + ggplot2::ggtitle(labels[i]) + ggplot2::theme(legend.position = "none")
  })
  combined <- patchwork::wrap_plots(plots, ncol = ncol)

  legend_df <- data.frame(pathway = factor(labels, levels = labels), x = 1, y = seq_along(labels))
  legend_plot <- ggplot2::ggplot(legend_df, ggplot2::aes(x = x, y = y, color = pathway)) +
    ggplot2::geom_point(size = 3) +
    ggplot2::scale_color_manual(values = colors, name = legend_title) +
    ggplot2::theme_void() +
    ggplot2::theme(legend.position = "right")
  legend <- cowplot::get_legend(legend_plot)
  out <- cowplot::plot_grid(combined, legend, ncol = 2, rel_widths = c(5, 2))
  attr(out, "color_map") <- data.frame(label = labels, color = unname(colors), ID = ids, NES = selected$NES, stringsAsFactors = FALSE)
  out
}
