import sqlite3

import pandas as pd

from insider_trading.repository.edgar.edgar_repository import EdgarRepository


class TestEdgarRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:  # noqa: F821
        self.conn = conn
        self.edgar_repo = EdgarRepository(conn)