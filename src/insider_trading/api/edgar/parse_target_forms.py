import datetime
import logging
import re
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation
from typing import Any


class ParseTargetForms:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def get_header_value(self, submission: str, field: str) -> str | None:
        """Extract a value from the SEC submission header."""
        pattern: str = rf"^{re.escape(field)}:\s*(.*?)\s*$"

        match: re.Match[str] | None = re.search(
            pattern,
            submission,
            flags=re.MULTILINE | re.IGNORECASE,
        )

        return match.group(1).strip() if match else None

    def get_acceptance_datetime(self, submission: str) -> str | None:
        """Extract acceptance datetime from the SEC submission."""
        match: re.Match[str] | None = re.search(
            r"<ACCEPTANCE-DATETIME>\s*(\d{14})",
            submission,
            flags=re.IGNORECASE,
        )

        if match is None:
            return None

        value: str = match.group(1)

        return f"{value[:4]}-{value[4:6]}-{value[6:8]}T{value[8:10]}:{value[10:12]}:{value[12:14]}"

    def get_text(self, element: ET.Element, path: str) -> str | None:
        """Extract XML element text."""
        result: ET.Element | None = element.find(path)

        if result is None or result.text is None:
            return None

        value: str = result.text.strip()

        return value or None

    def get_value(self, element: ET.Element, path: str) -> str | None:
        """Extract the value child of an XML element."""
        return self.get_text(element, f"{path}/value")

    def get_decimal(self, element: ET.Element, path: str) -> Decimal | None:
        """Extract an XML numeric value."""
        value: str | None = self.get_value(element, path)

        if value is None:
            return None

        try:
            return Decimal(value)
        except InvalidOperation:
            return None

    def get_bool(self, element: ET.Element, path: str) -> int:
        """Convert SEC XML boolean values to SQLite integers."""
        return int(self.get_text(element, path) == "1")

    def extract_primary_xml(self, submission: str) -> ET.Element:
        """Extract the primary Form 4 XML document."""
        documents: list[str] = re.findall(
            r"<DOCUMENT>(.*?)</DOCUMENT>",
            submission,
            flags=re.DOTALL | re.IGNORECASE,
        )

        for document in documents:
            type_match: re.Match[str] | None = re.search(
                r"<TYPE>\s*([^\r\n<]+)",
                document,
                flags=re.IGNORECASE,
            )

            if type_match is None:
                continue

            if type_match.group(1).strip().upper() not in {"4", "4/A"}:
                continue

            xml_match: re.Match[str] | None = re.search(
                r"<XML>\s*(.*?)\s*</XML>",
                document,
                flags=re.DOTALL | re.IGNORECASE,
            )

            if xml_match is None:
                continue

            return ET.fromstring(xml_match.group(1).strip())

        raise ValueError("Primary Form 4 XML document not found.")

    def parse_reporting_owner(self, root: ET.Element) -> dict[str, Any]:
        """Extract the first reporting owner."""
        owner: ET.Element | None = root.find("reportingOwner")

        if owner is None:
            raise ValueError("Reporting owner information not found.")

        return {
            "company_conformed_name": self.get_text(owner, "reportingOwnerId/rptOwnerName"),
            "reporting_owner_cik": self.get_text(owner, "reportingOwnerId/rptOwnerCik"),
            "reporting_owner_isDirector": self.get_bool(
                owner, "reportingOwnerRelationship/isDirector"
            ),
            "reporting_owner_isOfficer": self.get_bool(
                owner, "reportingOwnerRelationship/isOfficer"
            ),
            "reporting_owner_isTenPercentOwner": self.get_bool(
                owner, "reportingOwnerRelationship/isTenPercentOwner"
            ),
            "reporting_owner_isOther": self.get_bool(owner, "reportingOwnerRelationship/isOther"),
            "reporting_owner_officer_title": self.get_text(
                owner, "reportingOwnerRelationship/officerTitle"
            ),
        }

    def parse_issuer(self, root: ET.Element) -> dict[str, Any]:
        """Extract issuer information."""
        issuer: ET.Element | None = root.find("issuer")

        if issuer is None:
            raise ValueError("Issuer information not found.")

        return {
            "issuer_company_conformed_name": self.get_text(issuer, "issuerName"),
            "issuer_cik": self.get_text(issuer, "issuerCik"),
            "issuer_sic": None,
            "issuer_organization_name": None,
            "issuer_trading_symbol": self.get_text(issuer, "issuerTradingSymbol"),
        }

    def parse_transactions(
        self,
        root: ET.Element,
        issuer_trading_symbol: str | None,
    ) -> list[dict[str, Any]]:
        """Extract non-derivative transactions."""
        transactions: list[dict[str, Any]] = []

        for transaction in root.findall("nonDerivativeTable/nonDerivativeTransaction"):
            transaction_data: dict[str, Any] = {
                "issuer_trading_symbol": issuer_trading_symbol,
                "security_title": self.get_value(transaction, "securityTitle"),
                "transaction_date": self.get_value(transaction, "transactionDate"),
                "transaction_code": self.get_text(transaction, "transactionCoding/transactionCode"),
                "equity_swap_involved": self.get_bool(
                    transaction, "transactionCoding/equitySwapInvolved"
                ),
                "transaction_shares": self.get_decimal(
                    transaction, "transactionAmounts/transactionShares"
                ),
                "transaction_price_per_share": self.get_decimal(
                    transaction,
                    "transactionAmounts/transactionPricePerShare",
                ),
                "transaction_acquired_disposed_code": self.get_value(
                    transaction,
                    "transactionAmounts/transactionAcquiredDisposedCode",
                ),
                "shares_owned_following_transaction": self.get_decimal(
                    transaction,
                    "postTransactionAmounts/sharesOwnedFollowingTransaction",
                ),
                "direct_or_indirect_ownership": self.get_value(
                    transaction,
                    "ownershipNature/directOrIndirectOwnership",
                ),
                "nature_of_ownership": self.get_value(
                    transaction, "ownershipNature/natureOfOwnership"
                ),
            }

            transactions.append(transaction_data)

        return transactions

    def parse_form_four(self, submission: str, link: str) -> dict[str, Any]:
        """Parse an SEC Form 4 submission into filing and transaction data."""
        root: ET.Element = self.extract_primary_xml(submission)

        issuer_data: dict[str, Any] = self.parse_issuer(root)
        owner_data: dict[str, Any] = self.parse_reporting_owner(root)

        filing_data: dict[str, Any] = {
            "link": link,
            "date_entered_into_db": datetime.date.today().isoformat(),
            # Document information
            "acceptance_datetime": self.get_acceptance_datetime(submission),
            "conformed_submission_type": self.get_header_value(
                submission, "CONFORMED SUBMISSION TYPE"
            ),
            "conformed_period_of_report": self.get_text(root, "periodOfReport"),
            "public_document_count": self.get_header_value(submission, "PUBLIC DOCUMENT COUNT"),
            "filed_as_of_date": self.get_header_value(submission, "FILED AS OF DATE"),
            "date_as_of_change": self.get_header_value(submission, "DATE AS OF CHANGE"),
            # Reporting owner information
            **owner_data,
            # Issuer information
            **issuer_data,
        }

        transactions: list[dict[str, Any]] = self.parse_transactions(
            root,
            issuer_data["issuer_trading_symbol"],
        )

        return {
            "filing": filing_data,
            "transactions": transactions,
        }
