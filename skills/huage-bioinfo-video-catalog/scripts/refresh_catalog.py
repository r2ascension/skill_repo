from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_UID = "405009023"
DEFAULT_UP_NAME = "华哥生信AI"
DEFAULT_SPACE_NAME = "华哥生信官方"
DEFAULT_OUTPUT_ROOT = Path(r"E:\codex\huage_bioinfo_video_catalog")

EXCLUDED_TITLES = {
    "人工智能体一： OpenClaw 龙虾介绍， AI Agent 实战": "AI agent demo rather than a bioinformatics technique lesson",
    "生信千人培训计划": "program announcement rather than a concrete technique lesson",
    "Nature复现：课程亮点": "course promotion rather than a concrete technique lesson",
    "华哥生信来b站啦": "account introduction rather than a concrete technique lesson",
}

CATEGORY_ORDER = [
    "入门与环境",
    "Bulk RNA-seq / 芯片 / 公共数据库",
    "单细胞基础",
    "单细胞进阶",
    "空间与多组学",
    "Nature复现与科研复盘",
    "专题案例与扩展课",
]

OPENCLI_FALLBACKS = [
    r"C:\Users\simon\AppData\Roaming\npm\opencli.cmd",
    r"C:\Users\simon\AppData\Roaming\npm\opencli",
]


def resolve_opencli() -> str:
    for candidate in ("opencli", "opencli.cmd"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    for candidate in OPENCLI_FALLBACKS:
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Could not locate opencli. Add it to PATH or update OPENCLI_FALLBACKS.")


def run_opencli(profile: str | None, args: list[str]) -> Any:
    cmd = [resolve_opencli()]
    if profile:
        cmd.extend(["--profile", profile])
    cmd.extend(args)
    cmd.extend(["-f", "json"])
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=os.environ.copy(),
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or f"opencli failed: {' '.join(cmd)}"
        raise RuntimeError(message)
    return json.loads(result.stdout)


def fetch_all_videos(profile: str | None, uid: str) -> list[dict[str, Any]]:
    videos: list[dict[str, Any]] = []
    page = 1
    while True:
        batch = run_opencli(
            profile,
            [
                "bilibili",
                "user-videos",
                uid,
                "--limit",
                "50",
                "--page",
                str(page),
                "--order",
                "pubdate",
                "--window",
                "background",
                "--site-session",
                "ephemeral",
            ],
        )
        if not batch:
            break
        videos.extend(batch)
        page += 1
    return videos


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_numeric_prefix(title: str) -> str:
    return re.sub(r"^\s*\d+\s*[\.、]?\s*", "", title).strip()


def classify_video(title: str) -> str:
    clean = strip_numeric_prefix(title)

    if title.startswith("Nature复现："):
        return "Nature复现与科研复盘"
    if any(token in clean for token in ["黑色素瘤", "孟德尔"]):
        return "专题案例与扩展课"
    if any(token in clean for token in ["空间转录组", "空间定位", "共定位", "ATAC-seq", "Signac", "多组学"]):
        return "空间与多组学"
    if any(
        token in clean
        for token in [
            "SCENIC",
            "CellPhoneDB",
            "CellChat",
            "Monocle",
            "PHATE",
            "velocyto",
            "scVelo",
            "InferCNV",
            "CytoTRACE",
            "GSVA",
            "RNA velocity",
            "CNV",
            "细胞互作",
            "拟时间",
            "通路活性",
        ]
    ):
        return "单细胞进阶"
    if any(
        token in clean
        for token in [
            "单细胞",
            "Seurat",
            "Marker",
            "DoubletFinder",
            "Cell Ranger",
            "Scanpy",
            "PBMC",
            "marker基因",
            "PCA降",
            "降维聚类",
            "注释",
            "可视化",
        ]
    ):
        return "单细胞基础"
    if any(
        token in clean
        for token in [
            "ChIP-seq",
            "RNA-seq",
            "TCGA",
            "芯片",
            "生存曲线",
            "富集",
            "GO",
            "KEGG",
            "DO",
            "通路集",
            "差异分析",
            "上游分析",
            "蛋白互作",
        ]
    ):
        return "Bulk RNA-seq / 芯片 / 公共数据库"
    if any(
        token in clean
        for token in [
            "R语言",
            "RStudio",
            "Jupyter",
            "Linux",
            "Miniconda",
            "WSL2",
            "环境",
            "软件安装",
            "Spyder",
        ]
    ):
        return "入门与环境"
    return "专题案例与扩展课"


def infer_series(title: str) -> str:
    if title.startswith("Nature复现："):
        return "2026-03 Nature复现短课"
    if re.match(r"^\d+\s", title):
        return "2026-05 系统生信/单细胞课"
    if re.match(r"^\d+\.", title):
        return "2026-04 精简生信基础课"
    return "专题扩展课"


def build_focus(title: str, category: str) -> str:
    clean = strip_numeric_prefix(title)
    if title.startswith("Nature复现："):
        return f"围绕顶刊复现，重点是{clean.removeprefix('Nature复现：').strip()}。"
    if "全流程" in clean:
        return f"偏整套流程串讲，覆盖{clean}。"
    if "案例" in clean:
        return f"偏案例驱动，重点是{clean}。"
    if category == "入门与环境":
        return f"偏环境与工具准备，主要讲{clean}。"
    if category == "专题案例与扩展课":
        return f"偏专题扩展，重点是{clean}。"
    return f"重点讲{clean}。"


def extract_bvid(url: str) -> str:
    match = re.search(r"/video/(BV[0-9A-Za-z]+)", url)
    if not match:
        raise ValueError(f"Could not extract BV id from {url}")
    return match.group(1)


def build_learning_route(grouped: OrderedDict[str, list[dict[str, Any]]]) -> list[str]:
    route = []
    if grouped.get("入门与环境"):
        route.append("先看 `入门与环境`，补齐 R / RStudio / Jupyter / Linux / Conda 基础。")
    if grouped.get("Bulk RNA-seq / 芯片 / 公共数据库"):
        route.append("再看 `Bulk RNA-seq / 芯片 / 公共数据库`，建立差异分析、富集分析、TCGA/GEO 思路。")
    if grouped.get("单细胞基础"):
        route.append("之后进入 `单细胞基础`，按读入 -> 质控 -> 整合 -> 聚类 -> 注释 -> 可视化 顺序学习。")
    if grouped.get("单细胞进阶"):
        route.append("掌握基础后看 `单细胞进阶`，补轨迹、细胞通讯、调控网络、CNV、RNA velocity。")
    if grouped.get("空间与多组学"):
        route.append("再进入 `空间与多组学`，理解空转、ATAC、联合分析和空间映射。")
    if grouped.get("Nature复现与科研复盘") or grouped.get("专题案例与扩展课"):
        route.append("最后看 `Nature复现与科研复盘` 和 `专题案例与扩展课`，把方法串到真实论文与案例里。")
    return route


def render_markdown(snapshot: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# {snapshot['up_name']} 生信技术视频清单")
    lines.append("")
    lines.append(f"- 更新时间: `{snapshot['snapshot_time']}`")
    lines.append(f"- 来源: Bilibili `{snapshot['space_name']}` (uid `{snapshot['uid']}`)，使用 `opencli bilibili user-videos` 实时抓取")
    lines.append(f"- 总投稿数: `{snapshot['total_videos']}`")
    lines.append(f"- 纳入生信技术范围: `{snapshot['included_count']}`")
    lines.append(f"- 排除的非技术/宣传视频: `{snapshot['excluded_count']}`")
    lines.append("")
    lines.append("## 简要概览")
    lines.append("")
    for category, items in snapshot["grouped_videos"].items():
        lines.append(f"- `{category}`: `{len(items)}` 条")
    lines.append("")
    lines.append("## 推荐学习顺序")
    lines.append("")
    for step in snapshot["learning_route"]:
        lines.append(f"- {step}")
    lines.append("")
    lines.append("## 排除项")
    lines.append("")
    for item in snapshot["excluded_videos"]:
        lines.append(f"- `{item['title']}`: {item['reason']}")
    lines.append("")
    lines.append("## 分组清单")
    lines.append("")
    for category, items in snapshot["grouped_videos"].items():
        lines.append(f"### {category}")
        lines.append("")
        for item in items:
            lines.append(
                f"- `{item['date']}` | [{item['title']}]({item['url']}) | 播放 `{item['plays']}` | {item['focus']}"
            )
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_snapshot(videos: list[dict[str, Any]], uid: str) -> dict[str, Any]:
    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for raw in videos:
        title = normalize_whitespace(str(raw["title"]))
        record = {
            "title": title,
            "date": raw["date"],
            "plays": raw["plays"],
            "likes": raw["likes"],
            "url": raw["url"],
            "bvid": extract_bvid(raw["url"]),
        }
        if title in EXCLUDED_TITLES:
            record["reason"] = EXCLUDED_TITLES[title]
            excluded.append(record)
            continue

        category = classify_video(title)
        record["category"] = category
        record["series"] = infer_series(title)
        record["focus"] = build_focus(title, category)
        included.append(record)

    grouped: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for category in CATEGORY_ORDER:
        grouped[category] = [item for item in included if item["category"] == category]
    grouped = OrderedDict((key, value) for key, value in grouped.items() if value)

    snapshot = {
        "snapshot_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "up_name": DEFAULT_UP_NAME,
        "space_name": DEFAULT_SPACE_NAME,
        "uid": uid,
        "total_videos": len(videos),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "included_videos": included,
        "excluded_videos": excluded,
        "grouped_videos": grouped,
        "learning_route": build_learning_route(grouped),
    }
    return snapshot


def write_outputs(snapshot: dict[str, Any], skill_root: Path, output_root: Path) -> tuple[Path, Path]:
    references_dir = skill_root / "references"
    references_dir.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)

    dated_stem = f"huage_bioinfo_video_catalog_{datetime.now().strftime('%Y%m%d')}"

    current_json_path = references_dir / "current_catalog.json"
    current_md_path = references_dir / "current_catalog.md"
    dated_json_path = output_root / f"{dated_stem}.json"
    dated_md_path = output_root / f"{dated_stem}.md"

    current_json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    current_md_path.write_text(render_markdown(snapshot), encoding="utf-8")
    dated_json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    dated_md_path.write_text(render_markdown(snapshot), encoding="utf-8")

    return dated_md_path, current_md_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh Huage bioinformatics video catalog via opencli.")
    parser.add_argument("--profile", help="opencli Browser Bridge profile name")
    parser.add_argument("--uid", default=DEFAULT_UID, help="Bilibili uid to scan")
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Directory for dated markdown/json exports",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    output_root = Path(args.output_root)

    videos = fetch_all_videos(args.profile, args.uid)
    snapshot = build_snapshot(videos, args.uid)
    dated_md_path, current_md_path = write_outputs(snapshot, skill_root, output_root)

    print(f"Fetched {snapshot['total_videos']} total videos.")
    print(f"Included {snapshot['included_count']} bioinformatics-tech videos.")
    print(f"Excluded {snapshot['excluded_count']} non-technical/promotional videos.")
    print(f"Wrote snapshot: {current_md_path}")
    print(f"Wrote dated export: {dated_md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
