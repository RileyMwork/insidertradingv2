from dataclasses import dataclass, field
from datetime import date, datetime

from insider_trading.model.insider_transaction import InsiderTransaction


@dataclass(frozen=True)
class Filing:

    # Metadata fields
    id: int
    link: str

    # Document Info
    acceptance_datetime: datetime
    conformed_submission_type: int
    conformed_period_of_report: datetime
    public_document_count: int
    filed_as_of_date: date
    date_as_of_change: date

    # Reporting Owner Info
    company_conformed_name: str
    reporting_owner_cik: str
    reporting_owner_isDirector: bool
    reporting_owner_isOfficer: bool
    reporting_owner_isTenPercentOwner: bool
    reporting_owner_isOther: bool
    reporting_owner_officer_title: str

    # Issuer Info
    issuer_company_conformed_name: str
    issuer_cik: str
    issuer_sic: str
    issuer_organization_name: str
    issuer_trading_symbol: str

    # Transaction List
    transactions: tuple[InsiderTransaction, ...] = field(default_factory=tuple)