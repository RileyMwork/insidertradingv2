# from main.components.infrastructure.repository.sql.select.select_base import SelectBase
# from main.components.infrastructure.repository.sql.insert.insert_base import InsertBase
import sqlite3

import pandas as pd

from insider_trading.repository.insert_base import InsertBase
from insider_trading.repository.select_base import SelectBase


class InsiderTransactionRepository(SelectBase, InsertBase):
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        SelectBase.__init__(self, conn)
        InsertBase.__init__(self, conn)
        self.table_name = "insider_transactions"

    def insert_all_transactions(self, df : pd.DataFrame) -> int | None:
        inserted_rows = self.insert_all_from_df(df, self.table_name)
        return inserted_rows
    
    def get_all_distinct_filed_dates(self) -> list[str]:
        rows, columns = self.select_raw("SELECT DISTINCT filed_date FROM insider_transactions ORDER BY filed_date DESC")  # noqa: E501
        return [row[0] for row in rows]