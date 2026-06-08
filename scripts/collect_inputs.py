#!/usr/bin/env python3
"""Collect diary source artifacts into a JSONL manifest."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


TEXT_SUFFIXES = {
    ".txt",
    ".md",
    ".markdown",
    ".csv",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".log",
    ".rtf",
}
AUDIO_SUFFIXES = {".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg", ".opus", ".amr"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".heic", ".webp", ".gif", ".tiff", ".bmp"}
DOCUMENT_SUFFIXES = {".pdf", ".docx", ".pptx", ".xlsx"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".DS_Store"}


def iso_from_timestamp(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts).astimezone().isoformat(timespec="seconds")


def iter_files(inputs: list[Path]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        if item.is_dir():
            for root, dirs, names in os.walk(item):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in names:
                    path = Path(root) / name
                    if path.is_file():
                        files.append(path)
        elif item.is_file():
            files.append(item)
    return sorted(files, key=lambda p: (p.stat().st_mtime, str(p)))


def read_text(path: Path, max_chars: int) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding, errors="replace")[:max_chars]
        except UnicodeDecodeError:
            continue
    return path.read_bytes()[:max_chars].decode("utf-8", errors="replace")


def extract_pdf(path: Path, max_chars: int) -> str:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        chunks: list[str] = []
        for page in reader.pages[:20]:
            chunks.append(page.extract_text() or "")
            if sum(len(chunk) for chunk in chunks) >= max_chars:
                break
        return "\n".join(chunks)[:max_chars]
    except Exception:
        pass

    if shutil.which("pdftotext"):
        try:
            output = subprocess.check_output(
                ["pdftotext", "-layout", str(path), "-"],
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            return output.decode("utf-8", errors="replace")[:max_chars]
        except Exception:
            return ""
    return ""


def extract_docx(path: Path, max_chars: int) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            xml_bytes = archive.read("word/document.xml")
        root = ET.fromstring(xml_bytes)
        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs: list[str] = []
        for paragraph in root.findall(".//w:p", namespace):
            texts = [node.text or "" for node in paragraph.findall(".//w:t", namespace)]
            if texts:
                paragraphs.append("".join(texts))
        return "\n".join(paragraphs)[:max_chars]
    except Exception:
        return ""


def extract_pptx(path: Path, max_chars: int) -> str:
    try:
        chunks: list[str] = []
        with zipfile.ZipFile(path) as archive:
            slide_names = sorted(name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml"))
            for name in slide_names:
                root = ET.fromstring(archive.read(name))
                texts = [node.text or "" for node in root.iter() if node.tag.endswith("}t")]
                if texts:
                    chunks.append(" ".join(texts))
                if sum(len(chunk) for chunk in chunks) >= max_chars:
                    break
        return "\n\n".join(chunks)[:max_chars]
    except Exception:
        return ""


def extract_xlsx(path: Path, max_chars: int) -> str:
    try:
        import openpyxl  # type: ignore

        workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
        rows: list[str] = []
        for sheet in workbook.worksheets[:5]:
            rows.append(f"[Sheet: {sheet.title}]")
            for values in sheet.iter_rows(max_row=100, values_only=True):
                row = ["" if value is None else str(value) for value in values]
                if any(row):
                    rows.append(",".join(csv_quote(cell) for cell in row))
                if sum(len(line) for line in rows) >= max_chars:
                    return "\n".join(rows)[:max_chars]
        return "\n".join(rows)[:max_chars]
    except Exception:
        return ""


def csv_quote(value: str) -> str:
    if any(char in value for char in [",", '"', "\n"]):
        return '"' + value.replace('"', '""') + '"'
    return value


def strip_html(path: Path, max_chars: int) -> str:
    raw = read_text(path, max_chars * 2)
    raw = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = re.sub(r"\s+", " ", html.unescape(raw)).strip()
    return raw[:max_chars]


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in AUDIO_SUFFIXES:
        return "audio"
    if suffix in VIDEO_SUFFIXES:
        return "video"
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in TEXT_SUFFIXES or suffix in {".html", ".htm"}:
        return "text"
    if suffix in DOCUMENT_SUFFIXES:
        return "document"
    return "unknown"


def extract_text(path: Path, kind: str, max_chars: int) -> tuple[str, list[str]]:
    suffix = path.suffix.lower()
    flags: list[str] = []
    text = ""

    if kind == "text":
        text = strip_html(path, max_chars) if suffix in {".html", ".htm"} else read_text(path, max_chars)
    elif suffix == ".pdf":
        text = extract_pdf(path, max_chars)
    elif suffix == ".docx":
        text = extract_docx(path, max_chars)
    elif suffix == ".pptx":
        text = extract_pptx(path, max_chars)
    elif suffix == ".xlsx":
        text = extract_xlsx(path, max_chars)

    if kind in {"audio", "video"}:
        flags.append("requires_transcription")
    if kind == "image":
        flags.append("requires_ocr")
    if kind == "document" and not text:
        flags.append("text_extraction_failed")
    if len(text) >= max_chars:
        flags.append("text_truncated")
    return text, flags


def build_record(path: Path, date: str | None, max_chars: int) -> dict:
    stat = path.stat()
    kind = classify(path)
    text, flags = extract_text(path, kind, max_chars)
    mime_type, _ = mimetypes.guess_type(str(path))
    return {
        "path": str(path.resolve()),
        "name": path.name,
        "suffix": path.suffix.lower(),
        "kind": kind,
        "mime_type": mime_type,
        "size_bytes": stat.st_size,
        "modified_at": iso_from_timestamp(stat.st_mtime),
        "created_at": iso_from_timestamp(stat.st_ctime),
        "target_date": date,
        "text": text,
        "flags": flags,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect local diary inputs into JSONL.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Files or folders to scan")
    parser.add_argument("--out", required=True, type=Path, help="Output JSONL manifest")
    parser.add_argument("--date", help="Target diary date, YYYY-MM-DD")
    parser.add_argument("--max-chars", type=int, default=20000, help="Max extracted characters per file")
    args = parser.parse_args()

    missing = [str(path) for path in args.inputs if not path.exists()]
    if missing:
        print(f"Missing inputs: {', '.join(missing)}", file=sys.stderr)
        return 2

    files = iter_files(args.inputs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for path in files:
            record = build_record(path, args.date, args.max_chars)
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {len(files)} records to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
