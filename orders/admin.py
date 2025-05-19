from django.contrib import admin
from .models import Order

# Переконайтеся, що тут лише один виклик:
admin.site.register(Order)
