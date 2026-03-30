# Story 1.4: List Tasks Filtered by User

Status: ready-for-dev

## Story

As a user,
I want to see only the tasks I own or created,
so that I never see another user's private tasks.

## Acceptance Criteria

1. Running `python todo.py list-user 1` shows only tasks where owner_id=1 OR created_by=1
2. Tasks created by user 1 but owned by user 2 appear in both users' listings
3. No `list_all` command or function exists — every listing requires a user_id
4. If user_id argument is missing, argparse shows usage error

## Tasks / Subtasks

- [ ] Add `list-user` subcommand to argparse with required user_id arg (AC: #3, #4)
- [ ] Implement `list_tasks_for_user(user_id)` with SQL: `WHERE owner_id = ? OR created_by = ?` (AC: #1, #2)
- [ ] Format and print task list to console (id, title, status, priority, owner, due_date)
- [ ] Do NOT implement any list_all function (AC: #3)

## Dev Notes

- This is a critical governance decision: visibility is always scoped to a user
- SQL query: `SELECT * FROM tasks WHERE owner_id = ? OR created_by = ?` with user_id for both params
- Display status and priority using Enum names for readability
- Consider showing "[unassigned]" when owner_id is None

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 1.4]
- [Source: decisions.md - Visibilidad entre usuarios]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
