from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    link = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    date_posted = Column(DateTime, default=datetime.utcnow)
    
    # AI Enrichment fields
    ai_score = Column(Float, nullable=True)
    ai_summary = Column(String, nullable=True)
    key_skills = Column(String, nullable=True) # Stored as comma-separated string
