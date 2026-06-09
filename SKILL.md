---
name: daily-diary
description: Create verified local Markdown diary entries from arbitrary daily inputs, defaulting to polished English with optional additional languages while preserving the writer's original thoughts, wording, biases, emotions, and point of view. Use when the user asks to make a diary, journal, daily log, or life record from dumped text, files, folders, screenshots, audio/video, voice notes, chat exports, or mixed materials; includes chronological organization, transcription/OCR coordination, web/current-event fact checking, date/weather enrichment, strict authorial-fidelity rules, pre-writing confirmation of scope and verification targets, and saving a local YYYY-MM-DD.md file. Do not publish to GitHub and do not create covers unless the user explicitly asks outside this skill.
---

# Daily Diary

## Goal

Turn messy daily material into one polished local Markdown diary file named after the target date, such as `2026-06-09.md`. Default to English diary prose, then add other languages only when the user requests them or selects them during the pre-writing confirmation. Preserve the writer's original thoughts, wording, biases, emotions, and point of view; organize events by time; verify objective claims; enrich with date/weather/context; and save the finished `.md` file locally.

## Default Workflow

1. **Set the scope.** Determine the target date, timezone, output languages, location for weather, and local output directory. Default to English only, the user's current date/timezone, and `./diary` under the current workspace when not specified. Ask only for missing information that blocks weather lookup, source access, or the user's requested language choice.
2. **Collect inputs.** Run `scripts/collect_inputs.py` on provided files/folders when there are local artifacts. It produces a JSONL manifest with file metadata, extracted text where possible, and flags for OCR/transcription.
3. **Transcribe or OCR missing content.** For audio/video, use an available speech-to-text workflow and preserve timestamps when possible. For screenshots/images, OCR visible text if it is likely diary-relevant. Save derived transcripts as source artifacts and include them in the timeline.
4. **Build a timeline.** Order material by explicit timestamps, EXIF/metadata, file modified times, filenames, and narrative cues. Keep uncertain ordering explicit instead of inventing precision.
5. **Confirm before writing.** Before drafting diary prose, tell the user the planned date, language list, weather location, source set, uncertain claims to verify, and local output path. Wait for confirmation when the user is present. If the user explicitly asked for unattended processing, record assumptions and continue.
6. **Apply authorial fidelity.** Read `references/writing-fidelity.md` before drafting. Do not sanitize, balance, moralize, soften, or replace the writer's stated opinions, assumptions, biases, emotions, or self-description. Only organize and clarify the diary format.
7. **Research and verify.** Search for today's weather, current events, named people/companies/places, and any phrases like "好像", "似乎", "不确定", "maybe", "I think", or "not sure". Use primary or reputable sources and record citations in working notes. Do not silently overwrite the writer's claim in the diary voice; put objective corrections in verification notes while preserving what the writer said.
8. **Draft diary data.** Create a `diary_data.json` object following `references/output-schema.md`. Include `primary_language: "en"`, `language_order`, weather, timeline, fact checks, tags, source summaries, and any requested language versions.
9. **Render Markdown.** Run `scripts/render_diary.py --data diary_data.json --dir <local-diary-folder>`. The output file must be named `YYYY-MM-DD.md` unless the user explicitly asks for another name. Review the result for authorial fidelity, factual notes, readable language sections, and clean Markdown.
10. **Report back.** Return the local Markdown path, unresolved uncertainties, and the most important verification sources.

## Input Handling

- Treat user-provided text as a source artifact, not as final prose.
- Never mutate original source files.
- For many files, first create a temporary working directory such as `.daily-diary-work/YYYY-MM-DD/` and keep manifests, transcripts, and fact notes there. The final output remains a single local Markdown file.
- If a source has no reliable time, place it under an "unknown time" bucket and infer position only when surrounding evidence is strong.
- Preserve the writer's exact claims and characteristic phrasing whenever they matter to meaning. For copyrighted third-party material, quote only short excerpts and summarize the rest.

Useful command:

```bash
python /Users/shanwei/.codex/skills/daily-diary/scripts/collect_inputs.py \
  --date YYYY-MM-DD \
  --out diary-work/YYYY-MM-DD/manifest.jsonl \
  <files-or-folders>
```

## Verification Rules

Read `references/research-checklist.md` before researching or fact-checking. Always browse/search for information that can change over time: weather, news, schedules, prices, leaders, company facts, events, laws, product details, and anything the user frames as uncertain.

When correcting, keep the diary author-faithful:

- Never correct opinions, biases, preferences, emotional reactions, self-judgments, or values as if they were factual errors.
- Never rewrite the diary to sound more reasonable, neutral, polite, charitable, optimistic, or socially acceptable than the source material.
- Preserve the writer's subjective language in the diary voice.
- If an objective fact is wrong, keep what the writer believed or said visible in the diary, then put the factual correction in `fact_checks` or `Verification Notes`.
- If the evidence is mixed, keep the uncertainty visible instead of creating false confidence.

## Output Shape

Use `references/output-schema.md` for the JSON data contract and Markdown structure. Default to:

- A local Markdown file named `YYYY-MM-DD.md`.
- Optional YAML frontmatter for local archive metadata.
- Date, weekday, location, and weather.
- A short source summary.
- A chronological timeline.
- `English Diary` as the primary version.
- Optional additional diary sections, such as `中文日记`, only when requested or confirmed.
- A concise `Verification Notes` section when factual corrections matter.

Render command:

```bash
python /Users/shanwei/.codex/skills/daily-diary/scripts/render_diary.py \
  --data .daily-diary-work/YYYY-MM-DD/diary_data.json \
  --dir ./diary
```

Do not publish, commit, push, or create cover assets as part of this skill. The final deliverable is the local `.md` file.
