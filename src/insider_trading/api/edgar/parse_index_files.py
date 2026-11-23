
import logging


class ParseIndexFiles:
    def __init__(self) -> None:
        self.base_url = "https://www.sec.gov/Archives/"
        self.logger = logging.getLogger(__name__)

    def extract_form_links(
        self,
        index_file_text: str,
        form_type: str = "4",
    ) -> list[str]:
        self.logger.info(
            "Extracting SEC filing links for form type '%s'.",
            form_type,
        )

        lines = index_file_text.splitlines()
        results: list[str] = []

        for parts in (line.split("|") for line in lines if "|" in line):
            if len(parts) != 5:
                continue

            cik, name, f_type, date_filed, file_path = parts

            if form_type and f_type != form_type:
                continue

            results.append(self.base_url + file_path)

        self.logger.info(
            "Extracted %s links for form type '%s'.",
            len(results),
            form_type,
        )

        self.logger.debug(
            "Completed parsing %s lines from SEC index file.",
            len(lines),
        )

        return results
