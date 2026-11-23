import time

from insider_trading.api.edgar.edgar_api_base import EdgarApiBase


class FetchTargetForms(EdgarApiBase):
    """
    Fetches target forms from the SEC EDGAR database.
    """

    def __init__(self) -> None:
        super().__init__()

    def fetch_forms(self, link_list: list[str]) -> list[str]:
        total_forms: int = len(link_list)

        if total_forms == 0:
            self.logger.warning("No SEC forms provided for fetching.")
            return []

        start_time = time.perf_counter()

        self.logger.info("Starting fetch of %s SEC forms.", total_forms)

        forms: list[str] = self.fetch_all(link_list)

        elapsed_time = time.perf_counter() - start_time

        average_time: float = elapsed_time / total_forms

        self.logger.info(
            "Successfully fetched %s of %s SEC forms.",
            len(forms),
            total_forms,
        )

        self.logger.info(
            "Finished fetching SEC forms in %.2f seconds.",
            elapsed_time,
        )

        self.logger.info(
            "Average time per requested form: %.2f seconds.",
            average_time,
        )

        return forms
