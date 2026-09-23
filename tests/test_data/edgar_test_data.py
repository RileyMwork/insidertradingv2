
from datetime import date, date, datetime
from decimal import Decimal

from insider_trading.model.filing import Filing
from insider_trading.model.insider_transaction import InsiderTransaction


class EdgarTestData:
    def __init__(self) -> None:
        self.test_filing_1 = Filing(
            link="https://www.sec.gov/Archives/edgar/data/320193/example.xml",
            # Document Info
            acceptance_datetime=datetime(2026, 9, 19, 16, 32, 10),
            conformed_submission_type=4,
            conformed_period_of_report=datetime(2026, 9, 18),
            public_document_count=1,
            filed_as_of_date=date(2026, 9, 19),
            date_as_of_change=date(2026, 9, 19),
            # Reporting Owner Info
            company_conformed_name="Apple Inc.",
            reporting_owner_cik="0001234567",
            reporting_owner_isDirector=True,
            reporting_owner_isOfficer=False,
            reporting_owner_isTenPercentOwner=False,
            reporting_owner_isOther=False,
            reporting_owner_officer_title="",
            # Issuer Info
            issuer_company_conformed_name="Apple Inc.",
            issuer_cik="0000320193",
            issuer_sic="3571",
            issuer_organization_name="Apple Inc.",
            issuer_trading_symbol="AAPL",
        )

        self.test_filing_2 = Filing(
                    link="https://www.sec.gov/Archives/edgar/data/320194/example.xml",
                    # Document Info
                    acceptance_datetime=datetime(2025, 9, 19, 16, 32, 10),
                    conformed_submission_type=4,
                    conformed_period_of_report=datetime(2025, 9, 18),
                    public_document_count=1,
                    filed_as_of_date=date(2025, 9, 19),
                    date_as_of_change=date(2025, 9, 19),
                    # Reporting Owner Info
                    company_conformed_name="Test Inc.",
                    reporting_owner_cik="0001234567",
                    reporting_owner_isDirector=True,
                    reporting_owner_isOfficer=False,
                    reporting_owner_isTenPercentOwner=False,
                    reporting_owner_isOther=False,
                    reporting_owner_officer_title="",
                    # Issuer Info
                    issuer_company_conformed_name="Test Inc.",
                    issuer_cik="0000320194",
                    issuer_sic="3571",
                    issuer_organization_name="Test Inc.",
                    issuer_trading_symbol="TEST",
            )

        self.test_transaction_1 = InsiderTransaction(
                    issuer_trading_symbol="TEST",
                    security_title="Common Stock",
                    transaction_date=date(2025, 9, 18),
                    transaction_code="P",
                    equity_swap_involved=False,
                    transaction_shares=Decimal("500"),
                    transaction_price_per_share=Decimal("245.50"),
                    transaction_acquired_disposed_code="A",
                    shares_owned_following_transaction=Decimal("12500"),
                    direct_or_indirect_ownership="D",
                    nature_of_ownership=None,
                    filing_id=self.test_filing_1.id
            )

        self.test_transaction_2 = InsiderTransaction(
                            issuer_trading_symbol="AAPL",
                            security_title="Common Stock",
                            transaction_date=date(2026, 9, 18),
                            transaction_code="S",
                            equity_swap_involved=False,
                            transaction_shares=Decimal("200"),
                            transaction_price_per_share=Decimal("2.50"),
                            transaction_acquired_disposed_code="A",
                            shares_owned_following_transaction=Decimal("12500"),
                            direct_or_indirect_ownership="D",
                            nature_of_ownership=None,
                            filing_id=self.test_filing_2.id
                    )
