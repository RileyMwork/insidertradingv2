import logging
import sqlite3
from typing import Any

from insider_trading.repository.db_connection import DbConnection


class SelectBase(DbConnection):
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        super().__init__(conn)
        self.logger = logging.getLogger(__name__)

    def select(
        self,
        select_columns: list[str],
        table_name: str,
        where_columns: list[str] | None = None,
        where_values: list[Any] | None = None,
        order_by_column: str | None = None,
        order_by_direction: str | None = None,
        limit: int | None = None,
    ) -> list[tuple[Any, ...]]:
        if where_columns is None:
            where_columns = []

        if where_values is None:
            where_values = []

        if len(where_columns) != len(where_values):
            raise ValueError("where_columns and where_values must have the same length.")

        cursor = self.conn.cursor()

        if where_columns:
            where_clause = "WHERE " + " AND ".join([f"{col} = ?" for col in where_columns])
        else:
            where_clause = ""

        if order_by_column:
            order_by_clause = f"ORDER BY {order_by_column}"

            if order_by_direction:
                order_by_clause += f" {order_by_direction}"
        else:
            order_by_clause = ""

        limit_clause = f"LIMIT {limit}" if limit is not None else ""

        statement = (
            f"SELECT {', '.join(select_columns)} "
            f"FROM {table_name} "
            f"{where_clause} {order_by_clause} {limit_clause}"
        )

        try:
            self.logger.debug(
                "Executing SQL: %s | Values: %s",
                statement,
                where_values,
            )

            cursor.execute(statement, where_values)

            rows: list[tuple[Any, ...]] = [tuple(row) for row in cursor.fetchall()]

            self.logger.info(
                "SELECT query returned %s row(s) from table '%s'.",
                len(rows),
                table_name,
            )

            return rows

        except sqlite3.Error:
            self.logger.exception(
                "Failed to execute SELECT query on table '%s'.",
                table_name,
            )
            raise

        finally:
            cursor.close()

    def select_raw(
        self,
        sql: str,
    ) -> tuple[list[tuple[Any, ...]], list[str]]:
        cursor = self.conn.cursor()

        try:
            self.logger.debug("Executing raw SQL: %s", sql)

            cursor.execute(sql)

            rows: list[tuple[Any, ...]] = [tuple(row) for row in cursor.fetchall()]

            columns: list[str] = (
                [col[0] for col in cursor.description] if cursor.description is not None else []
            )

            self.logger.info(
                "Raw SQL query returned %s row(s) and %s column(s).",
                len(rows),
                len(columns),
            )

            return rows, columns

        except sqlite3.Error:
            self.logger.exception("Failed to execute raw SQL query.")
            raise

        finally:
            cursor.close()
