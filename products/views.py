from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Product
from .forms import ProductForm
from django.db import models
from notifications.email_notifications import send_email_notification

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        # Сортування за GET-параметрами (наприклад, sort_by=name)
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')
        if sort_by:
            if order == 'desc':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('name')
        return queryset

import csv
from django.http import HttpResponse
from .models import Product

def export_products(request, in_stock_only=False):
    """Експорт продуктів у CSV, з можливістю фільтрувати тільки ті, яких немає в наявності"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['Назва', 'Категорія', 'Ціна', 'Знижка', 'Кінцева ціна', 'Наявність'])

    products = Product.objects.filter(in_stock=False) if not in_stock_only else Product.objects.all()

    for product in products:
        writer.writerow([
            product.name,
            product.category.name if product.category else "Без категорії",
            product.price,
            product.discount,
            product.final_price(),
            "В наявності" if product.in_stock else "Немає"
        ])

    return response

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
