import logging

from logger_setup import setup_logging
from scrapers import run_scraper
from storage import save_to_csv

setup_logging("multi-site.log")
logger: logging.Logger = logging.getLogger(__name__)


def check_data() -> None:
    logger.info("Scraping started, Please wait patiently.")
    results: dict = run_scraper()
    for name, data in results.items():
        save_to_csv(data, name)

    logger.info("Successfully saved all the data in Output folder.")


def main() -> None:
    check_data()


if __name__ == "__main__":
    main()
