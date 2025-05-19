import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"  # Або "smtp.office365.com" для Outlook
SMTP_PORT = 587  # Використовуй 587 (TLS) або 465 (SSL)

EMAIL_SENDER = "yuskevich11@gmail.com"
EMAIL_PASSWORD = "pyji dday orzg whcl"  # Використовуй App Password!

EMAIL_RECEIVER = "yuskevich12@gmail.com"
SUBJECT = "🔴 Товар закінчився!"

# Формуємо email
msg = MIMEMultipart()
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = SUBJECT

# Вміст email
message_body = "Товар закінчився! Перевірте наявність у системі."
msg.attach(MIMEText(message_body, "plain"))

# Відправлення
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()  # Захищене з'єднання
server.login(EMAIL_SENDER, EMAIL_PASSWORD)
server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
server.quit()

print("✅ Email надіслано успішно!")
