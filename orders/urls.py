from django.urls import path
from .views import (
    OrderListView,
    order_create,  # Функція-подання, не викликаємо її!
    OrderUpdateView,
    OrderDeleteView,
    OrderAnalyticsView,
    ExportOrdersXLSX,
    OrderDetailView, OrderAnalyticsView
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('analytics/', OrderAnalyticsView.as_view(), name='order-analytics'),
    path('create/', order_create, name='order-create'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('export/xlsx/', ExportOrdersXLSX.as_view(), name='export-orders-xlsx'),
]
