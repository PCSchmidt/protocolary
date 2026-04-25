#!/usr/bin/env bash
# block-dangerous.sh — Blocks destructive shell commands before execution
# Fires on PreToolUse (Bash tool). Exit code 2 = block with message.

COMMAND="${1:-}"

DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "git push --force origin main"
    "git push --force origin dev"
    "git reset --hard"
    "DROP DATABASE"
    "DROP TABLE"
    "db.dropDatabase()"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qF "$pattern"; then
        echo "BLOCKED: Dangerous command detected: '$pattern'. Review CLAUDE.md unbreakable rules." >&2
        exit 2
    fi
done

exit 0
