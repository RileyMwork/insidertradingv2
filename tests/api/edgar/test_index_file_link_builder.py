
from datetime import date

import pytest

from insider_trading.api.edgar.fetch_index_files import FetchIndexFiles


class TestFetchIndexFiles:
    builder: FetchIndexFiles

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.builder = FetchIndexFiles()

    def test_build_index_links_with_string_dates(self) -> None:
        start_date = "2026-10-05"
        end_date = "2026-10-09"

        actual_urls = self.builder.build_index_links(
            start_date,
            end_date,
            [],
        )

        expected_urls = [
            f"{self.builder.base_endpoint}2026/QTR4/master.20261005.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261006.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261007.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261008.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261009.idx",
        ]

        assert actual_urls == expected_urls

    def test_build_index_links_with_date_objects(self) -> None:
        start_date = date(2026, 10, 5)
        end_date = date(2026, 10, 7)

        actual_urls = self.builder.build_index_links(
            start_date,
            end_date,
            [],
        )

        expected_urls = [
            f"{self.builder.base_endpoint}2026/QTR4/master.20261005.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261006.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261007.idx",
        ]

        assert actual_urls == expected_urls

    def test_build_index_links_excludes_string_dates(self) -> None:
        start_date = "2026-10-05"
        end_date = "2026-10-09"
        dates_to_exclude: list[str | date] = [
            "2026-10-06",
            "2026-10-08",
        ]

        actual_urls = self.builder.build_index_links(
            start_date,
            end_date,
            dates_to_exclude,
        )

        expected_urls = [
            f"{self.builder.base_endpoint}2026/QTR4/master.20261005.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261007.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261009.idx",
        ]

        assert actual_urls == expected_urls

    def test_build_index_links_excludes_date_objects(self) -> None:
        start_date = date(2026, 10, 5)
        end_date = date(2026, 10, 9)
        dates_to_exclude: list[str | date] = [
            date(2026, 10, 6),
            date(2026, 10, 8),
        ]

        actual_urls = self.builder.build_index_links(
            start_date,
            end_date,
            dates_to_exclude,
        )

        expected_urls = [
            f"{self.builder.base_endpoint}2026/QTR4/master.20261005.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261007.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261009.idx",
        ]

        assert actual_urls == expected_urls

    def test_build_index_links_skips_weekends(self) -> None:
        # Friday through Monday
        start_date = "2026-10-09"
        end_date = "2026-10-12"

        actual_urls = self.builder.build_index_links(
            start_date,
            end_date,
            [],
        )

        expected_urls = [
            f"{self.builder.base_endpoint}2026/QTR4/master.20261009.idx",
            f"{self.builder.base_endpoint}2026/QTR4/master.20261012.idx",
        ]

        assert actual_urls == expected_urls

    @pytest.mark.parametrize(
        ("input_date", "expected_quarter"),
        [
            ("2026-01-15", "QTR1"),
            ("2026-04-15", "QTR2"),
            ("2026-07-15", "QTR3"),
            ("2026-10-15", "QTR4"),
        ],
    )
    def test_build_index_links_uses_correct_quarter(
        self,
        input_date: str,
        expected_quarter: str,
    ) -> None:
        actual_urls = self.builder.build_index_links(
            input_date,
            input_date,
            [],
        )

        expected_url = (
            f"{self.builder.base_endpoint}2026/{expected_quarter}/"
            f"master.{input_date.replace('-', '')}.idx"
        )

        assert actual_urls == [expected_url]

    def test_build_index_links_returns_empty_list_when_start_after_end(
        self,
    ) -> None:
        actual_urls = self.builder.build_index_links(
            "2026-10-10",
            "2026-10-05",
            [],
        )

        assert actual_urls == []

    def test_build_index_links_returns_empty_list_for_weekend_only_range(
        self,
    ) -> None:
        # Saturday and Sunday
        actual_urls = self.builder.build_index_links(
            "2026-10-10",
            "2026-10-11",
            [],
        )

        assert actual_urls == []

    def test_build_index_links_raises_value_error_for_invalid_date(self) -> None:
        with pytest.raises(ValueError):
            self.builder.build_index_links(
                "invalid-date",
                "2026-10-09",
                [],
            )

    def test_build_index_links_with_same_start_and_end_date(self) -> None:
        input_date = "2026-10-05"

        actual_urls = self.builder.build_index_links(
            input_date,
            input_date,
            [],
        )

        expected_urls = [
            f"{self.builder.base_endpoint}2026/QTR4/master.20261005.idx",
        ]

        assert actual_urls == expected_urls
        assert len(actual_urls) == 1
