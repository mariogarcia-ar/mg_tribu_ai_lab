# Story 3.2: Detect and Notify Overdue Tasks

Status: ready-for-dev

## Story

As a user,
I want to see which tasks are past their deadline and still open,
so that I can take action on overdue work.

## Acceptance Criteria

1. Running `python todo.py notify-overdue` prints overdue tasks to console as "OVERDUE: [task title] — assigned to [user name]"
2. A task is overdue when: due_date < today AND status NOT IN TaskStatus.terminal_states()
3. Tasks with status DONE or CANCELLED are never reported as overdue
4. Tasks with due_date=None are never reported as overdue
5. If task has owner_id set, notification shows owner's name
6. If task has owner_id=None, notification falls back to created_by user's name

## Tasks / Subtasks

- [ ] Add `notify-overdue` subcommand to argparse (no args required) (AC: #1)
- [ ] Implement `notify_overdue()` function (AC: #1)
- [ ] Query tasks WHERE due_date < today AND due_date IS NOT NULL (AC: #2, #4)
- [ ] Filter results using `TaskStatus.terminal_states()` — NOT hardcoded strings (AC: #2, #3)
- [ ] JOIN users table to get name: COALESCE owner_id, created_by for user lookup (AC: #5, #6)
- [ ] Print formatted notification per overdue task (AC: #1)

## Dev Notes

- CRITICAL: Use `TaskStatus.terminal_states()` for the check — this is the key governance decision that prevents the E1 bug where terminal states were hardcoded in multiple places
- SQL approach: `SELECT t.*, u.name FROM tasks t JOIN users u ON u.id = COALESCE(t.owner_id, t.created_by) WHERE t.due_date IS NOT NULL AND t.due_date < date('now')`
- Then filter in Python: `if TaskStatus(row['status']) not in TaskStatus.terminal_states()`
- This is the culminating demo: the feature that caused the infinite loop in E1 works cleanly in E2

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 3.2]
- [Source: decisions.md - Due date y overdue, Estados terminales]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
