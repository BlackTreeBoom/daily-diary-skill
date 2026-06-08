#!/usr/bin/env python3
"""Generate a polished SVG cover for a diary entry."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def svg(title: str, date: str, weather: str, subtitle: str, accent: str) -> str:
    title = esc(title)
    date = esc(date)
    weather = esc(weather)
    subtitle = esc(subtitle)
    accent = esc(accent)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0f172a"/>
      <stop offset="0.48" stop-color="#155e63"/>
      <stop offset="1" stop-color="#f59e0b"/>
    </linearGradient>
    <radialGradient id="glow" cx="76%" cy="22%" r="52%">
      <stop offset="0" stop-color="#fff7ed" stop-opacity="0.72"/>
      <stop offset="0.55" stop-color="#f8fafc" stop-opacity="0.1"/>
      <stop offset="1" stop-color="#0f172a" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="24" stdDeviation="24" flood-color="#020617" flood-opacity="0.35"/>
    </filter>
  </defs>
  <rect width="1600" height="900" fill="url(#bg)"/>
  <rect width="1600" height="900" fill="url(#glow)"/>
  <g opacity="0.18" fill="none" stroke="#e2e8f0" stroke-width="2">
    <path d="M140 170 C360 70 510 230 710 130 S1120 80 1410 180"/>
    <path d="M170 735 C350 640 500 760 710 675 S1110 590 1390 720"/>
    <path d="M245 260 H1340"/>
    <path d="M245 625 H1340"/>
  </g>
  <g opacity="0.42" fill="#f8fafc">
    <circle cx="280" cy="260" r="6"/>
    <circle cx="520" cy="212" r="4"/>
    <circle cx="810" cy="262" r="5"/>
    <circle cx="1050" cy="210" r="4"/>
    <circle cx="1300" cy="270" r="6"/>
    <circle cx="380" cy="655" r="4"/>
    <circle cx="690" cy="700" r="5"/>
    <circle cx="1010" cy="630" r="4"/>
    <circle cx="1260" cy="690" r="5"/>
  </g>
  <g filter="url(#shadow)">
    <path d="M430 270 C535 235 674 250 800 318 C926 250 1065 235 1170 270 L1170 706 C1068 674 926 690 800 765 C674 690 532 674 430 706 Z" fill="#fff7ed"/>
    <path d="M800 318 L800 765" stroke="#cbd5e1" stroke-width="4"/>
    <path d="M485 340 C586 318 672 333 750 380" fill="none" stroke="#94a3b8" stroke-width="7" stroke-linecap="round" opacity="0.55"/>
    <path d="M485 405 C596 382 674 402 742 442" fill="none" stroke="#94a3b8" stroke-width="7" stroke-linecap="round" opacity="0.45"/>
    <path d="M850 380 C938 328 1032 318 1115 344" fill="none" stroke="#94a3b8" stroke-width="7" stroke-linecap="round" opacity="0.55"/>
    <path d="M858 443 C952 398 1036 390 1112 410" fill="none" stroke="#94a3b8" stroke-width="7" stroke-linecap="round" opacity="0.45"/>
    <path d="M520 520 C660 470 750 525 800 588 C850 525 940 470 1080 520" fill="none" stroke="{accent}" stroke-width="9" stroke-linecap="round" opacity="0.82"/>
  </g>
  <g transform="translate(120 112)">
    <rect x="0" y="0" width="260" height="72" rx="18" fill="#f8fafc" opacity="0.16"/>
    <text x="28" y="46" font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="30" fill="#f8fafc">{date}</text>
  </g>
  <g transform="translate(1180 112)">
    <circle cx="38" cy="38" r="24" fill="#fde68a" opacity="0.92"/>
    <path d="M82 55 C99 30 136 34 146 64 C167 65 181 80 181 99 C181 120 163 136 140 136 H72 C46 136 26 119 26 96 C26 73 45 56 70 56 C73 56 77 56 82 55Z" fill="#e0f2fe" opacity="0.92"/>
    <text x="0" y="190" font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="28" fill="#f8fafc" opacity="0.9">{weather}</text>
  </g>
  <g transform="translate(120 728)">
    <text x="0" y="0" font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="78" font-weight="750" fill="#ffffff">{title}</text>
    <text x="4" y="70" font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="31" fill="#e2e8f0" opacity="0.92">{subtitle}</text>
  </g>
</svg>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an SVG diary cover.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--weather", default="")
    parser.add_argument("--subtitle", default="Chinese / English Daily Diary")
    parser.add_argument("--accent", default="#14b8a6")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(svg(args.title, args.date, args.weather, args.subtitle, args.accent), encoding="utf-8")
    print(f"Wrote cover to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
