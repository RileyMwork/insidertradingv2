
import os

from dotenv import load_dotenv

from insider_trading.api.base_http_client import BaseHttpClient
from insider_trading.api.rate_limiter import RateLimiter

load_dotenv()

class EdgarApiBase(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://www.sec.gov/Archives/"
        self.sec_user_agent = os.getenv("SEC_USER_AGENT")
        self.client = BaseHttpClient(user_agent=os.getenv("SEC_USER_AGENT"), rate_limiter=RateLimiter(1), status_forcelist=[429, 500, 502, 503, 504])  # noqa: E501