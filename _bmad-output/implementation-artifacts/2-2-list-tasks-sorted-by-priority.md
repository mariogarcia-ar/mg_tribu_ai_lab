# Story 2.2: List Tasks Sorted by Priority

Status: ready-for-dev

## Story

As a user,
I want my task list sorted by priority (highest first),
so that I see urgent tasks at the top.

## Acceptance Criteria

1. Running `python todo.py list-user 1` displays tasks sorted by priority descending (URGENT first, LOW last)
2. Sorting uses the integer value of TaskPriority, not alphabetical order of the name
3. Tasks without priority (NULL/default) sort after prioritized tasks

## Tasks / Subtasks

- [ ] Update `list_tasks_for_user()` SQL to add `ORDER BY priority DESC` (AC: #1, #2)
- [ ] Ensure priority display shows Enum name (e.g., "HIGH") not raw integer (AC: #1)
- [ ] Handle NULL priority in sort order (AC: #3)

## Dev Notes

- This modifies the existing `list_tasks_for_user()` from Story 1.4
- SQL: `ORDER BY COALESCE(priority, 0) DESC` — NULL priority treated as lowest
- Priority is stored as integer in DB, so `ORDER BY priority DESC` naturally gives correct order
- This is the key demo point: E1 sorted alphabetically (wrong), E2 sorts by integer (correct)

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 2.2]
- [Source: decisions.md - Prioridad, orden numérico]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
