import sqlite3

import pandas as pd

from insider_trading.repository.insert_base import InsertBase
from insider_trading.repository.select_base import SelectBase


class EdgarRepository(SelectBase, InsertBase):
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        SelectBase.__init__(self, conn)
        InsertBase.__init__(self, conn)
        self.filing_table = "filing"
        self.insider_transaction_table = "insider_transaction"

    def insert_all_transactions(self, df : pd.DataFrame) -> int | None:
        inserted_rows = self.insert_all_from_df(df, self.insider_transaction_table)
        return inserted_rows

    def get_latest_date_entered_into_db(self) -> str | None:
        rows, columns = self.select_raw(f"SELECT MAX(date_entered_into_db) FROM {self.filing_table}")  # noqa: E501
        return rows[0][0] if rows and rows[0][0] is not None else None
    
    def select_all_filings(self) -> pd.DataFrame:
        rows, columns = self.select_raw(f"SELECT * FROM {self.filing_table}")
        return pd.DataFrame(rows, columns=columns)

    def select_all_insider_transactions(self) -> pd.DataFrame:
        rows, columns = self.select_raw(f"SELECT * FROM {self.insider_transaction_table}")
        return pd.DataFrame(rows, columns=columns)

    def select_filings_by_date(self, date: str) -> pd.DataFrame:
        rows, columns = self.select_raw(f"SELECT * FROM {self.filing_table} WHERE date_entered_into_db = '{date}'")  # noqa: E501
        return pd.DataFrame(rows, columns=columns)

    def select_insider_transactions_by_date(self, date: str) -> pd.DataFrame:
        # need to join filing table
        rows, columns = self.select_raw(f"""
            SELECT it.*
            FROM {self.insider_transaction_table} it
            JOIN {self.filing_table} f ON it.filing_id = f.id
            WHERE f.date_entered_into_db = '{date}'
        """)
        return pd.DataFrame(rows, columns=columns)