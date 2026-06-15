# Metabolic pathway activity helper skeleton.

read_pathway_gene_table <- function(path, pathway_col = "pathway", gene_col = "gene", min_size = 5, max_size = 500) {
  .require_pkg("data.table")
  dt <- data.table::fread(path)
  missing <- setdiff(c(pathway_col, gene_col), names(dt))
  if (length(missing)) stop(sprintf("Pathway table missing columns: %s", paste(missing, collapse = ", ")), call. = FALSE)
  dt <- unique(dt[!is.na(get(pathway_col)) & !is.na(get(gene_col)), .(pathway = as.character(get(pathway_col)), gene = as.character(get(gene_col)))])
  sizes <- dt[, .N, by = pathway]
  keep <- sizes[N >= min_size & N <= max_size, pathway]
  dropped <- setdiff(sizes$pathway, keep)
  if (length(dropped)) warning(sprintf("Dropping %s pathways outside size range [%s, %s].", length(dropped), min_size, max_size), call. = FALSE)
  split(dt[pathway %in% keep]$gene, dt[pathway %in% keep]$pathway)
}

run_metabolism_ssgsea <- function(obj, genesets, assay = "RNA", slot_try = c("data", "counts"), min_size = 5, max_size = Inf, dense_max_gb = 8) {
  .require_pkg("GSVA")
  expr <- safe_get_assay_matrix(obj, assay = assay, slot_try = slot_try, dense = TRUE, dense_max_gb = dense_max_gb)
  overlap_stats <- lapply(names(genesets), function(nm) check_feature_overlap(genesets[[nm]], rownames(expr), label = nm))
  param <- GSVA::ssgseaParam(expr, genesets, minSize = min_size, maxSize = max_size, normalize = TRUE)
  scores <- GSVA::gsva(param)
  attr(scores, "overlap_stats") <- overlap_stats
  scores
}

run_metabolism_aucell <- function(obj, genesets, assay = "RNA", slot_try = c("counts", "data"), ncores = 1, dense_max_gb = 8) {
  .require_pkg("AUCell")
  expr <- safe_get_assay_matrix(obj, assay = assay, slot_try = slot_try, dense = TRUE, dense_max_gb = dense_max_gb)
  rankings <- AUCell::AUCell_buildRankings(expr, nCores = ncores, plotStats = FALSE, verbose = FALSE)
  auc <- AUCell::AUCell_calcAUC(genesets, rankings, verbose = FALSE)
  AUCell::getAUC(auc)
}

attach_activity_assay <- function(obj, activity_matrix, assay_out = "METABOLISM", overwrite = FALSE) {
  .require_pkg("SeuratObject")
  if (assay_out %in% SeuratObject::Assays(obj) && !overwrite) {
    stop(sprintf("Assay '%s' already exists. Set overwrite=TRUE or choose a new assay_out.", assay_out), call. = FALSE)
  }
  if (!all(colnames(activity_matrix) %in% colnames(obj))) {
    stop("All activity matrix columns must be Seurat cell names.", call. = FALSE)
  }
  activity_matrix <- activity_matrix[, colnames(obj), drop = FALSE]
  obj[[assay_out]] <- SeuratObject::CreateAssayObject(data = as.matrix(activity_matrix))
  obj
}
