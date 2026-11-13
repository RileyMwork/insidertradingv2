
from datetime import date, datetime, timedelta

from insider_trading.api.edgar.edgar_api_base import EdgarApiBase


class FetchIndexFiles(EdgarApiBase):
    def __init__(self) -> None:
        super().__init__()
        self.base_endpoint = self.base_url + "edgar/daily-index/"

    def build_index_links(self, start_date: str | date, end_date: str | date, dates_to_exclude: list[str | date],) -> list[str]:  # noqa: E501
        def normalize(value: str | date) -> date:
            if isinstance(value, date):
                return value

            return datetime.strptime(value, "%Y-%m-%d").date()

        normalized_start_date = normalize(start_date)
        normalized_end_date = normalize(end_date)

        exclude_set = {normalize(value) for value in dates_to_exclude}

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

        return urls
