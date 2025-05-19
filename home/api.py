from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import Order
from datetime import datetime, timedelta

@api_view(['GET'])
def dashboard_stats(request):
    # Повертаємо статистику за останні 7 днів
    last_7_days = []
    for i in range(7):
        day = datetime.today() - timedelta(days=6 - i)
        count = Order.objects.filter(order_date__date=day.date()).count()
        last_7_days.append({
            'date': day.strftime("%d-%m"),
            'orders': count
        })
    return Response({'last_7_days': last_7_days})
