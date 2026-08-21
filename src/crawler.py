import time
import urllib.parse
import re
import feedparser
import pandas as pd
from datetime import date, timedelta
from src.utils import parse_published_date

TECH_TITLE_TERMS = ['trí tuệ nhân tạo', 'chatgpt', 'openai', 'ai tạo sinh', 'edtech', 'generative ai', 'llm']
EDU_TITLE_TERMS = ['giáo dục', 'đào tạo', 'trường', 'đại học', 'học sinh', 'sinh viên', 'giảng viên', 'giáo viên', 'sách giáo khoa', 'dạy', 'học']

class RSSCrawler:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://news.google.com/rss/search"
        self.name_to_domain = {
            variant.lower(): domain
            for domain, variants in config["outlets"].items()
            for variant in variants
        }

    def _daterange_chunks(self, start_str, end_str, chunk_days=31):
        start = date.fromisoformat(start_str)
        end = date.fromisoformat(end_str)
        cur = start
        while cur < end:
            nxt = min(cur + timedelta(days=chunk_days), end)
            yield cur.isoformat(), nxt.isoformat()
            cur = nxt

    def _is_title_relevant(self, title: str) -> bool:
        t_lower = title.lower()
        has_tech = bool(re.search(r'\bAI\b', title)) or any(term in t_lower for term in TECH_TITLE_TERMS)
        has_edu = any(term in t_lower for term in EDU_TITLE_TERMS)
        return has_tech and has_edu

    def run(self):
        all_records = []
        seen_urls = set()
        
        for c_start, c_end in self._daterange_chunks(
            self.config["search"]["start_date"], 
            self.config["search"]["end_date"],
            self.config["search"]["chunk_days"]
        ):
            for tech in self.config["search"]["tech_keywords"]:
                for edu in self.config["search"]["edu_keywords"]:
                    q = f'{tech} {edu} after:{c_start} before:{c_end}'
                    params = {'q': q, 'hl': 'vi-VN', 'gl': 'VN', 'ceid': 'VN:vi'}
                    url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
                    feed = feedparser.parse(url)

                    for e in feed.entries:
                        link = e.get("link", "")
                        if not link or link in seen_urls:
                            continue
                        
                        source_name = e.get("source", {}).get("title", "Unknown")
                        domain = self.name_to_domain.get(source_name.strip().lower())
                        raw_title = e.get("title", "")

                        if domain and self._is_title_relevant(raw_title):
                            seen_urls.add(link)
                            day, month, year = parse_published_date(e.get("published", "NO DATE"))
                            all_records.append({
                                "title": raw_title.rsplit(" - ", 1)[0].strip() if " - " in raw_title else raw_title.strip(),
                                "date": day, "month": month, "year": year,
                                "link": link, "outlet_domain": domain
                            })
                    time.sleep(0.3)
                    
        return pd.DataFrame(all_records)
