# GitHub Publishing

Publish only after the diary entry and assets have been reviewed for privacy.

## Repository Rules

- Prefer an existing local repo supplied by the user.
- Do not create a public repository unless explicitly requested.
- If no remote exists, commit locally and tell the user push was skipped.
- If the working tree has unrelated changes, avoid touching them. Add only the diary entry and copied assets.
- Use a clear commit message such as `Add diary for 2026-06-08`.

## Suggested Layout

```text
entries/
  YYYY/
    MM/
      YYYY-MM-DD-diary.md
      YYYY-MM-DD-cover.svg
assets/
  covers/
```

Use the layout already present in the repo when one exists.

## Publishing Command

```bash
/Users/shanwei/.codex/skills/daily-diary/scripts/publish_to_github.sh \
  --repo /path/to/repo \
  --entry /path/to/YYYY-MM-DD-diary.md \
  --asset /path/to/cover.svg \
  --dest entries/YYYY/MM \
  --message "Add diary for YYYY-MM-DD"
```

The script:

1. Copies the entry and assets into the destination folder.
2. Runs `git add` only for those copied files.
3. Creates a commit when there are staged changes.
4. Pushes the current branch when a remote is configured, unless `--no-push` is passed.

If publishing fails, keep the rendered files and report the exact failure.
