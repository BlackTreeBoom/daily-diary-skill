---
name: daily-diary
description: Create verified personal diary entries from arbitrary daily inputs, defaulting to polished English with optional additional languages. Use when the user asks to make a diary, journal, daily log, life record, or GitHub-published diary from dumped text, files, folders, screenshots, audio/video, voice notes, chat exports, or mixed materials; includes chronological organization, transcription/OCR coordination, web/current-event fact checking, date/weather enrichment, pre-writing confirmation of scope and verification targets, attractive cover generation, and GitHub publishing or syncing.
---

# Daily Diary

## Goal

Turn messy daily material into a polished diary entry. Default to English diary prose, then add other languages only when the user requests them or selects them during the pre-writing confirmation. Preserve the user's lived perspective, organize events by time, verify uncertain claims, enrich with date/weather/context, create or select an attractive cover, and publish the finished Markdown entry plus assets to GitHub when a repository is available.

## Default Workflow

1. **Set the scope.** Determine the target date, timezone, output languages, location for weather, and GitHub repo path/branch. Default to English only, plus the user's current date/timezone when not specified. Ask only for missing information that blocks publishing, weather lookup, or the user's requested language choice.
2. **Collect inputs.** Run `scripts/collect_inputs.py` on provided files/folders when there are local artifacts. It produces a JSONL manifest with file metadata, extracted text where possible, and flags for OCR/transcription.
3. **Transcribe or OCR missing content.** For audio/video, use an available speech-to-text workflow and preserve timestamps when possible. For screenshots/images, OCR visible text if it is likely diary-relevant. Save derived transcripts as source artifacts and include them in the timeline.
4. **Build a timeline.** Order material by explicit timestamps, EXIF/metadata, file modified times, filenames, and narrative cues. Keep uncertain ordering explicit instead of inventing precision.
5. **Confirm before writing.** Before drafting diary prose, tell the user the planned date, language list, weather location, source set, uncertain claims to verify, and GitHub destination. Wait for confirmation when the user is present. If the user explicitly asked for unattended processing, record assumptions and continue.
6. **Research and verify.** Search for today's weather, current events, named people/companies/places, and any phrases like "好像", "似乎", "不确定", "maybe", "I think", or "not sure". Use primary or reputable sources, record citations in working notes, and correct factual errors without overwriting the user's subjective feeling.
7. **Draft diary data.** Create a `diary_data.json` object following `references/output-schema.md`. Include `primary_language: "en"`, `language_order`, weather, timeline, fact checks, tags, source summaries, cover metadata, and any requested language versions.
8. **Create the cover.** Prefer a content-aware generated image when image generation is available. Otherwise run `scripts/make_cover_svg.py` to create a clean, attractive SVG cover using the date, title, weather, and mood.
9. **Render Markdown.** Run `scripts/render_diary.py --data diary_data.json --out <entry.md>`. Review the result for tone, factual corrections, readable language sections, and clean image paths.
10. **Publish to GitHub.** If a local GitHub repo is available, run `scripts/publish_to_github.sh` to copy the entry/assets, commit, and push. If no repo is available, create the files locally and ask for the target repo/path.
11. **Report back.** Return the entry path, cover path, commit/push result, unresolved uncertainties, and the most important verification sources.

## Input Handling

- Treat user-provided text as a source artifact, not as final prose.
- Never mutate original source files.
- For many files, first create a working directory such as `diary-work/YYYY-MM-DD/` and keep manifests, transcripts, fact notes, generated cover, and rendered Markdown there.
- If a source has no reliable time, place it under an "unknown time" bucket and infer position only when surrounding evidence is strong.
- Preserve meaningful quotes sparingly. For copyrighted material, quote only short excerpts and summarize the rest.

Useful command:

```bash
python /Users/shanwei/.codex/skills/daily-diary/scripts/collect_inputs.py \
  --date YYYY-MM-DD \
  --out diary-work/YYYY-MM-DD/manifest.jsonl \
  <files-or-folders>
```

## Verification Rules

Read `references/research-checklist.md` before researching or fact-checking. Always browse/search for information that can change over time: weather, news, schedules, prices, leaders, company facts, events, laws, product details, and anything the user frames as uncertain.

When correcting, keep the diary emotionally truthful:

- Correct objective facts in the factual layer.
- Keep subjective language in the diary voice.
- If the evidence is mixed, write a careful formulation instead of a confident claim.
- Put detailed citations in `fact_checks` or working notes; the diary body should read naturally.

## Output Shape

Use `references/output-schema.md` for the JSON data contract and Markdown structure. Default to:

- A cover image at the top.
- YAML frontmatter for GitHub/blog compatibility.
- Date, weekday, location, and weather.
- A short source summary.
- A chronological timeline.
- `English Diary` as the primary version.
- Optional additional diary sections, such as `中文日记`, only when requested or confirmed.
- A concise `Verification Notes` section when factual corrections matter.

Render command:

```bash
python /Users/shanwei/.codex/skills/daily-diary/scripts/render_diary.py \
  --data diary-work/YYYY-MM-DD/diary_data.json \
  --out diary-work/YYYY-MM-DD/YYYY-MM-DD-diary.md
```

## Cover Guidance

Use a cover that feels like the day, not a generic productivity banner. Good covers include one concrete motif from the diary, one time/weather cue, and a quiet sense of chronology.

If using deterministic SVG:

```bash
python /Users/shanwei/.codex/skills/daily-diary/scripts/make_cover_svg.py \
  --title "今日标题" \
  --date YYYY-MM-DD \
  --weather "晴，24-31°C" \
  --subtitle "English Daily Diary" \
  --out diary-work/YYYY-MM-DD/cover.svg
```

If using AI image generation, ask for a 16:9 cover with no readable text/logos/watermarks, enough negative space, and visual elements grounded in the diary content.

## GitHub Publishing

Read `references/github-publishing.md` before publishing. Prefer the user's existing diary repo. Do not create a new public repo unless the user explicitly asks.

Typical command:

```bash
/Users/shanwei/.codex/skills/daily-diary/scripts/publish_to_github.sh \
  --repo /path/to/diary-repo \
  --entry diary-work/YYYY-MM-DD/YYYY-MM-DD-diary.md \
  --asset diary-work/YYYY-MM-DD/cover.svg \
  --dest entries/YYYY/MM \
  --message "Add diary for YYYY-MM-DD"
```

The script commits and pushes by default when a remote exists. Use `--no-push` only when the user asks to keep changes local.
