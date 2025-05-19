from django.db import models
from products.models import Product


class InventoryTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('in', 'Надходження'),
        ('out', 'Відвантаження'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} {self.quantity} для {self.product.name}"
