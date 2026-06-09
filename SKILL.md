---
name: daily-diary
description: Create concise, verified local Markdown diary entries from arbitrary daily inputs while preserving the writer's original thoughts, wording, biases, emotions, and point of view. Use when the user asks to make a diary, journal, daily log, or life record from dumped text, files, folders, screenshots, audio/video, voice notes, chat exports, or mixed materials; includes chronological organization, transcription/OCR coordination, web/current-event fact checking, date/weather enrichment, strict authorial-fidelity rules, a compact YYYYMMDD周X天气 heading, 3-4 paragraph diary prose, default 300-400 characters/words with a 800-1000 maximum unless verbatim preservation is requested, pre-writing confirmation of scope and compression when inputs are large, and saving a local YYYY-MM-DD.md file. Do not publish to GitHub and do not create covers unless the user explicitly asks outside this skill.
---

# Daily Diary

## Goal

Turn messy daily material into one concise local Markdown diary file named after the target date, such as `2026-06-09.md`. The diary itself starts with a compact heading like `20260603周日晴`, then the diary body begins on the next line. Preserve the writer's original thoughts, wording, biases, emotions, and point of view; organize events by time; verify objective claims; enrich with date/weather/context; and save the finished `.md` file locally.

## Default Workflow

1. **Set the scope.** Determine the target date, timezone, output languages, location for weather, and local output directory. Default to English only, the user's current date/timezone, and `./diary` under the current workspace when not specified. Ask only for missing information that blocks weather lookup, source access, or the user's requested language choice.
2. **Collect inputs.** Run `scripts/collect_inputs.py` on provided files/folders when there are local artifacts. It produces a JSONL manifest with file metadata, extracted text where possible, and flags for OCR/transcription.
3. **Transcribe or OCR missing content.** For audio/video, use an available speech-to-text workflow and preserve timestamps when possible. For screenshots/images, OCR visible text if it is likely diary-relevant. Save derived transcripts as source artifacts and include them in the timeline.
4. **Build a timeline.** Order material by explicit timestamps, EXIF/metadata, file modified times, filenames, and narrative cues. Keep uncertain ordering explicit instead of inventing precision.
5. **Confirm before writing.** Before drafting diary prose, tell the user the planned date, language list, weather location, source set, uncertain claims to verify, local output path, target length, and whether source volume requires compression. Wait for confirmation when the source material is large or when meaningful content may be omitted. If the user explicitly asked for unattended processing, record assumptions and continue.
6. **Apply authorial fidelity.** Read `references/writing-fidelity.md` before drafting. Do not sanitize, balance, moralize, soften, or replace the writer's stated opinions, assumptions, biases, emotions, or self-description. Only organize and clarify the diary format.
7. **Research and verify.** Search for today's weather, current events, named people/companies/places, and any phrases like "好像", "似乎", "不确定", "maybe", "I think", or "not sure". Use primary or reputable sources and record citations in working notes. Do not silently overwrite the writer's claim in the diary voice; put objective corrections in verification notes while preserving what the writer said.
8. **Draft diary data.** Create a `diary_data.json` object following `references/output-schema.md`. Include `primary_language: "en"`, `language_order`, weather, timeline, fact checks, tags, source summaries, and any requested language versions.
9. **Render Markdown.** Run `scripts/render_diary.py --data diary_data.json --dir <local-diary-folder>`. The output file must be named `YYYY-MM-DD.md` unless the user explicitly asks for another name. Review the result for the compact heading, 3-4 paragraphs by default, target length, authorial fidelity, factual notes, and clean Markdown.
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
  --out .daily-diary-work/YYYY-MM-DD/manifest.jsonl \
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
- First line: compact heading `YYYYMMDD周X天气`, for example `20260603周日晴`.
- Second line onward: diary body, without report-style metadata sections by default.
- Do not add a separate title by default; the compact heading is the title.
- Default length: about 300-400 characters for Chinese or 300-400 words for English.
- Hard default maximum: 800-1000 characters/words when inputs are large, unless the user explicitly says to keep everything verbatim.
- Default paragraph count: 3-4 paragraphs; use more only when the source material is genuinely large and the user confirms a longer entry.
- No source summary or timeline in the final diary unless the user asks for them.
- A concise `Verification Notes` section only when factual corrections or unresolved checks materially matter.

If the user provides thousands of characters/words or many files, confirm whether to compress to the default diary length before writing. Do not silently discard important content; explain that the default diary is concise and ask whether to preserve all details.

Render command:

```bash
python /Users/shanwei/.codex/skills/daily-diary/scripts/render_diary.py \
  --data .daily-diary-work/YYYY-MM-DD/diary_data.json \
  --dir ./diary
```

Do not publish, commit, push, or create cover assets as part of this skill. The final deliverable is the local `.md` file.
