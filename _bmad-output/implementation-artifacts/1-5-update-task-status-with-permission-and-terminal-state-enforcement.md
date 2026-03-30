# Story 1.5: Update Task Status with Permission and Terminal State Enforcement

Status: ready-for-dev

## Story

As a user,
I want to change a task's status only if I have permission and the task is not in a terminal state,
so that completed or cancelled tasks remain immutable.

## Acceptance Criteria

1. Running `python todo.py update 1 in_progress 1` updates task 1 status to IN_PROGRESS when user 1 is owner or creator
2. If task is in terminal state (DONE or CANCELLED), system prints error: task cannot be modified
3. If user is neither owner nor creator, system prints permission error
4. If status string is invalid (not in TaskStatus), system prints error listing valid values
5. Terminal state check uses `TaskStatus.terminal_states()`, not hardcoded strings

## Tasks / Subtasks

- [ ] Add `update` subcommand to argparse with args: task_id, status, user_id (AC: #1)
- [ ] Implement `update_task_status(task_id, status, user_id)` (AC: #1)
- [ ] Validate status string against TaskStatus Enum — reject invalid values with helpful message (AC: #4)
- [ ] Check task current status against `TaskStatus.terminal_states()` — block if terminal (AC: #2, #5)
- [ ] Check user permission: user must be owner_id or created_by (AC: #3)
- [ ] Update status in DB using Enum value (AC: #1)

## Dev Notes

- Permission check pattern: load task, verify `user_id in (task.owner_id, task.created_by)`
- Terminal state check: `TaskStatus(current_status) in TaskStatus.terminal_states()`
- Use `TaskStatus[status_string.upper()]` to convert CLI input to Enum (catch KeyError for invalid)
- This permission + terminal check pattern will be reused in Stories 2.1 and 3.1

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 1.5]
- [Source: decisions.md - Estados terminales, Permisos]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
