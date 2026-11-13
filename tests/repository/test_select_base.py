import sqlite3
from collections.abc import Generator
from typing import Any

import pytest

from insider_trading.repository.db_connection import DbConnection
from insider_trading.repository.select_base import SelectBase


class TestSelectBase:
    # Declare class attributes for mypy
    test_table: str
    db_connection: DbConnection
    connection: sqlite3.Connection
    select_base: SelectBase
    cursor: sqlite3.Cursor

    @pytest.fixture(autouse=True, scope="class")
    @classmethod
    def setup_and_teardown(cls) -> Generator[None, Any]:
        # Setup
        cls.test_table = "test_table"

        cls.db_connection = DbConnection()
        cls.connection = cls.db_connection.connect()

        cls.select_base = SelectBase(cls.connection)
        cls.cursor = cls.connection.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """
        cls.cursor.execute(sql)

        insert_statement = f"INSERT INTO {cls.test_table} (name, age) VALUES (?, ?)"
        data = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
        cls.cursor.executemany(insert_statement, data)

        cls.connection.commit()

        yield

        # Teardown
        try:
            cls.cursor.execute("DROP TABLE IF EXISTS test_table")
            cls.connection.commit()
        finally:
            cls.cursor.close()
            cls.connection.close()


    def test_select(self) -> None:
        select_columns = ["id", "name", "age"]
        table_name = self.test_table
        where_columns = ["name"]
        where_values = ["Alice"]
        order_by_column = "age"
        order_by_direction = "DESC"
        limit = 1

        result = self.select_base.select(
            select_columns,
            table_name,
            where_columns,
            where_values,
            order_by_column,
            order_by_direction,
            limit
        )

        assert result == [(1, "Alice", 30)]

    def test_select_raw(self) -> None:
        sql = f"SELECT * FROM {self.test_table} WHERE age > 25"
        rows, columns = self.select_base.select_raw(sql)

        assert rows == [(1, "Alice", 30), (3, "Charlie", 35)]
        assert columns == ["id", "name", "age"]