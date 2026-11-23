import time

from insider_trading.api.edgar.edgar_api_base import EdgarApiBase


class FetchTargetForms(EdgarApiBase):
    """
    Fetches target forms from the SEC EDGAR database.
    """

    def __init__(self) -> None:
        super().__init__()

    def fetch_forms(self, link_list: list[str]) -> list[str]:
        start_time = time.time()
        print(f"Fetching {len(link_list)} forms")
        forms = self.fetch_all(link_list)
        end_time = time.time()
        print(f"Successfully fetched {len(forms)} forms")
        print(f"Finished fetching forms in {end_time - start_time:.2f} seconds")
        print(f"Average time per form: {(end_time - start_time) / len(forms):.2f} seconds")
        return forms