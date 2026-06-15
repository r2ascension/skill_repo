# Bulk RNA-seq Workflow

## Project Setup

Confirm:

- Species and genome build, such as hg38 or mm10.
- Paired-end versus single-end.
- Sample to group mapping.
- Whether the analysis starts from FASTQ, BAM, or a count matrix.
- Available disk space; alignment intermediates can be large.

## Download With Aspera

```bash
mkdir -p 00.rawdata
# Put download links in fastq_links.txt, one per line.
while read url; do
  ascp -QT -l 300m -P33001 -i ~/.aspera/connect/etc/asperaweb_id_dsa.openssh "$url" 00.rawdata/
done < fastq_links.txt
```

If Aspera is unavailable, use `wget`, `curl`, SRA Toolkit, ENA Browser, or the repository's recommended method.

## Reference And Alignment

Download a prebuilt HISAT2 index when available, or build one from genome FASTA:

```bash
hisat2-build genome.fa genome
```

Paired-end alignment pattern:

```bash
mkdir -p 02.bam
hisat2 -p 8 -x 00.ref/hg38/genome           -1 sample_R1.fastq.gz           -2 sample_R2.fastq.gz           | samtools sort -@ 8 -o 02.bam/sample.sorted.bam
samtools index 02.bam/sample.sorted.bam
```

Keep sample naming consistent before count generation.

## featureCounts

```bash
bamlist=$(ls 02.bam/*.sorted.bam | tr '
' ' ')
featureCounts -T 10 -p -t exon -g gene_name           -a 00.ref/hg38.refGene.gtf           -o 03.count/all.sample.counts.txt $bamlist
```

Remove `-p` for single-end data. Use `gene_id` rather than `gene_name` when duplicate gene symbols are a risk.

## Count Matrix Cleanup

```r
counts <- read.delim("03.count/all.sample.counts.txt", comment.char = "#", check.names = FALSE)
rownames(counts) <- counts$Geneid
count_mat <- counts[, grep(".bam$", colnames(counts))]
colnames(count_mat) <- sub(".sorted.bam$", "", basename(colnames(count_mat)))
```

## limma-voom Differential Analysis

```r
library(edgeR)
library(limma)

group <- factor(metadata$group, levels = c("normal", "disease"))
dge <- DGEList(counts = count_mat, group = group)
keep <- filterByExpr(dge)
dge <- dge[keep, , keep.lib.sizes = FALSE]
dge <- calcNormFactors(dge)

design <- model.matrix(~ group)
v <- voom(dge, design, plot = TRUE)
fit <- lmFit(v, design)
fit <- eBayes(fit)
deg <- topTable(fit, coef = 2, number = Inf)
```

## Volcano And Heatmap

```r
library(ggplot2)
deg$change <- "stable"
deg$change[deg$P.Value < 0.05 & deg$logFC > 0.5] <- "up"
deg$change[deg$P.Value < 0.05 & deg$logFC < -0.5] <- "down"

ggplot(deg, aes(logFC, -log10(P.Value), color = change)) +
  geom_point(alpha = 0.7, size = 1) +
  geom_vline(xintercept = c(-0.5, 0.5), linetype = 2) +
  geom_hline(yintercept = -log10(0.05), linetype = 2) +
  theme_bw()
```

Heatmap pattern:

```r
library(pheatmap)
top_genes <- rownames(head(deg[order(deg$P.Value), ], 50))
expr <- cpm(dge, log = TRUE)[top_genes, ]
pheatmap(expr, scale = "row", annotation_col = metadata)
```

## Enrichment

```r
library(clusterProfiler)
ego <- enrichGO(gene = up_genes, OrgDb = org.Hs.eg.db, keyType = "SYMBOL", ont = "BP")
dotplot(ego)
```

Use separate up and down gene lists when biological interpretation differs.

## Alternative Splicing With rMATS

rMATS needs BAM lists by group and a matching GTF:

```bash
rmats.py --b1 group1_bams.txt --b2 group2_bams.txt           --gtf 00.ref/genes.gtf           --od 05.rmats --tmp 05.rmats/tmp           -t paired --readLength 150 --nthread 8
```

Interpret skipped exon, mutually exclusive exon, alternative 5 prime splice site, alternative 3 prime splice site, and retained intron outputs separately.
