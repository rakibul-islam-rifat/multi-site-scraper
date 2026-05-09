import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from scrapers.base import BaseScraper

logger: logging.Logger = logging.getLogger(__name__)


class BookScraper(BaseScraper):
    _START_URL = "https://books.toscrape.com/catalogue/page-1.html"

    @staticmethod
    def get_title(card: Tag) -> str | None:
        title: Tag | None = card.select_one("article.product_pod > h3 > a")
        return str(title.get("title")) if title else None

    @staticmethod
    def get_price(card: Tag) -> float | None:
        tag: Tag | None = card.select_one("div.product_price > p.price_color")
        if not tag:
            return None
        price_text: str = tag.get_text(strip=True)

        try:
            return float(price_text[1:])
        except ValueError:
            return None

    @staticmethod
    def get_next_page(soup: BeautifulSoup) -> str | None:
        tag: Tag | None = soup.select_one("li.next > a")
        return str(tag.get("href")) if tag else None

    def parse(self, card: Tag) -> dict:
        return {"Title": self.get_title(card), "Price": self.get_price(card)}

    def scrape(self, url: str) -> list:
        current_url: str | None = url
        books_data = []

        while current_url:
            response = self._fetch(current_url)
            if response is None:
                break
            soup = BeautifulSoup(response.text, "lxml")

            for card in soup.select("article.product_pod"):
                books_data.append(self.parse(card))

            next_page: str | None = self.get_next_page(soup)
            current_url = urljoin(current_url, next_page) if next_page else None

        logger.info("Successfully grabbed %d books data!", len(books_data))
        return books_data
