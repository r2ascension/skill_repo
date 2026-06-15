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


CHANNEL_UID = "1948639457"
CHANNEL_NAME = "OnekeyAI"
CHANNEL_URL = f"https://space.bilibili.com/{CHANNEL_UID}"

CORE_KEYWORDS = {
    "omics": [r"多组学", r"传统组学", r"组学", r"文本模态"],
    "survival": [r"生存", r"cox", r"cox loss"],
    "modeling": [r"结构化数据", r"多分类", r"交叉验证", r"combat", r"批次", r"聚类"],
}

EXTENDED_KEYWORDS = {
    "foundation": [r"onekeycomp", r"onekey-comp", r"feature_cluster"],
    "support": [r"病理组学", r"差异化", r"平替"],
}

EXCLUDE_PATTERNS = [
    r"答疑汇总",
    r"电脑配置",
    r"自动勾画",
    r"超分重建",
    r"公开课",
    r"私房课",
    r"科研路径",
]

MANUAL_EXTENDED_BVIDS = {
    "BV1Bg4y1V7AZ",
    "BV1Md4y1g7nX",
    "BV163411W7iD",
    "BV1wb421z7py",
    "BV1mN4y1D7sK",
    "BV1Tf421q7u2",
    "BV1T44y1a7jp",
    "BV1Vi421U7s2",
}


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


def run_opencli(*args: str) -> str:
    command = [OPENCLI_BIN, *args]
    for attempt in range(2):
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env={**os.environ, **OPENCLI_ENV},
        )
        if completed.returncode == 0:
            return completed.stdout
        message = (completed.stderr or completed.stdout or "").lower()
        if "stale page identity" in message and attempt == 0:
            continue
        sys.stderr.write(completed.stderr or completed.stdout)
        raise SystemExit(completed.returncode)
    raise SystemExit(1)


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
    return json.loads(raw)


def fetch_video_meta(bvid: str) -> dict[str, str]:
    try:
        raw = run_opencli(
            "bilibili",
            "video",
            bvid,
            "--window",
            "background",
            "--site-session",
            "ephemeral",
            "-f",
            "json",
        )
    except SystemExit:
        return {}
    rows = json.loads(raw)
    meta: dict[str, str] = {}
    for row in rows:
        field = row.get("field")
        if field:
            meta[field] = row.get("value", "")
    return meta


def extract_bvid(url: str) -> str:
    match = re.search(r"/video/([^/?]+)", url)
    return match.group(1) if match else ""


def matched_labels(title: str, patterns: dict[str, list[str]]) -> list[str]:
    hits: list[str] = []
    for label, label_patterns in patterns.items():
        for pattern in label_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                hits.append(label)
                break
    return hits


def should_exclude(title: str) -> bool:
    return any(re.search(pattern, title, re.IGNORECASE) for pattern in EXCLUDE_PATTERNS)


def classify_candidate(title: str, bvid: str) -> tuple[str | None, list[str]]:
    core_hits = matched_labels(title, CORE_KEYWORDS)
    if core_hits:
        return "core", sorted(set(core_hits))
    if bvid in MANUAL_EXTENDED_BVIDS:
        return "extended", ["manual"]
    if should_exclude(title):
        return None, []
    extended_hits = matched_labels(title, EXTENDED_KEYWORDS)
    if extended_hits:
        return "extended", sorted(set(extended_hits))
    return None, []


def summarize_text(text: str, limit: int = 180) -> str:
    compact = " ".join(text.split())
    if not compact:
        return "No description returned; inspect with opencli bilibili subtitle if needed."
    return compact[: limit - 3] + "..." if len(compact) > limit else compact


def collect_candidates(
    uid: str,
    max_pages: int,
    limit: int,
    include_extended: bool,
    fetch_details: bool,
) -> list[dict]:
    candidates: list[dict] = []
    for page in range(1, max_pages + 1):
        videos = fetch_user_videos(uid, page, limit)
        if not videos:
            break
        for item in videos:
            title = item.get("title", "")
            url = item.get("url", "")
            bvid = extract_bvid(url)
            category, hits = classify_candidate(title, bvid)
            if category is None:
                continue
            if category == "extended" and not include_extended:
                continue
            meta = fetch_video_meta(bvid) if fetch_details and bvid else {}
            candidates.append(
                {
                    "category": category,
                    "matched_rules": hits,
                    "title": title,
                    "date": item.get("date", ""),
                    "url": url,
                    "bvid": bvid,
                    "plays": item.get("plays", ""),
                    "duration": meta.get("duration", ""),
                    "publish_time": meta.get("publish_time", ""),
                    "description": meta.get("description", ""),
                }
            )
    return candidates


def write_outputs(candidates: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    snapshot_name = f"onekeyai_bioinfo_candidates_{date.today().isoformat()}"
    json_path = output_dir / f"{snapshot_name}.json"
    md_path = output_dir / f"{snapshot_name}.md"

    json_path.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in candidates:
        grouped[item["category"]].append(item)

    lines = [
        "# OnekeyAI Bioinfo Candidate Videos",
        "",
        f"- Snapshot date: `{date.today().isoformat()}`",
        f"- Channel: [{CHANNEL_NAME}]({CHANNEL_URL})",
        "- Generated by `scripts/refresh_index.py` through `opencli bilibili`.",
        "- This is a candidate list, not the final human-curated map.",
        "",
    ]
    for category in ("core", "extended"):
        if not grouped.get(category):
            continue
        lines.append(f"## {category.title()}")
        lines.append("")
        for item in grouped[category]:
            summary = summarize_text(item.get("description", ""))
            lines.append(
                f"- `{item['date']}` [{item['title']}]({item['url']}) `{item['bvid']}`: "
                f"rules={','.join(item['matched_rules']) or 'none'}; {summary}"
            )
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refresh candidate OnekeyAI bioinfo videos through opencli."
    )
    parser.add_argument("--uid", default=CHANNEL_UID, help="Bilibili UID. Defaults to OnekeyAI.")
    parser.add_argument("--max-pages", type=int, default=8, help="Maximum pages to scan.")
    parser.add_argument("--limit", type=int, default=50, help="Results per page.")
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent.parent / "references"),
        help="Directory for generated JSON and Markdown outputs.",
    )
    parser.add_argument("--core-only", action="store_true", help="Skip extended candidates.")
    parser.add_argument("--skip-details", action="store_true", help="Do not fetch per-video metadata.")
    args = parser.parse_args()

    candidates = collect_candidates(
        uid=args.uid,
        max_pages=args.max_pages,
        limit=args.limit,
        include_extended=not args.core_only,
        fetch_details=not args.skip_details,
    )
    write_outputs(candidates, Path(args.output_dir))
    print(f"Collected {len(candidates)} candidate videos into {args.output_dir}")


if __name__ == "__main__":
    main()
