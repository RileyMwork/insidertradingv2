from insider_trading.api.edgar.fetch_index_files import FetchIndexFiles
from insider_trading.api.edgar.fetch_target_forms import FetchTargetForms
from insider_trading.api.edgar.parse_index_files import ParseIndexFiles

index_file_fetcher = FetchIndexFiles()

index_file_content = index_file_fetcher.get_latest_index_file(max_days_back=7)

parser = ParseIndexFiles()

form_links = parser.extract_form_links(index_file_content, form_type="4")

target_form_fetcher = FetchTargetForms()
target_forms = target_form_fetcher.fetch_forms(form_links)

print(f"Fetched {len(target_forms)} target forms")

print(target_forms[:5])  # Print the first 5 target forms for inspection
