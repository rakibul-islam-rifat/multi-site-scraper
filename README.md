# 🕷️ Multi-Site Scraper

A clean, extensible web scraping framework built with Python — designed around real software engineering principles. Not just a script that grabs data, but a proper architecture that scales.

---

## 🏗️ Architecture

```
multi-site-scraper/
├── fetch_urls.py          # Shared HTTP layer with retry logic & rate limiting
├── logger_setup.py        # Centralized logging configuration
├── storage.py             # CSV persistence layer
├── main.py                # Entry point
└── scrapers/
    ├── __init__.py        # Public API — exports run_scraper
    ├── base.py            # Abstract base class (Template Method Pattern)
    ├── book_scraper.py    # books.toscrape.com implementation
    ├── quote_scraper.py   # quotes.toscrape.com implementation
    └── runner.py          # Registry & orchestration layer
```

The design follows the **Template Method Pattern** — `BaseScraper` defines the skeleton of the scraping algorithm, and each concrete scraper fills in only what's different. Adding a new site means writing one new class and registering it in one place. `main.py` never changes.

---

## ✨ Features

- **OOP-first design** with abstract base class enforcing a clean contract across all scrapers
- **Factory + Registry pattern** — swap, add, or disable scrapers by editing a single list
- **Automatic CSV naming** via `__name__` — no hardcoded filenames anywhere
- **Robust HTTP layer** with retry logic, exponential backoff, rate limiting, and proper error wrapping
- **Pagination handling** built into each scraper via `urljoin`-safe next-page detection
- **Structured logging** with rotating file handler and console output
- **Type-annotated** throughout for IDE support and clarity

---

## 🚀 Getting Started

### Install dependencies

```bash
uv pip install requests beautifulsoup4 lxml
```

### Run

```bash
python main.py
```

Output CSVs will be saved to the `output/` folder automatically.

---

## 📦 What Gets Scraped

| Site | Fields |
|------|--------|
| books.toscrape.com | Title, Price |
| quotes.toscrape.com | Quote, Author, Tags |

---

## ➕ Adding a New Scraper

1. Create `scrapers/new_scraper.py` inheriting from `BaseScraper`
2. Set `_START_URL` and implement `parse()` and `scrape()`
3. Register it in `scrapers/runner.py`:

```python
from .new_scraper import NewScraper

_SCRAPER_REGISTRY: list[type[BaseScraper]] = [
    BookScraper,
    QuoteScraper,
    NewScraper,  # ← one line
]
```

That's it. The rest of the system picks it up automatically — including CSV naming and orchestration.

---

## 🛠️ Tech Stack

- **Python 3.12+**
- **requests** — HTTP
- **BeautifulSoup4 + lxml** — HTML parsing
- **csv** — storage
- **logging** — structured logs
- **abc** — abstract base class enforcement
- **uv** — package management

---

## 👤 Author

**Rifat** — [github.com/rakibul-islam-rifat](https://github.com/rakibul-islam-rifat)  
Freelance Python developer • Web scraping & automation • Fiverr: `rifat_automates`