# CONTEXT_BUDGET.md — Transcelerate | Context Management Rules

## The Problem

Claude's context window degrades with load. Auto-compaction fires at ~83.5% and is LOSSY —
it retains only 20-30% of details. Losing domain context mid-gate causes regressions, re-work,
and inconsistent code. This file defines the protocol to prevent that.

## Critical Thresholds

| Level | Approx Tokens | Action Required |
|---|---|---|
| 40% (~80K) | Warning | Save PLANS.md; finish current sub-task; do not start new sub-task |
| 50% (~100K) | Stop | Save state, commit, use `/clear`, resume with `/start` |
| 83.5% (~167K) | Auto-compact fires | LOSSY — avoid reaching this level |

Use `/context-check` at any time for current token usage.

## Always-Loaded Files (load every session, ~3,000–4,000 tokens)

1. `CLAUDE.md` — behavioral rules and gates
2. `SPEC.md` — scope lock
3. `ERRORS.md` — failure log (check before diagnosing)
4. `MEMORY_SEMANTIC.md` — USDM domain knowledge and patterns
5. `PLANS.md` — current context save state

**Total always-loaded budget: ~4K tokens. Leave the rest for working context.**

## On-Demand Files (load only when actively working in that domain)

| File | Load When |
|---|---|
| `DECISIONS.md` | Architectural question arises; evaluating tradeoffs |
| `MEMORY_CORRECTIONS.md` | Estimating task duration; choosing approach |
| `MEMORY_EPISODIC.md` | Checking recent gate history or session log |
| `VERSION_ROADMAP.md` | Starting or closing a gate |
| `TESTS.md` | Writing tests or reviewing coverage |
| `DEPLOYMENT_CONFIG.md` | Touching Docker, environment variables, or CI |
| `API_REGISTRY.md` | Adding or modifying an API endpoint |
| `DEMO_CHECKS.md` | Working on Streamlit dashboard |
| `Research/*.md` | Background questions about USDM or market |

## Context Save Protocol (before `/clear`)

1. Write CONTEXT SAVE block to `PLANS.md`:
   - Current gate and sub-task
   - Completed items this session
   - Pending tasks (ordered by priority)
   - Test count
   - Any decisions made or errors encountered
2. Commit: `git commit -m "wip: context save at [gate]"`
3. Run `/clear` (lossless — preserves all files; only clears conversation history)
4. In new session: load always-loaded files, read PLANS.md latest save

## Large Gate Strategy

If a gate is estimated at 3+ hours:
- Split into sub-gates labeled Gate Xa and Gate Xb
- Update VERSION_ROADMAP.md before starting
- Each sub-gate gets its own approval confirmation (not a formal approval word, but
  an explicit "ready to continue to Gate Xb?")
- Context save between sub-gates regardless of token level

## Never Use `/compact`

`/compact` is lossy. It summarizes the conversation and discards details.
Always use `/clear` instead. `/clear` only clears the conversation window;
all files on disk (including PLANS.md) are preserved and reloaded in the next session.
