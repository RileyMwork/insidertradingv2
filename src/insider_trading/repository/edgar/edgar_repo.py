
import sqlite3
from typing import Any

import pandas as pd

from insider_trading.repository.db_connection import DbConnection
from insider_trading.repository.insert_base import InsertBase
from insider_trading.repository.select_base import SelectBase


class EdgarRepo(DbConnection):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection)
        self.select_base = SelectBase(connection)
        self.insert_base = InsertBase(connection)
        self.filing_table = "filing"
        self.insider_transaction_table = "insider_transaction"

    def insert_all_from_df(self, df: pd.DataFrame, table_name: str) -> int | None:
        return self.insert_base.insert_all_from_df(df, table_name)

    def insert(self, table_name: str, columns: list[str], values: tuple[Any, ...]) -> int | None:
        return self.insert_base.insert(table_name, columns, values)

    def select(self, select_columns: list[str], table_name: str, where_columns: list[str] | None = None, where_values: list[Any] | None = None,) -> list[tuple[Any, ...]]:  # noqa: E501
        return self.select_base.select(select_columns, table_name, where_columns, where_values)

    def select_raw(self, sql: str) -> tuple[list[tuple[Any, ...]], list[str]]:
        return self.select_base.select_raw(sql)

    def select_all(self) -> tuple[list[tuple[Any, ...]], list[str]]:
        sql = (f"SELECT * FROM {self.insider_transaction_table} it JOIN {self.filing_table} f ON it.filing_id = f.id")  # noqa: E501
        return self.select_raw(sql)

    def get_latest_filing_date(self) -> str | None:
        sql = f"SELECT MAX(date_entered_into_db) FROM {self.filing_table}"
        rows, _ = self.select_raw(sql)

        if rows and isinstance(rows[0][0], str):
            return rows[0][0]

        return None

    def get_insider_transactions_by_filing_date(self, filing_date: str) -> list[tuple[Any, ...]]:
        select_columns = ["it.*", "f.*"]
        table_name = (f"{self.insider_transaction_table} it JOIN {self.filing_table} f ON it.filing_id = f.id")  # noqa: E501
        where_columns = ["f.date_entered_into_db"]
        where_values = [filing_date]

        return self.select(select_columns, table_name, where_columns, where_values)
