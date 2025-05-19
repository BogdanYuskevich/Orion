import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "yuskevich11@gmail.com"
EMAIL_PASSWORD = "pyji dday orzg whcl"

def send_email_notification(receiver_email, subject, message_body):
    """Надсилає email-сповіщення адміністратору про закінчення товару"""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message_body, "plain"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, receiver_email, msg.as_string())
    server.quit()

    print(f"✅ Email надіслано на {receiver_email}")
