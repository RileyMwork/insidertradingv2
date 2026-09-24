import sqlite3
from typing import Any

import pandas as pd

from insider_trading.repository.db_connection import DbConnection


class InsertBase(DbConnection):
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        super().__init__(conn)

    def insert_all_from_df(self, df: pd.DataFrame, table_name: str) -> int | None:
        inserted_rows = df.to_sql(table_name, self.conn, if_exists="append", index=False)
        if inserted_rows:
            print(inserted_rows)
        else:
            print("No Rows Inserted")
        return inserted_rows
    
    def insert(self, table_name: str, columns: list[str], values: tuple[Any, ...]) -> int | None:
        cursor = self.conn.cursor()

        placeholders = ", ".join(["?" for _ in values])

        statement = (
            f"INSERT INTO {table_name} "
            f"({', '.join(columns)}) "
            f"VALUES ({placeholders})"
        )

        cursor.execute(statement, values)
        self.conn.commit()

        print(f"Inserted {cursor.rowcount} row(s).")

        return cursor.lastrowid