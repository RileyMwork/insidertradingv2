
import pytest

from insider_trading.api.edgar.parse_index_files import ParseIndexFiles


class TestParseIndexFiles:
    parser: ParseIndexFiles

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.parser = ParseIndexFiles()

    def test_extract_form_links_returns_form_4_by_default(self) -> None:
        index_file_text = (
            "754|Dine Brands Global, Inc.|8-K|20261120|"
            "edgar/data/49754/0001193125-26-469349.txt\n"
            "4977|AFLAC INC|4|20261120|"
            "edgar/data/4977/0001104659-26-130427.txt\n"
            "50725|GRIFFON CORP|4|20261120|"
            "edgar/data/50725/0001628280-26-075300.txt\n"
            "54476|EVERGY METRO, INC.|8-K|20261120|"
            "edgar/data/54476/0001193125-26-470295.txt\n"
            "5981|AMERICAN VANGUARD CORP|4|20261120|"
            "edgar/data/5981/0001193125-26-470657.txt"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
        )

        expected_links = [
            f"{self.parser.base_url}"
            "edgar/data/4977/0001104659-26-130427.txt",
            f"{self.parser.base_url}"
            "edgar/data/50725/0001628280-26-075300.txt",
            f"{self.parser.base_url}"
            "edgar/data/5981/0001193125-26-470657.txt",
        ]

        assert actual_links == expected_links

    def test_extract_form_links_with_specific_form_type(self) -> None:
        index_file_text = (
            "754|Dine Brands Global, Inc.|8-K|20261120|"
            "edgar/data/49754/0001193125-26-469349.txt\n"
            "4977|AFLAC INC|4|20261120|"
            "edgar/data/4977/0001104659-26-130427.txt\n"
            "54476|EVERGY METRO, INC.|8-K|20261120|"
            "edgar/data/54476/0001193125-26-470295.txt\n"
            "67887|MOOG INC.|10-K|20261120|"
            "edgar/data/67887/0001628280-26-075202.txt"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
            "8-K",
        )

        expected_links = [
            f"{self.parser.base_url}"
            "edgar/data/49754/0001193125-26-469349.txt",
            f"{self.parser.base_url}"
            "edgar/data/54476/0001193125-26-470295.txt",
        ]

        assert actual_links == expected_links

    def test_extract_form_links_with_empty_form_type_returns_all_forms(
        self,
    ) -> None:
        index_file_text = (
            "4977|AFLAC INC|4|20261120|"
            "edgar/data/4977/0001104659-26-130427.txt\n"
            "754|Dine Brands Global, Inc.|8-K|20261120|"
            "edgar/data/49754/0001193125-26-469349.txt\n"
            "67887|MOOG INC.|10-K|20261120|"
            "edgar/data/67887/0001628280-26-075202.txt"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
            "",
        )

        expected_links = [
            f"{self.parser.base_url}"
            "edgar/data/4977/0001104659-26-130427.txt",
            f"{self.parser.base_url}"
            "edgar/data/49754/0001193125-26-469349.txt",
            f"{self.parser.base_url}"
            "edgar/data/67887/0001628280-26-075202.txt",
        ]

        assert actual_links == expected_links

    def test_extract_form_links_returns_multiple_links_for_same_cik(
        self,
    ) -> None:
        index_file_text = (
            "63296|MATTHEWS INTERNATIONAL CORP|4|20261120|"
            "edgar/data/63296/0000063296-26-000128.txt\n"
            "63296|MATTHEWS INTERNATIONAL CORP|4|20261120|"
            "edgar/data/63296/0000063296-26-000129.txt\n"
            "63296|MATTHEWS INTERNATIONAL CORP|4|20261120|"
            "edgar/data/63296/0000063296-26-000130.txt\n"
            "63296|MATTHEWS INTERNATIONAL CORP|8-K|20261120|"
            "edgar/data/63296/0000063296-26-000118.txt"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
        )

        expected_links = [
            f"{self.parser.base_url}"
            "edgar/data/63296/0000063296-26-000128.txt",
            f"{self.parser.base_url}"
            "edgar/data/63296/0000063296-26-000129.txt",
            f"{self.parser.base_url}"
            "edgar/data/63296/0000063296-26-000130.txt",
        ]

        assert actual_links == expected_links
        assert len(actual_links) == 3

    def test_extract_form_links_ignores_lines_without_pipes(
        self,
    ) -> None:
        index_file_text = (
            "This is a header line\n"
            "4977|AFLAC INC|4|20261120|"
            "edgar/data/4977/0001104659-26-130427.txt\n"
            "This line has no pipe characters"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
        )

        expected_links = [
            f"{self.parser.base_url}"
            "edgar/data/4977/0001104659-26-130427.txt",
        ]

        assert actual_links == expected_links

    def test_extract_form_links_ignores_lines_with_invalid_column_count(
        self,
    ) -> None:
        index_file_text = (
            "4977|AFLAC INC|4|20261120\n"
            "50725|GRIFFON CORP|4|20261120|"
            "edgar/data/50725/0001628280-26-075300.txt|extra\n"
            "52827|RAYONIER INC|4|20261120|"
            "edgar/data/52827/0000052827-26-000110.txt"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
        )

        expected_links = [
            f"{self.parser.base_url}"
            "edgar/data/52827/0000052827-26-000110.txt",
        ]

        assert actual_links == expected_links

    def test_extract_form_links_returns_empty_list_for_empty_input(
        self,
    ) -> None:
        index_file_text = ""

        actual_links = self.parser.extract_form_links(
            index_file_text,
        )

        assert actual_links == []

    def test_extract_form_links_returns_empty_list_when_no_forms_match(
        self,
    ) -> None:
        index_file_text = (
            "754|Dine Brands Global, Inc.|8-K|20261120|"
            "edgar/data/49754/0001193125-26-469349.txt\n"
            "67887|MOOG INC.|10-K|20261120|"
            "edgar/data/67887/0001628280-26-075202.txt"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
            "4",
        )

        assert actual_links == []

    def test_extract_form_links_preserves_duplicate_file_paths(
        self,
    ) -> None:
        index_file_text = (
            "4977|AFLAC INC|4|20261120|"
            "edgar/data/4977/0001104659-26-130427.txt\n"
            "4977|AFLAC INC|4|20261120|"
            "edgar/data/4977/0001104659-26-130427.txt"
        )

        actual_links = self.parser.extract_form_links(
            index_file_text,
        )

        expected_link = (
            f"{self.parser.base_url}"
            "edgar/data/4977/0001104659-26-130427.txt"
        )

        assert actual_links == [expected_link, expected_link]
        assert len(actual_links) == 2
