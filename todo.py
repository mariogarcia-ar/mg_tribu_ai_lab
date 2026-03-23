#!/usr/bin/env python3
import sqlite3
import argparse
from datetime import datetime

DB_NAME = "todo.db"
VALID_STATUSES = ["pending", "in_progress", "blocked", "review", "done", "cancelled"]


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
            priority TEXT DEFAULT 'medium',
            created_at TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS shared_tasks (
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (task_id, user_id),
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
    )
    conn.commit()
    return conn


def create_task(title):
    conn = get_connection()
    conn.execute(
        "INSERT INTO tasks (title, status, created_at) VALUES (?, 'pending', ?)",
        (title, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    print(f"Task created: {title}")


def list_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT id, title, status, created_at FROM tasks").fetchall()
    conn.close()
    if not rows:
        print("No tasks found.")
        return
    for row in rows:
        print(f"[{row[0]}] {row[1]} ({row[2]}) - {row[3]}")


def update_status(task_id, status):
    if status not in VALID_STATUSES:
        print(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        return
    conn = get_connection()
    cursor = conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        print(f"Task {task_id} not found.")
    else:
        print(f"Task {task_id} updated to '{status}'.")


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        print(f"Task {task_id} not found.")
    else:
        print(f"Task {task_id} deleted.")


def create_user(name, email):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email),
    )
    conn.commit()
    conn.close()
    print(f"User created: {name} ({email})")


def assign_task_to_user(task_id, user_id):
    conn = get_connection()
    user = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        print(f"User {user_id} not found.")
        conn.close()
        return
    cursor = conn.execute("UPDATE tasks SET user_id = ? WHERE id = ?", (user_id, task_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        print(f"Task {task_id} not found.")
    else:
        print(f"Task {task_id} assigned to user {user_id}.")


def list_tasks_by_user(user_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT id, title, status, created_at, 'owner' as role FROM tasks WHERE user_id = ?
           UNION
           SELECT t.id, t.title, t.status, t.created_at, 'shared' as role
           FROM tasks t JOIN shared_tasks st ON t.id = st.task_id WHERE st.user_id = ?""",
        (user_id, user_id),
    ).fetchall()
    conn.close()
    if not rows:
        print(f"No tasks found for user {user_id}.")
        return
    for row in rows:
        print(f"[{row[0]}] {row[1]} ({row[2]}) [{row[4]}] - {row[3]}")


def share_task(task_id, user_id):
    conn = get_connection()
    task = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        print(f"Task {task_id} not found.")
        conn.close()
        return
    user = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        print(f"User {user_id} not found.")
        conn.close()
        return
    conn.execute(
        "INSERT OR IGNORE INTO shared_tasks (task_id, user_id) VALUES (?, ?)",
        (task_id, user_id),
    )
    conn.commit()
    conn.close()
    print(f"Task {task_id} shared with user {user_id}.")


def update_status_as_user(task_id, status, user_id):
    if status not in VALID_STATUSES:
        print(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        return
    conn = get_connection()
    # Check if user is owner or shared
    task = conn.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        print(f"Task {task_id} not found.")
        conn.close()
        return
    shared = conn.execute(
        "SELECT 1 FROM shared_tasks WHERE task_id = ? AND user_id = ?",
        (task_id, user_id),
    ).fetchone()
    if task[0] != user_id and not shared:
        print(f"User {user_id} does not have access to task {task_id}.")
        conn.close()
        return
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    print(f"Task {task_id} updated to '{status}' by user {user_id}.")


def set_priority(task_id, priority):
    # priority can be: low, medium, high, urgent
    conn = get_connection()
    cursor = conn.execute("UPDATE tasks SET priority = ? WHERE id = ?", (priority, task_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        print(f"Task {task_id} not found.")
    else:
        print(f"Task {task_id} priority set to '{priority}'.")


def get_tasks_sorted_by_priority():
    # return all tasks sorted by priority, highest first
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, title, status, priority, created_at FROM tasks ORDER BY priority DESC"
    ).fetchall()
    conn.close()
    if not rows:
        print("No tasks found.")
        return
    for row in rows:
        print(f"[{row[0]}] {row[1]} ({row[2]}) priority={row[3]} - {row[4]}")


def delete_task_as_user(task_id, user_id):
    conn = get_connection()
    task = conn.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        print(f"Task {task_id} not found.")
        conn.close()
        return
    # Only owner can delete
    if task[0] != user_id:
        print(f"User {user_id} cannot delete task {task_id}. Only the owner can delete.")
        conn.close()
        return
    conn.execute("DELETE FROM shared_tasks WHERE task_id = ?", (task_id,))
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Task {task_id} deleted by user {user_id}.")


def main():
    parser = argparse.ArgumentParser(description="Simple TODO app")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Create a new task")
    add_p.add_argument("title", help="Task title")

    sub.add_parser("list", help="List all tasks")

    upd_p = sub.add_parser("update", help="Update task status")
    upd_p.add_argument("id", type=int, help="Task ID")
    upd_p.add_argument("status", choices=VALID_STATUSES, help="New status")

    del_p = sub.add_parser("delete", help="Delete a task")
    del_p.add_argument("id", type=int, help="Task ID")

    user_p = sub.add_parser("create-user", help="Create a new user")
    user_p.add_argument("name", help="User name")
    user_p.add_argument("email", help="User email")

    assign_p = sub.add_parser("assign", help="Assign a task to a user")
    assign_p.add_argument("task_id", type=int, help="Task ID")
    assign_p.add_argument("user_id", type=int, help="User ID")

    ulist_p = sub.add_parser("list-user", help="List tasks for a user")
    ulist_p.add_argument("user_id", type=int, help="User ID")

    share_p = sub.add_parser("share", help="Share a task with a user")
    share_p.add_argument("task_id", type=int, help="Task ID")
    share_p.add_argument("user_id", type=int, help="User ID to share with")

    upd_as_p = sub.add_parser("update-as", help="Update task status as a specific user")
    upd_as_p.add_argument("task_id", type=int, help="Task ID")
    upd_as_p.add_argument("status", choices=VALID_STATUSES, help="New status")
    upd_as_p.add_argument("user_id", type=int, help="User ID")

    prio_p = sub.add_parser("set-priority", help="Set task priority")
    prio_p.add_argument("task_id", type=int, help="Task ID")
    prio_p.add_argument("priority", help="Priority: low, medium, high, urgent")

    sub.add_parser("list-by-priority", help="List tasks sorted by priority")

    del_as_p = sub.add_parser("delete-as", help="Delete a task as a specific user")
    del_as_p.add_argument("task_id", type=int, help="Task ID")
    del_as_p.add_argument("user_id", type=int, help="User ID")

    args = parser.parse_args()

    if args.command == "add":
        create_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "update":
        update_status(args.id, args.status)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "create-user":
        create_user(args.name, args.email)
    elif args.command == "assign":
        assign_task_to_user(args.task_id, args.user_id)
    elif args.command == "list-user":
        list_tasks_by_user(args.user_id)
    elif args.command == "share":
        share_task(args.task_id, args.user_id)
    elif args.command == "update-as":
        update_status_as_user(args.task_id, args.status, args.user_id)
    elif args.command == "set-priority":
        set_priority(args.task_id, args.priority)
    elif args.command == "list-by-priority":
        get_tasks_sorted_by_priority()
    elif args.command == "delete-as":
        delete_task_as_user(args.task_id, args.user_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
