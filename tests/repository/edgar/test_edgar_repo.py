import sqlite3
from collections.abc import Generator
from typing import Any

import pytest

from insider_trading.repository.db_connection import DbConnection
from insider_trading.repository.edgar.edgar_repo import EdgarRepo
from tests.test_data.edgar_repo_test_data import clear_edgar_test_data, seed_edgar_test_data


class TestEdgarRepo:
    # Declare class attributes for mypy
    test_table: str
    db_connection: DbConnection
    connection: sqlite3.Connection
    edgar_repo: EdgarRepo
    cursor: sqlite3.Cursor

    @pytest.fixture(autouse=True, scope="class")
    @classmethod
    def setup_and_teardown(cls) -> Generator[None, Any]:
        # Setup

        cls.db_connection = DbConnection()
        cls.connection = cls.db_connection.connect()

        cls.edgar_repo = EdgarRepo(cls.connection)
        cls.cursor = cls.connection.cursor()

        seed_edgar_test_data(cls.connection)

        yield

        # Teardown
        try:
            clear_edgar_test_data(cls.connection)
        finally:
            cls.cursor.close()
            cls.connection.close()

    def test_select_all(self) -> None:
        rows, columns = self.edgar_repo.select_all()

        assert len(rows) > 2
        assert "id" in columns
        assert "filing_id" in columns
        assert "date_entered_into_db" in columns

    def test_get_latest_filing_date(self) -> None:
        all_filing_dates = self.edgar_repo.select(["date_entered_into_db"], self.edgar_repo.filing_table)  # noqa: E501

        latest_filing_date = self.edgar_repo.get_latest_filing_date()

        expected_latest_date = max(row[0] for row in all_filing_dates)

        assert latest_filing_date == expected_latest_date

    def test_get_insider_transactions_by_filing_date(self) -> None:
        filing_date = "2026-10-01"
    
        expected_rows, _ = self.edgar_repo.select_raw(
            f"""
            SELECT it.*, f.*
            FROM insider_transaction it
            JOIN filing f ON it.filing_id = f.id
            WHERE f.date_entered_into_db = '{filing_date}'
            """
        )
    
        actual_rows = self.edgar_repo.get_insider_transactions_by_filing_date(
            filing_date
        )
    
        assert len(actual_rows) == 5
        assert actual_rows == expected_rows

    def test_get_all_distinct_filed_dates(self) -> None:
        all_filed_dates = self.edgar_repo.select(
            ["filed_as_of_date"],
            self.edgar_repo.filing_table,
        )

        actual_filed_dates = self.edgar_repo.get_all_distinct_filed_dates()

        expected_filed_dates = sorted(
            {row[0] for row in all_filed_dates},
            reverse=True,
        )

        assert actual_filed_dates == expected_filed_dates
        assert len(actual_filed_dates) == len(set(actual_filed_dates))
        assert actual_filed_dates == sorted(actual_filed_dates, reverse=True)