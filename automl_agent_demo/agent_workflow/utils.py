import requests
from bs4 import BeautifulSoup

class DataExtractor:
    @staticmethod
    def fetch_url_content(url: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None

    @staticmethod
    def parse_html(content: str) -> BeautifulSoup:
        return BeautifulSoup(content, 'lxml')

    @staticmethod
    def extract_data(soup: BeautifulSoup, tag: str, attrs: dict) -> str:
        # Initialize a list to keep all elements in order
        elements = []

        # Extract all relevant tags
        for tag in soup.find_all(['p', 'code', 'div'], recursive=True):
            if tag.name == 'p':
                elements.append(('paragraph', tag.get_text()))
            if tag.name == 'code':
                elements.append(('code', tag.get_text()))
            elif tag.name == 'div' and 'section' in tag.get('class', []):
                elements.append(('section', tag.get_text()))

        extracted_content = ""
        for i, (element_type, text) in enumerate(elements):
            extracted_content = extracted_content + "\n" + f"{element_type.capitalize()} {i + 1}: {text}"

        return extracted_content
