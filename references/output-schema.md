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
      "result": "What was found",
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

- English: polished diary prose, not a literal translation.
- Chinese, when requested: natural, literary but not ornate; first person when source material is first person.
- Other languages, when requested: write naturally for that language instead of translating sentence-by-sentence.
- Keep private and emotional details intact unless the user asks for anonymization.
- Do not fabricate sensory detail, conversations, or motives.
