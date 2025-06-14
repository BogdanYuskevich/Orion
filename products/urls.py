
from django.urls import path
from .views import export_products
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/export/', export_products, name='export-products'),
    path('products/export/out-of-stock/', export_products, {'in_stock_only': False}, name='export-out-of-stock'),
]
