# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational laboratory ("Lab AI") that teaches AI-assisted development governance by contrasting two approaches through live-coding workshops. The central thesis: the advantage isn't in using AI, it's in using it without losing control.

- **Encuentro 1 (branch `encuentro1`):** Code-Centric anti-pattern — generate code fast, discover implicit decisions break things
- **Encuentro 2 (branch TBD):** System-Centric best practice — Think → Decide → Execute → Verify cycle with explicit `decisions.md`

## Stack

- Python (stdlib only: `sqlite3`, `argparse`)
- No external dependencies, no build system, no CI/CD
- SQLite for persistence
- Target output: a CLI TODO app (`todo.py`) built live during workshops

## Repository Structure

- `docs/encuentro1/readme.md` — Full runbook for Workshop 1 (4 stages)
- `docs/encuentro2/readme.md` — Full runbook for Workshop 2 (4 stages)
- `my-prompt.md` — Branch/feature planning notes
- Code files are generated during the workshops, not pre-existing

## Domain Model

**Task:** id, title, status (Enum: PENDING, IN_PROGRESS, BLOCKED, REVIEW, DONE, CANCELLED), priority (Enum: LOW=1, MEDIUM=2, HIGH=3, URGENT=4), user_id (optional owner), created_by, created_at, due_date (optional)

**User:** id, name, email

**Key rules (Encuentro 2):**
- Terminal states (DONE, CANCELLED) defined once in `TaskStatus.terminal_states()` — tasks in these states cannot be modified
- Users see only their own tasks (owner OR created_by); no `list_all()`
- Priority sorting uses integer enum values

## Language

Workshop documentation is in Spanish. Code identifiers and comments should follow whatever convention is established during the live session.
