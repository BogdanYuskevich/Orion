# dashboard/views.py
from django.shortcuts import render
from django.db.models import Sum
from customers.models import Customer
from products.models import Product
from orders.models import Order
from employees.models import Employee

def dashboard_view(request):
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_orders   = Order.objects.count()
    total_employees = Employee.objects.count()  # Оновлення кількості співробітників

    context = {
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_employees': total_employees,
    }
    return render(request, 'dashboard/dashboard.html', context)
