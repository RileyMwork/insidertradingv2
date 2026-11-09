# import os
# import sqlite3

# from dotenv import load_dotenv

# load_dotenv()

# def test_db_connection() -> None:
#     db_location = os.getenv("DB_LOCATION")
#     if not db_location:
#         raise ValueError("DB_LOCATION environment variable is not set")

#     conn = sqlite3.connect(db_location)
#     cursor = conn.cursor()

#     # Check if the connection is open
#     assert conn is not None, "Failed to establish a database connection"

#     # Check if the connection is valid by executing a simple query
#     cursor.execute("SELECT sqlite_version();")
#     version = cursor.fetchone()
#     assert version is not None, "Failed to execute query on the database"

#     print(f"SQLite version: {version[0]}")

#     # Close the connection
#     conn.close()