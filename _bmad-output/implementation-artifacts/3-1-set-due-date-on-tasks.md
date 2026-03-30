# Story 3.1: Set Due Date on Tasks

Status: ready-for-dev

## Story

As a user,
I want to set an optional due date on my task,
so that I can track deadlines.

## Acceptance Criteria

1. Running `python todo.py set-due 1 2026-04-15 1` sets task 1 due_date to 2026-04-15
2. If task is in terminal state, system prints error: task cannot be modified
3. Tasks with no due_date (None) are valid — not an error
4. If user provides invalid date format, system prints error with expected format (YYYY-MM-DD)
5. Permission check: user must be owner or creator

## Tasks / Subtasks

- [ ] Add `set-due` subcommand to argparse with args: task_id, due_date, user_id (AC: #1)
- [ ] Implement `set_due_date(task_id, due_date, user_id)` (AC: #1)
- [ ] Reuse permission + terminal state check pattern (AC: #2, #5)
- [ ] Validate date format with `datetime.datetime.strptime(date_str, '%Y-%m-%d')` (AC: #4)
- [ ] Update due_date in DB as ISO string (AC: #1)

## Dev Notes

- due_date column already exists from Story 1.1 schema (nullable TEXT)
- Same permission + terminal check pattern as Stories 1.5 and 2.1
- Store date as ISO string: `YYYY-MM-DD`
- None means "no deadline" — this is semantically valid, not missing data

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 3.1]
- [Source: decisions.md - Due date y overdue]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
