from job_hunter.scrapers.base import BaseScraper
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random

class LinkedInScraper(BaseScraper):
    \"\"\"
    Scrapes LinkedIn public jobs using Playwright.
    \"\"\"
    def __init__(self):
        self.locations = ["Mumbai", "Pune"]
        self.keywords = "Cyber Security"

    def login(self):
        pass # Using public endpoint

    def search_jobs(self, keywords, location):
        pass

    def extract_job_details(self):
        print("[LinkedIn Scraper] Starting Playwright...")
        extracted = []
        try:
            with sync_playwright() as p:
                # Use a plausible user agent
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                )
                page = context.new_page()

                for location in self.locations:
                    url = f"https://www.linkedin.com/jobs/search?keywords={self.keywords}&location={location}&f_E=3"
                    print(f"[LinkedIn Scraper] Searching in {location}...")
                    
                    page.goto(url, timeout=60000)
                    
                    # Scroll down a few times to load dynamic content
                    for _ in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(random.uniform(1.5, 3.0))

                    html = page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    job_cards = soup.find_all("div", class_="base-card")
                    
                    for card in job_cards:
                        title_elem = card.find("h3", class_="base-search-card__title")
                        company_elem = card.find("h4", class_="base-search-card__subtitle")
                        location_elem = card.find("span", class_="job-search-card__location")
                        url_elem = card.find("a", class_="base-card__full-link")
                        
                        if title_elem and company_elem and url_elem:
                            link = url_elem['href'].split('?')[0] # Clean tracking params
                            extracted.append({
                                "title": title_elem.text.strip(),
                                "company": company_elem.text.strip(),
                                "location": location_elem.text.strip() if location_elem else location,
                                "link": link,
                                "description": f"{title_elem.text.strip()} at {company_elem.text.strip()}" # Description fetched by LLM or left basic to save bandwidth
                            })

                browser.close()
                print(f"[LinkedIn Scraper] Successfully scraped {len(extracted)} real jobs from LinkedIn.")
        except Exception as e:
            print(f"[LinkedIn Scraper] Error: {e}")
            
        return extracted
