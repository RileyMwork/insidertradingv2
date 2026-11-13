
import threading
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseHttpClient:
    def __init__(
        self,
        user_agent: str | None = None,
        headers: dict[str, str] | None = None,
        rate_limiter: Any | None = None,
        retries: int = 3,
        backoff_factor: float = 1.5,
        status_forcelist: list[int] | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.session = requests.Session()

        if user_agent:
            self.session.headers["User-Agent"] = user_agent

        if headers:
            self.session.headers.update(headers)

        retry = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist or [500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.rate_limiter = rate_limiter
        self.timeout = timeout

        self._lock = threading.Lock()
        self._reset_stats()

    def _reset_stats(self) -> None:
        self.completed: int = 0
        self.success: int = 0
        self.failed: int = 0

    def _record_success(self) -> None:
        with self._lock:
            self.completed += 1
            self.success += 1

    def _record_failure(self) -> None:
        with self._lock:
            self.completed += 1
            self.failed += 1

    def _print_progress(self, total: int) -> None:
        print(
            f"[{self.completed}/{total}] "
            f"Success: {self.success} | Failed: {self.failed}",
            end="\r",
        )

    def get(self, url: str, **kwargs: Any) -> Response:
        if self.rate_limiter:
            self.rate_limiter.acquire()

        kwargs.setdefault("timeout", self.timeout)

        return self.session.get(url, **kwargs)

    def fetch(
        self,
        url: str,
        processor: Callable[[Response], Any] | None = None,
    ) -> tuple[str, Any | None]:
        """
        Fetch a single URL.

        Returns:
            A tuple containing the URL and processed result.

        If processor is None, returns response.text.
        Otherwise, returns processor(response).
        """
        try:
            response = self.get(url)

            if not response.ok:
                self._record_failure()
                return url, None

            self._record_success()

            if processor:
                return url, processor(response)

            return url, response.text

        except requests.RequestException:
            self._record_failure()
            return url, None

    def fetch_all(
        self,
        urls: Sequence[str],
        processor: Callable[[Response], Any] | None = None,
        max_workers: int = 10,
        show_progress: bool = True,
    ) -> list[Any]:
        """
        Fetch many URLs concurrently.

        Returns:
            A list of successfully processed results.
        """
        if not urls:
            return []

        self._reset_stats()

        results: list[Any] = []
        total = len(urls)

        if show_progress:
            print(f"Fetching {total} objects...\n")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.fetch, url, processor)
                for url in urls
            ]

            for future in as_completed(futures):
                _, result = future.result()

                if result is not None:
                    results.append(result)

                if show_progress:
                    self._print_progress(total)

        if show_progress:
            print()
            print(
                f"Done. Success: {self.success}, Failed: {self.failed}"
            )

        return results
