import logging

import pytest

from insider_trading.api.edgar.fetch_target_forms import FetchTargetForms

SEC_FORM_URLS: list[str] = [
    "https://www.sec.gov/Archives/edgar/data/100726/0001193125-26-470299.txt",
]


@pytest.fixture
def fetcher() -> FetchTargetForms:
    return FetchTargetForms()


def test_fetch_forms_returns_empty_list_when_no_links(
    fetcher: FetchTargetForms,
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING):
        result: list[str] = fetcher.fetch_forms([])

    assert result == []
    assert "No SEC forms provided for fetching." in caplog.text


def test_fetch_forms_fetches_real_sec_form(
    fetcher: FetchTargetForms,
) -> None:
    forms: list[str] = fetcher.fetch_forms(SEC_FORM_URLS)

    assert len(forms) == 1

    form: str = forms[0]

    assert "<SEC-DOCUMENT>" in form
    assert "<SEC-HEADER>" in form
    assert "0001193125-26-470299" in form
    assert "CONFORMED SUBMISSION TYPE:" in form
    assert "UNIFI INC" in form
    assert "<TYPE>4" in form


def test_fetch_forms_logs_successful_fetch(
    fetcher: FetchTargetForms,
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.INFO):
        forms: list[str] = fetcher.fetch_forms(SEC_FORM_URLS)

    assert len(forms) == 1
    assert "Starting fetch of 1 SEC forms." in caplog.text
    assert "Successfully fetched 1 of 1 SEC forms." in caplog.text
    assert "Finished fetching SEC forms in" in caplog.text
    assert "Average time per requested form:" in caplog.text
