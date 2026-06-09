# Output Schema

Create `diary_data.json` before rendering. Keep fields concise and factual.

```json
{
  "title": "A human title for the day",
  "date": "YYYY-MM-DD",
  "weekday": "Monday",
  "timezone": "Asia/Shanghai",
  "location": "City, Region",
  "weather": {
    "summary": "Cloudy, light rain in the evening",
    "short": "晴",
    "temperature": "22-28°C",
    "source": "Weather provider or URL"
  },
  "mood": "quiet / energetic / mixed",
  "tags": ["work", "family", "learning"],
  "primary_language": "en",
  "language_order": ["en"],
  "style": {
    "heading": "20260603周日晴",
    "target_length": "300-400 characters for Chinese or 300-400 words for English",
    "max_length": "800-1000 unless user requests verbatim preservation",
    "paragraphs": "3-4 by default",
    "include_metadata_sections": false
  },
  "source_summary": [
    "3 voice notes",
    "2 screenshots",
    "1 text note"
  ],
  "timeline": [
    {
      "time": "09:30",
      "title": "Short event title",
      "details": "One or two factual sentences.",
      "source": "voice-note-01.m4a"
    }
  ],
  "diary": {
    "en": {
      "opening": "One reflective opening sentence.",
      "body": [
        "Paragraph 1.",
        "Paragraph 2."
      ],
      "closing": "One closing sentence."
    },
    "zh-CN": {
      "opening": "One reflective opening sentence.",
      "body": [
        "Paragraph 1.",
        "Paragraph 2."
      ],
      "closing": "One closing sentence."
    }
  },
  "fact_checks": [
    {
      "claim": "Original uncertain claim",
      "status": "corrected / verified / unresolved",
      "original_wording": "Optional exact wording from the writer",
      "result": "What was found without rewriting the writer's subjective voice",
      "sources": ["https://example.com"]
    }
  ],
  "attachments": [
    {
      "path": "relative/or/original/path",
      "label": "Human label",
      "type": "image/audio/document/text"
    }
  ]
}
```

Markdown render order:

1. Compact heading, usually `YYYYMMDD周X天气`.
2. Diary body directly after the heading.
3. Optional additional language sections only when requested.
4. Brief verification notes only when factual corrections or unresolved checks materially matter.

Do not include YAML frontmatter, source summaries, metadata blocks, attachment lists, or timeline sections by default. Those details are working notes unless the user asks to include them.

Length:

- Default target: 300-400 characters for Chinese, or 300-400 words for English.
- Default maximum: 800-1000 characters/words even when inputs are large.
- If the source is thousands of characters/words or many files, confirm whether to compress before writing.
- Preserve all source content only when the user explicitly asks for verbatim or exhaustive retention.
- Default paragraph count: 3-4 paragraphs. Use more only for large confirmed outputs.

Tone:

- Preserve the writer's original thoughts, wording, biases, emotions, and point of view.
- English: readable diary prose, not a literal translation, but never more neutral or morally polished than the source.
- Chinese, when requested: natural, literary but not ornate; first person when source material is first person; preserve the same stance and bias.
- Other languages, when requested: write naturally for that language instead of translating sentence-by-sentence, while preserving the writer's stance.
- Keep private and emotional details intact unless the user asks for anonymization.
- Do not fabricate sensory detail, conversations, or motives.
