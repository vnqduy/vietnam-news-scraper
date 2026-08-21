# Vietnam News Scraper

A modular, robust Python scraping framework designed to collect, decode, and extract full-text news articles from major Vietnamese media outlets (e.g., *Dân Trí*, *Lao Động*, *VOV*, *VTV*, *Thanh Niên*).

Built to handle anti-bot protection, dynamic JavaScript rendering, and Google News RSS obfuscation using a multi-engine fallback architecture (**Requests** → **Cloudscraper** → **Headless Selenium**).

---

## 🏗️ Project Architecture

```text
vietnam-news-scraper/
├── README.md
├── requirements.txt
├── config.yaml
├── main.py
└── src/
    ├── __init__.py
    ├── crawler.py     # Searches & fetches Google News RSS feeds
    ├── decoder.py     # Decodes Google News RSS redirect links to real URLs
    ├── parser.py      # Multi-engine article body parser (JSON-LD, DOM, Selenium)
    └── utils.py       # Config loader & date parsing helpers
