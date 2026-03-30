#!/usr/bin/env python3
"""
TODO App — Encuentro 2 (System-Centric)
Código gobernado por decisions.md
"""
import sqlite3
import argparse
from enum import Enum, IntEnum
from datetime import datetime, date

DB_NAME = "todo.db"


# ── Enums: única fuente de verdad para estados y prioridades ──


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"

    @classmethod
    def terminal_states(cls):
        return {cls.DONE, cls.CANCELLED}


class TaskPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


# ── Database ──


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            priority_value INTEGER NOT NULL DEFAULT 2,
            created_at TEXT NOT NULL,
            due_date TEXT DEFAULT NULL,
            owner_id INTEGER,
            created_by INTEGER NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )"""
    )
    conn.commit()
    return conn


# ── Helpers ──


def _check_access(conn, task_id, user_id):
    """Verifica que el usuario tiene acceso a la tarea (owner o creator)."""
    task = conn.execute(
        "SELECT owner_id, created_by, status FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    if not task:
        raise ValueError(f"Task {task_id} not found.")
    if task[0] != user_id and task[1] != user_id:
        raise PermissionError(
            f"User {user_id} does not have access to task {task_id}."
        )
    return task


def _check_not_terminal(status_str):
    """Verifica que la tarea no está en estado terminal."""
    status = TaskStatus(status_str)
    if status in TaskStatus.terminal_states():
        raise ValueError(
            f"Task is in terminal state '{status.value}'. No modifications allowed."
        )


# ── Users ──


def create_user(name, email):
    conn = get_connection()
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    print(f"User created: {name} ({email})")


# ── Tasks ──


def create_task(title, created_by):
    conn = get_connection()
    user = conn.execute(
        "SELECT id FROM users WHERE id = ?", (created_by,)
    ).fetchone()
    if not user:
        print(f"User {created_by} not found.")
        conn.close()
        return
    conn.execute(
        "INSERT INTO tasks (title, status, priority_value, created_at, created_by) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            title,
            TaskStatus.PENDING.value,
            TaskPriority.MEDIUM.value,
            datetime.now().isoformat(),
            created_by,
        ),
    )
    conn.commit()
    conn.close()
    print(f"Task created: {title} (by user {created_by})")


def list_tasks_for_user(user_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT id, title, status, priority_value, created_at, due_date, owner_id, created_by
           FROM tasks
           WHERE owner_id = ? OR created_by = ?""",
        (user_id, user_id),
    ).fetchall()
    conn.close()
    if not rows:
        print(f"No tasks found for user {user_id}.")
        return
    for row in rows:
        status = TaskStatus(row[2]).name
        priority = TaskPriority(row[3]).name
        owner = f"owner={row[6]}" if row[6] else "unassigned"
        due = f" due={row[5]}" if row[5] else ""
        print(
            f"[{row[0]}] {row[1]} ({status}) priority={priority} "
            f"{owner} created_by={row[7]}{due}"
        )


def update_status(task_id, status_str, user_id):
    # Validar que el status es un Enum válido
    try:
        new_status = TaskStatus(status_str)
    except ValueError:
        valid = ", ".join(s.value for s in TaskStatus)
        print(f"Invalid status '{status_str}'. Must be one of: {valid}")
        return

    conn = get_connection()
    try:
        task = _check_access(conn, task_id, user_id)
        _check_not_terminal(task[2])
        conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (new_status.value, task_id)
        )
        conn.commit()
        print(f"Task {task_id} updated to '{new_status.value}' by user {user_id}.")
    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def delete_task(task_id, user_id):
    conn = get_connection()
    try:
        _check_access(conn, task_id, user_id)
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        print(f"Task {task_id} deleted by user {user_id}.")
    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def assign_task_to_user(task_id, owner_id, user_id):
    conn = get_connection()
    try:
        task = _check_access(conn, task_id, user_id)
        _check_not_terminal(task[2])
        # Verificar que el nuevo owner existe
        user = conn.execute(
            "SELECT id FROM users WHERE id = ?", (owner_id,)
        ).fetchone()
        if not user:
            print(f"User {owner_id} not found.")
            return
        conn.execute(
            "UPDATE tasks SET owner_id = ? WHERE id = ?", (owner_id, task_id)
        )
        conn.commit()
        print(f"Task {task_id} assigned to user {owner_id}.")
    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def set_priority(task_id, priority_str, user_id):
    # Validar que la prioridad es un Enum válido
    try:
        priority = TaskPriority[priority_str.upper()]
    except KeyError:
        valid = ", ".join(p.name.lower() for p in TaskPriority)
        print(f"Invalid priority '{priority_str}'. Must be one of: {valid}")
        return

    conn = get_connection()
    try:
        task = _check_access(conn, task_id, user_id)
        _check_not_terminal(task[2])
        conn.execute(
            "UPDATE tasks SET priority_value = ? WHERE id = ?",
            (priority.value, task_id),
        )
        conn.commit()
        print(f"Task {task_id} priority set to '{priority.name.lower()}' by user {user_id}.")
    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def list_tasks_by_priority(user_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT id, title, status, priority_value, created_at
           FROM tasks
           WHERE owner_id = ? OR created_by = ?
           ORDER BY priority_value DESC""",
        (user_id, user_id),
    ).fetchall()
    conn.close()
    if not rows:
        print(f"No tasks found for user {user_id}.")
        return
    for row in rows:
        status = TaskStatus(row[2]).name
        priority = TaskPriority(row[3]).name
        print(f"[{row[0]}] {row[1]} ({status}) priority={priority} - {row[4]}")


def set_due_date(task_id, due_date, user_id):
    # Validar formato de fecha
    try:
        date.fromisoformat(due_date)
    except ValueError:
        print(f"Invalid date format '{due_date}'. Use YYYY-MM-DD.")
        return

    conn = get_connection()
    try:
        task = _check_access(conn, task_id, user_id)
        _check_not_terminal(task[2])
        conn.execute(
            "UPDATE tasks SET due_date = ? WHERE id = ?", (due_date, task_id)
        )
        conn.commit()
        print(f"Task {task_id} due date set to {due_date} by user {user_id}.")
    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def notify_overdue():
    conn = get_connection()
    terminal_values = [s.value for s in TaskStatus.terminal_states()]
    placeholders = ", ".join("?" for _ in terminal_values)
    rows = conn.execute(
        f"""SELECT t.id, t.title, t.status, t.due_date, t.owner_id, t.created_by,
                   u_owner.name as owner_name, u_creator.name as creator_name
           FROM tasks t
           LEFT JOIN users u_owner ON t.owner_id = u_owner.id
           LEFT JOIN users u_creator ON t.created_by = u_creator.id
           WHERE t.due_date IS NOT NULL
             AND t.status NOT IN ({placeholders})""",
        terminal_values,
    ).fetchall()
    conn.close()

    today = date.today().isoformat()
    found = False
    for row in rows:
        if row[3] < today:
            found = True
            # Notificar a owner_id; si es None, fallback a created_by
            if row[4] is not None:
                notify_name = row[6] or f"user {row[4]}"
            else:
                notify_name = row[7] or f"user {row[5]}"
            status = TaskStatus(row[2]).name
            print(
                f"OVERDUE: [{row[0]}] {row[1]} ({status}) "
                f"due={row[3]} — assigned to {notify_name}"
            )
    if not found:
        print("No overdue tasks.")


# ── CLI ──


def main():
    parser = argparse.ArgumentParser(description="TODO App — System-Centric (E2)")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Create a new task")
    add_p.add_argument("title", help="Task title")
    add_p.add_argument("created_by", type=int, help="Creator user ID")

    list_p = sub.add_parser("list-user", help="List tasks for a user")
    list_p.add_argument("user_id", type=int, help="User ID")

    upd_p = sub.add_parser("update", help="Update task status")
    upd_p.add_argument("task_id", type=int, help="Task ID")
    upd_p.add_argument("status", help="New status")
    upd_p.add_argument("user_id", type=int, help="User ID")

    del_p = sub.add_parser("delete", help="Delete a task")
    del_p.add_argument("task_id", type=int, help="Task ID")
    del_p.add_argument("user_id", type=int, help="User ID")

    user_p = sub.add_parser("create-user", help="Create a new user")
    user_p.add_argument("name", help="User name")
    user_p.add_argument("email", help="User email")

    assign_p = sub.add_parser("assign", help="Assign a task to a user")
    assign_p.add_argument("task_id", type=int, help="Task ID")
    assign_p.add_argument("owner_id", type=int, help="New owner user ID")
    assign_p.add_argument("user_id", type=int, help="Your user ID")

    prio_p = sub.add_parser("set-priority", help="Set task priority")
    prio_p.add_argument("task_id", type=int, help="Task ID")
    prio_p.add_argument("priority", help="Priority: low, medium, high, urgent")
    prio_p.add_argument("user_id", type=int, help="User ID")

    lprio_p = sub.add_parser("list-by-priority", help="List tasks sorted by priority")
    lprio_p.add_argument("user_id", type=int, help="User ID")

    due_p = sub.add_parser("set-due", help="Set task due date")
    due_p.add_argument("task_id", type=int, help="Task ID")
    due_p.add_argument("due_date", help="Due date (YYYY-MM-DD)")
    due_p.add_argument("user_id", type=int, help="User ID")

    sub.add_parser("notify-overdue", help="Notify overdue tasks")

    args = parser.parse_args()

    if args.command == "add":
        create_task(args.title, args.created_by)
    elif args.command == "list-user":
        list_tasks_for_user(args.user_id)
    elif args.command == "update":
        update_status(args.task_id, args.status, args.user_id)
    elif args.command == "delete":
        delete_task(args.task_id, args.user_id)
    elif args.command == "create-user":
        create_user(args.name, args.email)
    elif args.command == "assign":
        assign_task_to_user(args.task_id, args.owner_id, args.user_id)
    elif args.command == "set-priority":
        set_priority(args.task_id, args.priority, args.user_id)
    elif args.command == "list-by-priority":
        list_tasks_by_priority(args.user_id)
    elif args.command == "set-due":
        set_due_date(args.task_id, args.due_date, args.user_id)
    elif args.command == "notify-overdue":
        notify_overdue()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
