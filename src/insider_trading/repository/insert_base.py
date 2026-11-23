import logging
import sqlite3
from typing import Any

import pandas as pd

from insider_trading.repository.db_connection import DbConnection


class InsertBase(DbConnection):
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        super().__init__(conn)
        self.logger = logging.getLogger(__name__)

    def insert_all_from_df(
        self,
        df: pd.DataFrame,
        table_name: str,
    ) -> int | None:
        self.logger.info(
            "Inserting %s DataFrame rows into table '%s'.",
            len(df),
            table_name,
        )

        try:
            inserted_rows = df.to_sql(
                table_name,
                self.conn,
                if_exists="append",
                index=False,
            )

            if inserted_rows:
                self.logger.info(
                    "Successfully inserted %s rows into table '%s'.",
                    inserted_rows,
                    table_name,
                )
            else:
                self.logger.warning(
                    "No rows were inserted into table '%s'.",
                    table_name,
                )

            return inserted_rows

        except (sqlite3.Error, pd.errors.DatabaseError):
            self.logger.exception(
                "Failed to insert DataFrame rows into table '%s'.",
                table_name,
            )
            raise

    def insert(
        self,
        table_name: str,
        columns: list[str],
        values: tuple[Any, ...],
    ) -> int | None:
        self.logger.debug(
            "Inserting a row into table '%s'.",
            table_name,
        )

        cursor = self.conn.cursor()

        placeholders = ", ".join(["?" for _ in values])

        statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        try:
            cursor.execute(statement, values)
            self.conn.commit()

            self.logger.info(
                "Successfully inserted %s row(s) into table '%s'.",
                cursor.rowcount,
                table_name,
            )

            return cursor.lastrowid

        except sqlite3.Error:
            self.conn.rollback()

            self.logger.exception(
                "Failed to insert row into table '%s'.",
                table_name,
            )
            raise

        finally:
            cursor.close()
