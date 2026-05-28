# DoRothEA + VIPER helper skeleton.

source_if_needed <- function(path) {
  if (file.exists(path)) source(path)
}

run_dorothea_viper_activity <- function(obj, assay = "RNA", organism = c("human", "mouse"), confidence = c("A", "B", "C"),
                                        slot_try = c("data", "counts"), minsize = 4,
                                        method = "scale", assay_out = "dorothea", dense_max_gb = 8) {
  organism <- match.arg(organism)
  .require_pkg("SeuratObject")
  .require_pkg("dorothea")

  preflight_seurat_activity(obj, assay = assay)
  expr <- safe_get_assay_matrix(obj, assay = assay, slot_try = slot_try, dense = TRUE, dense_max_gb = dense_max_gb)

  regulon_name <- if (organism == "human") "dorothea_hs" else "dorothea_mm"
  data(list = regulon_name, package = "dorothea", envir = environment())
  regulon <- get(regulon_name, envir = environment())
  regulon <- regulon[regulon$confidence %in% confidence, , drop = FALSE]
  overlap <- check_feature_overlap(regulon$target, rownames(expr), label = paste0("DoRothEA ", organism, " regulon"))

  if (!requireNamespace("viper", quietly = TRUE) && !requireNamespace("decoupleR", quietly = TRUE)) {
    stop("Either 'viper' or 'decoupleR' is required for activity inference.", call. = FALSE)
  }

  if (requireNamespace("dorothea", quietly = TRUE) && exists("run_viper", where = asNamespace("dorothea"), inherits = FALSE)) {
    obj <- dorothea::run_viper(
      obj,
      regulon,
      assay = assay,
      options = list(method = method, minsize = minsize, eset.filter = FALSE, verbose = FALSE)
    )
    if (assay_out != "dorothea" && "dorothea" %in% SeuratObject::Assays(obj)) {
      obj[[assay_out]] <- obj[["dorothea"]]
    }
    attr(obj, "dorothea_overlap") <- overlap
    return(obj)
  }

  stop("dorothea::run_viper() is not available in this environment; implement a decoupleR fallback if needed.", call. = FALSE)
}

summarize_dorothea_activity <- function(obj, group_col = "celltype", assay = "dorothea", slot_try = c("data", "scale.data")) {
  mat <- safe_get_assay_matrix(obj, assay = assay, slot_try = slot_try, dense = TRUE)
  long <- activity_matrix_to_long(mat, metadata = obj@meta.data, feature_col = "tf", score_col = "activity")
  summarize_activity_by_group(long, group_col = group_col, feature_col = "tf", score_col = "activity")
}

select_top_tf_markers <- function(marker_table, cluster_col = "cluster", gene_col = "gene", p_col = "p_val_adj", fc_col = "avg_log2FC", n = 10) {
  .require_pkg("dplyr")
  marker_table |>
    dplyr::filter(.data[[p_col]] < 0.05, is.finite(.data[[fc_col]])) |>
    dplyr::group_by(.data[[cluster_col]]) |>
    dplyr::arrange(.data[[p_col]], dplyr::desc(.data[[fc_col]]), .by_group = TRUE) |>
    dplyr::slice_head(n = n) |>
    dplyr::ungroup()
}
