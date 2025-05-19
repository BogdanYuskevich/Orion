from django.db import models
from customers.models import Customer
from products.models import Product  # Припускаємо, що ваша модель Product визначена у цьому модулі

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В очікуванні'),
        ('completed', 'Виконано'),
        ('canceled', 'Скасовано'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

    class Meta:
        ordering = ['-order_date']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Ціна за товар на момент створення замовлення (щоб зафіксувати, навіть якщо вона зміниться пізніше)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
