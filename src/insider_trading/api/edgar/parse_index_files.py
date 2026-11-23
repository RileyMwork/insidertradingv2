
class ParseIndexFiles:

    def __init__(self) -> None:
        self.base_url = "https://www.sec.gov/Archives/"
    
    def extract_form_links(self, index_file_text : str, form_type : str ="4") -> list[str]:
        lines = index_file_text.splitlines()
        results = []

        for parts in (line.split("|") for line in lines if "|" in line):
            if len(parts) != 5:
                continue

            cik, name, f_type, date_filed, file_path = parts

            if form_type and f_type != form_type:
                continue

            results.append(self.base_url + file_path)

        print(f"Extracted {len(results)} links for form type '{form_type}'")
        return results
