from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'discount', 'quantity', 'in_stock']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Назва продукту має містити щонайменше 3 символи.")
        return name

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Ціна повинна бути більше 0.")
        return price

    def clean_discount(self):
        discount = self.cleaned_data['discount']
        if discount < 0 or discount > 100:
            raise forms.ValidationError("Знижка має бути в діапазоні 0-100%.")
        return discount


    def product_list(request):
        search_query = request.GET.get('q', '')
        category_id = request.GET.get('category', '')
        sort_by = request.GET.get('sort_by', 'name')
        items_per_page = request.GET.get('items_per_page', 20)  # За замовчуванням 20 товарів

        products = Product.objects.all()

        if search_query:
            products = products.filter(name__icontains=search_query)

        if category_id:
            products = products.filter(category_id=category_id)

        products = products.order_by(sort_by)

        paginator = Paginator(products, items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()

        return render(request, 'product_list.html', {
            'page_obj': page_obj,
            'paginator': paginator,
            'products': page_obj.object_list,
            'categories': categories,
            'items_per_page': items_per_page
        })
