import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

# Configuration
SENDER_EMAIL = "newmove2030@gmail.com"
SENDER_PASSWORD = "vzowmfjiumdjeute"
RECEIVER_EMAIL = "rokiroy2207@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

def send_test_email():
    print(f"Attempting to send email from {SENDER_EMAIL} into {RECEIVER_EMAIL}...")
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "Test Email from Python Script"
        body = "This is a test email sent from the Python script to verify credentials."
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def check_imap_access():
    print(f"\nAttempting to check IMAP access for {SENDER_EMAIL}...")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(SENDER_EMAIL, SENDER_PASSWORD)
        mail.select('inbox')

        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            print("❌ No messages found!")
            return

        message_ids = messages[0].split()
        latest_ids = message_ids[-5:] # Get last 5 emails

        print(f"✅ IMAP Login successful. Last {len(latest_ids)} email subjects:")
        
        for email_id in latest_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = email.header.decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    print(f" - {subject}")
        
        mail.close()
        mail.logout()
            
    except Exception as e:
        print(f"❌ Failed to check IMAP: {e}")

if __name__ == "__main__":
    send_test_email()
    check_imap_access()
