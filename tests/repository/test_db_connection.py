from dotenv import load_dotenv

from insider_trading.repository.db_connection import DbConnection

load_dotenv()

def test_db_connection() -> None:
    db_connection = DbConnection()
    conn = db_connection.connect()
    cursor = conn.cursor()

    # Check if the connection is open
    assert conn is not None, "Failed to establish a database connection"

    # Check if the connection is valid by executing a simple query
    cursor.execute("SELECT sqlite_version();")
    version = cursor.fetchone()
    assert version is not None, "Failed to execute query on the database"

    print(f"SQLite version: {version[0]}")

    # Close the connection
    conn.close()