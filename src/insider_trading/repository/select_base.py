import sqlite3
from typing import Any

from insider_trading.repository.db_connection import DbConnection


class SelectBase(DbConnection):
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        super().__init__(conn)

    def select(self, select_columns: list[str], table_name: str, 
                where_columns: list[str] | None = None, 
                where_values: list[Any] | None = None, 
                order_by_column: str | None = None, 
                order_by_direction: str | None = None, 
                limit: int | None = None) -> tuple[Any, ...] | None:
        
        if where_columns is None:
            where_columns = []
        if where_values is None:
            where_values = []
        cursor = self.conn.cursor()

        if where_columns and where_values:
            where_clause = "WHERE " + " AND ".join([f"{col} = ?" for col in where_columns])
        else:
            where_clause = ""

        if order_by_column:
            order_by_clause = f"ORDER BY {order_by_column}"
            if order_by_direction:
                order_by_clause += f" {order_by_direction}"
        else:
            order_by_clause = ""

        if limit:
            limit_clause = f"LIMIT {limit}"
        else:
            limit_clause = ""

        statement = f"SELECT {', '.join(select_columns)} FROM {table_name} {where_clause} {order_by_clause} {limit_clause}"  # noqa: E501

        cursor.execute(statement, where_values)
        row = cursor.fetchone()

        if row is None:
            return None

        return tuple(row)      
    
    def select_raw(self, sql: str) -> tuple[list[tuple[Any, ...]], list[str]]:
        cursor = self.conn.cursor()
        cursor.execute(sql)
    
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    
        return rows, columns