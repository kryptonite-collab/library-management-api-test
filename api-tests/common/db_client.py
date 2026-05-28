import os
import sqlite3
from pathlib import Path
from typing import Optional

import pytest
from dotenv import load_dotenv


API_TESTS_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = API_TESTS_ROOT / ".env"

load_dotenv(ENV_PATH)


class DbClient:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = self._resolve_db_path(db_path)

    def ensure_available(self) -> None:
        if not self.db_path.exists():
            pytest.skip(f"SQLite database file does not exist: {self.db_path}")

    def get_book_by_isbn(self, isbn: str) -> Optional[dict]:
        return self._query_one(
            """
            SELECT id, title, author, isbn, genre, description, language,
                   shelfLocation, available, createdAt
            FROM Book
            WHERE isbn = ?
            """,
            (isbn,),
        )

    def delete_test_books_by_prefix(self, prefix: str = "TEST_AUTO_") -> int:
        self.ensure_available()

        if not prefix or not prefix.startswith("TEST_AUTO_"):
            raise ValueError("Only TEST_AUTO_ prefixed data can be cleaned up.")

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                DELETE FROM Book
                WHERE title LIKE ? OR isbn LIKE ?
                """,
                (f"{prefix}%", f"{prefix}%"),
            )
            connection.commit()

        return cursor.rowcount

    def get_audit_log_by_id(self, log_id: int) -> Optional[dict]:
        return self._query_one(
            """
            SELECT id, userId, action, entity, entityId, detail, createdAt
            FROM AuditLog
            WHERE id = ?
            """,
            (log_id,),
        )

    def insert_test_audit_log(self, audit_log_data: dict) -> dict:
        self.ensure_available()

        detail = audit_log_data.get("detail", "")
        if not detail.startswith("TEST_AUTO_"):
            raise ValueError("Only TEST_AUTO_ prefixed audit logs can be inserted by tests.")

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO AuditLog (userId, action, entity, entityId, detail)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    audit_log_data.get("userId"),
                    audit_log_data["action"],
                    audit_log_data["entity"],
                    audit_log_data.get("entityId"),
                    detail,
                ),
            )
            connection.commit()
            log_id = cursor.lastrowid

        return self.get_audit_log_by_id(log_id)

    def delete_test_audit_logs_by_prefix(self, prefix: str = "TEST_AUTO_") -> int:
        self.ensure_available()

        if not prefix or not prefix.startswith("TEST_AUTO_"):
            raise ValueError("Only TEST_AUTO_ prefixed audit logs can be cleaned up.")

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                DELETE FROM AuditLog
                WHERE detail LIKE ?
                """,
                (f"{prefix}%",),
            )
            connection.commit()

        return cursor.rowcount

    def get_audit_log_by_action_entity_entity_id(
        self,
        action: str,
        entity: str,
        entity_id: Optional[int],
    ) -> Optional[dict]:
        if entity_id is None:
            return self._query_one(
                """
                SELECT id, userId, action, entity, entityId, detail, createdAt
                FROM AuditLog
                WHERE action = ? AND entity = ? AND entityId IS NULL
                ORDER BY createdAt DESC
                LIMIT 1
                """,
                (action, entity),
            )

        return self._query_one(
            """
            SELECT id, userId, action, entity, entityId, detail, createdAt
            FROM AuditLog
            WHERE action = ? AND entity = ? AND entityId = ?
            ORDER BY createdAt DESC
            LIMIT 1
            """,
            (action, entity, entity_id),
        )

    def get_latest_audit_log(self) -> Optional[dict]:
        return self._query_one(
            """
            SELECT id, userId, action, entity, entityId, detail, createdAt
            FROM AuditLog
            ORDER BY createdAt DESC
            LIMIT 1
            """
        )

    def _query_one(self, sql: str, params: tuple = ()) -> Optional[dict]:
        self.ensure_available()

        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute(sql, params).fetchone()

        return dict(row) if row else None

    @classmethod
    def _resolve_db_path(cls, explicit_path: Optional[str]) -> Path:
        configured_path = explicit_path or os.getenv("SQLITE_DB_PATH")

        if configured_path:
            path = Path(configured_path)
            if path.is_absolute():
                return path

            api_tests_path = (API_TESTS_ROOT / path).resolve()
            if api_tests_path.exists():
                return api_tests_path

            return (PROJECT_ROOT / path).resolve()

        candidates = [
            PROJECT_ROOT / "backend" / "prisma" / "prisma" / "dev.db",
            PROJECT_ROOT / "backend" / "prisma" / "dev.db",
            API_TESTS_ROOT / ".." / "backend" / "prisma" / "prisma" / "dev.db",
        ]

        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved.exists():
                return resolved

        return candidates[0].resolve()
