import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from job_hunter.config.settings import SMTP_SERVER, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL, CSV_PATH, MIN_MATCH_SCORE_EMAIL
from job_hunter.database.db import get_session
from job_hunter.database.models import Job

def generate_html_report(jobs):
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #0056b3;">Daily Job Hunter Report</h2>
        <p>Found <strong>{len(jobs)}</strong> high-quality jobs matching your profile today.</p>
        <hr>
    """
    
    for job in jobs:
        html += f"""
        <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 8px;">
            <h3>{job.title} @ {job.company}</h3>
            <p><strong>AI Match Score:</strong> <span style="color: green; font-size: 1.1em;">{job.ai_score}/100</span></p>
            <p><strong>Skills:</strong> {job.key_skills}</p>
            <p><strong>Summary:</strong> {job.ai_summary}</p>
            <a href="{job.link}" style="display: inline-block; margin-top: 10px; padding: 8px 15px; background: #0056b3; color: #fff; text-decoration: none; border-radius: 5px;">View Job</a>
        </div>
        """
        
    html += "</body></html>"
    return html

def send_daily_email():
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("[!] Email credentials missing. Skipping email report.")
        return

    session = get_session()
    # Get jobs from last 24h with high score
    yesterday = datetime.utcnow() - timedelta(days=1)
    top_jobs = session.query(Job).filter(
        Job.date_posted >= yesterday,
        Job.ai_score >= MIN_MATCH_SCORE_EMAIL
    ).order_by(Job.ai_score.desc()).all()
    session.close()

    if not top_jobs:
        print("[*] No high-scoring jobs found today. Skipping email.")
        return

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"🚀 Top {len(top_jobs)} Cyber Security Jobs for {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    # Attach HTML
    html_content = generate_html_report(top_jobs)
    msg.attach(MIMEText(html_content, "html"))

    # Attach CSV
    try:
        with open(CSV_PATH, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= jobs.csv")
        msg.attach(part)
    except Exception as e:
        print(f"[-] Could not attach CSV: {e}")

    try:
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("[+] Daily email report sent successfully!")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")
