import schedule
import time
from job_hunter.scheduler.main_job import run_pipeline

if __name__ == "__main__":
    print("==================================================")
    print("   Advanced Cyber Security Job Hunter Pipeline    ")
    print("==================================================")
    
    # Run once immediately
    run_pipeline()
    
    # Schedule hourly
    schedule.every().hour.do(run_pipeline)
    
    print("[*] Scheduler running. Waiting for next execution...")
    while True:
        schedule.run_pending()
        time.sleep(60)
