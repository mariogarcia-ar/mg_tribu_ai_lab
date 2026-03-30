# Story 1.2: User Creation via CLI

Status: ready-for-dev

## Story

As a user,
I want to create a user account with name and email,
so that I can own and manage tasks.

## Acceptance Criteria

1. Running `python todo.py create-user "Ana" "ana@example.com"` creates a user with auto-generated id, name "Ana", email "ana@example.com"
2. The user id is printed to console after creation
3. If name or email is empty, system prints an error and does not create the user
4. CLI subcommand `create-user` is added to argparse with positional args: name, email

## Tasks / Subtasks

- [ ] Add `create-user` subcommand to argparse with name and email args (AC: #4)
- [ ] Implement `create_user(name, email)` function that inserts into users table (AC: #1)
- [ ] Print user id after successful creation (AC: #2)
- [ ] Validate name and email are not empty before insert (AC: #3)

## Dev Notes

- Builds on Story 1.1: `users` table and argparse skeleton already exist
- No email format validation required — just non-empty check
- Use `cursor.lastrowid` to get the auto-generated id

### References

- [Source: _bmad-output/planning-artifacts/epics.md - Story 1.2]
- [Source: CLAUDE.md - Running examples]

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
