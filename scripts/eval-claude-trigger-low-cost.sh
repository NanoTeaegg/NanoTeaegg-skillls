#!/usr/bin/env bash
set -euo pipefail

# Claude Code-specific trigger eval.
# This checks whether Claude CLI (`claude -p`) would invoke a skill from its
# description. It does not represent Cursor or Codex trigger behavior.

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <eval-set-json> <skill-path> [model]" >&2
  echo "Example: $0 evals/Development/requirements-definition/trigger-eval.json skills/Development/requirements-definition" >&2
  echo "Example with model override: $0 evals/Development/requirements-definition/trigger-eval.json skills/Development/requirements-definition sonnet" >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_CREATOR_ROOT="/Users/teaegg/.agents/skills/skill-creator"

EVAL_SET="$1"
SKILL_PATH="$2"
MODEL="${3:-}"

if [[ "$EVAL_SET" != /* ]]; then
  EVAL_SET="$REPO_ROOT/$EVAL_SET"
fi

if [[ "$SKILL_PATH" != /* ]]; then
  SKILL_PATH="$REPO_ROOT/$SKILL_PATH"
fi

cd "$SKILL_CREATOR_ROOT"

CMD=(
  python3 -m scripts.run_eval
  --eval-set "$EVAL_SET"
  --skill-path "$SKILL_PATH"
  --runs-per-query 1
  --verbose
)

if [[ -n "$MODEL" ]]; then
  CMD+=(--model "$MODEL")
fi

"${CMD[@]}"
