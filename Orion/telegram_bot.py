import requests
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

TELEGRAM_TOKEN = "7966266590:AAHJLrAQmL_-PrBmlWaHfHHJuxQ8ZlZXPHU"
CHAT_ID = "541931591"
WEBHOOK_URL = "https://your-domain.com/telegram-webhook"

def send_telegram_message(text, keyboard=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    requests.post(url, data=data)

def notify_out_of_stock(product):
    keyboard = {
        "inline_keyboard": [[{"text": "🔄 В наявності", "callback_data": f"back_in_stock_{product.id}"}]]
    }
    send_telegram_message(f"🔴 Товар *{product.name}* закінчився!", keyboard)

@csrf_exempt
def telegram_webhook(request):
    data = json.loads(request.body.decode("utf-8"))
    if "callback_query" in data:
        callback_data = data["callback_query"]["data"]
        chat_id = data["callback_query"]["message"]["chat"]["id"]

        if callback_data.startswith("back_in_stock_"):
            product_id = int(callback_data.split("_")[-1])
            ask_quantity(chat_id, product_id)

    return JsonResponse({"status": "ok"})

def ask_quantity(chat_id, product_id):
    send_telegram_message(f"Скільки одиниць товару доступно?", {"force_reply": True})

@csrf_exempt
def handle_quantity_reply(request):
    data = json.loads(request.body.decode("utf-8"))
    if "message" in data and "reply_to_message" in data["message"]:
        product_id = int(data["message"]["reply_to_message"]["text"].split("_")[-1])
        new_quantity = int(data["message"]["text"])

        from products.models import Product
        product = Product.objects.get(id=product_id)
        product.quantity = new_quantity
        product.in_stock = True
        product.save()

        send_telegram_message(f"✅ Товар *{product.name}* оновлений! Тепер доступно {new_quantity} одиниць.")
