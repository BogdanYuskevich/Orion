# forms.py

from django import forms
from .models import Employee

POSITION_CHOICES = [
    ('manager', 'Менеджер'),
    ('developer', 'Розробник'),
    ('designer', 'Дизайнер'),
    # додайте інші варіанти
]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'position']
        widgets = {
            'position': forms.Select(choices=POSITION_CHOICES),
        }
