# pre-compact.ps1 — Warns before context compact; instructs to use /clear instead
# Fires on PreCompact event. Exit code 2 = block with message.

Write-Error @"
BLOCKED: Do not use /compact — it is LOSSY (retains only 20-30% of context).

Instead:
  1. Write a CONTEXT SAVE block to PLANS.md
  2. Run: git commit -m "wip: context save"
  3. Use /clear (lossless — preserves all files, only clears conversation)
  4. In new session: load CLAUDE.md, SPEC.md, ERRORS.md, MEMORY_SEMANTIC.md, PLANS.md

See CONTEXT_BUDGET.md for full protocol.
"@

exit 2
