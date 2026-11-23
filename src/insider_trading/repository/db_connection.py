import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()


class DbConnection:
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        self.db_location = os.getenv("DB_LOCATION")
        self.conn = conn or self.connect()

    def connect(self) -> sqlite3.Connection:
        if self.db_location is None:
            raise ValueError("DB_LOCATION environment variable is not set")
        return sqlite3.connect(self.db_location)
