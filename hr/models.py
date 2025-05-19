from django.db import models
from accounts.models import CustomUser


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    hire_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"
