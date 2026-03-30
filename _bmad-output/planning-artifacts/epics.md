---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-mg_tribu_ai_lab.md
  - _bmad-output/planning-artifacts/product-brief-mg_tribu_ai_lab-distillate.md
  - idea.md
  - CLAUDE.md
mode: autonomous
---

# mg_tribu_ai_lab - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for the MG TRIBU AI Lab TODO app — the teaching vehicle used in Encuentro 2 (System-Centric approach). The app is a CLI TODO system with multi-user support, governed by `decisions.md`, built with Python stdlib only.

## Requirements Inventory

### Functional Requirements

FR1: System shall allow creating users with id, name, and email
FR2: System shall allow creating tasks with title and mandatory created_by (user_id)
FR3: Task status shall be a Python Enum with values: PENDING, IN_PROGRESS, BLOCKED, REVIEW, DONE, CANCELLED
FR4: Terminal states (DONE, CANCELLED) shall be defined in TaskStatus.terminal_states() — no transitions allowed out of these states
FR5: Task priority shall be a Python IntEnum with LOW=1, MEDIUM=2, HIGH=3, URGENT=4
FR6: System shall allow setting/updating task priority with permission check
FR7: Task owner_id shall be optional — None means "unassigned" (valid state, not error)
FR8: Listing tasks shall always require an explicit user_id — returns tasks where owner_id = user_id OR created_by = user_id. No list_all function.
FR9: Every task mutation shall require user_id and verify permissions (user must be owner or creator)
FR10: Tasks shall have an optional due_date — None means no deadline, never overdue
FR11: A task is overdue when due_date < today AND status NOT IN terminal_states
FR12: Overdue notification shall print to console, notifying owner_id; if None, notify created_by

### NonFunctional Requirements

NFR1: Python stdlib only — sqlite3, argparse, enum, datetime. No external dependencies.
NFR2: Single file implementation (todo.py)
NFR3: CLI interface using argparse
NFR4: SQLite database for persistence
NFR5: Enum values stored in DB — never raw strings
NFR6: Code identifiers in English, workshop docs in Spanish

### Additional Requirements

- decisions.md must be created before any code, documenting all design decisions
- The Enum definition is the single source of truth for valid states
- Priority sorting uses integer values (ORDER BY priority_value DESC), not string names
- Schema migrations must handle nullable columns with DEFAULT NULL
- No task sharing between users (explicit non-decision)

### UX Design Requirements

N/A — CLI application, no UI design document.

### FR Coverage Map

FR1: Epic 1 - User creation
FR2: Epic 1 - Task creation with creator
FR3: Epic 1 - Task status as Enum
FR4: Epic 1 - Terminal states enforcement
FR5: Epic 2 - Priority as IntEnum
FR6: Epic 2 - Set priority with permissions
FR7: Epic 1 - Optional owner_id
FR8: Epic 1 - List tasks filtered by user
FR9: Epic 1 - Permission-checked mutations
FR10: Epic 3 - Optional due_date
FR11: Epic 3 - Overdue detection logic
FR12: Epic 3 - Overdue notification output

## Epic List

### Epic 1: Task & User Management Foundation
Users can create accounts, create tasks, update task status, and list their own tasks — with proper lifecycle enforcement and permission checks.
**FRs covered:** FR1, FR2, FR3, FR4, FR7, FR8, FR9

### Epic 2: Task Prioritization
Users can assign and update priority levels on their tasks, and view tasks sorted by priority.
**FRs covered:** FR5, FR6

### Epic 3: Due Dates & Overdue Notifications
Users can set deadlines on tasks and the system detects and reports overdue tasks.
**FRs covered:** FR10, FR11, FR12

---

## Epic 1: Task & User Management Foundation

Users can create accounts, create and manage tasks with enforced lifecycle states, and list only their own tasks — with permissions verified on every mutation.

### Story 1.1: Create decisions.md and initialize database schema

As an instructor,
I want the governance contract and database schema established before any feature code,
So that all subsequent code respects explicit design decisions.

**Acceptance Criteria:**

**Given** the project has no existing code
**When** I create decisions.md with status enum, terminal states, priority, visibility, and ownership rules
**Then** the document exists and defines all rules that code must respect
**And** todo.py is initialized with sqlite3 database creation (tasks and users tables)
**And** TaskStatus Enum is defined with PENDING, IN_PROGRESS, BLOCKED, REVIEW, DONE, CANCELLED
**And** TaskPriority IntEnum is defined with LOW=1, MEDIUM=2, HIGH=3, URGENT=4
**And** TaskStatus includes a terminal_states() classmethod returning {DONE, CANCELLED}

### Story 1.2: User creation via CLI

As a user,
I want to create a user account with name and email,
So that I can own and manage tasks.

**Acceptance Criteria:**

**Given** the database is initialized
**When** I run `python todo.py create-user "Ana" "ana@example.com"`
**Then** a new user is created with an auto-generated id, name "Ana", and email "ana@example.com"
**And** the user id is printed to the console

**Given** I attempt to create a user
**When** name or email is empty
**Then** the system prints an error and does not create the user

### Story 1.3: Task creation with creator ownership

As a user,
I want to create a task assigned to my user id as creator,
So that the system tracks who originated each task.

**Acceptance Criteria:**

**Given** user with id=1 exists
**When** I run `python todo.py add "My task" 1`
**Then** a task is created with title "My task", created_by=1, owner_id=None, status=PENDING
**And** status is stored as the Enum value in the DB, not a raw string
**And** the task id is printed to the console

**Given** user_id does not exist
**When** I run `python todo.py add "Task" 999`
**Then** the system prints an error and does not create the task

### Story 1.4: List tasks filtered by user

As a user,
I want to see only the tasks I own or created,
So that I never see another user's private tasks.

**Acceptance Criteria:**

**Given** user 1 created task A and user 2 created task B
**When** I run `python todo.py list-user 1`
**Then** only task A is displayed (not task B)

**Given** user 1 created task A and task A has owner_id=2
**When** I run `python todo.py list-user 1`
**Then** task A is displayed (because user 1 is the creator)
**And** when I run `python todo.py list-user 2`, task A is also displayed (because user 2 is the owner)

**Given** no list_all command exists
**When** I attempt any listing without a user_id
**Then** the system requires a user_id argument

### Story 1.5: Update task status with permission and terminal state enforcement

As a user,
I want to change a task's status only if I have permission and the task is not in a terminal state,
So that completed or cancelled tasks remain immutable.

**Acceptance Criteria:**

**Given** task 1 exists with status PENDING and user 1 is the creator
**When** I run `python todo.py update 1 in_progress 1`
**Then** task status is updated to IN_PROGRESS

**Given** task 1 has status DONE (terminal state)
**When** I run `python todo.py update 1 pending 1`
**Then** the system prints an error: task is in a terminal state and cannot be modified

**Given** user 3 is neither owner nor creator of task 1
**When** I run `python todo.py update 1 in_progress 3`
**Then** the system prints a permission error

**Given** I provide an invalid status string (e.g., "completed")
**When** I run `python todo.py update 1 completed 1`
**Then** the system prints an error listing valid status values from the Enum

---

## Epic 2: Task Prioritization

Users can assign priority levels to their tasks and view tasks sorted by priority using integer-based ordering.

### Story 2.1: Set task priority with permissions

As a user,
I want to set a priority level on my task,
So that I can indicate urgency using a consistent, sortable scale.

**Acceptance Criteria:**

**Given** task 1 exists and user 1 is the creator
**When** I run `python todo.py set-priority 1 high 1`
**Then** task priority is set to HIGH (value=3)

**Given** task 1 is in a terminal state (DONE or CANCELLED)
**When** I run `python todo.py set-priority 1 high 1`
**Then** the system prints an error: task is in a terminal state and cannot be modified

**Given** user 2 has no permission on task 1
**When** I run `python todo.py set-priority 1 high 2`
**Then** the system prints a permission error

**Given** I provide an invalid priority (e.g., "critical")
**When** I run `python todo.py set-priority 1 critical 1`
**Then** the system prints an error listing valid priority values

### Story 2.2: List tasks sorted by priority

As a user,
I want my task list sorted by priority (highest first),
So that I see urgent tasks at the top.

**Acceptance Criteria:**

**Given** user 1 has tasks with priorities URGENT, LOW, HIGH
**When** I run `python todo.py list-user 1`
**Then** tasks are displayed in order: URGENT (4), HIGH (3), LOW (1)
**And** sorting uses the integer value, not alphabetical order of the name

---

## Epic 3: Due Dates & Overdue Notifications

Users can set optional deadlines on tasks, and the system detects and reports tasks that are past due.

### Story 3.1: Set due date on tasks

As a user,
I want to set an optional due date on my task,
So that I can track deadlines.

**Acceptance Criteria:**

**Given** task 1 exists and user 1 has permission
**When** I run `python todo.py set-due 1 2026-04-15 1`
**Then** task due_date is set to 2026-04-15

**Given** task 1 is in a terminal state
**When** I run `python todo.py set-due 1 2026-04-15 1`
**Then** the system prints an error: task is in a terminal state

**Given** task 1 has no due_date set
**When** I query the task
**Then** due_date is None — this is valid, not an error

**Given** user provides an invalid date format
**When** I run `python todo.py set-due 1 "april 15" 1`
**Then** the system prints an error with the expected format (YYYY-MM-DD)

### Story 3.2: Detect and notify overdue tasks

As a user,
I want to see which tasks are past their deadline and still open,
So that I can take action on overdue work.

**Acceptance Criteria:**

**Given** task 1 has due_date=2026-03-01 and status=PENDING (today is 2026-03-30)
**When** I run `python todo.py notify-overdue`
**Then** the console prints "OVERDUE: [task title] — assigned to [user name]"

**Given** task 2 has due_date=2026-03-01 and status=DONE
**When** I run `python todo.py notify-overdue`
**Then** task 2 is NOT reported as overdue (terminal state check uses TaskStatus.terminal_states())

**Given** task 3 has due_date=None
**When** I run `python todo.py notify-overdue`
**Then** task 3 is NOT reported as overdue (no deadline = never overdue)

**Given** task 4 has owner_id=None and created_by=1
**When** task 4 is overdue
**Then** notification shows the name of user 1 (created_by fallback)

**Given** task 5 has owner_id=2
**When** task 5 is overdue
**Then** notification shows the name of user 2 (owner takes precedence)
