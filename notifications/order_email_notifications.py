import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "yuskevich11@gmail.com"
EMAIL_PASSWORD = "pyji dday orzg whcl"  # Використовуй App Password


def send_order_notification(receiver_email, order, order_items):
    """
    Надсилає email-сповіщення про нове замовлення із переліком товарів.

    Параметри:
      receiver_email – адреса отримувача (наприклад, менеджера)
      order – об'єкт замовлення
      order_items – список позицій замовлення (OrderItem), для кожного з яких
                     використовуються значення price_at_order, quantity та product.name
    """
    subject = "Нове замовлення!"

    # Формуємо перелік замовлених товарів
    items_text = ""
    for item in order_items:
        items_text += (
            f"{item.product.name} - кількість: {item.quantity}, "
            f"ціна: {item.price_at_order} грн\n"
        )

    message_body = (
        f"Нове замовлення отримано!\n\n"
        f"Замовлення №: {order.id}\n"
        f"Клієнт: {order.customer}\n"
        f"Дата: {order.order_date.strftime('%Y-%m-%d %H:%M')}\n\n"
        f"Замовлені товари:\n{items_text}\n"
        f"Загальна сума: {order.total_amount} грн\n\n"

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
