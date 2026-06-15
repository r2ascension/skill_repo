    from __future__ import annotations

    import json
    import ssl
    import subprocess
    import time
    import urllib.parse
    import urllib.request
    from datetime import datetime
    from pathlib import Path

    CONFIG = {
        "url": "https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=MzAxMDkxODM1Ng==&scene=1&album_id=1698018533277761536&count=3&from=singlemessage#wechat_redirect",
        "skill_name": "opencli-weixin-album-single-cell-advanced",
        "focus": "advanced single-cell practice, multiplexing, sample hashing, comparative group design, integration, and deeper single-cell analysis tactics",
        "scope_note": "keep the full album because 单细胞进阶 is already a curated advanced single-cell collection from 生信技能树",
        "boundary_note": "",
        "categories": [
            {"key": "experimental-design", "title": "Experimental Design And Multiplexing", "keywords": ["Cell Hashing", "混样品", "样品"], "summary": "Focuses on single-cell experimental design, multiplexing, and sample-handling tactics."},
{"key": "comparison-and-visualization", "title": "Comparison And Visualization", "keywords": ["比例差异", "火山图", "比较"], "summary": "Covers comparative analysis and visualization tactics across groups or cell subtypes."},
{"key": "advanced-workflow", "title": "Advanced Workflow Notes", "keywords": ["单细胞", "进阶", "教程"], "summary": "Captures advanced single-cell workflows and deeper analysis notes not covered by a narrower bucket."}
        ],
    }

    SSL_CONTEXT = ssl.create_default_context()
    HTTP_HEADERS = {"User-Agent": "Mozilla/5.0"}


    def run_powershell(command: str) -> str:
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr or completed.stdout)
        return completed.stdout.strip()


    def fetch_json_with_retry(url: str) -> dict:
        last_error = None
        for delay in (0, 1, 2, 4):
            if delay:
                time.sleep(delay)
            try:
                req = urllib.request.Request(url, headers=HTTP_HEADERS)
                with urllib.request.urlopen(req, timeout=30, context=SSL_CONTEXT) as response:
                    return json.loads(response.read().decode("utf-8", errors="replace"))
            except Exception as exc:  # noqa: BLE001
                last_error = exc
        raise last_error


    def parse_album_query(url: str) -> tuple[str, str]:
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        return query["__biz"][0], query["album_id"][0]


    def fetch_album_metadata(url: str, session: str) -> dict:
        run_powershell(f"opencli browser {session} open '{url}' | Out-Null")
        payload = run_powershell(
            f"opencli browser {session} eval 'JSON.stringify({title: document.title, text: document.body.innerText.slice(0,260)})'"
        )
        meta = json.loads(payload)
        lines = [line.strip() for line in meta["text"].splitlines() if line.strip()]
        account = lines[1] if len(lines) > 1 else ""
        count_line = next((line for line in lines if "篇内容" in line), "")
        intro_lines = [line for line in lines[2:6] if "篇内容" not in line and "Reads" not in line and "阅读" not in line]
        return {
            "title": meta["title"],
            "account": account,
            "count_line": count_line,
            "intro": " ".join(intro_lines[:2]).strip(),
        }


    def normalize_article_date(item: dict) -> str:
        create_time = item.get("create_time")
        if create_time:
            try:
                return datetime.fromtimestamp(int(create_time)).strftime("%Y-%m-%d")
            except Exception:  # noqa: BLE001
                return ""
        return ""


    def fetch_album_articles(url: str) -> dict:
        biz, album_id = parse_album_query(url)
        all_entries = []
        begin_msgid = None
        begin_itemidx = None

        for _ in range(200):
            params = {
                "action": "getalbum",
                "__biz": biz,
                "album_id": album_id,
                "count": "10",
                "f": "json",
            }
            if begin_msgid:
                params["begin_msgid"] = begin_msgid
                params["begin_itemidx"] = begin_itemidx or "1"
            api_url = "https://mp.weixin.qq.com/mp/appmsgalbum?" + urllib.parse.urlencode(params)
            payload = fetch_json_with_retry(api_url)
            batch = payload.get("getalbum_resp", {}).get("article_list", [])
            if not isinstance(batch, list) or not batch:
                break
            if (
                begin_msgid is not None
                and all_entries
                and batch[0].get("msgid") == all_entries[-1].get("msgid")
                and batch[0].get("itemidx") == all_entries[-1].get("itemidx")
            ):
                batch = batch[1:]
            if not batch:
                break
            for item in batch:
                all_entries.append({
                    "title": item.get("title", ""),
                    "url": (item.get("url", "") or "").replace("http://", "https://"),
                    "msgid": item.get("msgid", ""),
                    "itemidx": item.get("itemidx", ""),
                    "pos_num": item.get("pos_num", ""),
                    "date": normalize_article_date(item),
                })
            if payload.get("getalbum_resp", {}).get("continue_flag") != "1":
                break
            begin_msgid = batch[-1].get("msgid")
            begin_itemidx = batch[-1].get("itemidx", "1")

        deduped = []
        seen = set()
        for item in all_entries:
            key = (item["msgid"], item["itemidx"])
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
        return {"biz": biz, "album_id": album_id, "articles": deduped}


    def classify_article(title: str) -> tuple[str, str]:
        lowered = title.lower()
        for category in CONFIG["categories"]:
            if any(keyword.lower() in lowered for keyword in category["keywords"]):
                return category["key"], category["title"]
        first = CONFIG["categories"][0]
        return first["key"], first["title"]


    def summarize_title(title: str, category_title: str) -> str:
        if "教程" in title or "实战" in title:
            return f"Practical {category_title.lower()} article with a hands-on or tutorial emphasis."
        if "原理" in title or "解析" in title:
            return f"Explains the core idea or mechanism behind a {category_title.lower()} topic."
        return f"Relevant {category_title.lower()} entry kept from the curated album."


    def main() -> None:
        meta = fetch_album_metadata(CONFIG["url"], CONFIG["skill_name"].replace("opencli-", ""))
        fetched = fetch_album_articles(CONFIG["url"])
        articles = []
        for item in fetched["articles"]:
            category_key, category_title = classify_article(item["title"])
            item["category_key"] = category_key
            item["category_title"] = category_title
            item["brief"] = summarize_title(item["title"], category_title)
            articles.append(item)

        reference_dir = Path(__file__).resolve().parent.parent / "references"
        reference_dir.mkdir(parents=True, exist_ok=True)
        snapshot_date = datetime.now().strftime("%Y-%m-%d")
        stem = CONFIG["skill_name"].replace("opencli-", "")
        payload = {
            "snapshot_date": snapshot_date,
            "account": meta["account"],
            "album_title": meta["title"],
            "count": len(articles),
            "articles": articles,
        }
        json_text = json.dumps(payload, ensure_ascii=False, indent=2)
        (reference_dir / f"{stem}-articles-latest.json").write_text(json_text, encoding="utf-8")
        (reference_dir / f"{stem}-articles-{snapshot_date}.json").write_text(json_text, encoding="utf-8")

        category_map = {category["key"]: category for category in CONFIG["categories"]}
        grouped = {}
        for article in articles:
            grouped.setdefault(article["category_key"], []).append(article)

        lines = [
            f"# {CONFIG['skill_name']} Map",
            "",
            f"- Snapshot date: `{snapshot_date}`",
            f"- Account: `{meta['account']}`",
            f"- Album title: `{meta['title']}`",
            f"- Source album URL: {CONFIG['url']}",
            f"- Total articles: `{len(articles)}`",
            f"- Focus: {CONFIG['focus']}",
        ]
        if meta.get("intro"):
            lines.append(f"- Album intro: {meta['intro']}")
        if CONFIG["boundary_note"]:
            lines.append(f"- Boundary note: {CONFIG['boundary_note']}")
        lines.append("")
        for category in CONFIG["categories"]:
            items = grouped.get(category["key"], [])
            if not items:
                continue
            lines.append(f"## {category['title']}")
            lines.append("")
            for item in items:
                lines.append(
                    f"- `{item['date'] or 'unknown-date'}` [{item['title']}]({item['url']}) `{item['msgid']}`: {item['brief']}"
                )
            lines.append("")
        text = "\n".join(lines).rstrip() + "\n"
        (reference_dir / f"{stem}-album-map-latest.md").write_text(text, encoding="utf-8")
        (reference_dir / f"{stem}-album-map-{snapshot_date}.md").write_text(text, encoding="utf-8")
        print(f"Refreshed {CONFIG['skill_name']} with {len(articles)} articles.")


    if __name__ == "__main__":
        main()
