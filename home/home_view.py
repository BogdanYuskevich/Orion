from django.shortcuts import render
from customers.models import Customer
from products.models import Product
from orders.models import Order
from employees.models import Employee
from datetime import datetime, timedelta

def home_view(request):
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_employees = Employee.objects.count()

    # Отримуємо останні 5 замовлень
    latest_orders = Order.objects.order_by('-order_date')[:5]

    # Дані для графіку: продажі за останні 7 днів
    chart_labels = []
    chart_data = []
    for i in range(7):
        day = datetime.today() - timedelta(days=6 - i)
        chart_labels.append(day.strftime("%d-%m"))
        daily_orders = Order.objects.filter(order_date__date=day.date()).count()
        chart_data.append(daily_orders)

    # Події для календаря (можна розширити)
    calendar_events = [
        {
            'title': 'Інвентаризація',
            'start': datetime.today().strftime("%Y-%m-%d")
        }
    ]

    context = {
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_employees': total_employees,
        'latest_orders': latest_orders,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'calendar_events': calendar_events,
    }
    return render(request, 'home/home.html', context)
