#!/usr/bin/env python3
import sqlite3
import argparse
from datetime import datetime

DB_NAME = "todo.db"


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
            created_at TEXT NOT NULL,
            user_id INTEGER,
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
    if status not in ("pending", "done"):
        print("Status must be 'pending' or 'done'.")
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
        "SELECT id, title, status, created_at FROM tasks WHERE user_id = ?",
        (user_id,),
    ).fetchall()
    conn.close()
    if not rows:
        print(f"No tasks found for user {user_id}.")
        return
    for row in rows:
        print(f"[{row[0]}] {row[1]} ({row[2]}) - {row[3]}")


def main():
    parser = argparse.ArgumentParser(description="Simple TODO app")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Create a new task")
    add_p.add_argument("title", help="Task title")

    sub.add_parser("list", help="List all tasks")

    upd_p = sub.add_parser("update", help="Update task status")
    upd_p.add_argument("id", type=int, help="Task ID")
    upd_p.add_argument("status", choices=["pending", "done"], help="New status")

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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
