# session-start.ps1 — Prints session initialization checklist at session start
# Fires on SessionStart event.

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

Write-Output @"
=== TRANSCELERATE SESSION START [$timestamp] ===

Load these files before doing any work:
  1. CLAUDE.md       — behavioral rules and gates
  2. SPEC.md         — scope lock (check before accepting any task)
  3. ERRORS.md       — check FIRST before diagnosing any error
  4. MEMORY_SEMANTIC.md — USDM domain knowledge
  5. PLANS.md        — current context save state and pending work

Current gate: Check VERSION_ROADMAP.md
Context budget: Check CONTEXT_BUDGET.md (warn at 40%, stop at 50%)

Type /context-check for current token usage.
=================================================
"@

exit 0
