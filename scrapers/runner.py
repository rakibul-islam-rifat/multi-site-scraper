from .base import BaseScraper
from .books_scraper import BookScraper
from .quotes_scraper import QuoteScraper

_SCRAPER_REGISTRY: list[type[BaseScraper]] = [
    BookScraper,
    QuoteScraper,
]


def run_scraper():
    results: dict = {}
    for scraper_class in _SCRAPER_REGISTRY:
        scraper: BaseScraper = scraper_class()
        results[scraper_class.__name__] = scraper.run()
    return results
