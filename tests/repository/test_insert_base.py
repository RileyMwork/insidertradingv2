import sqlite3
from collections.abc import Generator
from typing import Any

import pandas as pd
import pytest

from insider_trading.repository.db_connection import DbConnection
from insider_trading.repository.insert_base import InsertBase


class TestInsertBase:
    # Declare class attributes for mypy
    test_table: str
    db_connection: DbConnection
    connection: sqlite3.Connection
    insert_base: InsertBase
    cursor: sqlite3.Cursor

    @pytest.fixture(autouse=True, scope="class")
    @classmethod
    def setup_and_teardown(cls) -> Generator[None, Any]:
        # Setup
        cls.test_table = "test_table"

        cls.db_connection = DbConnection()
        cls.connection = cls.db_connection.connect()

        cls.insert_base = InsertBase(cls.connection)
        cls.cursor = cls.connection.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """
        cls.cursor.execute(sql)
        cls.connection.commit()

        yield

        # Teardown
        try:
            cls.cursor.execute("DROP TABLE IF EXISTS test_table")
            cls.connection.commit()
        finally:
            cls.cursor.close()
            cls.connection.close()

    def test_insert_all_from_df(self) -> None:
        entry = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})

        inserted_rows = self.insert_base.insert_all_from_df(entry, self.test_table)

        assert inserted_rows == 2

    def test_insert(self) -> None:
        columns = ["name", "age"]
        values = ("Charlie", 28)

        last_row_id = self.insert_base.insert(self.test_table, columns, values)

        assert last_row_id is not None

        self.cursor.execute(f"SELECT * FROM {self.test_table} WHERE id = ?", (last_row_id,))
        row = self.cursor.fetchone()

        assert row is not None
        assert row[1] == "Charlie"
        assert row[2] == 28
