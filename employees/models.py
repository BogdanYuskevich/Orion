# models.py

from django.db import models

POSITION_CHOICES = [
    ('manager', 'Менеджер'),
    ('developer', 'Розробник'),
    ('designer', 'Дизайнер'),
    # додайте інші варіанти за потребою
]

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='developer')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
