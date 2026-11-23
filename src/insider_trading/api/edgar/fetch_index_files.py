import logging
from datetime import date, datetime, timedelta

import requests

from insider_trading.api.edgar.edgar_api_base import EdgarApiBase


class FetchIndexFiles(EdgarApiBase):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.base_endpoint = self.base_url + "edgar/daily-index/"

    def build_index_links(
        self,
        start_date: str | date,
        end_date: str | date,
        dates_to_exclude: list[str | date],
    ) -> list[str]:
        self.logger.info(
            "Building SEC index links from %s to %s.",
            start_date,
            end_date,
        )

        self.logger.debug(
            "Dates excluded from index link generation: %s",
            dates_to_exclude,
        )

        def normalize(value: str | date) -> date:
            if isinstance(value, date):
                return value

            return datetime.strptime(value, "%Y-%m-%d").date()

        normalized_start_date = normalize(start_date)
        normalized_end_date = normalize(end_date)

        exclude_set: set[date] = {normalize(value) for value in dates_to_exclude}

        current_date = normalized_start_date
        urls: list[str] = []

        while current_date <= normalized_end_date:
            if current_date.weekday() < 5 and current_date not in exclude_set:
                quarter = (current_date.month - 1) // 3 + 1

                url = (
                    f"{self.base_endpoint}"
                    f"{current_date.year}/QTR{quarter}/"
                    f"master.{current_date.strftime('%Y%m%d')}.idx"
                )

                urls.append(url)

            current_date += timedelta(days=1)

        self.logger.info(
            "Generated %s SEC index links.",
            len(urls),
        )

        return urls

    def fetch_index_file(self, url: str) -> str:
        self.logger.info("Fetching SEC index file: %s", url)

        try:
            response = self.get(url)
            response.raise_for_status()

            self.logger.debug(
                "Successfully fetched SEC index file: %s",
                url,
            )

            return response.text

        except requests.RequestException:
            self.logger.exception(
                "Failed to fetch SEC index file: %s",
                url,
            )
            raise

    def fetch_index_files(
        self,
        urls: list[str],
        raise_on_error: bool = False,
    ) -> dict[str, str]:
        """
        Fetch multiple index files concurrently.

        Args:
            urls: URLs of the SEC index files.
            raise_on_error: Whether to raise an exception if a request fails.

        Returns:
            Dictionary mapping URLs to their index file contents.
        """
        if not urls:
            self.logger.warning("No SEC index file URLs provided for fetching.")
            return {}

        self.logger.info(
            "Starting concurrent fetch of %s SEC index files.",
            len(urls),
        )

        results: list[tuple[str, str]] = self.fetch_all(
            urls,
            processor=lambda response: (response.url, response.text),
            raise_on_error=raise_on_error,
        )

        index_files: dict[str, str] = dict(results)

        self.logger.info(
            "Retrieved %s of %s SEC index files.",
            len(index_files),
            len(urls),
        )

        return index_files

    def fetch_index_files_for_date_range(
        self,
        start_date: str | date,
        end_date: str | date,
        dates_to_exclude: list[str | date],
    ) -> dict[str, str]:
        self.logger.info(
            "Fetching SEC index files for date range %s through %s.",
            start_date,
            end_date,
        )

        urls = self.build_index_links(
            start_date,
            end_date,
            dates_to_exclude,
        )

        return self.fetch_index_files(urls)

    def get_latest_index_file(self, max_days_back: int = 7) -> str:
        """
        Fetch the most recent available index file.

        Starts with today's date and works backward, skipping weekends.
        """
        if max_days_back < 0:
            self.logger.error(
                "Invalid max_days_back value: %s",
                max_days_back,
            )
            raise ValueError("max_days_back cannot be negative")

        current_date = date.today()
        last_error: requests.HTTPError | None = None

        self.logger.info(
            "Searching for the latest SEC index file within the last %s days.",
            max_days_back,
        )

        for days_back in range(max_days_back + 1):
            target_date = current_date - timedelta(days=days_back)

            if target_date.weekday() >= 5:
                self.logger.debug(
                    "Skipping %s because it falls on a weekend.",
                    target_date,
                )
                continue

            quarter = (target_date.month - 1) // 3 + 1

            url = (
                f"{self.base_endpoint}"
                f"{target_date.year}/QTR{quarter}/"
                f"master.{target_date.strftime('%Y%m%d')}.idx"
            )

            try:
                self.logger.info(
                    "Attempting to fetch SEC index file for %s.",
                    target_date,
                )

                index_file_content = self.fetch_index_file(url)

                self.logger.info(
                    "Successfully fetched SEC index file for %s.",
                    target_date,
                )

                return index_file_content

            except requests.HTTPError as error:
                status_code = error.response.status_code if error.response is not None else None

                if status_code not in (403, 404):
                    self.logger.exception(
                        "Unexpected HTTP error while fetching index file for %s.",
                        target_date,
                    )
                    raise

                self.logger.warning(
                    "SEC index file request for %s returned HTTP %s. Trying an earlier date.",
                    target_date,
                    status_code,
                )

                last_error = error

        if last_error is not None:
            self.logger.error(
                "No accessible SEC index file found within the last %s days.",
                max_days_back,
            )
            raise last_error

        self.logger.error(
            "No SEC index file found within the last %s days.",
            max_days_back,
        )

        raise FileNotFoundError(f"No index file found within the last {max_days_back} days.")
