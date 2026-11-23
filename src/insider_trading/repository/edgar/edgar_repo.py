
import logging
import sqlite3
from typing import Any

import pandas as pd

from insider_trading.repository.db_connection import DbConnection
from insider_trading.repository.insert_base import InsertBase
from insider_trading.repository.select_base import SelectBase


class EdgarRepo(DbConnection):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection)

        self.logger = logging.getLogger(__name__)

        self.select_base = SelectBase(connection)
        self.insert_base = InsertBase(connection)

        self.filing_table = "filing"
        self.insider_transaction_table = "insider_transaction"

    def insert_all_from_df(
        self,
        df: pd.DataFrame,
        table_name: str,
    ) -> int | None:
        self.logger.info(
            "Inserting %s rows into '%s' table.",
            len(df),
            table_name,
        )

        return self.insert_base.insert_all_from_df(df, table_name)

    def insert(
        self,
        table_name: str,
        columns: list[str],
        values: tuple[Any, ...],
    ) -> int | None:
        self.logger.info(
            "Inserting row into '%s' table.",
            table_name,
        )

        return self.insert_base.insert(table_name, columns, values)

    def select(
        self,
        select_columns: list[str],
        table_name: str,
        where_columns: list[str] | None = None,
        where_values: list[Any] | None = None,
    ) -> list[tuple[Any, ...]]:
        self.logger.info(
            "Selecting records from '%s' table.",
            table_name,
        )

        return self.select_base.select(
            select_columns,
            table_name,
            where_columns,
            where_values,
        )

    def select_raw(
        self,
        sql: str,
    ) -> tuple[list[tuple[Any, ...]], list[str]]:
        self.logger.debug("Executing raw SQL through EdgarRepo.")

        return self.select_base.select_raw(sql)

    def select_all(self) -> tuple[list[tuple[Any, ...]], list[str]]:
        self.logger.info(
            "Selecting all records from '%s' and '%s' tables.",
            self.insider_transaction_table,
            self.filing_table,
        )

        sql = (
            f"SELECT * FROM {self.insider_transaction_table} it "
            f"JOIN {self.filing_table} f ON it.filing_id = f.id"
        )

        return self.select_raw(sql)

    def get_latest_filing_date(self) -> str | None:
        self.logger.info(
            "Getting latest filing date from '%s' table.",
            self.filing_table,
        )

        sql = (
            f"SELECT MAX(date_entered_into_db) "
            f"FROM {self.filing_table}"
        )

        rows, _ = self.select_raw(sql)

        if rows and isinstance(rows[0][0], str):
            latest_date: str = rows[0][0]

            self.logger.info(
                "Latest filing date found: %s.",
                latest_date,
            )

            return latest_date

        self.logger.warning(
            "No filing date found in '%s' table.",
            self.filing_table,
        )

        return None

    def get_insider_transactions_by_filing_date(
        self,
        filing_date: str,
    ) -> list[tuple[Any, ...]]:
        self.logger.info(
            "Getting insider transactions for filing date: %s.",
            filing_date,
        )

        select_columns: list[str] = ["it.*", "f.*"]

        table_name = (
            f"{self.insider_transaction_table} it "
            f"JOIN {self.filing_table} f ON it.filing_id = f.id"
        )

        where_columns: list[str] = ["f.date_entered_into_db"]
        where_values: list[Any] = [filing_date]

        return self.select(
            select_columns,
            table_name,
            where_columns,
            where_values,
        )

    def get_all_distinct_filed_dates(self) -> list[str]:
        self.logger.info(
            "Getting all distinct filed dates from '%s' table.",
            self.filing_table,
        )

        sql = (
            "SELECT DISTINCT filed_as_of_date "
            f"FROM {self.filing_table} "
            "ORDER BY filed_as_of_date DESC"
        )

        rows, _ = self.select_raw(sql)

        filed_dates: list[str] = [
            row[0] for row in rows if isinstance(row[0], str)
        ]

        self.logger.info(
            "Retrieved %s distinct filing dates.",
            len(filed_dates),
        )

        return filed_dates
