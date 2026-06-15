#!/usr/bin/env python
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


USER_QUERY = "网络硕导"
USER_UID = "189717004"
USER_URL = "https://space.bilibili.com/189717004"
DEFAULT_OUTPUT_DIR = Path(r"E:\codex\network-shuodao-writing-videos")
WRITING_REGEX = re.compile(
    r"(论文|写作|学位论文|开题|文献|引言|绪论|综述|评述|选题|实证|案例|理论基础|概念界定|"
    r"结论|建议|讨论|参考文献|引用|查重|AIGC|公式|目录|页眉|页码|图表|答辩PPT|"
    r"调查问卷|访谈提纲|沉浸式翻译|文献阅读工具)",
)

TOPIC_RULES = [
    (r"课程回顾与总结", "课程回顾与总结"),
    (r"导学课", "导学课"),
    (r"第一课.*(阅读学习文献|检索阅读英文文献)", "第一课：文献检索与阅读"),
    (r"第二课.*选题", "第二课：选题"),
    (r"第三课.*开题", "第三课：开题写作"),
    (r"第四课.*(文献综述|文献评述)", "第四课：文献综述/文献评述"),
    (r"第五课.*论文框架", "第五课：论文框架"),
    (r"第六课.*(绪论|引言)", "第六课：绪论/引言"),
    (r"第七课.*(概念界定|理论基础)", "第七课：概念界定与理论基础"),
    (r"第八课.*实证类核心章节", "第八课：实证类核心章节"),
    (r"第九课.*案例", "第九课：案例类核心章节"),
    (r"第十课.*结论与建议", "第十课：研究结论与建议"),
    (r"第十一课.*讨论", "第十一课：研究讨论"),
    (r"教育学论文的写法", "教育学论文写法"),
    (r"公共管理案例类的写法", "公共管理案例写法"),
    (r"经济学案例论文的写法", "经济学案例写法"),
    (r"访谈提纲", "访谈提纲设计"),
    (r"调查问卷", "调查问卷设计"),
    (r"降低论文AIGC|降低AI率", "降低 AIGC/AI 率"),
    (r"降低论文查重", "降低查重"),
    (r"论文图表格式", "论文图表格式"),
    (r"页眉", "页眉设置"),
    (r"页码设置|分页符|分节符", "页码与分节设置"),
    (r"行距|缩进|对齐方式", "正文格式：行距缩进对齐"),
    (r"自动生成论文目录", "自动生成目录"),
    (r"交叉引用标注参考文献", "交叉引用标注参考文献"),
    (r"特殊参考文献", "特殊参考文献引用"),
    (r"如何引用参考文献|什么是引用", "参考文献引用基础"),
    (r"下载中英文文献", "中英文文献下载"),
    (r"沉浸式翻译", "沉浸式翻译工具"),
    (r"文献阅读工具分享及使用", "文献阅读工具"),
    (r"手动录入论文公式|论文公式插入", "论文公式录入"),
    (r"毕业答辩PPT|开题答辩PPT", "答辩 PPT 制作"),
    (r"论文反诈|期刊代发", "论文反诈"),
]

GREETING_PREFIXES = (
    "ok",
    "hello",
    "各位同学大家好",
    "我是大家的网络硕导",
    "欢迎大家",
)


def resolve_opencli() -> str:
    candidates = [
        shutil.which("opencli"),
        shutil.which("opencli.cmd"),
        r"C:\Users\simon\AppData\Roaming\npm\opencli.cmd",
        r"C:\Users\simon\AppData\Roaming\npm\opencli.ps1",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise FileNotFoundError("opencli executable not found")


def run_opencli(*args: str) -> Any:
    cmd = [resolve_opencli(), *args, "-f", "json"]
    last_error = ""
    for attempt in range(1, 4):
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode == 0:
            try:
                return json.loads(completed.stdout)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"Failed to parse JSON from {' '.join(cmd)}\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
                ) from exc
        last_error = completed.stderr.strip() or completed.stdout.strip()
        if "Pre-navigation" in last_error or "This operation was aborted" in last_error:
            time.sleep(3 * attempt)
            continue
        break
    raise RuntimeError(f"Command failed after retries: {' '.join(cmd)}\n{last_error}")


def is_writing_video(title: str) -> bool:
    return bool(WRITING_REGEX.search(title))


def classify_category(title: str) -> str:
    if re.search(r"(答辩PPT|沉浸式翻译|文献阅读工具|下载中英文文献)", title):
        return "工具与答辩"
    if re.search(r"(论文反诈|期刊代发)", title):
        return "论文反诈与避坑"
    if re.search(r"(教育学论文|公共管理案例|经济学案例)", title):
        return "案例写法拓展"
    if re.search(r"(小白扫盲|论文小白|AIGC|查重|页眉|页码|图表|参考文献|引用|公式|目录|格式|问卷|访谈提纲)", title):
        return "小白扫盲与格式规范"
    if re.search(r"(学位论文写作|论文写作辅导|论文辅导)", title):
        return "主线课程"
    return "其他写作相关"


def canonical_topic(title: str) -> str:
    normalized = re.sub(r"\s+", "", title)
    for pattern, topic in TOPIC_RULES:
        if re.search(pattern, normalized):
            return topic
    return re.sub(r"[：:——\-（）()]+", " ", title).strip()


def pick_primary(videos: list[dict[str, Any]]) -> dict[str, Any]:
    def score(video: dict[str, Any]) -> tuple[int, str]:
        title = video["title"]
        return (
            2 if "干货版" in title else 1 if "课程回顾" in title else 0,
            video["date"],
        )

    return sorted(videos, key=score, reverse=True)[0]


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def subtitle_brief(items: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for item in items:
        text = clean_text(str(item.get("content", "")))
        if not text:
            continue
        lower = text.lower()
        if any(lower.startswith(prefix) for prefix in GREETING_PREFIXES):
            continue
        if len(text) == 1:
            continue
        chunks.append(text)
        if len(chunks) >= 8:
            break
    return "；".join(chunks)[:260]


def summary_brief(items: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for item in items:
        text = clean_text(str(item.get("content", "")))
        if not text or text.startswith("#"):
            continue
        chunks.append(text)
        if len(chunks) >= 4:
            break
    return "；".join(chunks)[:260]


def fetch_detail(bvid: str) -> tuple[str, str]:
    try:
        items = run_opencli("bilibili", "summary", bvid)
        if isinstance(items, list) and items:
            brief = summary_brief(items)
            if brief:
                return "summary", brief
    except Exception:
        pass

    return "title", ""


def fetch_all_videos(max_pages: int) -> list[dict[str, Any]]:
    videos: list[dict[str, Any]] = []
    for page in range(1, max_pages + 1):
        data = run_opencli("bilibili", "user-videos", USER_UID, "--page", str(page), "--limit", "50")
        if not data:
            break
        for item in data:
            url = str(item["url"])
            bvid_match = re.search(r"/video/(BV[\w]+)", url)
            item["bvid"] = bvid_match.group(1) if bvid_match else ""
            videos.append(item)
    return videos


def detail_priority(category: str, topic: str) -> tuple[int, int]:
    category_rank = {
        "主线课程": 0,
        "案例写法拓展": 1,
        "小白扫盲与格式规范": 2,
        "工具与答辩": 3,
        "论文反诈与避坑": 4,
        "其他写作相关": 5,
    }
    topic_rank = 0 if topic.startswith("第") or "课程回顾" in topic or "导学课" in topic else 1
    return category_rank.get(category, 99), topic_rank


def build_catalog(videos: list[dict[str, Any]], max_detailed_topics: int) -> dict[str, Any]:
    writing_videos = [video for video in videos if is_writing_video(str(video["title"]))]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for video in writing_videos:
        grouped[canonical_topic(str(video["title"]))].append(video)

    topics: list[dict[str, Any]] = []
    for topic, variants in grouped.items():
        ordered_variants = sorted(variants, key=lambda item: item["date"], reverse=True)
        primary = pick_primary(ordered_variants)
        topics.append(
            {
                "topic": topic,
                "category": classify_category(str(primary["title"])),
                "primary_video": primary,
                "variants": ordered_variants,
                "detail_source": "title",
                "detail_summary": f"围绕《{primary['title']}》展开，建议按标题主题继续细看完整视频。",
            }
        )

    prioritized = sorted(
        topics,
        key=lambda item: detail_priority(item["category"], item["topic"]),
    )
    for item in prioritized[:max_detailed_topics]:
        detail_source, detail = fetch_detail(str(item["primary_video"]["bvid"]))
        if detail:
            item["detail_source"] = detail_source
            item["detail_summary"] = detail

    topics.sort(
        key=lambda item: (
            ["主线课程", "案例写法拓展", "小白扫盲与格式规范", "工具与答辩", "论文反诈与避坑", "其他写作相关"].index(item["category"])
            if item["category"] in ["主线课程", "案例写法拓展", "小白扫盲与格式规范", "工具与答辩", "论文反诈与避坑", "其他写作相关"]
            else 99,
            item["primary_video"]["date"],
        ),
        reverse=False,
    )

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "user": {
            "query": USER_QUERY,
            "uid": USER_UID,
            "url": USER_URL,
        },
        "stats": {
            "all_videos": len(videos),
            "writing_related_videos": len(writing_videos),
            "writing_topics": len(topics),
        },
        "topics": topics,
    }


def write_markdown(catalog: dict[str, Any], path: Path) -> None:
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for topic in catalog["topics"]:
        by_category[topic["category"]].append(topic)

    lines = [
        "# 网络硕导写作视频清单",
        "",
        f"- 生成时间：{catalog['generated_at']}",
        f"- UP 主：{catalog['user']['query']}",
        f"- UID：{catalog['user']['uid']}",
        f"- 空间：{catalog['user']['url']}",
        f"- 全部投稿：{catalog['stats']['all_videos']}",
        f"- 写作相关视频：{catalog['stats']['writing_related_videos']}",
        f"- 合并后的主题数：{catalog['stats']['writing_topics']}",
        "",
        "## 使用说明",
        "",
        "- 同一主题下若有“干货版”“碎碎念版”“重制版”等，已合并到一个主题条目里。",
        "- 详细内容优先来自 B 站 AI 总结；若该视频没有 AI 总结，则回退到字幕开场内容进行归纳。",
        "",
    ]

    category_order = [
        "主线课程",
        "案例写法拓展",
        "小白扫盲与格式规范",
        "工具与答辩",
        "论文反诈与避坑",
        "其他写作相关",
    ]
    for category in category_order:
        items = by_category.get(category)
        if not items:
            continue
        lines.append(f"## {category}")
        lines.append("")
        for item in items:
            primary = item["primary_video"]
            lines.append(f"### {item['topic']}")
            lines.append("")
            lines.append(
                f"- 主视频：{primary['date']} | {primary['title']} | {primary['bvid']} | {primary['url']}"
            )
            if len(item["variants"]) > 1:
                variant_text = "；".join(
                    f"{video['date']}《{video['title']}》"
                    for video in item["variants"]
                )
                lines.append(f"- 同主题版本：{variant_text}")
            lines.append(f"- 内容摘要：{item['detail_summary']}")
            lines.append(f"- 摘要来源：{item['detail_source']}")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def copy_if_requested(source: Path, destination_dir: Path | None) -> None:
    if not destination_dir:
        return
    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination_dir / source.name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Use opencli to collect and summarize writing-related videos from 网络硕导."
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for the generated markdown and json outputs.",
    )
    parser.add_argument(
        "--reference-dir",
        help="Optional skill references directory that should receive a copy of the generated outputs.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=10,
        help="Maximum user-videos pages to scan.",
    )
    parser.add_argument(
        "--max-detailed-topics",
        type=int,
        default=16,
        help="How many grouped topics should fetch opencli summaries.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    reference_dir = Path(args.reference_dir) if args.reference_dir else None
    output_dir.mkdir(parents=True, exist_ok=True)

    videos = fetch_all_videos(args.max_pages)
    catalog = build_catalog(videos, args.max_detailed_topics)

    json_path = output_dir / "network_shuodao_writing_catalog.json"
    md_path = output_dir / "network_shuodao_writing_catalog.md"
    json_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(catalog, md_path)
    copy_if_requested(json_path, reference_dir)
    copy_if_requested(md_path, reference_dir)

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(
        json.dumps(
            {
                "all_videos": catalog["stats"]["all_videos"],
                "writing_related_videos": catalog["stats"]["writing_related_videos"],
                "writing_topics": catalog["stats"]["writing_topics"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
