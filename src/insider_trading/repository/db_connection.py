
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class DbConnection:
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        db_location: str | None = os.getenv("DB_LOCATION")

        if db_location is None:
            raise ValueError("DB_LOCATION environment variable is not set")

        # Resolve the database path relative to the project root
        # when a relative path is provided.
        self.db_location: Path = Path(db_location)

        if not self.db_location.is_absolute():
            project_root: Path = Path(__file__).resolve().parents[3]
            self.db_location = project_root / self.db_location

        self.conn: sqlite3.Connection = (
            conn if conn is not None else self.connect()
        )

    def connect(self) -> sqlite3.Connection:
        self.db_location.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.db_location)
