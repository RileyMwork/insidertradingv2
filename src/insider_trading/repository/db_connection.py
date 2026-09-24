import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

class DbConnection:
    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        db_name = os.getenv("DB_NAME")
        if db_name is None:
            raise ValueError("DB_NAME environment variable is not set")

        self.db_name = db_name
        self.base_dir = Path(__file__).resolve().parent.parent

        self.resources_dir = self.base_dir / "resources"
        self.resources_dir.mkdir(exist_ok=True)

        self.db_path = self.resources_dir / self.db_name

        self.conn = conn or self.connect()

    def create_db_file_if_not_exists(self) -> None:
        if self.db_path.exists():
            print(f"Database already exists: {self.db_path}")
        else:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            print(f"Created database: {self.db_path}")

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    