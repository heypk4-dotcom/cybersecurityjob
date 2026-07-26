# Advanced Cyber Security Job Hunter

An enterprise-grade, automated job hunting system designed for Cyber Security professionals. It scrapes job boards, scores them using an LLM based on resume keywords, saves them to a local SQLite database, emails you the top matches daily, and provides a Streamlit dashboard for exploring the data.

## Features
- **Modular Scrapers**: Supports Playwright for Javascript-heavy sites like YCombinator and LinkedIn.
- **LLM Scoring**: Uses OpenAI API to evaluate job descriptions against a strict set of resume keywords.
- **Deduplication**: Saves jobs to SQLite (`SQLAlchemy`) to ensure you never get spammed with the same job twice.
- **Daily Email Reports**: Beautiful HTML emails containing jobs scoring above a threshold, with CSV exports attached.
- **Streamlit Dashboard**: A local web interface to filter and read through scraped jobs.
- **Docker Ready**: `docker-compose.yml` for quick execution.
- **GitHub Actions**: Automated daily runs via `.github/workflows/schedule.yml`.

## Quickstart (Local)
1. Configure `.env` using `.env.example`.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. Run the scheduler:
   ```bash
   python main.py
   ```
4. Run the dashboard:
   ```bash
   streamlit run job_hunter/dashboard/app.py
   ```

## Quickstart (Docker)
Run the entire stack (Scraper background process + Streamlit Dashboard on port 8501):
```bash
docker-compose up -d --build
```
