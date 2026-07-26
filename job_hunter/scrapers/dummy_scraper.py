from job_hunter.scrapers.base import BaseScraper
import uuid

class DummyScraper(BaseScraper):
    """
    A dummy scraper that returns mock Cyber Security jobs for testing the pipeline safely.
    """
    def login(self):
        print("[Dummy] Logging in... (Mock)")

    def search_jobs(self, keywords, location):
        print(f"[Dummy] Searching for {keywords} in {location}...")

    def extract_job_details(self):
        print("[Dummy] Extracting jobs...")
        return [
            {
                "title": "Information Security Consultant",
                "company": "SecureTech Corp",
                "location": "Mumbai",
                "link": f"https://example.com/job/{uuid.uuid4()}",
                "description": "We are looking for a VAPT Consultant with 2.5 years of experience in Web Application Testing, API Testing, and using tools like Burp Suite and Nessus."
            },
            {
                "title": "Cyber Security Analyst",
                "company": "DefendNet",
                "location": "Pune",
                "link": f"https://example.com/job/{uuid.uuid4()}",
                "description": "Requires basic understanding of networking. Will perform generic IT helpdesk."
            }
        ]
