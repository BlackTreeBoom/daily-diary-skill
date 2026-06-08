#!/usr/bin/env python3
"""Render a bilingual diary Markdown file from diary_data.json."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def yaml_scalar(value: Any) -> str:
    if value is None:
        return '""'
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def yaml_list(values: list[Any]) -> str:
    return "[" + ", ".join(yaml_scalar(value) for value in values) + "]"


def line_join(lines: list[str]) -> str:
    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


def bullet_list(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values if value]


def language_heading(language: str) -> str:
    labels = {
        "en": "English Diary",
        "en-US": "English Diary",
        "en-GB": "English Diary",
        "zh": "中文日记",
        "zh-CN": "中文日记",
        "zh-TW": "中文日記",
        "ja": "日本語の日記",
        "ko": "한국어 일기",
        "fr": "Journal en français",
        "es": "Diario en español",
        "de": "Tagebuch auf Deutsch",
    }
    return labels.get(language, f"Diary ({language})")


def ordered_languages(data: dict[str, Any], diary: dict[str, Any]) -> list[str]:
    configured = data.get("language_order") or []
    primary = data.get("primary_language") or "en"
    ordered: list[str] = []
    for language in [primary, *configured, "en", *diary.keys()]:
        if language in diary and language not in ordered:
            ordered.append(language)
    return ordered


def render(data: dict[str, Any]) -> str:
    title = data.get("title") or f"Diary {data.get('date', '')}".strip()
    date = data.get("date", "")
    weather = data.get("weather") or {}
    cover = data.get("cover") or {}
    diary = data.get("diary") or {}

    frontmatter = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"date: {yaml_scalar(date)}",
        f"weekday: {yaml_scalar(data.get('weekday', ''))}",
        f"timezone: {yaml_scalar(data.get('timezone', ''))}",
        f"location: {yaml_scalar(data.get('location', ''))}",
        f"weather: {yaml_scalar(weather.get('summary', ''))}",
        f"temperature: {yaml_scalar(weather.get('temperature', ''))}",
        f"mood: {yaml_scalar(data.get('mood', ''))}",
        f"tags: {yaml_list(data.get('tags') or [])}",
        f"generated_at: {yaml_scalar(dt.datetime.now().astimezone().isoformat(timespec='seconds'))}",
        "---",
        "",
    ]

    lines: list[str] = frontmatter
    if cover.get("path"):
        alt = cover.get("alt") or title
        lines.extend([f"![{alt}]({cover['path']})", ""])

    lines.extend([f"# {title}", ""])

    meta_pairs = [
        ("日期 / Date", date),
        ("星期 / Weekday", data.get("weekday", "")),
        ("地点 / Location", data.get("location", "")),
        ("天气 / Weather", f"{weather.get('summary', '')} {weather.get('temperature', '')}".strip()),
        ("心情 / Mood", data.get("mood", "")),
    ]
    lines.extend([f"{label}: {value}" for label, value in meta_pairs if value])
    lines.append("")

    source_summary = data.get("source_summary") or []
    if source_summary:
        lines.extend(["## 素材概览 / Source Summary", ""])
        lines.extend(bullet_list(source_summary))
        lines.append("")

    timeline = data.get("timeline") or []
    if timeline:
        lines.extend(["## 时间线 / Timeline", ""])
        for item in timeline:
            time = item.get("time") or "时间不详"
            heading = item.get("title") or "Untitled"
            details = item.get("details") or ""
            source = item.get("source")
            suffix = f" _Source: {source}_" if source else ""
            lines.append(f"- **{time}** {heading}: {details}{suffix}")
        lines.append("")

    for language in ordered_languages(data, diary):
        section = diary.get(language) or {}
        lines.extend([f"## {language_heading(language)}", ""])
        for part in [section.get("opening"), *(section.get("body") or []), section.get("closing")]:
            if part:
                lines.extend([part, ""])

    fact_checks = data.get("fact_checks") or []
    if fact_checks:
        lines.extend(["## 校对与补全 / Verification Notes", ""])
        for item in fact_checks:
            claim = item.get("claim") or "Claim"
            status = item.get("status") or "checked"
            result = item.get("result") or ""
            sources = item.get("sources") or []
            source_text = ""
            if sources:
                source_text = " Sources: " + ", ".join(str(source) for source in sources)
            lines.append(f"- **{status}** {claim}: {result}{source_text}")
        lines.append("")

    attachments = data.get("attachments") or []
    if attachments:
        lines.extend(["## 附件 / Attachments", ""])
        for item in attachments:
            label = item.get("label") or item.get("path") or "Attachment"
            path = item.get("path") or ""
            type_name = item.get("type") or "file"
            lines.append(f"- [{type_name}] {label}: `{path}`")
        lines.append("")

    return line_join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a bilingual diary Markdown file.")
    parser.add_argument("--data", required=True, type=Path, help="Input diary_data.json")
    parser.add_argument("--out", required=True, type=Path, help="Output Markdown path")
    args = parser.parse_args()

    data = json.loads(args.data.read_text(encoding="utf-8"))
    markdown = render(data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown, encoding="utf-8")
    print(f"Wrote diary to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
