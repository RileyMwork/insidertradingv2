import os
import sqlite3
from collections.abc import Generator

import pandas as pd
import pytest
from dotenv import load_dotenv

from insider_trading.repository.edgar.edgar_repository import EdgarRepository
from tests.test_data.edgar_test_data import EdgarTestData

load_dotenv()

@pytest.fixture
def edgar_repo() -> Generator[EdgarRepository]:
    db_name = os.getenv("TEST_DB_NAME")

    if not db_name:
        raise ValueError("TEST_DB_NAME environment variable is not set")

    print(f"\nCurrent working directory: {os.getcwd()}")
    print(f"Configured database: {db_name}")
    print(f"Resolved database path: {os.path.abspath(db_name)}")
    print(f"Database exists: {os.path.isfile(db_name)}")

    conn = sqlite3.connect(db_name)

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()

    print(f"Tables SQLite can see: {tables}")

    repo = EdgarRepository(conn)

    yield repo

    conn.close()

def test_insert_all_transactions_into_filing_table(edgar_repo: EdgarRepository) -> None:
    edgar_test_data = EdgarTestData()

    filing_df = pd.DataFrame(
        [f.__dict__ for f in edgar_test_data.get_test_filings()]
    )

    inserted_rows = edgar_repo.insert_all_transactions(filing_df, edgar_repo.filing_table)

    assert inserted_rows == len(filing_df), (
        f"Expected {len(filing_df)} rows to be inserted, "
        f"but got {inserted_rows}"
    )

def test_get_latest_date_entered_into_db(edgar_repo: EdgarRepository) -> None:
    all_dates = edgar_repo.select_all_filings()["date_entered_into_db"].tolist()
    max_date = max(all_dates) if all_dates else None
    latest_date = edgar_repo.get_latest_date_entered_into_db()

    assert latest_date is not None, "Expected a date to be returned, but got None"
    assert latest_date == max_date, (f"Expected latest date to be {max_date}, but got {latest_date}")  # noqa: E501

def test_select_all_filings(edgar_repo: EdgarRepository) -> None:
    filings_df = edgar_repo.select_all_filings()
    assert not filings_df.empty, "Expected filings DataFrame to be non-empty"

def test_select_all_insider_transactions(edgar_repo: EdgarRepository) -> None:
    transactions_df = edgar_repo.select_all_insider_transactions()
    assert not transactions_df.empty, "Expected insider transactions DataFrame to be non-empty"

def test_select_filings_by_date(edgar_repo: EdgarRepository) -> None:
    all_dates = edgar_repo.select_all_filings()["date_entered_into_db"].tolist()
    if not all_dates:
        pytest.skip("No filings available to test select_filings_by_date")

    test_date = all_dates[0]
    filings_df = edgar_repo.select_filings_by_date(test_date)

    assert not filings_df.empty, f"Expected filings DataFrame for date {test_date} to be non-empty"

def test_select_insider_transactions_by_date(edgar_repo: EdgarRepository) -> None:
    all_dates = edgar_repo.select_all_filings()["date_entered_into_db"].tolist()
    if not all_dates:
        pytest.skip("No filings available to test select_insider_transactions_by_date")

    test_date = all_dates[0]
    transactions_df = edgar_repo.select_insider_transactions_by_date(test_date)

    assert not transactions_df.empty, f"Expected insider transactions DataFrame for date {test_date} to be non-empty"  # noqa: E501
