from job_hunter.scrapers.base import BaseScraper
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

class YCScraper(BaseScraper):
    \"\"\"
    Scrapes YCombinator Hacker News jobs using Playwright.
    \"\"\"
    def __init__(self):
        self.jobs = []

    def login(self):
        pass

    def search_jobs(self, keywords, location):
        pass # Not applicable for HN jobs page since it's a single feed

    def extract_job_details(self):
        print("[YC Scraper] Starting Playwright...")
        extracted = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("https://news.ycombinator.com/jobs", timeout=60000)
                
                # Wait for the jobs to load
                page.wait_for_selector(".athing", timeout=10000)
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                
                items = soup.find_all("tr", class_="athing")
                
                for item in items:
                    title_elem = item.find("span", class_="titleline")
                    if title_elem and title_elem.a:
                        title = title_elem.a.text
                        link = title_elem.a["href"]
                        if not link.startswith("http"):
                            link = f"https://news.ycombinator.com/{link}"
                            
                        # HN Jobs don't strictly separate company and location, it's usually in the title.
                        extracted.append({
                            "title": title,
                            "company": "YC Startup",
                            "location": "Remote / Specified in title",
                            "link": link,
                            "description": title # Using title as description since HN doesn't show full desc on feed
                        })
                        
                browser.close()
                print(f"[YC Scraper] Successfully scraped {len(extracted)} real jobs from YC HackerNews.")
        except Exception as e:
            print(f"[YC Scraper] Error: {e}")
            
        return extracted
