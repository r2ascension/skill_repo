# PROGENy helper skeleton.

run_progeny_activity <- function(obj, assay_in = "RNA", assay_out = "progeny", organism = c("Human", "Mouse"),
                                 top = 500, perm = 1, scale = FALSE, seed = 1) {
  organism <- match.arg(organism)
  .require_pkg("SeuratObject")
  .require_pkg("progeny")
  preflight_seurat_activity(obj, assay = assay_in)
  if (!is.null(seed)) set.seed(seed)
  if (!is.numeric(top) || top <= 0) stop("top must be a positive number.", call. = FALSE)
  if (!is.numeric(perm) || perm < 1) stop("perm must be >= 1.", call. = FALSE)

  obj <- progeny::progeny(
    obj,
    scale = scale,
    organism = organism,
    top = top,
    perm = perm,
    return_assay = TRUE
  )
  if (assay_out != "progeny" && "progeny" %in% SeuratObject::Assays(obj)) {
    obj[[assay_out]] <- obj[["progeny"]]
  }
  obj@misc$progeny_activity_params <- list(assay_in = assay_in, assay_out = assay_out, organism = organism, top = top, perm = perm, scale = scale, seed = seed)
  obj
}

scale_progeny_assay <- function(obj, assay = "progeny") {
  .require_pkg("Seurat")
  .require_pkg("SeuratObject")
  if (!assay %in% SeuratObject::Assays(obj)) stop(sprintf("Assay '%s' not found.", assay), call. = FALSE)
  obj <- Seurat::ScaleData(obj, assay = assay, verbose = FALSE)
  obj
}

extract_progeny_long <- function(obj, assay = "progeny", slot_try = c("scale.data", "data", "counts"), metadata_cols = NULL) {
  mat <- safe_get_assay_matrix(obj, assay = assay, slot_try = slot_try, dense = TRUE)
  meta <- obj@meta.data
  if (!is.null(metadata_cols)) meta <- meta[, metadata_cols, drop = FALSE]
  activity_matrix_to_long(mat, metadata = meta, feature_col = "pathway", score_col = "activity")
}

summarize_progeny_by_celltype <- function(obj, celltype_col = "celltype", assay = "progeny", slot_try = c("scale.data", "data")) {
  long <- extract_progeny_long(obj, assay = assay, slot_try = slot_try, metadata_cols = celltype_col)
  summarize_activity_by_group(long, group_col = celltype_col, feature_col = "pathway", score_col = "activity")
}
