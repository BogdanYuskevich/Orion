from django.db import models
from decimal import Decimal
from notifications.email_notifications import send_email_notification  # ✅ Імпорт функції

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категорія")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва продукту")
    description = models.TextField(blank=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    discount = models.PositiveIntegerField(default=0, verbose_name="Знижка (%)")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість")
    in_stock = models.BooleanField(default=True, verbose_name="В наявності")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категорія")

    def final_price(self):
        """Розрахунок фінальної ціни після знижки"""
        return round(self.price * (Decimal(1) - Decimal(self.discount) / Decimal(100)), 2)

    def save(self, *args, **kwargs):
        """Перевіряємо, чи товар закінчився, і надсилаємо email-сповіщення"""
        super().save(*args, **kwargs)
        if self.quantity == 0:
            send_email_notification(
                receiver_email="yuskevich12@gmail.com",
                product=self  # ✅ Передаємо товар у email-сповіщення
            )
            self.in_stock = False  # ✅ Оновлюємо статус товару
            super().save(*args, **kwargs)  # ✅ Додаткове збереження

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        ordering = ['name']
