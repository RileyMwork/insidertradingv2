import logging

from insider_trading.api.edgar.fetch_index_files import FetchIndexFiles
from insider_trading.api.edgar.fetch_target_forms import FetchTargetForms
from insider_trading.api.edgar.parse_index_files import ParseIndexFiles
from insider_trading.api.edgar.parse_target_forms import ParseTargetForms
from insider_trading.infrastructure.logging_config import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

logger.info("Starting insider trading application.")

index_file_fetcher = FetchIndexFiles()

index_file_content = index_file_fetcher.get_latest_index_file(max_days_back=7)

parser = ParseIndexFiles()

form_links = parser.extract_form_links(index_file_content, form_type="4")

target_form_fetcher = FetchTargetForms()

target_forms = target_form_fetcher.fetch_forms(form_links[0:5])

target_form_parser = ParseTargetForms()

print(target_form_parser.parse_form_four(target_forms[1], form_links[1]))
