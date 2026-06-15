from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


CHANNEL_UID = "1181501194"
CHANNEL_NAME = "组学大讲堂"
CHANNEL_URL = f"https://space.bilibili.com/{CHANNEL_UID}"

OUTPUT_MD_STEM = "omics-lecture-hall-bioinfo-video-map"
OUTPUT_JSON_STEM = "omics-lecture-hall-bioinfo-videos"

BUCKET_ORDER = [
    "核心生信分析",
    "测序与数据提交",
    "R语言与可视化",
    "科研案例与基础支撑",
]

BROWSER_SESSION = "omicslecturehall"

HIGHLIGHT_BVIDS = {
    "BV1k4dnY3EhH",  # WGCNA biomarker
    "BV1SbL7znEAk",  # SRA download
    "BV1qCQnYREhK",  # GEO upload
    "BV1MWoyYsESR",  # gene family concept
    "BV1XDoKYHEAm",  # Metascape
    "BV1p2E7zSEKm",  # R setup
    "BV1dk8wz4EDy",  # heatmap
    "BV1XyXHBjEaT",  # linux intro
}

SERIES_GUIDES: list[dict[str, object]] = [
    {
        "name": "WGCNA 与候选标志物专题",
        "patterns": [r"WGCNA"],
        "representative_bvid": "BV1k4dnY3EhH",
        "summary": "这一组从疾病 biomarker、预后因子、lncRNA 到作物性状网络，覆盖了 WGCNA 的典型输入、模块筛选和候选基因定位思路。",
    },
    {
        "name": "测序数据获取与公共数据库提交专题",
        "patterns": [r"SRA", r"GEO", r"上传", r"FASTQ", r"illumina", r"测序", r"16S"],
        "representative_bvid": "BV1SbL7znEAk",
        "summary": "这一组围绕原始数据下载、测序结果理解、MD5 校验，以及 GEO、转录组和 16S 数据上传流程，适合做项目数据流转清单。",
    },
    {
        "name": "基因家族、序列与功能注释专题",
        "patterns": [r"基因家族", r"Blast", r"Fasta", r"Interpro", r"MapMan", r"进化树", r"itol", r"Evolview", r"引物"],
        "representative_bvid": "BV1MWoyYsESR",
        "summary": "这一组把基因家族分析、序列比对、结构域、通路注释、系统发育树和引物设计串起来，适合植物或动物分子生信路线。",
    },
    {
        "name": "R 语言与科研绘图专题",
        "patterns": [r"R语言", r"绘图", r"热图", r"火山图", r"MA图", r"柱状图", r"气泡图", r"箱线图", r"直方图", r"饼图", r"折线图", r"OTU"],
        "representative_bvid": "BV1p2E7zSEKm",
        "summary": "这一组先搭 R 环境和数据结构基础，再进入统计检验与常见科研图形，属于该 UP 最完整的绘图课程链。",
    },
    {
        "name": "Linux 与分析环境支撑专题",
        "patterns": [r"linux", r"vscode", r"Vlookup"],
        "representative_bvid": "BV1XyXHBjEaT",
        "summary": "这一组偏环境和工具支撑，适合还在补 Linux、远程服务器、编辑器和表格整理基础的同学。",
    },
]

SUMMARY_RULES: list[tuple[str, str, list[str], str]] = [
    (r"linux介绍", "科研案例与基础支撑", ["linux", "environment"], "介绍 Linux 在生信流程中的角色、常见使用场景和入门路径。"),
    (r"linux云服务器登录", "科研案例与基础支撑", ["linux", "server"], "演示连接云服务器的基本方法，为远程运行生信分析做准备。"),
    (r"linux目录切换", "科研案例与基础支撑", ["linux", "filesystem"], "讲目录导航、路径识别和常用目录切换命令。"),
    (r"linux目录结构", "科研案例与基础支撑", ["linux", "filesystem"], "解释 Linux 文件系统层级，帮助理解后续数据与脚本存放位置。"),
    (r"linux命令行技巧", "科研案例与基础支撑", ["linux", "shell"], "总结命令行操作技巧，提高生信环境中的终端使用效率。"),
    (r"linux文件操作", "科研案例与基础支撑", ["linux", "file-ops"], "讲文件查看、复制、移动和整理，适合作为生信数据管理基础。"),
    (r"群体研究分析思路文献1", "科研案例与基础支撑", ["literature", "population-study"], "用水蜜桃糖酸风味案例拆解群体研究的表型设计、遗传关联和候选位点挖掘思路。"),
    (r"文献2：芥菜的起源、驯化与多样性", "科研案例与基础支撑", ["literature", "domestication"], "借芥菜案例讲群体遗传和驯化研究如何组织样本、变异与群体结构分析。"),
    (r"文献3：紫花苜蓿的基因组选择特征", "科研案例与基础支撑", ["literature", "genomic-selection"], "围绕紫花苜蓿案例梳理基因组选择特征分析的研究问题与结果组织方式。"),
    (r"基于WGCNA分析玉米株高相关基因网络", "核心生信分析", ["WGCNA", "coexpression"], "演示如何用 WGCNA 把表达模块与株高表型关联，并定位关键基因网络。"),
    (r"基于WGCNA分析乳腺癌相关的重要lncRNAs", "核心生信分析", ["WGCNA", "lncRNA"], "展示 WGCNA 在肿瘤表达数据中识别关键 lncRNA 模块与候选分子的流程。"),
    (r"基于WGCNA筛选宫颈癌相关预后因子", "核心生信分析", ["WGCNA", "survival"], "围绕宫颈癌案例说明 WGCNA 与预后因子筛选的联动分析思路。"),
    (r"基于WGCNA筛选过敏性哮喘相关biomarker", "核心生信分析", ["WGCNA", "biomarker"], "用哮喘案例讲 WGCNA 如何筛与疾病相关的候选 biomarker。"),
    (r"Metascape进行基因注释富集分析", "核心生信分析", ["enrichment", "metascape"], "演示用 Metascape 做功能注释和富集分析，适合作为差异基因后的解释步骤。"),
    (r"KM-plotter网站使用方法", "核心生信分析", ["survival", "web-tool"], "介绍 KM-plotter 的生存分析用法，用于快速验证候选基因与预后的关系。"),
    (r"UALCAN网站使用方法", "核心生信分析", ["expression", "web-tool"], "讲 UALCAN 的表达与临床信息查询，用于公共数据库的快速验证。"),
    (r"Blast序列比对", "核心生信分析", ["blast", "sequence"], "介绍 BLAST 序列比对的基本用途和常见使用场景。"),
    (r"Fasta序列处理", "核心生信分析", ["fasta", "sequence"], "讲 FASTA 序列截取、整理与批量提取，属于基础序列处理技能。"),
    (r"NCBI高通量测序数据SRA下载", "测序与数据提交", ["SRA", "download"], "演示从 NCBI SRA 获取高通量测序原始数据，是公共数据复用的基础步骤。"),
    (r"转录组二代测序Fasta数据上传", "测序与数据提交", ["upload", "transcriptome"], "围绕转录组数据提交讲上传前准备、文件格式和提交动作。"),
    (r"微生物16S测序数据上传", "测序与数据提交", ["upload", "16S"], "讲 16S 测序数据上传流程，适合微生物组项目数据归档。"),
    (r"GEO账号信息完善以及上传整体思路", "测序与数据提交", ["GEO", "upload"], "说明 GEO 账号配置、元数据准备和整体上传逻辑。"),
    (r"上传数据准备与归纳", "测序与数据提交", ["upload", "workflow"], "梳理数据上传前的文件整理、信息归纳和提交流程准备。"),
    (r"上传整体思路", "测序与数据提交", ["upload", "workflow"], "从整体层面说明公共数据库上传任务应如何组织与分步执行。"),
    (r"数据上传与邮件书写", "测序与数据提交", ["upload", "communication"], "补充上传过程中的邮件沟通与资料说明写法，偏流程支撑。"),
    (r"测序结果fastq数据解读", "测序与数据提交", ["FASTQ", "sequencing"], "讲 FASTQ 结果的基本结构和测序结果阅读方式。"),
    (r"数据完整性校验MD5", "测序与数据提交", ["checksum", "sequencing"], "介绍 MD5 校验在测序数据传输和归档中的作用。"),
    (r"测序原理关键技术解读", "测序与数据提交", ["sequencing", "principles"], "解释测序原理和关键技术背景，帮助理解下游数据特征。"),
    (r"illumina边合成成边测序原理", "测序与数据提交", ["illumina", "principles"], "介绍 Illumina 边合成边测序的基本原理。"),
    (r"基因家族概念介绍", "核心生信分析", ["gene-family", "concept"], "介绍基因家族分析的核心概念、常见目标和整体研究框架。"),
    (r"基因家族分析文献解读", "核心生信分析", ["gene-family", "literature"], "结合具体物种案例拆解基因家族分析论文的思路、步骤和结果组织。"),
    (r"文献[123]：.*基因家族分析", "核心生信分析", ["gene-family", "literature"], "通过具体文献案例说明基因家族分析的常见流程与结果表达方式。"),
    (r"蛋白质互作网络构建", "核心生信分析", ["PPI", "network"], "讲蛋白质互作网络构建，用于差异基因后的网络层面解释。"),
    (r"MapMan植物通路注释软件使用教程", "核心生信分析", ["pathway", "mapman"], "介绍 MapMan 做植物通路注释与可视化的基本用法。"),
    (r"Interpro数据库查看结构域", "核心生信分析", ["domain", "interpro"], "讲如何用 InterPro 查看蛋白结构域，用于功能推断与注释。"),
    (r"聚类热图之Hiplot", "核心生信分析", ["heatmap", "hiplot"], "介绍 Hiplot 绘制聚类热图的用法，适合作为表达矩阵可视化补充。"),
    (r"itol美化进化树", "核心生信分析", ["phylogeny", "itol"], "讲用 iTOL 美化进化树，方便系统发育结果展示。"),
    (r"进化树的构建与美化Evolview", "核心生信分析", ["phylogeny", "evolview"], "介绍 Evolview 在进化树展示与注释中的基本使用。"),
    (r"Indel引物设计", "核心生信分析", ["primer", "indel"], "讲 Indel 位点引物设计，用于变异验证或分型实验衔接。"),
    (r"SSR引物设计", "核心生信分析", ["primer", "SSR"], "讲 SSR 引物设计的基础流程，偏分子标记与验证支撑。"),
    (r"SNP引物设计", "核心生信分析", ["primer", "SNP"], "讲 SNP 引物设计，适合作为变异结果下游实验验证的连接步骤。"),
    (r"R语言简介及R语言编程运行环境搭建", "R语言与可视化", ["R", "setup"], "介绍 R 语言定位并完成基础运行环境搭建。"),
    (r"R语言第三方包安装方法与技巧", "R语言与可视化", ["R", "packages"], "讲 CRAN 与 Bioconductor 包安装，是后续生信分析环境准备。"),
    (r"R语言数据类型使用技巧", "R语言与可视化", ["R", "data-structures"], "解释向量、数据框、因子和列表等核心数据结构。"),
    (r"R语言数据读入与写出方法与技巧", "R语言与可视化", ["R", "io"], "讲表格数据读写和文件输入输出，是生信数据处理基础。"),
    (r"R语言循环与判断语句", "R语言与可视化", ["R", "control-flow"], "讲循环和条件判断，为批量分析脚本打基础。"),
    (r"R语言数据分类汇总统计", "R语言与可视化", ["R", "aggregation"], "介绍 apply、tapply、lapply、aggregate 等汇总统计方法。"),
    (r"R语言数据reshape", "R语言与可视化", ["R", "reshape"], "讲长宽表转换，适合下游统计建模与可视化准备。"),
    (r"R语言T检验分析原理", "R语言与可视化", ["R", "statistics"], "介绍 T 检验原理、代码实现和结果可视化。"),
    (r"R语言方差分析分析原理", "R语言与可视化", ["R", "statistics"], "介绍方差分析的原理、代码实现与结果展示。"),
    (r"R语言绘图点线图-plot绘图参数详解", "R语言与可视化", ["R", "plot"], "讲基础 plot 点线图及核心参数设置。"),
    (r"R语言绘图-par\(\)绘图参数详解", "R语言与可视化", ["R", "plot"], "解释 par() 控制画布布局和绘图全局参数。"),
    (r"R语言颜色透明色表示-添加图例legend及位置调整", "R语言与可视化", ["R", "plot"], "讲颜色透明度、图例添加与位置调整等图形细节。"),
    (r"R语言柱状图绘制-及x坐标轴调整", "R语言与可视化", ["R", "barplot"], "演示柱状图绘制和坐标轴微调。"),
    (r"R语言绘图-text图片中添加文字及调整", "R语言与可视化", ["R", "annotation"], "讲在图中添加文字注释与位置样式调整。"),
    (r"R语言绘图-boxplot箱形图绘制", "R语言与可视化", ["R", "boxplot"], "讲箱线图绘制，用于分布比较和异常值展示。"),
    (r"R语言绘图-hist频率直方图绘制", "R语言与可视化", ["R", "histogram"], "讲直方图绘制，用于连续变量分布观察。"),
    (r"R语言绘图-pie饼图绘制", "R语言与可视化", ["R", "pie"], "讲饼图绘制与类别占比展示。"),
    (r"R语言绘图-拼图之画布的分隔", "R语言与可视化", ["R", "layout"], "讲多图拼接时的画布切分与布局安排。"),
    (r"基础柱状图绘制方法", "R语言与可视化", ["plotting", "barplot"], "讲基础柱状图的构建思路和常用展示场景。"),
    (r"分组柱状图与堆叠柱状图绘制过程", "R语言与可视化", ["plotting", "barplot"], "比较分组柱状图与堆叠柱状图的绘制方式。"),
    (r"基础饼图的绘制过程", "R语言与可视化", ["plotting", "pie"], "讲基础饼图的绘制步骤和比例展示逻辑。"),
    (r"折线图绘图过程", "R语言与可视化", ["plotting", "line"], "讲折线图与误差线的结合展示，适合时间序列或分组趋势。"),
    (r"数据分布--密度图、箱线图、直方图绘图过程", "R语言与可视化", ["plotting", "distribution"], "讲几种常见分布图的场景和绘制流程。"),
    (r"特殊点图--火山图和MA图绘制过程", "R语言与可视化", ["plotting", "DEG"], "围绕差异分析常见的火山图和 MA 图讲绘制与解读。"),
    (r"柱状图和气泡图（富集分析结果可视化）", "R语言与可视化", ["plotting", "enrichment"], "讲富集分析结果常见的柱状图和气泡图展示。"),
    (r"基因表达数据绘制聚类热图", "R语言与可视化", ["plotting", "heatmap"], "讲基因表达矩阵的聚类热图绘制与版式控制。"),
    (r"OTU丰度数据绘制聚类热图", "R语言与可视化", ["plotting", "OTU"], "讲 OTU 丰度矩阵热图，适合微生物组结果可视化。"),
    (r"Excel使用-Vlookup", "科研案例与基础支撑", ["excel", "table"], "讲用 Excel VLOOKUP 做表格映射，适合作为生信结果整理辅助技能。"),
    (r"生物信息编程工具-vscode", "科研案例与基础支撑", ["vscode", "environment"], "介绍 VS Code 在生信脚本编辑与运行中的基础用途。"),
]

FALLBACK_RULES: list[tuple[str, str, list[str], str]] = [
    (r"基因家族", "核心生信分析", ["gene-family"], "围绕基因家族分析的概念、文献或流程展开，是植物和动物生信中的常见专题。"),
    (r"上传", "测序与数据提交", ["upload"], "围绕公共数据库或项目文件上传流程展开，属于数据归档与交付支撑。"),
    (r"R语言|绘图|热图|火山图|MA图|柱状图|气泡图|箱线图|直方图|饼图", "R语言与可视化", ["plotting"], "围绕 R 或常见科研可视化图形的制作展开，属于生信结果展示基础。"),
    (r"测序|FASTQ|illumina|SRA|GEO|16S", "测序与数据提交", ["sequencing"], "围绕测序数据、公共数据库或提交流程展开。"),
]


def resolve_opencli() -> str:
    for name in ("opencli.cmd", "opencli", "opencli.ps1"):
        found = shutil.which(name)
        if found:
            return found
    for candidate in (
        r"C:\Users\simon\AppData\Roaming\npm\opencli.cmd",
        r"C:\Users\simon\AppData\Roaming\npm\opencli",
        r"C:\Users\simon\AppData\Roaming\npm\opencli.ps1",
    ):
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Could not resolve opencli on this machine.")


OPENCLI_BIN = resolve_opencli()
OPENCLI_ENV = {"OPENCLI_BROWSER_COMMAND_TIMEOUT": "180"}


def run_opencli(*args: str) -> str:
    completed = subprocess.run(
        [OPENCLI_BIN, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env={**os.environ, **OPENCLI_ENV},
    )
    if completed.returncode == 0:
        return completed.stdout
    sys.stderr.write(completed.stderr or completed.stdout)
    raise SystemExit(completed.returncode)


def fetch_user_videos(uid: str, page: int, limit: int) -> list[dict]:
    raw = run_opencli(
        "bilibili",
        "user-videos",
        uid,
        "--limit",
        str(limit),
        "--page",
        str(page),
        "--order",
        "pubdate",
        "--window",
        "background",
        "--site-session",
        "ephemeral",
        "-f",
        "json",
    )
    rows = json.loads(raw)
    if not isinstance(rows, list):
        raise ValueError(f"Unexpected response type for page {page}: {type(rows)!r}")
    return rows


def fetch_browser_detail(bvid: str) -> dict[str, object]:
    run_opencli("browser", BROWSER_SESSION, "open", f"https://www.bilibili.com/video/{bvid}")
    raw = run_opencli(
        "browser",
        BROWSER_SESSION,
        "eval",
        (
            "JSON.stringify({"
            "title: window.__INITIAL_STATE__?.videoData?.title ?? '',"
            "pubdate: window.__INITIAL_STATE__?.videoData?.pubdate ?? null,"
            "duration: window.__INITIAL_STATE__?.videoData?.duration ?? null,"
            "view: window.__INITIAL_STATE__?.videoData?.stat?.view ?? null,"
            "like: window.__INITIAL_STATE__?.videoData?.stat?.like ?? null,"
            "favorite: window.__INITIAL_STATE__?.videoData?.stat?.favorite ?? null,"
            "share: window.__INITIAL_STATE__?.videoData?.stat?.share ?? null,"
            "tag_name: (window.__INITIAL_STATE__?.tags ?? []).map(t => t.tag_name)"
            "})"
        ),
    )
    detail = json.loads(raw)
    if not isinstance(detail, dict):
        raise ValueError(f"Unexpected browser detail for {bvid}: {type(detail)!r}")
    return detail


def extract_bvid(url: str) -> str:
    match = re.search(r"/video/([^/?]+)", url)
    return match.group(1) if match else ""


def classify_title(title: str) -> tuple[str, list[str], str]:
    for pattern, bucket, tags, summary in SUMMARY_RULES:
        if re.search(pattern, title, re.IGNORECASE):
            return bucket, tags, summary
    for pattern, bucket, tags, summary in FALLBACK_RULES:
        if re.search(pattern, title, re.IGNORECASE):
            return bucket, tags, summary
    return (
        "科研案例与基础支撑",
        ["general"],
        "与生信工作流相关的基础支撑内容，适合作为该频道的补充学习项。",
    )


def enrich_highlights(items: list[dict]) -> None:
    lookup = {item["bvid"]: item for item in items}
    for bvid in HIGHLIGHT_BVIDS:
        item = lookup.get(bvid)
        if not item:
            continue
        try:
            detail = fetch_browser_detail(bvid)
        except Exception as exc:
            item["detail_error"] = str(exc)
            continue
        tag_names = [str(tag) for tag in detail.get("tag_name", []) if str(tag).strip()]
        duration = detail.get("duration")
        view = detail.get("view")
        like = detail.get("like")
        favorite = detail.get("favorite")
        share = detail.get("share")
        item["page_tags"] = tag_names
        item["duration_seconds"] = duration
        item["view_count"] = view
        item["like_count"] = like
        item["favorite_count"] = favorite
        item["share_count"] = share
        item["detail_source"] = "opencli browser __INITIAL_STATE__"


def build_series_sections(items: list[dict]) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    for series in SERIES_GUIDES:
        pattern_list = [re.compile(pattern, re.IGNORECASE) for pattern in series["patterns"]]  # type: ignore[index]
        matches = [
            item
            for item in items
            if any(pattern.search(str(item["title"])) for pattern in pattern_list)
        ]
        if not matches:
            continue
        representative = next(
            (item for item in matches if item["bvid"] == series["representative_bvid"]),
            matches[0],
        )
        sections.append(
            {
                "name": series["name"],
                "summary": series["summary"],
                "count": len(matches),
                "representative": representative,
                "titles": [item["title"] for item in matches[:8]],
            }
        )
    return sections


def collect_items(uid: str, max_pages: int, limit: int, with_highlights: bool) -> list[dict]:
    items: list[dict] = []
    seen_bvids: set[str] = set()
    for page in range(1, max_pages + 1):
        rows = fetch_user_videos(uid, page, limit)
        if not rows:
            break
        for row in rows:
            url = row.get("url", "")
            bvid = extract_bvid(url)
            if not bvid or bvid in seen_bvids:
                continue
            seen_bvids.add(bvid)
            title = row.get("title", "").strip()
            bucket, tags, summary = classify_title(title)
            items.append(
                {
                    "bucket": bucket,
                    "tags": tags,
                    "title": title,
                    "date": row.get("date", ""),
                    "plays": row.get("plays", ""),
                    "likes": row.get("likes", ""),
                    "url": url,
                    "bvid": bvid,
                    "content_summary": summary,
                }
            )
    if with_highlights:
        enrich_highlights(items)
    return items


def write_outputs(items: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    dated_json = output_dir / f"{OUTPUT_JSON_STEM}-{today}.json"
    dated_md = output_dir / f"{OUTPUT_MD_STEM}-{today}.md"
    latest_json = output_dir / f"{OUTPUT_JSON_STEM}-latest.json"
    latest_md = output_dir / f"{OUTPUT_MD_STEM}-latest.md"

    payload = {
        "snapshot_date": today,
        "channel_name": CHANNEL_NAME,
        "channel_uid": CHANNEL_UID,
        "channel_url": CHANNEL_URL,
        "video_count": len(items),
        "items": items,
    }
    json_text = json.dumps(payload, ensure_ascii=False, indent=2)
    dated_json.write_text(json_text, encoding="utf-8")
    latest_json.write_text(json_text, encoding="utf-8")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        grouped[item["bucket"]].append(item)
    series_sections = build_series_sections(items)

    lines = [
        "# 组学大讲堂生信视频清单",
        "",
        f"- Snapshot date: `{today}`",
        "- Source: live collection through `opencli bilibili search --type user` and `opencli bilibili user-videos`",
        f"- Channel: [{CHANNEL_NAME}]({CHANNEL_URL})",
        f"- Channel UID: `{CHANNEL_UID}`",
        f"- Total included videos: `{len(items)}`",
        "- Scope: include the creator's bioinformatics analysis, sequencing workflow, R visualization, Linux support, upload workflow, and literature walkthrough videos",
        "- Note: content summaries are title-derived from the live channel list; inspect single videos separately if a deeper outline is needed",
        "",
        "## Bucket Counts",
        "",
    ]
    for bucket in BUCKET_ORDER:
        lines.append(f"- {bucket}: `{len(grouped.get(bucket, []))}`")
    lines.append("")

    lines.extend(
        [
            "## 重点系列导览",
            "",
            "- 这一节把全量视频整理成更像课程地图的系列入口，代表视频补抓了页面标签、时长和播放量。",
            "- 当前页面级细节来自 `opencli browser` 直接读取 Bilibili 视频页 `__INITIAL_STATE__`。",
            "",
        ]
    )
    for series in series_sections:
        representative = series["representative"]
        details: list[str] = []
        if representative.get("duration_seconds"):
            details.append(f"时长={representative['duration_seconds']}s")
        if representative.get("view_count") is not None:
            details.append(f"播放={representative['view_count']}")
        if representative.get("page_tags"):
            details.append(f"页面标签={','.join(representative['page_tags'])}")
        detail_text = "；".join(details) if details else "页面细节未补抓成功"
        lines.append(
            f"- **{series['name']}** `{series['count']}条`：{series['summary']} "
            f"代表视频为 [{representative['title']}]({representative['url']}) `{representative['bvid']}`，{detail_text}。"
        )
        lines.append(f"  系列条目示例：{'；'.join(series['titles'])}")
    lines.append("")

    for bucket in BUCKET_ORDER:
        bucket_items = grouped.get(bucket, [])
        if not bucket_items:
            continue
        lines.append(f"## {bucket}")
        lines.append("")
        for item in bucket_items:
            detail_bits: list[str] = []
            if item.get("page_tags"):
                detail_bits.append(f"page_tags={','.join(item['page_tags'])}")
            if item.get("duration_seconds"):
                detail_bits.append(f"duration={item['duration_seconds']}s")
            if item.get("view_count") is not None:
                detail_bits.append(f"views={item['view_count']}")
            detail_prefix = "; ".join(detail_bits)
            if detail_prefix:
                detail_prefix = f"{detail_prefix}; "
            lines.append(
                f"- `{item['date']}` [{item['title']}]({item['url']}) `{item['bvid']}`: "
                f"tags={','.join(item['tags'])}; {detail_prefix}{item['content_summary']}"
            )
        lines.append("")

    md_text = "\n".join(lines)
    dated_md.write_text(md_text, encoding="utf-8")
    latest_md.write_text(md_text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refresh 组学大讲堂 bioinformatics videos through opencli."
    )
    parser.add_argument("--uid", default=CHANNEL_UID, help="Bilibili UID. Defaults to 组学大讲堂.")
    parser.add_argument("--max-pages", type=int, default=6, help="Maximum pages to scan.")
    parser.add_argument("--limit", type=int, default=50, help="Results per page.")
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent.parent / "references"),
        help="Directory for generated JSON and Markdown outputs.",
    )
    parser.add_argument(
        "--skip-highlights",
        action="store_true",
        help="Do not fetch page-level details for representative videos.",
    )
    args = parser.parse_args()

    items = collect_items(
        uid=args.uid,
        max_pages=args.max_pages,
        limit=args.limit,
        with_highlights=not args.skip_highlights,
    )
    write_outputs(items, Path(args.output_dir))
    print(f"Collected {len(items)} videos into {args.output_dir}")


if __name__ == "__main__":
    main()
