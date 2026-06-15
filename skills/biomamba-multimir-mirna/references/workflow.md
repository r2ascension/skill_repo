# multiMiR Workflow

## Query Types

multiMiR can query by:

- `mirna`: one or more miRNA IDs.
- `target`: gene symbols or IDs.
- `disease.drug`: disease and drug association tables.
- `table`: validated, predicted, disease, drug, or all data classes depending on package version.

Start by deciding the biological question:

- Which genes might be targeted by a miRNA?
- Which miRNAs regulate a gene list?
- Which miRNA-target pairs have disease evidence?
- Which pairs connect to drug response?

## Basic Query

```r
library(multiMiR)

res <- get_multimir(
  org = "hsa",
  mirna = c("hsa-miR-21-5p", "hsa-miR-155-5p"),
  table = "all",
  summary = TRUE
)

tab <- res@data
head(tab)
```

Some versions use `get.multimir`; check the installed package:

```r
exists("get_multimir")
exists("get.multimir")
```

## Query From Targets

```r
res <- get_multimir(
  org = "hsa",
  target = c("PTEN", "TP53", "VEGFA"),
  table = "validated",
  summary = TRUE
)
targets <- res@data
```

Prefer validated interactions when preparing conservative mechanistic hypotheses. Use predicted results for exploratory screening, and label them as predicted.

## Filtering

Typical filters:

```r
library(dplyr)
clean <- tab %>%
  filter(!is.na(mature_mirna_id), !is.na(target_symbol)) %>%
  distinct(mature_mirna_id, target_symbol, database, .keep_all = TRUE)

validated <- clean %>% filter(type == "validated")
predicted <- clean %>% filter(type == "predicted")
```

Use database source counts, prediction score, or target support as confidence metrics when columns are available.

## Export

```r
library(openxlsx)
write.xlsx(clean, "multimir_results.xlsx", overwrite = TRUE)
```

## Network Visualization

```r
library(igraph)
library(ggraph)

edges <- clean %>% select(from = mature_mirna_id, to = target_symbol) %>% distinct()
g <- graph_from_data_frame(edges, directed = TRUE)
ggraph(g, layout = "fr") +
  geom_edge_link(alpha = 0.3) +
  geom_node_point() +
  geom_node_text(aes(label = name), repel = TRUE)
```

Keep only top supported pairs when the network is too dense.

## Sankey Visualization

Use Sankey plots for miRNA to target to disease/drug paths:

```r
library(ggsankey)
sankey_df <- clean %>%
  select(mirna = mature_mirna_id, target = target_symbol, disease = disease) %>%
  filter(!is.na(disease)) %>%
  make_long(mirna, target, disease)

ggplot(sankey_df, aes(x = x, next_x = next_x, node = node, next_node = next_node, fill = factor(node))) +
  geom_sankey(flow.alpha = 0.5, node.color = "grey30") +
  geom_sankey_label(aes(label = node), size = 3) +
  theme_sankey()
```

## Interpretation

Do not infer regulation from prediction alone. Prioritize pairs supported by validated databases, consistent expression direction, disease context, and literature.
