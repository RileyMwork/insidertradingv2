
import sqlite3


def seed_edgar_test_data(conn: sqlite3.Connection) -> None:
    """Insert predictable test data into filing and insider_transaction."""

    filings = [
        (
            "https://www.sec.gov/Archives/edgar/data/1000001/000100000126000001/",
            "2026-10-01",
            "2026-10-01T08:30:00",
            4,
            "2026-09-29",
            1,
            "2026-10-01",
            "2026-10-01",
            "Apple Inc.",
            "1000001",
            1, 1, 0, 0,
            "Chief Executive Officer",
            "Apple Inc.",
            "1000001",
            "3571",
            "Apple Inc.",
            "AAPL",
        ),
        (
            "https://www.sec.gov/Archives/edgar/data/1000002/000100000226000002/",
            "2026-10-01",
            "2026-10-01T09:15:00",
            4,
            "2026-09-30",
            1,
            "2026-10-01",
            "2026-10-01",
            "Microsoft Corp.",
            "1000002",
            1, 1, 0, 0,
            "Chief Financial Officer",
            "Microsoft Corp.",
            "1000002",
            "7372",
            "Microsoft Corp.",
            "MSFT",
        ),
        (
            "https://www.sec.gov/Archives/edgar/data/1000003/000100000326000003/",
            "2026-10-05",
            "2026-10-05T10:00:00",
            4,
            "2026-10-04",
            1,
            "2026-10-05",
            "2026-10-05",
            "NVIDIA Corp.",
            "1000003",
            1, 1, 0, 0,
            "President",
            "NVIDIA Corp.",
            "1000003",
            "3674",
            "NVIDIA Corp.",
            "NVDA",
        ),
    ]

    filing_sql = """
        INSERT INTO filing (
            link,
            date_entered_into_db,
            acceptance_datetime,
            conformed_submission_type,
            conformed_period_of_report,
            public_document_count,
            filed_as_of_date,
            date_as_of_change,
            company_conformed_name,
            reporting_owner_cik,
            reporting_owner_isDirector,
            reporting_owner_isOfficer,
            reporting_owner_isTenPercentOwner,
            reporting_owner_isOther,
            reporting_owner_officer_title,
            issuer_company_conformed_name,
            issuer_cik,
            issuer_sic,
            issuer_organization_name,
            issuer_trading_symbol
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    transaction_sql = """
        INSERT INTO insider_transaction (
            issuer_trading_symbol,
            security_title,
            transaction_date,
            transaction_code,
            equity_swap_involved,
            transaction_shares,
            transaction_price_per_share,
            transaction_acquired_disposed_code,
            shares_owned_following_transaction,
            direct_or_indirect_ownership,
            nature_of_ownership,
            filing_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    cursor = conn.cursor()

    try:
        # Insert filings and capture their generated primary keys.
        filing_ids: list[int] = []

        for filing in filings:
            cursor.execute(filing_sql, filing)

            if cursor.lastrowid is None:
                raise RuntimeError("Failed to retrieve generated filing ID.")

            filing_ids.append(cursor.lastrowid)

        # Associate transactions with the actual generated filing IDs.
        transactions = [
            # Filing 1: Apple - two sales and one purchase
            (
                "AAPL", "Common Stock", "2026-09-29", "P",
                0, 100, 250.00, "A", 10100, "D", None, filing_ids[0],
            ),
            (
                "AAPL", "Common Stock", "2026-09-30", "S",
                0, 50, 255.00, "D", 10050, "D", None, filing_ids[0],
            ),
            (
                "AAPL", "Common Stock", "2026-09-30", "S",
                0, 25, 256.00, "D", 10025, "D", None, filing_ids[0],
            ),

            # Filing 2: Microsoft - purchase and option exercise
            (
                "MSFT", "Common Stock", "2026-09-30", "P",
                0, 200, 500.00, "A", 20200, "D", None, filing_ids[1],
            ),
            (
                "MSFT", "Common Stock", "2026-09-30", "M",
                0, 100, 0.00, "A", 20300, "D", None, filing_ids[1],
            ),

            # Filing 3: NVIDIA - indirect ownership sale
            (
                "NVDA", "Common Stock", "2026-10-04", "S",
                0, 500, 180.00, "D", 9500, "I",
                "Family Trust", filing_ids[2],
            ),
        ]

        cursor.executemany(transaction_sql, transactions)
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()


def clear_edgar_test_data(conn: sqlite3.Connection) -> None:
    """Delete only records created by seed_edgar_test_data."""

    test_ciks = ("1000001", "1000002", "1000003")
    placeholders = ", ".join("?" for _ in test_ciks)

    try:
        conn.execute(
            f"""
            DELETE FROM insider_transaction
            WHERE filing_id IN (
                SELECT id FROM filing
                WHERE reporting_owner_cik IN ({placeholders})
            )
            """,
            test_ciks,
        )

        conn.execute(
            f"""
            DELETE FROM filing
            WHERE reporting_owner_cik IN ({placeholders})
            """,
            test_ciks,
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise
