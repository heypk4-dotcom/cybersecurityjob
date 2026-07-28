# Scraper System Failures Log

This document outlines the various reasons why the Cyber Security Job Hunter pipeline might fail, specifically in a CI/CD environment like GitHub Actions.

## Why Did Today's Scraper Fail?
Based on the error logs from the GitHub Actions execution, today's failure was caused by a specific environment setup issue during the `Install dependencies` step:

1. **Dependency File Encoding Error:** The pipeline crashed immediately while running `pip install -r requirements.txt`. This happened because line 10 (`psycopg2-binary==2.9.9`) was incorrectly encoded (likely a UTF-16 copy-paste issue), causing `pip` to read it with null bytes and spaces (`p s y c o p g 2 - b i n a r y = = 2 . 9 . 9`). This resulted in a syntax error that halted the GitHub Action before the scraper script could even start. (This issue has now been fixed in the codebase).

*(Note: Had the dependencies installed correctly, the scraper could still have failed later due to the following common issues:)*

2. **LinkedIn Anti-Bot Protection (IP Blocking):** LinkedIn aggressively monitors and blocks traffic coming from data center IP addresses, including GitHub Actions runners. Even with Playwright running in headless mode and using a spoofed User-Agent, LinkedIn often detects the automated browser and serves a CAPTCHA or a soft-block page. When this happens, `BeautifulSoup` fails to find the `.base-card` elements, returning 0 jobs, or Playwright times out waiting for the page to load.
3. **SMTP (Email) Authentication Block:** The pipeline uses `smtp.gmail.com`. Google frequently flags and blocks login attempts originating from new, unrecognized server IP addresses (like a GitHub Actions runner) as "suspicious activity," even if an App Password is used. This causes the `smtplib.SMTPAuthenticationError` during the `send_system_email` or `send_daily_email` steps.

## Comprehensive List of Potential System Failures

### 1. Web Scraping & Playwright Issues
* **DOM/HTML Layout Changes:** Platforms like LinkedIn frequently change their CSS class names (e.g., `base-search-card__title` might become `job-card-list__title`). When the DOM structure changes, the BeautifulSoup parsers fail to extract the expected data.
* **Headless Browser Detection:** Modern bot-mitigation systems (Cloudflare, Datadome, LinkedIn's internal anti-bot) can detect Playwright's headless Chromium browser by inspecting JavaScript properties (`navigator.webdriver`).
* **Timeouts:** The GitHub Actions runner might experience slow network connectivity. If the page takes longer than `timeout=60000` (60 seconds) to load, Playwright will throw a `TimeoutError` and crash the scraper.

### 2. LLM Processing Failures
* **Dependency Conflicts (OpenAI vs HTTPX):** The `openai` python package depends on `httpx`. Older versions of `openai` (like `1.14.2`) passed a `proxies` argument to `httpx`. However, newer versions of `httpx` (like `0.28.0+`) completely removed this argument. This causes the script to crash immediately on startup with `Client.__init__() got an unexpected keyword argument 'proxies'`. The fix is to ensure the `openai` package is kept up-to-date (e.g., `>=1.50.0`) in `requirements.txt`.
* **API Key Rate Limits:** Both OpenAI and Groq have strict rate limits. If you process hundreds of jobs at once, the API might return a 429 Too Many Requests error.
* **JSON Parsing Errors:** The LLM is prompted to return a JSON object, but occasionally it might return malformed JSON or include conversational text. The `json.loads(content)` step in `llm_processor.py` would then fail with a `JSONDecodeError`.

### 3. GitHub Actions Environment Issues
* **OS Compatibility for Dependencies (Ubuntu 24.04 vs 22.04):** GitHub occasionally updates `ubuntu-latest` to a newer OS version (e.g., from Ubuntu 22.04 to Ubuntu 24.04). Older versions of Playwright (like `1.42.0`) expect older system libraries (`libasound2`, `libffi7`) which no longer exist in the newer OS, causing `playwright install-deps` to fail with "Package has no installation candidate". Pinning the runner to `ubuntu-22.04` instead of `ubuntu-latest` prevents these sudden breakages.
* **Missing GitHub Secrets:** If any of the environment variables (`SENDER_EMAIL`, `SENDER_PASSWORD`, `RECEIVER_EMAIL`, `OPENAI_API_KEY`, `DATABASE_URL`) are not correctly configured in the repository's Settings > Secrets, the Python script will lack the necessary credentials to run.
* **Runner Resource Exhaustion:** Running Playwright browsers consumes significant memory. The default GitHub Actions Ubuntu runner might occasionally run out of memory (OOM) and kill the process.

### 4. Database & Concurrency Failures
* **SQLite Locking:** While SQLite is fine for local testing, if multiple GitHub Action jobs run simultaneously and try to write to `jobs.db`, it can cause a `database is locked` error.

## Recommendations for Mitigation
- **Use Proxies:** Integrate residential proxies (e.g., BrightData, Smartproxy) with Playwright to bypass LinkedIn's data center IP blocks.
- **Error Handling:** Wrap the `json.loads()` in the LLM processor with a fallback mechanism.
- **App Passwords:** Ensure the Google account being used for SMTP has 2FA enabled and a valid, dedicated "App Password" generated specifically for this project.
- **Artifacts:** Modify the GitHub Actions workflow to upload logs as an artifact so that debugging exact errors is easier.
