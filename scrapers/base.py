import logging
from abc import ABC, abstractmethod

from fetch_urls import fetch_url

logger: logging.Logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    _START_URL: str = ""

    def _fetch(self, url: str):
        try:
            return fetch_url(url)
        except (RuntimeError, ConnectionError) as e:
            logger.critical("Script Failed, %s", e)
            return

    def scrape(self, url: str):
        response = self._fetch(url)
        return self.parse(response)

    @abstractmethod
    def parse(self, card):
        pass

    def run(self):
        return self.scrape(self._START_URL)
