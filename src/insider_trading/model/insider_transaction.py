from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class InsiderTransaction:
    issuer_trading_symbol: str
    security_title: str
    transaction_date: date
    transaction_code: str
    equity_swap_involved: bool
    transaction_shares: Decimal
    transaction_price_per_share: Decimal
    transaction_acquired_disposed_code: str
    shares_owned_following_transaction: Decimal
    direct_or_indirect_ownership: str
    nature_of_ownership: str | None
    filing_id: int