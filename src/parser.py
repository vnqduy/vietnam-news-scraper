import json
import time
import requests
import cloudscraper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class ArticleScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        self.cloud_scraper = cloudscraper.create_scraper()
        self.driver = None

    def _init_selenium(self):
        if self.driver is None:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('user-agent=' + self.headers["User-Agent"])
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def _extract_json_ld(self, soup):
        for script in soup.find_all("script", type="application/ld+json"):
            if not script.string:
                continue
            try:
                data = json.loads(script.string)
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if item.get("@type") in ["NewsArticle", "Article"]:
                        body = item.get("articleBody")
                        if body and len(body) > 100:
                            return body.strip()
            except Exception:
                continue
        return None

    def _parse_html(self, html, domain):
        soup = BeautifulSoup(html, "html.parser")
        
        json_body = self._extract_json_ld(soup)
        if json_body:
            return json_body

        body = None
        if "dantri.com.vn" in domain:
            body = soup.find("div", class_="singular-content") or soup.find("div", class_="dt-news__content")
        elif "laodong.vn" in domain:
            body = soup.find("div", class_="article-content") or soup.find("div", class_="art-body")
        
        if not body:
            body = soup.find("article") or soup

        paragraphs = [p.get_text(strip=True) for p in body.find_all(["p", "div", "span"]) if len(p.get_text(strip=True)) > 30]
        clean_text = "\n\n".join(dict.fromkeys(paragraphs))
        return clean_text if len(clean_text) > 100 else None

    def scrape_url(self, url, domain):
        # Fallback 1: Standard Requests / Cloudscraper
        try:
            resp = self.cloud_scraper.get(url, headers=self.headers, timeout=8)
            if resp.status_code == 200:
                text = self._parse_html(resp.content, domain)
                if text:
                    return text
        except Exception:
            pass

        # Fallback 2: Headless Selenium Engine
        try:
            self._init_selenium()
            self.driver.get(url)
            time.sleep(2)
            return self._parse_html(self.driver.page_source, domain)
        except Exception:
            return None

    def close(self):
        if self.driver:
            self.driver.quit()
