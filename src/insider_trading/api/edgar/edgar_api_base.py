import os

from dotenv import load_dotenv

from insider_trading.api.base_http_client import BaseHttpClient
from insider_trading.api.rate_limiter import RateLimiter

load_dotenv()


class EdgarApiBase(BaseHttpClient):
    def __init__(self) -> None:
        sec_user_agent = os.getenv("SEC_USER_AGENT")

        if not sec_user_agent:
            raise ValueError("SEC_USER_AGENT environment variable is not configured.")

        super().__init__(
            user_agent=sec_user_agent,
            rate_limiter=RateLimiter(1),
            status_forcelist=[429, 500, 502, 503, 504],
        )

        self.base_url = "https://www.sec.gov/Archives/"
