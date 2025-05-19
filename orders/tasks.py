# orders/tasks.py
from datetime import datetime
from orders.models import Order  # імпортуємо модель замовлень

def generate_daily_report():
    """
    Функція для генерації щоденного звіту.
    Підраховує кількість замовлень за поточний день.
    """
    today = datetime.today().date()
    order_count = Order.objects.filter(order_date__date=today).count()

    print(f"Daily report for {today}: {order_count} orders")
    return order_count
