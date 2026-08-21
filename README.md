# Vietnam News Scraper

A modular, robust Python web scraping framework designed to search, decode, and extract full-text news articles from major Vietnamese media outlets, such as *Dân Trí*, *Lao Động*, *VOV*, *VTV*, and *Thanh Niên*.

The framework is built to handle anti-bot protection, dynamic JavaScript rendering, and Google News RSS obfuscation using a multi-engine fallback architecture:

**Requests → Cloudscraper → Headless Selenium**

---

## Project Architecture

```text
vietnam-news-scraper/
├── README.md
├── requirements.txt
├── config.yaml
├── main.py
└── src/
    ├── __init__.py
    ├── crawler.py     # Searches and fetches Google News RSS feeds
    ├── decoder.py     # Decodes Google News RSS redirect links to real URLs
    ├── parser.py      # Multi-engine article body parser (JSON-LD, DOM, Selenium)
    └── utils.py       # Config loader and date parsing helpers
```

---

## Multi-Engine Extraction Pipeline

Standard HTTP requests often fail against major Vietnamese news domains due to rate limits and anti-bot protections.

The extraction pipeline uses a three-tier fallback approach:

1. **JSON-LD Schema Extraction**  
   Parses embedded `application/ld+json` metadata directly from the source HTML.

2. **Cloudscraper Engine**  
   Handles basic Cloudflare and site-level anti-bot protections when standard HTTP requests fail.

3. **Headless Chrome with Selenium**  
   Uses browser automation to render JavaScript-heavy or heavily protected pages, such as *Lao Động* and *Dân Trí*.

---

## Quick Start

### 1. Prerequisites

Ensure that Python 3.8 or later is installed.

For local execution, Google Chrome should also be installed on your system if Selenium-based extraction is required.

### 2. Installation

Clone the repository:

```bash
git clone https://github.com/your-username/vietnam-news-scraper.git
cd vietnam-news-scraper
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### Google Colab and Linux

For Google Colab or compatible Linux environments, install Chromium and ChromeDriver:

```bash
apt-get update
apt-get install -y chromium-chromedriver google-chrome-stable
```

---

## Usage

Run the complete scraping pipeline with:

```bash
python main.py
```

Processed data will automatically be saved to the `data/` directory.

The generated files include:

- `data/raw_rss.csv` — Filtered Google News RSS search results
- `data/decoded_links.csv` — Decoded original news outlet URLs
- `data/aied_news_final.csv` — Final dataset containing full article text and character counts

---

## Configuration

Search keywords, date ranges, targeted news outlets, chunk sizes, and output settings are managed through `config.yaml`.

Example configuration:

```yaml
search:
  start_date: "2017-01-01"
  end_date: "2017-12-31"
  chunk_days: 31

  tech_keywords:
    - '"trí tuệ nhân tạo"'
    - "ChatGPT"
    - "OpenAI"

  edu_keywords:
    - "giáo dục"
    - "đào tạo"
    - "trường học"

outlets:
  "dantri.com.vn":
    - "Báo Dân trí"
    - "Dân trí"

  "laodong.vn":
    - "Laodong.vn"
    - "Báo Lao Động"
    - "Lao Động"

  "vov.vn":
    - "VOV"
    - "vov.vn"
    - "Báo điện tử VOV"
```

---

## License

Distributed under the MIT License.
