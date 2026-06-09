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
    "temperature": "22-28°C",
    "source": "Weather provider or URL"
  },
  "mood": "quiet / energetic / mixed",
  "tags": ["work", "family", "learning"],
  "primary_language": "en",
  "language_order": ["en"],
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

1. YAML frontmatter.
2. Title and daily metadata.
3. Source summary.
4. Timeline.
5. English diary.
6. Optional additional language sections, in `language_order`.
7. Verification notes.
8. Attachments.

Tone:

- Preserve the writer's original thoughts, wording, biases, emotions, and point of view.
- English: readable diary prose, not a literal translation, but never more neutral or morally polished than the source.
- Chinese, when requested: natural, literary but not ornate; first person when source material is first person; preserve the same stance and bias.
- Other languages, when requested: write naturally for that language instead of translating sentence-by-sentence, while preserving the writer's stance.
- Keep private and emotional details intact unless the user asks for anonymization.
- Do not fabricate sensory detail, conversations, or motives.
