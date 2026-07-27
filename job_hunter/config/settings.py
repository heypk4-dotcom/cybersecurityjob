import os
from dotenv import load_dotenv

load_dotenv()

# Email
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# LLM 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", os.getenv("GROQ_API_KEY")) # Fallback for demo
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# DB
DB_PATH = os.path.join("data", "jobs.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
CSV_PATH = os.path.join("data", "jobs.csv")
JSON_PATH = os.path.join("data", "jobs.json")

# App
MIN_MATCH_SCORE_EMAIL = 60
