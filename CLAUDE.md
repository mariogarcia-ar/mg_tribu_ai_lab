# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Educational laboratory ("Lab AI") that teaches AI-assisted development governance through live-coding workshops. Central thesis: the advantage isn't in using AI — it's in using it without losing control.

This is **Encuentro 2** (branch `encuentro2`) — the System-Centric approach using the Think/Decide/Execute/Verify cycle.

## Stack

- Python (stdlib only: `sqlite3`, `argparse`, `enum`, `datetime`)
- No external dependencies, no build system, no CI/CD
- SQLite for persistence
- CLI TODO app (`todo.py`) governed by `decisions.md`

## Repository Structure

- `decisions.md` — **The contract.** All code must respect this file. If code violates a decision, it gets rejected.
- `todo.py` — CLI TODO app built following decisions.md
- `demo.sh` — Interactive demo showing protections vs E1 bugs
- `docs/encuentro1/readme.md` — Runbook for Workshop 1 (Code-Centric anti-pattern)
- `docs/encuentro2/readme.md` — Runbook for Workshop 2 (System-Centric)

## Key Rules (from decisions.md)

1. **Status and Priority are Enums** — never raw strings. `TaskStatus` and `TaskPriority` are the single source of truth.
2. **Terminal states** (`DONE`, `CANCELLED`) are defined in `TaskStatus.terminal_states()` — tasks in these states cannot be modified.
3. **No `list_all`** — every listing requires an explicit `user_id`. Users only see tasks where they are `owner_id` or `created_by`.
4. **Every mutation requires `user_id`** — the system always checks permissions (owner or creator).
5. **Task sharing is NOT implemented** — explicit decision, not an oversight.
6. **Priority sorting uses integer values** — `TaskPriority(IntEnum)` with LOW=1, MEDIUM=2, HIGH=3, URGENT=4.
7. **Overdue detection** uses `TaskStatus.terminal_states()`, not hardcoded strings.

## Running

```bash
# Run the demo
bash demo.sh

# Individual commands
python todo.py create-user "Ana" "ana@example.com"
python todo.py add "My task" 1              # created_by = user 1
python todo.py list-user 1
python todo.py update 1 in_progress 1       # task_id, status, user_id
python todo.py set-priority 1 high 1
python todo.py set-due 1 2026-04-15 1
python todo.py notify-overdue
```

## Language

Workshop documentation is in Spanish. Code uses English identifiers.
