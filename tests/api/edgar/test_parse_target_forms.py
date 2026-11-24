import datetime
import xml.etree.ElementTree as ET
from decimal import Decimal
from typing import Any

import pytest

from insider_trading.api.edgar.parse_target_forms import ParseTargetForms

FORM4_SUBMISSION: str = """<SEC-DOCUMENT>0000070858-26-000602.txt : 20261120
<SEC-HEADER>
ACCESSION NUMBER: 0000070858-26-000602
CONFORMED SUBMISSION TYPE: 4
PUBLIC DOCUMENT COUNT: 2
CONFORMED PERIOD OF REPORT: 20261118
FILED AS OF DATE: 20261120
DATE AS OF CHANGE: 20261120
<ACCEPTANCE-DATETIME>20261120142534
</SEC-HEADER>

<DOCUMENT>
<TYPE>EX-99
<SEQUENCE>2
<FILENAME>jfa.txt
<DESCRIPTION>JOINT FILING AGREEMENT
<TEXT>
Joint Filing Agreement
</TEXT>
</DOCUMENT>

<DOCUMENT>
<TYPE>4
<SEQUENCE>1
<FILENAME>primary_doc.xml
<DESCRIPTION>PRIMARY DOCUMENT
<TEXT>
<XML>
<?xml version="1.0" encoding="UTF-8"?>
<ownershipDocument>
    <schemaVersion>X0609</schemaVersion>
    <documentType>4</documentType>
    <periodOfReport>2026-11-18</periodOfReport>

    <issuer>
        <issuerCik>0001178839</issuerCik>
        <issuerName>Neuberger Municipal Fund Inc.</issuerName>
        <issuerTradingSymbol>NBH</issuerTradingSymbol>
    </issuer>

    <reportingOwner>
        <reportingOwnerId>
            <rptOwnerCik>0000070858</rptOwnerCik>
            <rptOwnerName>Bank of America</rptOwnerName>
        </reportingOwnerId>
        <reportingOwnerAddress>
            <rptOwnerStreet1>100 North Tryon Street</rptOwnerStreet1>
            <rptOwnerCity>Charlotte</rptOwnerCity>
            <rptOwnerState>NC</rptOwnerState>
            <rptOwnerZipCode>28255</rptOwnerZipCode>
        </reportingOwnerAddress>
        <reportingOwnerRelationship>
            <isDirector>0</isDirector>
            <isOfficer>0</isOfficer>
            <isTenPercentOwner>1</isTenPercentOwner>
            <isOther>0</isOther>
        </reportingOwnerRelationship>
    </reportingOwner>

    <reportingOwner>
        <reportingOwnerId>
            <rptOwnerCik>0000728612</rptOwnerCik>
            <rptOwnerName>Merrill Lynch</rptOwnerName>
        </reportingOwnerId>
        <reportingOwnerAddress>
            <rptOwnerStreet1>One Bryant Park</rptOwnerStreet1>
            <rptOwnerCity>New York</rptOwnerCity>
            <rptOwnerState>NY</rptOwnerState>
            <rptOwnerZipCode>10036</rptOwnerZipCode>
        </reportingOwnerAddress>
        <reportingOwnerRelationship>
            <isDirector>0</isDirector>
            <isOfficer>0</isOfficer>
            <isTenPercentOwner>1</isTenPercentOwner>
            <isOther>0</isOther>
        </reportingOwnerRelationship>
    </reportingOwner>

    <nonDerivativeTable>
        <nonDerivativeTransaction>
            <securityTitle>
                <value>Common Stock</value>
            </securityTitle>
            <transactionDate>
                <value>2026-11-18</value>
            </transactionDate>
            <transactionCoding>
                <transactionCode>P</transactionCode>
                <equitySwapInvolved>0</equitySwapInvolved>
            </transactionCoding>
            <transactionAmounts>
                <transactionShares>
                    <value>288</value>
                </transactionShares>
                <transactionPricePerShare>
                    <value>9.135</value>
                </transactionPricePerShare>
                <transactionAcquiredDisposedCode>
                    <value>A</value>
                </transactionAcquiredDisposedCode>
            </transactionAmounts>
            <postTransactionAmounts>
                <sharesOwnedFollowingTransaction>
                    <value>288</value>
                </sharesOwnedFollowingTransaction>
            </postTransactionAmounts>
            <ownershipNature>
                <directOrIndirectOwnership>
                    <value>I</value>
                </directOrIndirectOwnership>
                <natureOfOwnership>
                    <value>See footnotes</value>
                </natureOfOwnership>
            </ownershipNature>
        </nonDerivativeTransaction>

        <nonDerivativeTransaction>
            <securityTitle>
                <value>Common Stock</value>
            </securityTitle>
            <transactionDate>
                <value>2026-11-18</value>
            </transactionDate>
            <transactionCoding>
                <transactionCode>S</transactionCode>
                <equitySwapInvolved>0</equitySwapInvolved>
            </transactionCoding>
            <transactionAmounts>
                <transactionShares>
                    <value>188</value>
                </transactionShares>
                <transactionPricePerShare>
                    <value>9.11</value>
                </transactionPricePerShare>
                <transactionAcquiredDisposedCode>
                    <value>D</value>
                </transactionAcquiredDisposedCode>
            </transactionAmounts>
            <postTransactionAmounts>
                <sharesOwnedFollowingTransaction>
                    <value>100</value>
                </sharesOwnedFollowingTransaction>
            </postTransactionAmounts>
            <ownershipNature>
                <directOrIndirectOwnership>
                    <value>I</value>
                </directOrIndirectOwnership>
            </ownershipNature>
        </nonDerivativeTransaction>

        <nonDerivativeTransaction>
            <securityTitle>
                <value>Common Stock</value>
            </securityTitle>
            <transactionDate>
                <value>2026-11-18</value>
            </transactionDate>
            <transactionCoding>
                <transactionCode>S</transactionCode>
                <equitySwapInvolved>0</equitySwapInvolved>
            </transactionCoding>
            <transactionAmounts>
                <transactionShares>
                    <value>100</value>
                </transactionShares>
                <transactionPricePerShare>
                    <value>9.11</value>
                </transactionPricePerShare>
                <transactionAcquiredDisposedCode>
                    <value>D</value>
                </transactionAcquiredDisposedCode>
            </transactionAmounts>
            <postTransactionAmounts>
                <sharesOwnedFollowingTransaction>
                    <value>0</value>
                </sharesOwnedFollowingTransaction>
            </postTransactionAmounts>
            <ownershipNature>
                <directOrIndirectOwnership>
                    <value>I</value>
                </directOrIndirectOwnership>
            </ownershipNature>
        </nonDerivativeTransaction>
    </nonDerivativeTable>

    <footnotes>
        <footnote id="F1">Transaction executed pursuant to joint filing.</footnote>
        <footnote id="F2">Shares held indirectly.</footnote>
        <footnote id="F3">See additional ownership information.</footnote>
    </footnotes>

    <ownerSignature>
        <signatureName>Bank of America</signatureName>
        <signatureDate>2026-11-20</signatureDate>
    </ownerSignature>

    <ownerSignature>
        <signatureName>Merrill Lynch</signatureName>
        <signatureDate>2026-11-20</signatureDate>
    </ownerSignature>
</ownershipDocument>
</XML>
</TEXT>
</DOCUMENT>
</SEC-DOCUMENT>
"""


@pytest.fixture
def parser() -> ParseTargetForms:
    return ParseTargetForms()


# ---------------------------------------------------------------------------
# get_header_value
# ---------------------------------------------------------------------------


def test_get_header_value_returns_value(
    parser: ParseTargetForms,
) -> None:
    result: str | None = parser.get_header_value(
        FORM4_SUBMISSION,
        "CONFORMED SUBMISSION TYPE",
    )

    assert result == "4"


def test_get_header_value_handles_whitespace(
    parser: ParseTargetForms,
) -> None:
    submission: str = "FILED AS OF DATE:    20261120   \n"

    result: str | None = parser.get_header_value(
        submission,
        "FILED AS OF DATE",
    )

    assert result == "20261120"


def test_get_header_value_is_case_insensitive(
    parser: ParseTargetForms,
) -> None:
    submission: str = "filed as of date: 20261120\n"

    result: str | None = parser.get_header_value(
        submission,
        "FILED AS OF DATE",
    )

    assert result == "20261120"


def test_get_header_value_returns_none_when_missing(
    parser: ParseTargetForms,
) -> None:
    result: str | None = parser.get_header_value(
        FORM4_SUBMISSION,
        "MISSING FIELD",
    )

    assert result is None


# ---------------------------------------------------------------------------
# get_acceptance_datetime
# ---------------------------------------------------------------------------


def test_get_acceptance_datetime_returns_formatted_datetime(
    parser: ParseTargetForms,
) -> None:
    result: str | None = parser.get_acceptance_datetime(FORM4_SUBMISSION)

    assert result == "2026-11-20T14:25:34"


def test_get_acceptance_datetime_returns_none_when_missing(
    parser: ParseTargetForms,
) -> None:
    result: str | None = parser.get_acceptance_datetime("<SEC-HEADER></SEC-HEADER>")

    assert result is None


# ---------------------------------------------------------------------------
# get_text
# ---------------------------------------------------------------------------


def test_get_text_returns_element_text(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><name>Bank of America</name></root>")

    result: str | None = parser.get_text(element, "name")

    assert result == "Bank of America"


def test_get_text_strips_whitespace(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><name>  Bank of America  </name></root>")

    result: str | None = parser.get_text(element, "name")

    assert result == "Bank of America"


def test_get_text_returns_none_when_element_missing(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root></root>")

    result: str | None = parser.get_text(element, "name")

    assert result is None


def test_get_text_returns_none_when_element_empty(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><name></name></root>")

    result: str | None = parser.get_text(element, "name")

    assert result is None


# ---------------------------------------------------------------------------
# get_value
# ---------------------------------------------------------------------------


def test_get_value_returns_nested_value(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring(
        "<root><securityTitle><value>Common Stock</value></securityTitle></root>"
    )

    result: str | None = parser.get_value(element, "securityTitle")

    assert result == "Common Stock"


def test_get_value_returns_none_when_value_missing(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><securityTitle></securityTitle></root>")

    result: str | None = parser.get_value(element, "securityTitle")

    assert result is None


# ---------------------------------------------------------------------------
# get_decimal
# ---------------------------------------------------------------------------


def test_get_decimal_returns_decimal(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><shares><value>288.50</value></shares></root>")

    result: Decimal | None = parser.get_decimal(element, "shares")

    assert result == Decimal("288.50")


def test_get_decimal_returns_none_when_value_missing(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root></root>")

    result: Decimal | None = parser.get_decimal(element, "shares")

    assert result is None


def test_get_decimal_returns_none_for_invalid_value(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><shares><value>invalid</value></shares></root>")

    result: Decimal | None = parser.get_decimal(element, "shares")

    assert result is None


# ---------------------------------------------------------------------------
# get_bool
# ---------------------------------------------------------------------------


def test_get_bool_returns_one_for_true(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><isDirector>1</isDirector></root>")

    result: int = parser.get_bool(element, "isDirector")

    assert result == 1


def test_get_bool_returns_zero_for_false(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root><isDirector>0</isDirector></root>")

    result: int = parser.get_bool(element, "isDirector")

    assert result == 0


def test_get_bool_returns_zero_when_missing(
    parser: ParseTargetForms,
) -> None:
    element: ET.Element = ET.fromstring("<root></root>")

    result: int = parser.get_bool(element, "isDirector")

    assert result == 0


# ---------------------------------------------------------------------------
# extract_primary_xml
# ---------------------------------------------------------------------------


def test_extract_primary_xml_returns_primary_form_four(
    parser: ParseTargetForms,
) -> None:
    result: ET.Element = parser.extract_primary_xml(FORM4_SUBMISSION)

    assert result.tag == "ownershipDocument"
    assert result.findtext("documentType") == "4"


def test_extract_primary_xml_ignores_exhibit_document(
    parser: ParseTargetForms,
) -> None:
    result: ET.Element = parser.extract_primary_xml(FORM4_SUBMISSION)

    assert result.find("issuer") is not None
    assert result.find("reportingOwner") is not None


def test_extract_primary_xml_raises_when_form_four_missing(
    parser: ParseTargetForms,
) -> None:
    submission: str = """
    <DOCUMENT>
        <TYPE>EX-99</TYPE>
        <TEXT>Exhibit document</TEXT>
    </DOCUMENT>
    """

    with pytest.raises(
        ValueError,
        match="Primary Form 4 XML document not found",
    ):
        parser.extract_primary_xml(submission)


def test_extract_primary_xml_raises_when_xml_invalid(
    parser: ParseTargetForms,
) -> None:
    submission: str = """
    <DOCUMENT>
        <TYPE>4</TYPE>
        <XML><ownershipDocument></XML>
    </DOCUMENT>
    """

    with pytest.raises(ET.ParseError):
        parser.extract_primary_xml(submission)


# ---------------------------------------------------------------------------
# parse_reporting_owner
# ---------------------------------------------------------------------------


def test_parse_reporting_owner_returns_first_owner(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = parser.extract_primary_xml(FORM4_SUBMISSION)

    result: dict[str, Any] = parser.parse_reporting_owner(root)

    assert result == {
        "company_conformed_name": "Bank of America",
        "reporting_owner_cik": "0000070858",
        "reporting_owner_isDirector": 0,
        "reporting_owner_isOfficer": 0,
        "reporting_owner_isTenPercentOwner": 1,
        "reporting_owner_isOther": 0,
        "reporting_owner_officer_title": None,
    }


def test_parse_reporting_owner_raises_when_missing(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = ET.fromstring("<ownershipDocument></ownershipDocument>")

    with pytest.raises(
        ValueError,
        match="Reporting owner information not found",
    ):
        parser.parse_reporting_owner(root)


# ---------------------------------------------------------------------------
# parse_issuer
# ---------------------------------------------------------------------------


def test_parse_issuer_returns_issuer_information(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = parser.extract_primary_xml(FORM4_SUBMISSION)

    result: dict[str, Any] = parser.parse_issuer(root)

    assert result == {
        "issuer_company_conformed_name": "Neuberger Municipal Fund Inc.",
        "issuer_cik": "0001178839",
        "issuer_sic": None,
        "issuer_organization_name": None,
        "issuer_trading_symbol": "NBH",
    }


def test_parse_issuer_raises_when_missing(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = ET.fromstring("<ownershipDocument></ownershipDocument>")

    with pytest.raises(
        ValueError,
        match="Issuer information not found",
    ):
        parser.parse_issuer(root)


# ---------------------------------------------------------------------------
# parse_transactions
# ---------------------------------------------------------------------------


def test_parse_transactions_returns_all_transactions(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = parser.extract_primary_xml(FORM4_SUBMISSION)

    result: list[dict[str, Any]] = parser.parse_transactions(
        root,
        "NBH",
    )

    assert len(result) == 3


def test_parse_transactions_returns_purchase_transaction(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = parser.extract_primary_xml(FORM4_SUBMISSION)

    result: list[dict[str, Any]] = parser.parse_transactions(
        root,
        "NBH",
    )

    transaction: dict[str, Any] = result[0]

    assert transaction == {
        "issuer_trading_symbol": "NBH",
        "security_title": "Common Stock",
        "transaction_date": "2026-11-18",
        "transaction_code": "P",
        "equity_swap_involved": 0,
        "transaction_shares": Decimal("288"),
        "transaction_price_per_share": Decimal("9.135"),
        "transaction_acquired_disposed_code": "A",
        "shares_owned_following_transaction": Decimal("288"),
        "direct_or_indirect_ownership": "I",
        "nature_of_ownership": "See footnotes",
    }


def test_parse_transactions_returns_sale_transactions(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = parser.extract_primary_xml(FORM4_SUBMISSION)

    result: list[dict[str, Any]] = parser.parse_transactions(
        root,
        "NBH",
    )

    first_sale: dict[str, Any] = result[1]
    second_sale: dict[str, Any] = result[2]

    assert first_sale["transaction_code"] == "S"
    assert first_sale["transaction_shares"] == Decimal("188")
    assert first_sale["transaction_price_per_share"] == Decimal("9.11")
    assert first_sale["transaction_acquired_disposed_code"] == "D"
    assert first_sale["shares_owned_following_transaction"] == Decimal("100")

    assert second_sale["transaction_code"] == "S"
    assert second_sale["transaction_shares"] == Decimal("100")
    assert second_sale["transaction_price_per_share"] == Decimal("9.11")
    assert second_sale["transaction_acquired_disposed_code"] == "D"
    assert second_sale["shares_owned_following_transaction"] == Decimal("0")


def test_parse_transactions_returns_empty_list_when_missing(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = ET.fromstring("<ownershipDocument></ownershipDocument>")

    result: list[dict[str, Any]] = parser.parse_transactions(
        root,
        "NBH",
    )

    assert result == []


def test_parse_transactions_handles_missing_nature_of_ownership(
    parser: ParseTargetForms,
) -> None:
    root: ET.Element = ET.fromstring(
        """
        <ownershipDocument>
            <nonDerivativeTable>
                <nonDerivativeTransaction>
                    <securityTitle><value>Common Stock</value></securityTitle>
                    <transactionDate><value>2026-11-18</value></transactionDate>
                    <transactionCoding>
                        <transactionCode>P</transactionCode>
                        <equitySwapInvolved>0</equitySwapInvolved>
                    </transactionCoding>
                    <transactionAmounts>
                        <transactionShares><value>10</value></transactionShares>
                        <transactionPricePerShare><value>5.00</value></transactionPricePerShare>
                        <transactionAcquiredDisposedCode><value>A</value></transactionAcquiredDisposedCode>
                    </transactionAmounts>
                    <postTransactionAmounts>
                        <sharesOwnedFollowingTransaction><value>10</value></sharesOwnedFollowingTransaction>
                    </postTransactionAmounts>
                    <ownershipNature>
                        <directOrIndirectOwnership><value>D</value></directOrIndirectOwnership>
                    </ownershipNature>
                </nonDerivativeTransaction>
            </nonDerivativeTable>
        </ownershipDocument>
        """
    )

    result: list[dict[str, Any]] = parser.parse_transactions(
        root,
        "NBH",
    )

    assert len(result) == 1
    assert result[0]["nature_of_ownership"] is None


# ---------------------------------------------------------------------------
# parse_form_four
# ---------------------------------------------------------------------------


def test_parse_form_four_returns_filing_and_transactions(
    parser: ParseTargetForms,
) -> None:
    link: str = "https://www.sec.gov/Archives/edgar/data/1178839/000007085826000602/"

    result: dict[str, Any] = parser.parse_form_four(
        FORM4_SUBMISSION,
        link,
    )

    filing: dict[str, Any] = result["filing"]
    transactions: list[dict[str, Any]] = result["transactions"]

    assert filing["link"] == link
    assert filing["acceptance_datetime"] == "2026-11-20T14:25:34"
    assert filing["conformed_submission_type"] == "4"
    assert filing["conformed_period_of_report"] == "2026-11-18"
    assert filing["public_document_count"] == "2"
    assert filing["filed_as_of_date"] == "20261120"
    assert filing["date_as_of_change"] == "20261120"

    assert filing["company_conformed_name"] == "Bank of America"
    assert filing["reporting_owner_cik"] == "0000070858"
    assert filing["reporting_owner_isDirector"] == 0
    assert filing["reporting_owner_isOfficer"] == 0
    assert filing["reporting_owner_isTenPercentOwner"] == 1
    assert filing["reporting_owner_isOther"] == 0
    assert filing["reporting_owner_officer_title"] is None

    assert filing["issuer_company_conformed_name"] == ("Neuberger Municipal Fund Inc.")
    assert filing["issuer_cik"] == "0001178839"
    assert filing["issuer_sic"] is None
    assert filing["issuer_organization_name"] is None
    assert filing["issuer_trading_symbol"] == "NBH"

    assert len(transactions) == 3


def test_parse_form_four_sets_date_entered_into_db(
    parser: ParseTargetForms,
) -> None:
    result: dict[str, Any] = parser.parse_form_four(
        FORM4_SUBMISSION,
        "https://www.sec.gov/example",
    )

    expected_date: str = datetime.date.today().isoformat()

    assert result["filing"]["date_entered_into_db"] == expected_date


def test_parse_form_four_uses_first_reporting_owner(
    parser: ParseTargetForms,
) -> None:
    result: dict[str, Any] = parser.parse_form_four(
        FORM4_SUBMISSION,
        "https://www.sec.gov/example",
    )

    filing: dict[str, Any] = result["filing"]

    assert filing["company_conformed_name"] == "Bank of America"
    assert filing["reporting_owner_cik"] == "0000070858"


def test_parse_form_four_raises_when_xml_missing(
    parser: ParseTargetForms,
) -> None:
    submission: str = """
    <DOCUMENT>
        <TYPE>EX-99</TYPE>
        <TEXT>Exhibit</TEXT>
    </DOCUMENT>
    """

    with pytest.raises(
        ValueError,
        match="Primary Form 4 XML document not found",
    ):
        parser.parse_form_four(
            submission,
            "https://www.sec.gov/example",
        )
