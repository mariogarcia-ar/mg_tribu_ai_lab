# Story 2.1: Set Task Priority with Permissions

Status: ready-for-dev

## Story

As a user,
I want to set a priority level on my task,
so that I can indicate urgency using a consistent, sortable scale.

## Acceptance Criteria

1. Running `python todo.py set-priority 1 high 1` sets task 1 priority to HIGH (value=3)
2. If task is in terminal state, system prints error: task cannot be modified
3. If user has no permission (not owner or creator), system prints permission error
4. If priority string is invalid (not in TaskPriority), system prints error listing valid values

## Tasks / Subtasks

- [ ] Add `set-priority` subcommand to argparse with args: task_id, priority, user_id (AC: #1)
- [ ] Implement `set_priority(task_id, priority, user_id)` (AC: #1)
- [ ] Reuse permission + terminal state check pattern from Story 1.5 (AC: #2, #3)
- [ ] Validate priority string against TaskPriority Enum (AC: #4)
- [ ] Update priority in DB using IntEnum integer value (AC: #1)

## Dev Notes

- Same permission + terminal check pattern as Story 1.5 — consider extracting a helper if not already done
- Store `TaskPriority[priority_string.upper()].value` (the integer) in DB
- Use `TaskPriority[name]` to convert CLI input, catch KeyError for invalid

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 2.1]
- [Source: decisions.md - Prioridad]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
