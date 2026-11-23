
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging() -> None:
    project_root = Path(__file__).resolve().parents[3]
    log_directory = project_root / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                filename=log_directory / f"application_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",  # noqa: E501
                maxBytes=5_000_000,
                backupCount=5,
                encoding="utf-8",
            ),
        ],
        force=True,
    )
