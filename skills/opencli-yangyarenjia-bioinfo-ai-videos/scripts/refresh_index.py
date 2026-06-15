    from __future__ import annotations

    import json
    import os
    import re
    import shutil
    import subprocess
    import sys
    from datetime import date
    from pathlib import Path

    CONFIG = {
        "skill_name": "opencli-yangyarenjia-bioinfo-ai-videos",
        "channel_name": "养鸭人家",
        "uid": "631273618",
        "channel_url": "https://space.bilibili.com/631273618",
        "scope_note": "keep videos that directly teach AI tools for data analysis, scientific research, writing, project management, DeepSeek practice, or adjacent open-science workflow; keep any explicit bioinformatics items that appear in future refreshes",
        "boundary_note": "this channel skews broader than strict bioinformatics; keep the AI-for-research core and note explicitly when a kept video is bioinformatics-adjacent rather than a wet-lab or omics tutorial.",
        "include_keywords": ["AI", "DeepSeek", "AIGC", "OpenClaw", "编程", "数据分析", "论文", "科研", "研究", "写作", "办公", "图书馆", "OpenAI", "GPT", "Gemini"],
        "exclude_keywords": [],
        "manual_include_bvids": [],
        "manual_exclude_bvids": [],
        "include_all": False,
        "categories": [
            {"key": "ai-tools-and-practice", "title": "AI Tools And Practical Workflow", "keywords": ["AI", "DeepSeek", "OpenClaw", "编程", "数据分析", "Gemini", "OpenAI", "GPT"], "summary": "Focuses on concrete AI tools, practical workflow, coding, or data-analysis enablement."},
{"key": "research-writing-and-projects", "title": "Research Writing And Project Workflow", "keywords": ["论文", "科研", "研究", "写作", "项目"], "summary": "Explains how AI supports paper writing, research design, project management, or full research workflow."},
{"key": "productivity-and-literacy", "title": "Productivity, Editing, And AI Literacy", "keywords": ["办公", "图书馆", "编辑", "出版", "素养"], "summary": "Covers productivity, publishing, information service, editing, or AI literacy for research-adjacent work."}
        ],
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


    def extract_bvid(url: str) -> str:
        match = re.search(r"/video/([^/?]+)", url)
        return match.group(1) if match else ""


    def compile_pattern(words: list[str]) -> re.Pattern[str] | None:
        if not words:
            return None
        return re.compile("|".join(re.escape(word) for word in words), re.IGNORECASE)


    def classify_title(title: str) -> tuple[str, str, list[str], str]:
        lowered = title.lower()
        for category in CONFIG["categories"]:
            matched = [word for word in category["keywords"] if word.lower() in lowered]
            if matched:
                return category["key"], category["title"], matched, category["summary"]
        if CONFIG["categories"]:
            first = CONFIG["categories"][0]
            return first["key"], first["title"], [], first["summary"]
        return "general", "General Related Videos", [], "Kept because it falls inside the configured scope."


    def select_videos(videos: list[dict]) -> list[dict]:
        include_pattern = compile_pattern(CONFIG["include_keywords"])
        exclude_pattern = compile_pattern(CONFIG["exclude_keywords"])
        selected: list[dict] = []
        manual_include = set(CONFIG["manual_include_bvids"])
        manual_exclude = set(CONFIG["manual_exclude_bvids"])

        for item in videos:
            title = (item.get("title") or "").strip()
            url = item.get("url") or ""
            bvid = extract_bvid(url)
            if not title or not bvid:
                continue
            if bvid in manual_exclude:
                continue
            included = CONFIG["include_all"] or bvid in manual_include
            if include_pattern and include_pattern.search(title):
                included = True
            if exclude_pattern and exclude_pattern.search(title) and bvid not in manual_include:
                included = False
            if not included:
                continue
            category_key, category_title, matched_words, summary = classify_title(title)
            selected.append(
                {
                    "title": title,
                    "date": item.get("date", ""),
                    "url": url,
                    "bvid": bvid,
                    "plays": item.get("plays", ""),
                    "likes": item.get("likes", ""),
                    "category_key": category_key,
                    "category_title": category_title,
                    "matched_words": matched_words,
                    "summary": summary,
                }
            )
        return selected


    def write_outputs(selected: list[dict], output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        snapshot_date = date.today().isoformat()
        stem = "yangyarenjia-bioinfo-ai-videos"
        json_path = output_dir / f"{stem}-videos-{snapshot_date}.json"
        latest_json_path = output_dir / f"{stem}-videos-latest.json"
        md_path = output_dir / f"{stem}-video-map-{snapshot_date}.md"
        latest_md_path = output_dir / f"{stem}-video-map-latest.md"

        payload = {
            "snapshot_date": snapshot_date,
            "channel_name": CONFIG["channel_name"],
            "uid": CONFIG["uid"],
            "channel_url": CONFIG["channel_url"],
            "scope_note": CONFIG["scope_note"],
            "count": len(selected),
            "videos": selected,
        }

        text = [
            f"# OpenCLI 养鸭人家 Bioinfo AI Videos Map",
            "",
            f"- Snapshot date: `{snapshot_date}`",
            "- Source: live collection through `opencli bilibili user-videos`",
            f"- Channel: [{CONFIG['channel_name']}](https://space.bilibili.com/631273618)",
            f"- Scope: {CONFIG['scope_note']}",
        ]
        if CONFIG["boundary_note"]:
            text.append(f"- Boundary note: {CONFIG['boundary_note']}")
        text.extend([f"- Total selected videos: `{len(selected)}`", ""])

        grouped: dict[str, list[dict]] = {}
        titles: dict[str, str] = {}
        for item in selected:
            grouped.setdefault(item["category_key"], []).append(item)
            titles[item["category_key"]] = item["category_title"]

        for category in CONFIG["categories"]:
            items = grouped.get(category["key"], [])
            if not items:
                continue
            text.append(f"## {category['title']}")
            text.append("")
            for item in items:
                match_text = ", ".join(item["matched_words"]) if item["matched_words"] else "channel-scope"
                text.append(
                    f"- `{item['date']}` [{item['title']}]({item['url']}) `{item['bvid']}`: "
                    f"matches `{match_text}`; {item['summary']}"
                )
            text.append("")

        latest_json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        latest_md_path.write_text("\n".join(text).rstrip() + "\n", encoding="utf-8")
        md_path.write_text("\n".join(text).rstrip() + "\n", encoding="utf-8")


    def main() -> None:
        output_dir = Path(__file__).resolve().parent.parent / "references"
        selected = select_videos(fetch_user_videos(CONFIG["uid"], max_pages=8, limit=50))
        write_outputs(selected, output_dir)
        print(f"Refreshed {CONFIG['skill_name']} with {len(selected)} scoped videos.")


    if __name__ == "__main__":
        main()
