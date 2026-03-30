# Story 1.1: Create decisions.md and Initialize Database Schema

Status: ready-for-dev

## Story

As an instructor,
I want the governance contract and database schema established before any feature code,
so that all subsequent code respects explicit design decisions.

## Acceptance Criteria

1. `decisions.md` exists at project root with rules for: status enum values, terminal states, priority enum with integer values, visibility (no list_all), ownership (created_by required, owner_id optional), and task sharing (explicitly out of scope)
2. `todo.py` is created with sqlite3 database initialization creating `users` table (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL) and `tasks` table (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'PENDING', priority INTEGER DEFAULT 2, owner_id INTEGER, created_by INTEGER NOT NULL, due_date TEXT, created_at TEXT NOT NULL, FOREIGN KEY owner_id → users(id), FOREIGN KEY created_by → users(id))
3. `TaskStatus` Enum is defined with members: PENDING, IN_PROGRESS, BLOCKED, REVIEW, DONE, CANCELLED
4. `TaskStatus` includes a `terminal_states()` classmethod returning `{DONE, CANCELLED}`
5. `TaskPriority` IntEnum is defined with LOW=1, MEDIUM=2, HIGH=3, URGENT=4
6. Database tables are created via `init_db()` function using `CREATE TABLE IF NOT EXISTS`

## Tasks / Subtasks

- [ ] Create `decisions.md` with all governance rules (AC: #1)
- [ ] Create `todo.py` with imports: sqlite3, argparse, enum, datetime (AC: #2)
- [ ] Define `TaskStatus(Enum)` with 6 states and `terminal_states()` classmethod (AC: #3, #4)
- [ ] Define `TaskPriority(IntEnum)` with 4 levels (AC: #5)
- [ ] Implement `init_db()` creating users and tasks tables (AC: #6)
- [ ] Add `if __name__ == '__main__'` with argparse skeleton (AC: #2)

## Dev Notes

- Python stdlib only: sqlite3, argparse, enum, datetime
- Single file: `todo.py` — all code lives here
- Store Enum `.value` in DB (the string name for status, integer for priority)
- `terminal_states()` returns a set, not a list — enables `status in TaskStatus.terminal_states()`
- This is a teaching lab: keep code clear and readable, no clever abstractions
- decisions.md is written in Spanish (workshop docs language), code identifiers in English

### Project Structure Notes

- `todo.py` at project root
- `decisions.md` at project root
- SQLite DB file: `todo.db` (created at runtime)

### References

- [Source: idea.md - Funcionalidades core]
- [Source: CLAUDE.md - Key Rules]
- [Source: _bmad-output/planning-artifacts/epics.md - Story 1.1]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
