from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


WORKSPACE_ROOT = Path(r"E:\AI\codex")
SOURCE_SKILL_ROOT = WORKSPACE_ROOT / "skills"
LOCAL_SKILL_ROOT = Path(r"C:\Users\simon\.codex\skills")
CHANNEL_UID = "475600552"
CHANNEL_NAME = "大家好我是呼同学"
CHANNEL_URL = f"https://space.bilibili.com/{CHANNEL_UID}"
SKILL_NAME = "opencli-hutongxue-research-bioinfo-cache"


CATEGORY_RULES = [
    (
        "causal-inference-and-mr",
        "Causal Inference And Mendelian Randomization",
        ("孟德尔随机化", "mendelian", "MR分析"),
    ),
    (
        "docking-and-screening",
        "Virtual Screening And Docking",
        ("虚拟药物筛选", "分子对接"),
    ),
    (
        "spatial-and-single-cell-literature",
        "Spatial And Single-Cell Literature Walkthrough",
        ("空间转录组", "单细胞分析"),
    ),
    (
        "cell-communication",
        "Cell Communication",
        ("cell-chat", "cellchat", "通讯分析"),
    ),
    (
        "ml-and-immune-modeling",
        "Machine Learning And Immune Modeling",
        ("机器学习模型", "机器学习", "列线图", "免疫浸润"),
    ),
    (
        "deg-wgcna-and-network",
        "DE WGCNA And Network Analysis",
        ("差异分析", "wgcna", "ppi蛋白网络", "ppi蛋白"),
    ),
    (
        "case-driven-bioinformatics",
        "Case Driven Bioinformatics",
        ("公共数据库完成6分", "生信分析完整思路", "文献解读", "干湿结合"),
    ),
    (
        "plotting-and-color",
        "Plotting And Color",
        ("科研作图配色", "配色网站", "代码配色", "配色教学"),
    ),
    (
        "docker-and-research-environment",
        "Docker And Research Environment",
        ("docker", "rstudio服务器", "镜像仓库", "云服务器", "生信云服务器"),
    ),
    (
        "literature-and-productivity",
        "Literature And Productivity",
        ("文献文档小技巧", "excel表格文献整理", "免费下载知网", "截图固定置顶"),
    ),
    (
        "research-methods-and-projects",
        "Research Methods And Projects",
        ("大创项目申报", "互联网＋", "挑战杯"),
    ),
    (
        "postgrad-prep",
        "Postgraduate Prep",
        ("考研复试", "选导师", "个人陈述", "升级简历", "稳过复试", "直博", "保研", "全面发展"),
    ),
]

EXCLUDE_PATTERNS = [
    "4+4",
    "坠楼",
    "烧炭",
    "伤医",
    "原神",
    "抽奖",
    "荣誉年报",
    "药理学配套口诀",
    "思维导图",
    "医学生资料第",
    "微生物学期末复习",
    "寄生虫学期末复习",
    "西综全套精品思维导图",
    "医生看病现状",
    "就业现状分析",
    "录取通知书",
    "研究员",
    "医学天才",
]


def resolve_opencli() -> str:
    for name in ("opencli.cmd", "opencli", "opencli.ps1"):
        found = shutil.which(name)
        if found:
            return found
    fallback_candidates = [
        r"C:\Users\simon\AppData\Roaming\npm\opencli.cmd",
        r"C:\Users\simon\AppData\Roaming\npm\opencli",
        r"C:\Users\simon\AppData\Roaming\npm\opencli.ps1",
    ]
    for candidate in fallback_candidates:
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Could not resolve opencli on this machine.")


OPENCLI_BIN = resolve_opencli()
OPENCLI_ENV = {"OPENCLI_BROWSER_COMMAND_TIMEOUT": "120"}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def copy_to_local(skill_dir: Path) -> None:
    target = LOCAL_SKILL_ROOT / skill_dir.name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill_dir, target)


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
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr or completed.stdout)
        raise SystemExit(completed.returncode)
    return completed.stdout


def fetch_user_videos(uid: str, max_pages: int, limit: int) -> list[dict]:
    items: list[dict] = []
    for page in range(1, max_pages + 1):
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
        if not rows:
            break
        items.extend(rows)
        if len(rows) < limit:
            break
    return items


def should_exclude(title: str) -> bool:
    lowered = title.lower()
    return any(pattern.lower() in lowered for pattern in EXCLUDE_PATTERNS)


def classify_title(title: str) -> tuple[str, str] | None:
    lowered = title.lower()
    for key, display, keywords in CATEGORY_RULES:
        if any(keyword.lower() in lowered for keyword in keywords):
            return key, display
    return None


def collect_items(uid: str, max_pages: int, limit: int) -> list[dict]:
    kept: list[dict] = []
    for item in fetch_user_videos(uid, max_pages=max_pages, limit=limit):
        title = item.get("title", "").strip()
        if not title or should_exclude(title):
            continue
        matched = classify_title(title)
        if not matched:
            continue
        category_key, category_title = matched
        url = item.get("url", "")
        bvid_match = re.search(r"/video/([^/?]+)", url)
        kept.append(
            {
                "title": title,
                "date": item.get("date", ""),
                "url": url,
                "bvid": bvid_match.group(1) if bvid_match else "",
                "plays": item.get("plays", 0),
                "likes": item.get("likes", 0),
                "category_key": category_key,
                "category_title": category_title,
            }
        )
    return kept


def render_skill_md(snapshot_name: str) -> str:
    categories = "\n".join(
        f"- `{display}`" for _, display, _ in CATEGORY_RULES
    )
    return "\n".join(
        [
            "---",
            f"name: {SKILL_NAME}",
            (
                "description: Internal source cache for `大家好我是呼同学` videos that are relevant to bioinformatics, "
                "research methods, plotting, productivity, Docker environment setup, or adjacent research-learning functions. "
                "This is an evidence cache for rebuilding function-level skills, not the preferred public entrypoint."
            ),
            "---",
            "",
            f"# {SKILL_NAME}",
            "",
            "Use this skill as a source cache when rebuilding or auditing the function-level learning skills that absorb content from 呼同学.",
            "",
            "## Quick Start",
            "",
            f"- Start from [references/{snapshot_name}.md](references/{snapshot_name}.md) for the latest filtered source snapshot.",
            "- Refresh with `python scripts/refresh_index.py` when the user wants the latest eligible videos from this channel.",
            "",
            "## Scope Rules",
            "",
            "- Keep only videos that can be mapped into concrete research, bioinformatics, environment, plotting, or postgraduate-prep functions.",
            "- Exclude channel commentary, social hot-take videos, and medicine-course memorization material from the function-level rebuild pipeline.",
            "- Internal source categories tracked here:",
            categories,
            "",
        ]
    )


def render_openai_yaml() -> str:
    return "\n".join(
        [
            "interface:",
            '  display_name: "OpenCLI 呼同学 Source Cache"',
            '  short_description: "Internal source cache for 呼同学 research and bioinformatics videos."',
            '  default_prompt: "Use $opencli-hutongxue-research-bioinfo-cache only as an evidence cache for rebuilding function-level skills from 呼同学 content."',
            "",
        ]
    )


def render_reference_md(items: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        grouped[item["category_title"]].append(item)
    lines = [
        "# 呼同学 Source Cache",
        "",
        f"- Snapshot date: `{date.today().isoformat()}`",
        f"- Channel: [{CHANNEL_NAME}]({CHANNEL_URL})",
        f"- Included videos: `{len(items)}`",
        "- Scope: only videos that map into concrete function-level skills.",
        "",
    ]
    for category in sorted(grouped):
        lines.append(f"## {category}")
        lines.append("")
        for item in grouped[category]:
            lines.append(
                f"- `{item['date']}` [{item['title']}]({item['url']}) `{item['bvid']}`"
            )
        lines.append("")
    return "\n".join(lines)


def render_refresh_script() -> str:
    return Path(__file__).read_text(encoding="utf-8")


def main() -> None:
    items = collect_items(CHANNEL_UID, max_pages=3, limit=50)
    skill_dir = SOURCE_SKILL_ROOT / SKILL_NAME
    ensure_dir(skill_dir / "agents")
    ensure_dir(skill_dir / "references")
    ensure_dir(skill_dir / "scripts")
    snapshot_name = f"hutongxue-research-bioinfo-cache-{date.today().isoformat()}"
    payload = {
        "snapshot_date": date.today().isoformat(),
        "channel_name": CHANNEL_NAME,
        "uid": CHANNEL_UID,
        "channel_url": CHANNEL_URL,
        "count": len(items),
        "videos": items,
    }
    write_text(skill_dir / "SKILL.md", render_skill_md(f"{snapshot_name}-latest"))
    write_text(skill_dir / "agents" / "openai.yaml", render_openai_yaml())
    write_text(skill_dir / "scripts" / "refresh_index.py", render_refresh_script())
    write_text(skill_dir / "references" / f"{snapshot_name}-latest.md", render_reference_md(items))
    write_text(skill_dir / "references" / f"{snapshot_name}-latest.json", json.dumps(payload, ensure_ascii=False, indent=2))
    write_text(skill_dir / "references" / "hutongxue-research-bioinfo-cache-latest.md", render_reference_md(items))
    write_text(skill_dir / "references" / "hutongxue-research-bioinfo-cache-latest.json", json.dumps(payload, ensure_ascii=False, indent=2))
    copy_to_local(skill_dir)
    print(f"Generated {SKILL_NAME}: {len(items)} videos")


if __name__ == "__main__":
    main()
