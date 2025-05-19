import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Конфігурація SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "yuskevich11@gmail.com"
EMAIL_PASSWORD = "pyji dday orzg whcl"  # Використовуй App Password

def send_email_notification(receiver_email, product):
    """Надсилає email-сповіщення адміністратору про закінчення товару"""
    subject = f"🔴 {product.name} закінчився!"
    message_body = (
        f"Товар **{product.name}** закінчився!\n"
        f"Категорія: {product.category.name if product.category else 'Без категорії'}\n"
        f"Ціна: {product.price} грн\n"
        f"Опис: {product.description}\n\n"
        f"Будь ласка, перевірте наявність у системі."
    )

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message_body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, receiver_email, msg.as_string())
        server.quit()
        print(f"✅ Email надіслано адміністратору: {receiver_email}")
    except Exception as e:
        print(f"❌ Помилка під час надсилання email: {e}")
