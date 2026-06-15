# 组学大讲堂生信视频清单

- Snapshot date: `2026-06-15`
- Source: live collection through `opencli bilibili search --type user` and `opencli bilibili user-videos`
- Channel: [组学大讲堂](https://space.bilibili.com/1181501194)
- Channel UID: `1181501194`
- Total included videos: `76`
- Scope: include the creator's bioinformatics analysis, sequencing workflow, R visualization, Linux support, upload workflow, and literature walkthrough videos
- Note: content summaries are title-derived from the live channel list; inspect single videos separately if a deeper outline is needed

## Bucket Counts

- 核心生信分析: `25`
- 测序与数据提交: `11`
- R语言与可视化: `29`
- 科研案例与基础支撑: `11`

## 重点系列导览

- 这一节把全量视频整理成更像课程地图的系列入口，代表视频补抓了页面标签、时长和播放量。
- 当前页面级细节来自 `opencli browser` 直接读取 Bilibili 视频页 `__INITIAL_STATE__`。

- **WGCNA 与候选标志物专题** `4条`：这一组从疾病 biomarker、预后因子、lncRNA 到作物性状网络，覆盖了 WGCNA 的典型输入、模块筛选和候选基因定位思路。 代表视频为 [01.基于WGCNA筛选过敏性哮喘相关biomarker](https://www.bilibili.com/video/BV1k4dnY3EhH) `BV1k4dnY3EhH`，时长=1423s；播放=104；页面标签=biomarker,生物信息,WGCNA。
  系列条目示例：04.基于WGCNA分析玉米株高相关基因网络；03.基于WGCNA分析乳腺癌相关的重要lncRNAs；02.基于WGCNA筛选宫颈癌相关预后因子；01.基于WGCNA筛选过敏性哮喘相关biomarker
- **测序数据获取与公共数据库提交专题** `10条`：这一组围绕原始数据下载、测序结果理解、MD5 校验，以及 GEO、转录组和 16S 数据上传流程，适合做项目数据流转清单。 代表视频为 [01.NCBI高通量测序数据SRA下载](https://www.bilibili.com/video/BV1SbL7znEAk) `BV1SbL7znEAk`，时长=1448s；播放=3461；页面标签=NCBI,SRA,科研,数据下载。
  系列条目示例：01.NCBI高通量测序数据SRA下载；转录组二代测序Fasta数据上传；数据上传与邮件书写；上传整体思路；微生物16S测序数据上传；GEO账号信息完善以及上传整体思路；上传数据准备与归纳；03.测序结果fastq数据解读
- **基因家族、序列与功能注释专题** `17条`：这一组把基因家族分析、序列比对、结构域、通路注释、系统发育树和引物设计串起来，适合植物或动物分子生信路线。 代表视频为 [基因家族概念介绍](https://www.bilibili.com/video/BV1MWoyYsESR) `BV1MWoyYsESR`，时长=611s；播放=2714；页面标签=基因家族,生物信息,文献解读。
  系列条目示例：利用Interpro数据库查看结构域；MapMan植物通路注释软件使用教程；03.Blast序列比对；02.Fasta序列处理-截取-批量提取；基因家族分析文献解读-香椿JAZ家族；基因家族分析文献解读-刀鲚NHE家族；基因家族分析文献解读-黄瓜CBF家族；文献2：菠萝当中WRKY基因家族分析
- **R 语言与科研绘图专题** `30条`：这一组先搭 R 环境和数据结构基础，再进入统计检验与常见科研图形，属于该 UP 最完整的绘图课程链。 代表视频为 [01.R语言简介及R语言编程运行环境搭建](https://www.bilibili.com/video/BV1p2E7zSEKm) `BV1p2E7zSEKm`，时长=1158s；播放=202；页面标签=绘图,统计,R语言,生物信息。
  系列条目示例：10.OTU丰度数据绘制聚类热图；09.基因表达数据绘制聚类热图（下）；08.基因表达数据绘制聚类热图（上）；07.柱状图和气泡图（富集分析结果可视化）；06.特殊点图--火山图和MA图绘制过程；05.数据分布--密度图、箱线图、直方图绘图过程；04.折线图绘图过程（结合点图、误差线显示）；03.基础饼图的绘制过程
- **Linux 与分析环境支撑专题** `8条`：这一组偏环境和工具支撑，适合还在补 Linux、远程服务器、编辑器和表格整理基础的同学。 代表视频为 [01.linux介绍](https://www.bilibili.com/video/BV1XyXHBjEaT) `BV1XyXHBjEaT`，时长=472s；播放=37；页面标签=操作系统,学习,教程,linux,生物信息。
  系列条目示例：03.linux目录切换；02.linux云服务器登录；05.linux命令行技巧；06.linux文件操作；04.linux目录结构；01.linux介绍；Excel使用-Vlookup（生物信息）；生物信息编程工具-vscode

## 核心生信分析

- `2025-06-19` [利用Interpro数据库查看结构域](https://www.bilibili.com/video/BV1ufNiz7EU6) `BV1ufNiz7EU6`: tags=domain,interpro; 讲如何用 InterPro 查看蛋白结构域，用于功能推断与注释。
- `2025-06-11` [MapMan植物通路注释软件使用教程](https://www.bilibili.com/video/BV11uTQzXEih) `BV11uTQzXEih`: tags=pathway,mapman; 介绍 MapMan 做植物通路注释与可视化的基本用法。
- `2025-05-11` [03.Blast序列比对](https://www.bilibili.com/video/BV1iFETz3ELH) `BV1iFETz3ELH`: tags=blast,sequence; 介绍 BLAST 序列比对的基本用途和常见使用场景。
- `2025-05-09` [02.Fasta序列处理-截取-批量提取](https://www.bilibili.com/video/BV1Wn5GztETG) `BV1Wn5GztETG`: tags=fasta,sequence; 讲 FASTA 序列截取、整理与批量提取，属于基础序列处理技能。
- `2025-04-16` [07.Metascape进行基因注释富集分析](https://www.bilibili.com/video/BV1XDoKYHEAm) `BV1XDoKYHEAm`: tags=enrichment,metascape; page_tags=科研,生物信息,WGCNA; duration=695s; views=499; 演示用 Metascape 做功能注释和富集分析，适合作为差异基因后的解释步骤。
- `2025-04-15` [06.KM-plotter网站使用方法](https://www.bilibili.com/video/BV1HJopYmEjt) `BV1HJopYmEjt`: tags=survival,web-tool; 介绍 KM-plotter 的生存分析用法，用于快速验证候选基因与预后的关系。
- `2025-04-14` [05.UALCAN网站使用方法](https://www.bilibili.com/video/BV1KeoGYtEAF) `BV1KeoGYtEAF`: tags=expression,web-tool; 讲 UALCAN 的表达与临床信息查询，用于公共数据库的快速验证。
- `2025-04-10` [04.基于WGCNA分析玉米株高相关基因网络](https://www.bilibili.com/video/BV1cbduY3EQ3) `BV1cbduY3EQ3`: tags=WGCNA,coexpression; 演示如何用 WGCNA 把表达模块与株高表型关联，并定位关键基因网络。
- `2025-04-10` [03.基于WGCNA分析乳腺癌相关的重要lncRNAs](https://www.bilibili.com/video/BV1swdgYmEC8) `BV1swdgYmEC8`: tags=WGCNA,lncRNA; 展示 WGCNA 在肿瘤表达数据中识别关键 lncRNA 模块与候选分子的流程。
- `2025-04-08` [02.基于WGCNA筛选宫颈癌相关预后因子](https://www.bilibili.com/video/BV15kdnYcEmo) `BV15kdnYcEmo`: tags=WGCNA,survival; 围绕宫颈癌案例说明 WGCNA 与预后因子筛选的联动分析思路。
- `2025-04-08` [01.基于WGCNA筛选过敏性哮喘相关biomarker](https://www.bilibili.com/video/BV1k4dnY3EhH) `BV1k4dnY3EhH`: tags=WGCNA,biomarker; page_tags=biomarker,生物信息,WGCNA; duration=1423s; views=104; 用哮喘案例讲 WGCNA 如何筛与疾病相关的候选 biomarker。
- `2025-04-03` [蛋白质互作网络构建](https://www.bilibili.com/video/BV1fLZ1YkEwU) `BV1fLZ1YkEwU`: tags=PPI,network; 讲蛋白质互作网络构建，用于差异基因后的网络层面解释。
- `2025-03-25` [基因家族分析文献解读-香椿JAZ家族](https://www.bilibili.com/video/BV18YotY5EvF) `BV18YotY5EvF`: tags=gene-family,literature; 结合具体物种案例拆解基因家族分析论文的思路、步骤和结果组织。
- `2025-03-25` [基因家族分析文献解读-刀鲚NHE家族](https://www.bilibili.com/video/BV1SYotYVE4d) `BV1SYotYVE4d`: tags=gene-family,literature; 结合具体物种案例拆解基因家族分析论文的思路、步骤和结果组织。
- `2025-03-25` [基因家族分析文献解读-黄瓜CBF家族](https://www.bilibili.com/video/BV1DYotY5EcL) `BV1DYotY5EcL`: tags=gene-family,literature; 结合具体物种案例拆解基因家族分析论文的思路、步骤和结果组织。
- `2025-03-24` [文献2：菠萝当中WRKY基因家族分析](https://www.bilibili.com/video/BV1T4oyYpEfJ) `BV1T4oyYpEfJ`: tags=gene-family,literature; 通过具体文献案例说明基因家族分析的常见流程与结果表达方式。
- `2025-03-24` [文献3：木薯当中NBS基因家族分析分析思路总结](https://www.bilibili.com/video/BV1T4oyYpE2Q) `BV1T4oyYpE2Q`: tags=gene-family,literature; 通过具体文献案例说明基因家族分析的常见流程与结果表达方式。
- `2025-03-24` [文献1：马铃薯当中HSP20基因家族分析](https://www.bilibili.com/video/BV1gHoyYdEpx) `BV1gHoyYdEpx`: tags=gene-family,literature; 通过具体文献案例说明基因家族分析的常见流程与结果表达方式。
- `2025-03-24` [基因家族概念介绍](https://www.bilibili.com/video/BV1MWoyYsESR) `BV1MWoyYsESR`: tags=gene-family,concept; page_tags=基因家族,生物信息,文献解读; duration=611s; views=2714; 介绍基因家族分析的核心概念、常见目标和整体研究框架。
- `2025-03-14` [聚类热图之Hiplot](https://www.bilibili.com/video/BV1QiQgYSEPn) `BV1QiQgYSEPn`: tags=heatmap,hiplot; 介绍 Hiplot 绘制聚类热图的用法，适合作为表达矩阵可视化补充。
- `2025-03-05` [01.Indel引物设计](https://www.bilibili.com/video/BV1Rv94YGEde) `BV1Rv94YGEde`: tags=primer,indel; 讲 Indel 位点引物设计，用于变异验证或分型实验衔接。
- `2025-03-05` [02.SSR引物设计](https://www.bilibili.com/video/BV1vv94YGERj) `BV1vv94YGERj`: tags=primer,SSR; 讲 SSR 引物设计的基础流程，偏分子标记与验证支撑。
- `2025-03-05` [03.SNP引物设计](https://www.bilibili.com/video/BV1vv94YGEp3) `BV1vv94YGEp3`: tags=primer,SNP; 讲 SNP 引物设计，适合作为变异结果下游实验验证的连接步骤。
- `2025-02-21` [进化树的构建与美化Evolview](https://www.bilibili.com/video/BV12pAoeNEC7) `BV12pAoeNEC7`: tags=phylogeny,evolview; 介绍 Evolview 在进化树展示与注释中的基本使用。
- `2025-02-21` [itol美化进化树](https://www.bilibili.com/video/BV1NWAoevE9y) `BV1NWAoevE9y`: tags=phylogeny,itol; 讲用 iTOL 美化进化树，方便系统发育结果展示。

## 测序与数据提交

- `2025-04-25` [01.NCBI高通量测序数据SRA下载](https://www.bilibili.com/video/BV1SbL7znEAk) `BV1SbL7znEAk`: tags=SRA,download; page_tags=NCBI,SRA,科研,数据下载; duration=1448s; views=3461; 演示从 NCBI SRA 获取高通量测序原始数据，是公共数据复用的基础步骤。
- `2025-03-12` [转录组二代测序Fasta数据上传](https://www.bilibili.com/video/BV1qCQnYRE4h) `BV1qCQnYRE4h`: tags=upload,transcriptome; 围绕转录组数据提交讲上传前准备、文件格式和提交动作。
- `2025-03-12` [数据上传与邮件书写](https://www.bilibili.com/video/BV1YQQnYJEXA) `BV1YQQnYJEXA`: tags=upload,communication; 补充上传过程中的邮件沟通与资料说明写法，偏流程支撑。
- `2025-03-12` [上传整体思路](https://www.bilibili.com/video/BV1ZCQnYRENV) `BV1ZCQnYRENV`: tags=upload,workflow; 从整体层面说明公共数据库上传任务应如何组织与分步执行。
- `2025-03-12` [微生物16S测序数据上传](https://www.bilibili.com/video/BV1qCQnYRExY) `BV1qCQnYRExY`: tags=upload,16S; 讲 16S 测序数据上传流程，适合微生物组项目数据归档。
- `2025-03-12` [GEO账号信息完善以及上传整体思路](https://www.bilibili.com/video/BV1qCQnYREhK) `BV1qCQnYREhK`: tags=GEO,upload; page_tags=NCBI,GEO,数据上传; duration=569s; views=606; 说明 GEO 账号配置、元数据准备和整体上传逻辑。
- `2025-03-12` [上传数据准备与归纳](https://www.bilibili.com/video/BV1qCQnYREA2) `BV1qCQnYREA2`: tags=upload,workflow; 梳理数据上传前的文件整理、信息归纳和提交流程准备。
- `2025-02-20` [03.测序结果fastq数据解读](https://www.bilibili.com/video/BV1ooAJejEct) `BV1ooAJejEct`: tags=FASTQ,sequencing; 讲 FASTQ 结果的基本结构和测序结果阅读方式。
- `2025-02-20` [04.数据完整性校验MD5](https://www.bilibili.com/video/BV1GsAJeuE54) `BV1GsAJeuE54`: tags=checksum,sequencing; 介绍 MD5 校验在测序数据传输和归档中的作用。
- `2025-02-20` [02.测序原理关键技术解读](https://www.bilibili.com/video/BV1joAJe7EwB) `BV1joAJe7EwB`: tags=sequencing,principles; 解释测序原理和关键技术背景，帮助理解下游数据特征。
- `2025-02-20` [01.illumina边合成成边测序原理](https://www.bilibili.com/video/BV1doAJejEV5) `BV1doAJejEV5`: tags=illumina,principles; 介绍 Illumina 边合成边测序的基本原理。

## R语言与可视化

- `2025-08-01` [10.OTU丰度数据绘制聚类热图](https://www.bilibili.com/video/BV1D38wzmEqS) `BV1D38wzmEqS`: tags=plotting,OTU; 讲 OTU 丰度矩阵热图，适合微生物组结果可视化。
- `2025-07-31` [09.基因表达数据绘制聚类热图（下）](https://www.bilibili.com/video/BV1DV8wzjEgN) `BV1DV8wzjEgN`: tags=plotting,heatmap; 讲基因表达矩阵的聚类热图绘制与版式控制。
- `2025-07-30` [08.基因表达数据绘制聚类热图（上）](https://www.bilibili.com/video/BV1dk8wz4EDy) `BV1dk8wz4EDy`: tags=plotting,heatmap; page_tags=统计,绘图,R语言,生物信息; duration=1848s; views=194; 讲基因表达矩阵的聚类热图绘制与版式控制。
- `2025-07-29` [07.柱状图和气泡图（富集分析结果可视化）](https://www.bilibili.com/video/BV1q68wzZEcq) `BV1q68wzZEcq`: tags=plotting,enrichment; 讲富集分析结果常见的柱状图和气泡图展示。
- `2025-07-28` [06.特殊点图--火山图和MA图绘制过程](https://www.bilibili.com/video/BV1YS8wzXEV6) `BV1YS8wzXEV6`: tags=plotting,DEG; 围绕差异分析常见的火山图和 MA 图讲绘制与解读。
- `2025-07-24` [05.数据分布--密度图、箱线图、直方图绘图过程](https://www.bilibili.com/video/BV1v28wz9Ege) `BV1v28wz9Ege`: tags=plotting,distribution; 讲几种常见分布图的场景和绘制流程。
- `2025-07-11` [04.折线图绘图过程（结合点图、误差线显示）](https://www.bilibili.com/video/BV1kJKmziEYV) `BV1kJKmziEYV`: tags=plotting,line; 讲折线图与误差线的结合展示，适合时间序列或分组趋势。
- `2025-07-07` [03.基础饼图的绘制过程](https://www.bilibili.com/video/BV1BbKmz8EAD) `BV1BbKmz8EAD`: tags=plotting,pie; 讲基础饼图的绘制步骤和比例展示逻辑。
- `2025-07-04` [02.分组柱状图与堆叠柱状图绘制过程](https://www.bilibili.com/video/BV1zxKmzaELn) `BV1zxKmzaELn`: tags=plotting,barplot; 比较分组柱状图与堆叠柱状图的绘制方式。
- `2025-06-30` [01.基础柱状图绘制方法](https://www.bilibili.com/video/BV11GKmz3Ems) `BV11GKmz3Ems`: tags=plotting,barplot; 讲基础柱状图的构建思路和常用展示场景。
- `2025-06-29` [19.R语言绘图-拼图之画布的分隔](https://www.bilibili.com/video/BV1LJKDzPEja) `BV1LJKDzPEja`: tags=R,layout; 讲多图拼接时的画布切分与布局安排。
- `2025-06-28` [18.R语言绘图-pie饼图绘制](https://www.bilibili.com/video/BV1WwKDz1ENK) `BV1WwKDz1ENK`: tags=R,pie; 讲饼图绘制与类别占比展示。
- `2025-06-27` [17.R语言绘图-hist频率直方图绘制](https://www.bilibili.com/video/BV1sfKSzmEst) `BV1sfKSzmEst`: tags=R,histogram; 讲直方图绘制，用于连续变量分布观察。
- `2025-06-26` [16.R语言绘图-boxplot箱形图绘制](https://www.bilibili.com/video/BV1zgKDzgE9n) `BV1zgKDzgE9n`: tags=R,boxplot; 讲箱线图绘制，用于分布比较和异常值展示。
- `2025-06-20` [15.R语言绘图-text图片中添加文字及调整](https://www.bilibili.com/video/BV1Q9NizSEii) `BV1Q9NizSEii`: tags=R,annotation; 讲在图中添加文字注释与位置样式调整。
- `2025-06-18` [14.R语言柱状图绘制-及x坐标轴调整](https://www.bilibili.com/video/BV1ufNiz7ESD) `BV1ufNiz7ESD`: tags=R,barplot; 演示柱状图绘制和坐标轴微调。
- `2025-06-13` [13.R语言颜色透明色表示-添加图例legend及位置调整](https://www.bilibili.com/video/BV1k5TQzJESd) `BV1k5TQzJESd`: tags=R,plot; 讲颜色透明度、图例添加与位置调整等图形细节。
- `2025-06-09` [12.R语言绘图-par()绘图参数详解](https://www.bilibili.com/video/BV1G97qzXESb) `BV1G97qzXESb`: tags=R,plot; 解释 par() 控制画布布局和绘图全局参数。
- `2025-06-06` [11.R语言绘图点线图-plot绘图参数详解](https://www.bilibili.com/video/BV15S7qzxESe) `BV15S7qzxESe`: tags=R,plot; 讲基础 plot 点线图及核心参数设置。
- `2025-06-04` [10.R语言方差分析分析原理-代码实现-结果可视化](https://www.bilibili.com/video/BV15S7qzxEW3) `BV15S7qzxEW3`: tags=R,statistics; 介绍方差分析的原理、代码实现与结果展示。
- `2025-05-30` [09.R语言T检验分析原理-代码实现-结果可视化-批量T检验](https://www.bilibili.com/video/BV1kVjuzpEQy) `BV1kVjuzpEQy`: tags=R,statistics; 介绍 T 检验原理、代码实现和结果可视化。
- `2025-05-28` [08.R语言数据reshape-长型数据与宽型数据转换-方便数据后续分析](https://www.bilibili.com/video/BV1wVjuzWE9m) `BV1wVjuzWE9m`: tags=R,reshape; 讲长宽表转换，适合下游统计建模与可视化准备。
- `2025-05-26` [07.R语言数据分类汇总统计applytapplylapplyaggregate学习](https://www.bilibili.com/video/BV1CVjuzpEh4) `BV1CVjuzpEh4`: tags=R,aggregation; 介绍 apply、tapply、lapply、aggregate 等汇总统计方法。
- `2025-05-23` [06.R语言循环与判断语句](https://www.bilibili.com/video/BV1dfJGzFE1V) `BV1dfJGzFE1V`: tags=R,control-flow; 讲循环和条件判断，为批量分析脚本打基础。
- `2025-05-21` [05.R语言数据读入与写出方法与技巧readtable-writetable](https://www.bilibili.com/video/BV1ofJGzFEjz) `BV1ofJGzFEjz`: tags=R,io; 讲表格数据读写和文件输入输出，是生信数据处理基础。
- `2025-05-19` [04.R语言数据类型使用技巧标量，向量，数据框，因子，列表（下）](https://www.bilibili.com/video/BV1ifJGzFESw) `BV1ifJGzFESw`: tags=R,data-structures; 解释向量、数据框、因子和列表等核心数据结构。
- `2025-05-16` [03.R语言数据类型使用技巧标量，向量，数据框，因子，列表（上）](https://www.bilibili.com/video/BV16GEJzDEBS) `BV16GEJzDEBS`: tags=R,data-structures; 解释向量、数据框、因子和列表等核心数据结构。
- `2025-05-14` [02.R语言第三方包安装方法与技巧（CRANbioconductor）](https://www.bilibili.com/video/BV1z5EJzJE9z) `BV1z5EJzJE9z`: tags=R,packages; 讲 CRAN 与 Bioconductor 包安装，是后续生信分析环境准备。
- `2025-05-12` [01.R语言简介及R语言编程运行环境搭建](https://www.bilibili.com/video/BV1p2E7zSEKm) `BV1p2E7zSEKm`: tags=R,setup; page_tags=绘图,统计,R语言,生物信息; duration=1158s; views=202; 介绍 R 语言定位并完成基础运行环境搭建。

## 科研案例与基础支撑

- `2026-03-26` [03.linux目录切换](https://www.bilibili.com/video/BV1GyXHB7EZa) `BV1GyXHB7EZa`: tags=linux,filesystem; 讲目录导航、路径识别和常用目录切换命令。
- `2026-03-26` [02.linux云服务器登录](https://www.bilibili.com/video/BV1XyXHBjEzn) `BV1XyXHBjEzn`: tags=linux,server; 演示连接云服务器的基本方法，为远程运行生信分析做准备。
- `2026-03-26` [05.linux命令行技巧](https://www.bilibili.com/video/BV1GyXHB7Edi) `BV1GyXHB7Edi`: tags=linux,shell; 总结命令行操作技巧，提高生信环境中的终端使用效率。
- `2026-03-26` [06.linux文件操作](https://www.bilibili.com/video/BV1YyXHB7Est) `BV1YyXHB7Est`: tags=linux,file-ops; 讲文件查看、复制、移动和整理，适合作为生信数据管理基础。
- `2026-03-26` [04.linux目录结构](https://www.bilibili.com/video/BV19yXHBjEu7) `BV19yXHBjEu7`: tags=linux,filesystem; 解释 Linux 文件系统层级，帮助理解后续数据与脚本存放位置。
- `2026-03-26` [01.linux介绍](https://www.bilibili.com/video/BV1XyXHBjEaT) `BV1XyXHBjEaT`: tags=linux,environment; page_tags=操作系统,学习,教程,linux,生物信息; duration=472s; views=37; 介绍 Linux 在生信流程中的角色、常见使用场景和入门路径。
- `2025-07-25` [03.文献3：紫花苜蓿的基因组选择特征](https://www.bilibili.com/video/BV1ra8wzPEtv) `BV1ra8wzPEtv`: tags=literature,genomic-selection; 围绕紫花苜蓿案例梳理基因组选择特征分析的研究问题与结果组织方式。
- `2025-07-09` [02.文献2：芥菜的起源、驯化与多样性](https://www.bilibili.com/video/BV16sKmzAEPF) `BV16sKmzAEPF`: tags=literature,domestication; 借芥菜案例讲群体遗传和驯化研究如何组织样本、变异与群体结构分析。
- `2025-07-02` [01.群体研究分析思路文献1：水蜜桃糖酸风味遗传基础](https://www.bilibili.com/video/BV1CjKmzBEdW) `BV1CjKmzBEdW`: tags=literature,population-study; 用水蜜桃糖酸风味案例拆解群体研究的表型设计、遗传关联和候选位点挖掘思路。
- `2025-03-13` [Excel使用-Vlookup（生物信息）](https://www.bilibili.com/video/BV18NQAYZE3f) `BV18NQAYZE3f`: tags=excel,table; 讲用 Excel VLOOKUP 做表格映射，适合作为生信结果整理辅助技能。
- `2024-03-13` [生物信息编程工具-vscode](https://www.bilibili.com/video/BV1oF4m1F7P2) `BV1oF4m1F7P2`: tags=vscode,environment; 介绍 VS Code 在生信脚本编辑与运行中的基础用途。
