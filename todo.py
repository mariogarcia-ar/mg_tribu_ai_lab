import sqlite3
import argparse
from enum import Enum, IntEnum
from datetime import datetime


DB_PATH = 'todo.db'


class TaskStatus(Enum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    BLOCKED = 'BLOCKED'
    REVIEW = 'REVIEW'
    DONE = 'DONE'
    CANCELLED = 'CANCELLED'

    @classmethod
    def terminal_states(cls):
        return {cls.DONE, cls.CANCELLED}


class TaskPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            priority INTEGER DEFAULT 2,
            owner_id INTEGER,
            created_by INTEGER NOT NULL,
            due_date TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO CLI — Lab AI Encuentro 2')
    subparsers = parser.add_subparsers(dest='command')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
