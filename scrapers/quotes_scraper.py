import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from scrapers.base import BaseScraper

logger: logging.Logger = logging.getLogger(__name__)


class QuoteScraper(BaseScraper):
    _START_URL = "https://quotes.toscrape.com/page/1/"

    @staticmethod
    def get_quote(card: Tag) -> str | None:
        tag: Tag | None = card.select_one("span.text")
        return tag.get_text(strip=True) if tag else None

    @staticmethod
    def get_author(card: Tag) -> str | None:
        tag: Tag | None = card.select_one("span > small.author")
        return tag.get_text(strip=True) if tag else None

    @staticmethod
    def get_tags(card: Tag) -> list | None:
        tags = card.select("div.tags > a.tag")
        return [tag.get_text(strip=True) for tag in tags] if tags else None

    @staticmethod
    def get_next_page(soup: BeautifulSoup) -> str | None:
        tag: Tag | None = soup.select_one("li.next > a")
        return str(tag.get("href")) if tag else None

    def parse(self, card) -> dict:
        return {
            "Quote": self.get_quote(card),
            "Author": self.get_author(card),
            "Tags": self.get_tags(card),
        }

    def scrape(self, url: str) -> list:
        current_url: str | None = url
        quotes_data: list = []
        while current_url:
            response = self._fetch(current_url)
            if response is None:
                break

            soup: BeautifulSoup = BeautifulSoup(response.text, "lxml")

            for card in soup.select("div.quote"):
                quotes_data.append(self.parse(card))

            next_page: str | None = self.get_next_page(soup)
            current_url = urljoin(current_url, next_page) if next_page else None

        logger.info("Successfully grabbed %d quotes!", len(quotes_data))
        return quotes_data
