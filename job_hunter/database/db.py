import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from job_hunter.database.models import Base, Job
from job_hunter.config.settings import DB_PATH, CSV_PATH, JSON_PATH

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f'sqlite:///{DB_PATH}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()

def insert_job_if_not_exists(session, job_data):
    """
    Inserts a job. Avoids duplicates based on the job link.
    """
    existing_job = session.query(Job).filter_by(link=job_data.get('link')).first()
    if not existing_job:
        new_job = Job(**job_data)
        session.add(new_job)
        session.commit()
        return True
    return False

def export_db_to_files():
    """
    Exports the SQLite database to CSV and JSON using Pandas.
    """
    try:
        # Load directly using pandas and SQLAlchemy
        df = pd.read_sql_table('jobs', con=engine)
        df.to_csv(CSV_PATH, index=False)
        df.to_json(JSON_PATH, orient='records', indent=4)
        print(f"[+] Database exported to {CSV_PATH} and {JSON_PATH}")
    except Exception as e:
        print(f"[-] Error exporting DB: {e}")
