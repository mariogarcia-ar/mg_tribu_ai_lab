# Story 1.3: Task Creation with Creator Ownership

Status: ready-for-dev

## Story

As a user,
I want to create a task assigned to my user id as creator,
so that the system tracks who originated each task.

## Acceptance Criteria

1. Running `python todo.py add "My task" 1` creates a task with title="My task", created_by=1, owner_id=None, status=PENDING
2. Status is stored as the Enum value string in the DB (e.g., "PENDING"), not a raw arbitrary string
3. The task id is printed to console after creation
4. If user_id does not exist in users table, system prints an error and does not create the task

## Tasks / Subtasks

- [ ] Add `add` subcommand to argparse with args: title, created_by (AC: #1)
- [ ] Implement `add_task(title, created_by)` that validates user exists (AC: #4)
- [ ] Insert task with status=TaskStatus.PENDING.value, owner_id=None, created_at=now (AC: #1, #2)
- [ ] Print task id after creation (AC: #3)

## Dev Notes

- `created_by` is mandatory, `owner_id` defaults to None (unassigned = valid state)
- Store `TaskStatus.PENDING.value` in DB — the Enum name string
- Use `datetime.datetime.now().isoformat()` for created_at
- Validate user exists before insert: query users table by id

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 1.3]
- [Source: decisions.md - Tareas sin dueño]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
