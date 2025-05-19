from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['id']

class CustomerTask(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)  # Додаємо зв'язок!

    title = models.CharField(max_length=255, verbose_name="Назва завдання")
    description = models.TextField(blank=True, verbose_name="Опис")
    due_date = models.DateField(verbose_name="Дата виконання")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.title} - {self.customer}"

