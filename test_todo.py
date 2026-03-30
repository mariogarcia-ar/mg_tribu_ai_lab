"""
Tests for Story 1.1: decisions.md + database schema + enums.
Run with: python -m unittest test_todo.py
"""
import unittest
import sqlite3
import os
import tempfile


class TestTaskStatus(unittest.TestCase):

    def test_all_six_states_defined(self):
        from todo import TaskStatus
        expected = {'PENDING', 'IN_PROGRESS', 'BLOCKED', 'REVIEW', 'DONE', 'CANCELLED'}
        actual = {s.name for s in TaskStatus}
        self.assertEqual(actual, expected)

    def test_terminal_states_returns_set(self):
        from todo import TaskStatus
        terminals = TaskStatus.terminal_states()
        self.assertIsInstance(terminals, set)

    def test_terminal_states_contains_done_and_cancelled(self):
        from todo import TaskStatus
        terminals = TaskStatus.terminal_states()
        self.assertIn(TaskStatus.DONE, terminals)
        self.assertIn(TaskStatus.CANCELLED, terminals)

    def test_terminal_states_exact_members(self):
        from todo import TaskStatus
        self.assertEqual(TaskStatus.terminal_states(), {TaskStatus.DONE, TaskStatus.CANCELLED})

    def test_non_terminal_states_not_in_terminal(self):
        from todo import TaskStatus
        terminals = TaskStatus.terminal_states()
        for state in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED, TaskStatus.REVIEW]:
            self.assertNotIn(state, terminals)

    def test_terminal_state_membership_operator(self):
        """D-02: status in TaskStatus.terminal_states() must work."""
        from todo import TaskStatus
        self.assertTrue(TaskStatus.DONE in TaskStatus.terminal_states())
        self.assertFalse(TaskStatus.PENDING in TaskStatus.terminal_states())


class TestTaskPriority(unittest.TestCase):

    def test_all_four_levels_defined(self):
        from todo import TaskPriority
        expected = {'LOW', 'MEDIUM', 'HIGH', 'URGENT'}
        actual = {p.name for p in TaskPriority}
        self.assertEqual(actual, expected)

    def test_priority_integer_values(self):
        from todo import TaskPriority
        self.assertEqual(int(TaskPriority.LOW), 1)
        self.assertEqual(int(TaskPriority.MEDIUM), 2)
        self.assertEqual(int(TaskPriority.HIGH), 3)
        self.assertEqual(int(TaskPriority.URGENT), 4)

    def test_priority_integer_ordering(self):
        """D-03: ordering uses integer value, not name."""
        from todo import TaskPriority
        self.assertLess(TaskPriority.LOW, TaskPriority.MEDIUM)
        self.assertLess(TaskPriority.MEDIUM, TaskPriority.HIGH)
        self.assertLess(TaskPriority.HIGH, TaskPriority.URGENT)

    def test_priority_is_intenum(self):
        from todo import TaskPriority
        from enum import IntEnum
        self.assertTrue(issubclass(TaskPriority, IntEnum))


class TestInitDb(unittest.TestCase):

    def setUp(self):
        fd, self.tmp_path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        os.remove(self.tmp_path)  # init_db will create it

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)

    def _get_tables(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()
        return tables

    def _get_columns(self, db_path, table):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        cols = {row[1] for row in cursor.fetchall()}
        conn.close()
        return cols

    def test_creates_users_table(self):
        from todo import init_db
        init_db(self.tmp_path)
        self.assertIn('users', self._get_tables(self.tmp_path))

    def test_creates_tasks_table(self):
        from todo import init_db
        init_db(self.tmp_path)
        self.assertIn('tasks', self._get_tables(self.tmp_path))

    def test_users_table_columns(self):
        from todo import init_db
        init_db(self.tmp_path)
        cols = self._get_columns(self.tmp_path, 'users')
        self.assertIn('id', cols)
        self.assertIn('name', cols)
        self.assertIn('email', cols)

    def test_tasks_table_columns_complete(self):
        from todo import init_db
        init_db(self.tmp_path)
        cols = self._get_columns(self.tmp_path, 'tasks')
        expected = {'id', 'title', 'status', 'priority', 'owner_id', 'created_by', 'due_date', 'created_at'}
        self.assertEqual(cols, expected)

    def test_tasks_status_default_is_pending(self):
        from todo import init_db
        init_db(self.tmp_path)
        conn = sqlite3.connect(self.tmp_path)
        # Insert a minimal task and check default status
        conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)", ('Test', 'test@test.com')
        )
        conn.execute(
            "INSERT INTO tasks (title, created_by, created_at) VALUES (?, ?, ?)",
            ('Test task', 1, '2026-01-01')
        )
        conn.commit()
        cursor = conn.execute("SELECT status FROM tasks WHERE title='Test task'")
        row = cursor.fetchone()
        conn.close()
        self.assertEqual(row[0], 'PENDING')

    def test_tasks_priority_default_is_2(self):
        from todo import init_db
        init_db(self.tmp_path)
        conn = sqlite3.connect(self.tmp_path)
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Test', 't@t.com'))
        conn.execute(
            "INSERT INTO tasks (title, created_by, created_at) VALUES (?, ?, ?)",
            ('P task', 1, '2026-01-01')
        )
        conn.commit()
        cursor = conn.execute("SELECT priority FROM tasks WHERE title='P task'")
        row = cursor.fetchone()
        conn.close()
        self.assertEqual(row[0], 2)

    def test_init_db_idempotent(self):
        """CREATE TABLE IF NOT EXISTS — calling twice must not raise."""
        from todo import init_db
        init_db(self.tmp_path)
        init_db(self.tmp_path)  # should not raise

    def test_tasks_owner_id_nullable(self):
        """D-05: owner_id is optional (NULL is valid)."""
        from todo import init_db
        init_db(self.tmp_path)
        conn = sqlite3.connect(self.tmp_path)
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Test', 'u@u.com'))
        conn.execute(
            "INSERT INTO tasks (title, created_by, created_at) VALUES (?, ?, ?)",
            ('No owner task', 1, '2026-01-01')
        )
        conn.commit()
        cursor = conn.execute("SELECT owner_id FROM tasks WHERE title='No owner task'")
        row = cursor.fetchone()
        conn.close()
        self.assertIsNone(row[0])


class TestImports(unittest.TestCase):

    def test_module_imports_without_error(self):
        """todo.py must be importable with stdlib only."""
        import todo  # noqa: F401

    def test_sqlite3_available(self):
        import sqlite3  # noqa: F401

    def test_argparse_available(self):
        import argparse  # noqa: F401

    def test_enum_available(self):
        from enum import Enum, IntEnum  # noqa: F401

    def test_datetime_available(self):
        from datetime import datetime  # noqa: F401


if __name__ == '__main__':
    unittest.main(verbosity=2)
