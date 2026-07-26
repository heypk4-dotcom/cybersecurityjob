import schedule
import time
from job_hunter.scheduler.main_job import run_pipeline

if __name__ == "__main__":
    print("==================================================")
    print("   Advanced Cyber Security Job Hunter Pipeline    ")
    print("==================================================")
    
    # Run once immediately
    run_pipeline()
    
    # Schedule daily at 9 AM
    schedule.every().day.at("09:00").do(run_pipeline)
    
    print("[*] Scheduler running. Waiting for next execution...")
    while True:
        schedule.run_pending()
        time.sleep(60)
