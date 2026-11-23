
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
    
        Raises:
            requests.RequestException: If the HTTP request fails.
        """
        try:
            response = self.get(url)
            response.raise_for_status()
    
            if processor is not None:
                result = processor(response)
            else:
                result = response.text
    
            self._record_success()
    
            return url, result
    
        except requests.RequestException:
            self._record_failure()
            raise
        
        
    def fetch_all(
        self,
        urls: Sequence[str],
        processor: Callable[[Response], Any] | None = None,
        max_workers: int = 10,
        show_progress: bool = True,
        raise_on_error: bool = False,
    ) -> list[Any]:
        """
        Fetch many URLs concurrently.
    
        Successful results are returned in the same order as the input URLs.
    
        Args:
            urls: URLs to fetch.
            processor: Optional function to process each response.
            max_workers: Maximum number of concurrent workers.
            show_progress: Whether to display progress.
            raise_on_error: Whether to raise an exception if a request fails.
    
        Returns:
            A list containing successfully processed results.
    
        Raises:
            requests.RequestException: If raise_on_error is True and a
                request fails.
        """
        if not urls:
            return []
    
        self._reset_stats()
    
        total: int = len(urls)
        ordered_results: list[Any | None] = [None] * total
        errors: list[requests.RequestException] = []
    
        if show_progress:
            print(f"Fetching {total} objects...\n")
    
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index: dict[Any, int] = {
                executor.submit(self.fetch, url, processor): index
                for index, url in enumerate(urls)
            }
    
            for future in as_completed(future_to_index):
                index: int = future_to_index[future]
    
                try:
                    _, result = future.result()
                    ordered_results[index] = result
    
                except requests.RequestException as error:
                    errors.append(error)
    
                if show_progress:
                    self._print_progress(total)
    
        if show_progress:
            print()
            print(
                f"Done. Success: {self.success}, Failed: {self.failed}"
            )
    
        if raise_on_error and errors:
            raise errors[0]
    
        return [
            result
            for result in ordered_results
            if result is not None
        ]
    
    
    
    