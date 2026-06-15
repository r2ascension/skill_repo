# OnekeyAI Bioinfo Video Map

- Snapshot date: `2026-06-14`
- Source: live collection through `opencli bilibili search`, `user-videos`, and `video`
- Channel: [OnekeyAI](https://space.bilibili.com/1948639457)
- Scope: keep videos that are clearly tied to traditional omics, multi-omics, structured or tabular modeling, survival analysis, batch correction, cross-validation, clustering, and directly supporting helper modules
- Exclude by default: pure imaging-only tutorials, pure ROI drawing or segmentation, hardware buying advice, generic grant trend talks, and pure Q and A unless it is specifically about an omics component
- Caution: older Bilibili AI descriptions can be noisy; the titles below were manually re-grouped after live inspection

## Core Workflow

- `2026-05-31` [20260531训练营-sol16-多组学-深度（迁移）学习-单（多）中心-病理弱监督-瘤内瘤周](https://www.bilibili.com/video/BV1V2VS6wEeU) `BV1V2VS6wEeU`: OnekeyAI channel's clearest full-stack multi-omics workflow; covers image plus pathology fusion, WSI patch preprocessing, weak supervision, intratumoral and peritumoral radiomics, and feature or signature fusion.
- `2026-05-25` [20260524训练营-Sol15. 深度（迁移）学习-单（多）中心-组学特征-融合-临床各种可解释性-Web计算器](https://www.bilibili.com/video/BV1t6GW6jEZP) `BV1t6GW6jEZP`: focuses on deep-learning-plus-omics feature fusion, multicenter handling, SHAP or Grad-CAM explainability, fixed data splits, and web calculator deployment.
- `2026-05-17` [20260517训练营-传统组学+深度学习，内涵深度学习的多种玩法，with 交叉验证教程](https://www.bilibili.com/video/BV1jsLH68ETa) `BV1jsLH68ETa`: bridges classic omics, 2D or 2.5D or 3D deep learning, fusion strategies, ROI or peritumor slicing, and practical cross-validation setup.
- `2026-04-14` [20260412训练营-多分类深度学习+组学(with One vs Other)](https://www.bilibili.com/video/BV19EQvBmE4F) `BV19EQvBmE4F`: multi-class omics plus deep-learning workflow; compares plain omics with fusion models and explains One-vs-Other evaluation.
- `2026-03-15` [20260308训练营-文本模态解决方案，从此多组学又添一个新成员。](https://www.bilibili.com/video/BV1NLw3zfEp8) `BV1NLw3zfEp8`: extends the channel's omics framing to Chinese text data; covers text-to-structured features, TF-IDF or BOW style pipelines, and Transformer-based text features.
- `2024-07-18` [20240714训练营-多组学的奇技淫巧以及快速实践](https://www.bilibili.com/video/BV1sz421q7gt) `BV1sz421q7gt`: strong overview of image omics plus pathology omics integration, feature or result fusion, structured data conversion, and practical config ideas.
- `2024-07-16` [奇技淫巧-20240714-多组学论文，可以在哪些方向上进行差异化。](https://www.bilibili.com/video/BV1Tf421q7u2) `BV1Tf421q7u2`: less operational than the training camp video, but useful for deciding how to differentiate a multi-omics paper through modality, fusion, and dimensionality expansion.

## Survival And Structured Data

- `2025-07-16` [20250713训练营-任意结构化数据的生存模型，兼容任何表格数据](https://www.bilibili.com/video/BV19xutzrE1P) `BV19xutzrE1P`: structured-data survival modeling entry point; covers Cox-style labels, DNN and Transformer backbones, multi-head inputs, multitask variants, and c-index or KM or time-dependent ROC evaluation.
- `2025-07-09` [20250706训练营-2.5D vs 2D vs 传统组学生存分析（支持论文生成）](https://www.bilibili.com/video/BV1GwGnzdE88) `BV1GwGnzdE88`: compares 2D, 2.5D, and classic omics survival pipelines; strong for understanding how OnekeyAI frames survival modeling across modalities.
- `2025-07-02` [20250629训练营-基于原生cox loss的深度学习模型以及组学特征](https://www.bilibili.com/video/BV1Qcg6zgEbq) `BV1Qcg6zgEbq`: deep-learning survival modeling with native Cox loss, plus how to combine learned features with omics-style structured features.
- `2024-06-03` [OnekeyComp-Comp2结构化数据建模](https://www.bilibili.com/video/BV1Eb421i7nn) `BV1Eb421i7nn`: short module-level pointer for tabular or structured-data modeling inside the OnekeyComp line.
- `2024-02-28` [20240204训练营-生存分析在Onekey中如何实现？](https://www.bilibili.com/video/BV1zy421q7Vj) `BV1zy421q7Vj`: older but still relevant survival-analysis entry video for Onekey users who need the broad idea before the newer Cox-loss material.

## Evaluation And Helper Modules

- `2026-03-15` [OnekeyComp-Comp8-Combat批次矫正](https://www.bilibili.com/video/BV1Fsw3zXE1V) `BV1Fsw3zXE1V`: batch correction for multicenter studies; explains when Combat is appropriate, how to run it as a standalone module, and how to splice it into an existing omics pipeline.
- `2026-02-28` [20260208训练营-交叉验证在Onekey中如何做？](https://www.bilibili.com/video/BV1wzAtz3E9f) `BV1wzAtz3E9f`: shows how Onekey handles fold generation, repeated runs, and result aggregation for N-fold validation.
- `2025-06-18` [20250615训练营-无监督ITH Score以及多种聚类算法](https://www.bilibili.com/video/BV1siNhzoEoL) `BV1siNhzoEoL`: clustering-heavy video that matters for heterogeneity scoring, unsupervised region grouping, and comparing k-means against other clustering methods.
- `2024-08-01` [20240728训练营-多分类在Onekey中如何实现，Micro-Macro AUC，混淆矩阵](https://www.bilibili.com/video/BV1jT42167vE) `BV1jT42167vE`: evaluation-centric support video for multi-class omics work, especially metric presentation and One-vs-Other comparisons.
- `2023-11-12` [Onekey工具箱-OKT-gen_feature_cluster，可以对任意特征进行聚类分析以及可视化。](https://www.bilibili.com/video/BV1mN4y1D7sK) `BV1mN4y1D7sK`: compact helper video for clustering arbitrary feature matrices and visualizing the result.

## Foundations And Legacy

- `2024-05-13` [20240512训练营-传统组学组件答疑](https://www.bilibili.com/video/BV1wb421z7py) `BV1wb421z7py`: troubleshooting or FAQ style video for the classic omics components.
- `2023-05-28` [Onekey-Comp，传统组学解决方案，可以直接生成论文methods和results的那种](https://www.bilibili.com/video/BV1Bg4y1V7AZ) `BV1Bg4y1V7AZ`: older flagship traditional-omics solution video; keep it because many later videos build on this framing.
- `2022-09-21` [训练营[20220918]-Onekey2.0发布，还在等什么，一键生成传统组学论文](https://www.bilibili.com/video/BV1Md4y1g7nX) `BV1Md4y1g7nX`: early Onekey 2.0 release-era foundation for the channel's traditional-omics automation story.
- `2022-03-18` [OnekeyComp-传统组学任务](https://www.bilibili.com/video/BV163411W7iD) `BV163411W7iD`: compact older overview of the traditional-omics module stack, including feature extraction, filtering, machine learning, ROC, and confusion matrix.
- `2021-12-06` [张老师的半节课系列-简单聊聊多组学](https://www.bilibili.com/video/BV1T44y1a7jp) `BV1T44y1a7jp`: historical background item; keep as a legacy orientation video, but prioritize newer multi-omics workflow videos first.

## Boundary Items

- `2024-06-05` [20240602训练营-生境分析-传统组学的平替](https://www.bilibili.com/video/BV1Vi421U7s2) `BV1Vi421U7s2`: not strict bioinformatics, but useful if the user wants videos that compare habitat analysis against traditional omics logic.
