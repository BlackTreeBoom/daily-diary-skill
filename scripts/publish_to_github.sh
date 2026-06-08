#!/usr/bin/env bash
set -euo pipefail

repo=""
entry=""
dest="entries"
message=""
branch=""
push="1"
assets=()

usage() {
  cat <<'USAGE'
Usage:
  publish_to_github.sh --repo PATH --entry ENTRY.md [--asset FILE]... [--dest DIR] [--message MSG] [--branch BRANCH] [--no-push]
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="$2"; shift 2 ;;
    --entry)
      entry="$2"; shift 2 ;;
    --asset)
      assets+=("$2"); shift 2 ;;
    --dest)
      dest="$2"; shift 2 ;;
    --message)
      message="$2"; shift 2 ;;
    --branch)
      branch="$2"; shift 2 ;;
    --no-push)
      push="0"; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2 ;;
  esac
done

if [[ -z "$repo" || -z "$entry" ]]; then
  usage >&2
  exit 2
fi

if [[ ! -d "$repo/.git" ]]; then
  echo "Not a git repository: $repo" >&2
  exit 2
fi

if [[ ! -f "$entry" ]]; then
  echo "Entry not found: $entry" >&2
  exit 2
fi

cd "$repo"

if [[ -n "$branch" ]]; then
  if git show-ref --verify --quiet "refs/heads/$branch"; then
    git switch "$branch"
  else
    git switch -c "$branch"
  fi
fi

mkdir -p "$dest"
copied=()

entry_target="$dest/$(basename "$entry")"
cp "$entry" "$entry_target"
copied+=("$entry_target")

for asset in "${assets[@]}"; do
  if [[ ! -f "$asset" ]]; then
    echo "Asset not found: $asset" >&2
    exit 2
  fi
  asset_target="$dest/$(basename "$asset")"
  cp "$asset" "$asset_target"
  copied+=("$asset_target")
done

git add -- "${copied[@]}"

if git diff --cached --quiet; then
  echo "No diary changes to commit."
  exit 0
fi

if [[ -z "$message" ]]; then
  message="Add diary entry $(basename "$entry" .md)"
fi

git commit -m "$message"

if [[ "$push" == "1" ]]; then
  if git remote | grep -q .; then
    current_branch="$(git branch --show-current)"
    git push -u origin "$current_branch"
  else
    echo "Committed locally; push skipped because no git remote is configured."
  fi
else
  echo "Committed locally; push skipped by --no-push."
fi

echo "Published diary files:"
printf '  %s\n' "${copied[@]}"
