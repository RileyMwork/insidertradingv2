import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging() -> None:
    project_root = Path(__file__).resolve().parents[3]
    log_directory = project_root / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)

    timestamp: str = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    log_file: Path = log_directory / f"application_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                filename=log_file,
                maxBytes=5_000_000,
                backupCount=5,
                encoding="utf-8",
            ),
        ],
        force=True,
    )
