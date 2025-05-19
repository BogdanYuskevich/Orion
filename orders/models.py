from django.db import models
from customers.models import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)  # Поле notes

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

    class Meta:
        ordering = ['-order_date']
