from job_hunter.scrapers.yc_scraper import YCScraper
from job_hunter.scrapers.linkedin_scraper import LinkedInScraper
from job_hunter.processors.data_cleaner import clean_raw_jobs
from job_hunter.processors.llm_processor import process_job_with_llm
from job_hunter.database.db import init_db, get_session, insert_job_if_not_exists, export_db_to_files
from job_hunter.email.sender import send_daily_email

def run_pipeline():
    print("[*] Initializing Database...")
    init_db()
    
    print("[*] Starting Scrapers (Fetching Real Jobs)...")
    scrapers = [LinkedInScraper(), YCScraper()] 
    
    raw_jobs = []
    for scraper in scrapers:
        raw_jobs.extend(scraper.extract_job_details())
        
    print(f"[*] Fetched {len(raw_jobs)} raw jobs.")
    
    print("[*] Cleaning Data...")
    cleaned_jobs = clean_raw_jobs(raw_jobs)
    
    print("[*] Processing with LLM & Saving to DB...")
    session = get_session()
    new_jobs_count = 0
    
    for job in cleaned_jobs:
        from job_hunter.database.models import Job
        existing = session.query(Job).filter_by(link=job['link']).first()
        
        if not existing:
            llm_data = process_job_with_llm(job)
            job.update(llm_data)
            if insert_job_if_not_exists(session, job):
                new_jobs_count += 1
                
    session.close()
    print(f"[+] Added {new_jobs_count} new jobs to the database.")
    
    print("[*] Exporting Data...")
    export_db_to_files()
    
    print("[*] Sending Daily Email...")
    send_daily_email()
    
    print("[+] Pipeline Execution Complete.")
