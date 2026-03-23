#!/usr/bin/env python3
import sqlite3
import argparse
from datetime import datetime

DB_NAME = "todo.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
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

    args = parser.parse_args()

    if args.command == "add":
        create_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "update":
        update_status(args.id, args.status)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
