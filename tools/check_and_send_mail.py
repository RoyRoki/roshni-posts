import smtplib
import imaplib
import email
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = "newmove2030@gmail.com"
EMAIL_PASS = os.getenv("EMAIL_PASSWORD")
ALERT_RECIPIENT = "rokiroy2207@gmail.com"

def send_alert_email(subject, body):
    """
    Sends an email to the alert recipient.
    """
    if not EMAIL_PASS:
        print("Error: EMAIL_PASSWORD not set. Cannot send email.")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = ALERT_RECIPIENT
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, ALERT_RECIPIENT, text)
        server.quit()
        print(f"Alert email sent to {ALERT_RECIPIENT}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def check_recent_emails(limit=5):
    """
    Lists the last 'limit' emails from the inbox.
    """
    if not EMAIL_PASS:
        print("Error: EMAIL_PASSWORD not set. Cannot check emails.")
        return

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('inbox')

        _, search_data = mail.search(None, 'ALL')
        mail_ids = search_data[0].split()
        
        print(f"--- Last {limit} Emails ---")
        # Get the last 'limit' emails
        for i in range(len(mail_ids) - 1, max(len(mail_ids) - 1 - limit, -1), -1):
            _, msg_data = mail.fetch(mail_ids[i], '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = email.header.decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    from_ = msg.get("From")
                    print(f"From: {from_}\nSubject: {subject}\n---")
        
        mail.close()
        mail.logout()
    except Exception as e:
        print(f"Failed to check emails: {e}")

if __name__ == "__main__":
    # Test run
    print("Testing email functionality...")
    check_recent_emails(5)
    # Uncomment to test sending
    # send_alert_email("Test Alert", "This is a test alert from the automated script.")
