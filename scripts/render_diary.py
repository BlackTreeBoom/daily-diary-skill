#!/usr/bin/env python3
"""Render a local Markdown diary file from diary_data.json."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


def line_join(lines: list[str]) -> str:
    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


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


def compact_heading(data: dict[str, Any]) -> str:
    style = data.get("style") or {}
    if style.get("heading"):
        return str(style["heading"])

    date = str(data.get("date") or dt.date.today().isoformat())
    date_digits = re.sub(r"\D", "", date)
    if len(date_digits) != 8:
        date_digits = dt.date.today().strftime("%Y%m%d")

    weekday = str(data.get("weekday") or "").strip()
    weekday_map = {
        "monday": "周一",
        "mon": "周一",
        "tuesday": "周二",
        "tue": "周二",
        "wednesday": "周三",
        "wed": "周三",
        "thursday": "周四",
        "thu": "周四",
        "friday": "周五",
        "fri": "周五",
        "saturday": "周六",
        "sat": "周六",
        "sunday": "周日",
        "sun": "周日",
    }
    if not weekday.startswith("周"):
        weekday = weekday_map.get(weekday.lower(), "")
    if not weekday:
        try:
            parsed = dt.date.fromisoformat(f"{date_digits[:4]}-{date_digits[4:6]}-{date_digits[6:]}")
            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][parsed.weekday()]
        except ValueError:
            weekday = ""

    weather = data.get("weather") or {}
    weather_text = str(weather.get("short") or weather.get("summary") or "").strip()
    weather_text = re.split(r"[,，;；、\s]", weather_text, maxsplit=1)[0]
    return f"{date_digits}{weekday}{weather_text}".strip()


def section_parts(section: dict[str, Any]) -> list[str]:
    parts: list[str] = []
    for part in [section.get("opening"), *(section.get("body") or []), section.get("closing")]:
        if part:
            parts.append(str(part).strip())
    return [part for part in parts if part]


def render(data: dict[str, Any]) -> str:
    diary = data.get("diary") or {}

    lines: list[str] = [compact_heading(data), ""]

    languages = ordered_languages(data, diary)
    for index, language in enumerate(languages):
        section = diary.get(language) or {}
        if index > 0:
            lines.extend([f"## {language_heading(language)}", ""])
        for part in section_parts(section):
            lines.extend([part, ""])

    fact_checks = data.get("fact_checks") or []
    visible_checks = [item for item in fact_checks if item.get("include_in_diary", True)]
    if visible_checks:
        lines.extend(["## Verification Notes", ""])
        for item in visible_checks:
            claim = item.get("claim") or "Claim"
            status = item.get("status") or "checked"
            result = item.get("result") or ""
            lines.append(f"- **{status}** {claim}: {result}")
        lines.append("")

    return line_join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a local Markdown diary file.")
    parser.add_argument("--data", required=True, type=Path, help="Input diary_data.json")
    parser.add_argument("--out", type=Path, help="Output Markdown path. Defaults to DIR/YYYY-MM-DD.md")
    parser.add_argument("--dir", type=Path, default=Path("."), help="Output directory when --out is omitted")
    args = parser.parse_args()

    data = json.loads(args.data.read_text(encoding="utf-8"))
    markdown = render(data)
    date = data.get("date") or dt.date.today().isoformat()
    out = args.out or (args.dir / f"{date}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    print(f"Wrote diary to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
