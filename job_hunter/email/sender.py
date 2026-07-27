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
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
      </head>
      <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #2C3E50; background-color: #F8F9FA; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <div style="background: linear-gradient(135deg, #1A2980 0%, #26D0CE 100%); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 1px;">Cyber Security Job Matches</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Exclusively curated for Aryan Kumar</p>
            </div>
            
            <div style="padding: 30px;">
                <p style="font-size: 16px; line-height: 1.6; margin-bottom: 25px;">Hi <strong>Aryan</strong>,<br><br>Your AI assistant has scoured the web and found <strong>{len(jobs)}</strong> highly relevant roles matching your exact VAPT and Cyber Security experience.</p>
    """
    
    for job in jobs:
        html += f"""
                <div style="margin-bottom: 25px; padding: 20px; border-left: 4px solid #26D0CE; background: #F8F9FA; border-radius: 0 8px 8px 0;">
                    <h3 style="margin: 0 0 5px 0; color: #1A2980; font-size: 18px;">{job.title}</h3>
                    <p style="margin: 0 0 15px 0; color: #7F8C8D; font-size: 14px; font-weight: 500;">{job.company} &bull; {job.location}</p>
                    
                    <div style="margin-bottom: 15px;">
                        <span style="background: #E8F8F5; color: #117A65; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">Match Score: {job.ai_score}/100</span>
                    </div>
                    
                    <p style="margin: 0 0 10px 0; font-size: 14px; line-height: 1.5;"><strong>Why it's a match:</strong> {job.ai_summary}</p>
                    <p style="margin: 0 0 20px 0; font-size: 13px; color: #666; font-style: italic;"><strong>Key Skills:</strong> {job.key_skills}</p>
                    
                    <a href="{job.link}" style="display: inline-block; padding: 10px 20px; background: #1A2980; color: #fff; text-decoration: none; border-radius: 6px; font-size: 14px; font-weight: 500;">Apply Now</a>
                </div>
        """
        
    html += """
            </div>
            <div style="background: #F1F2F6; padding: 20px; text-align: center; font-size: 12px; color: #95A5A6;">
                <p style="margin: 0;">Automated via Cyber Security Job Hunter Pipeline</p>
            </div>
        </div>
      </body>
    </html>
    """
    return html

def send_daily_email():
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("[!] Email credentials missing. Skipping email report.")
        return

    session = get_session()
    # Get jobs from last 1h with high score
    past_hour = datetime.utcnow() - timedelta(hours=1)
    top_jobs = session.query(Job).filter(
        Job.date_posted >= past_hour,
        Job.ai_score >= MIN_MATCH_SCORE_EMAIL
    ).order_by(Job.ai_score.desc()).all()
    session.close()

    if not top_jobs:
        print("[*] No high-scoring jobs found today. Sending fallback email.")
        send_system_email(
            subject="Status: No Jobs Found (Hourly Alert)",
            body="Sorry, no new matching jobs were scraped in this hour."
        )
        return

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"🚀 {len(top_jobs)} New Cyber Security Jobs (Hourly Alert: {datetime.now().strftime('%H:%M')})"
    msg["From"] = SENDER_EMAIL
    receivers = [r.strip() for r in RECEIVER_EMAIL.split(',')]
    msg["To"] = ", ".join(receivers)

    # Attach HTML
    html_content = generate_html_report(top_jobs)
    msg.attach(MIMEText(html_content, "html"))

    # Attach CSV
    import os
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(CSV_PATH)}",
            )
            msg.attach(part)
    try:
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receivers, msg.as_string())
        server.quit()
        print("[+] Daily email report sent successfully!")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")

def send_system_email(subject, body):
    """Utility to send basic text emails (errors, welcome messages, no-jobs)."""
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        return

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    receivers = [r.strip() for r in RECEIVER_EMAIL.split(',')]
    msg["To"] = ", ".join(receivers)
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receivers, msg.as_string())
        server.quit()
        print(f"[+] System email '{subject}' sent successfully!")
    except Exception as e:
        print(f"[-] Failed to send system email: {e}")
