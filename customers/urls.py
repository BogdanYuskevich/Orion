# customers/urls.py

from django.urls import path
from . import views

import customers.models
from .views import (
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    CustomerDetailView,
    export_customers_csv,
)

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-list'),
    path('create/', CustomerCreateView.as_view(), name='customer-create'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),

    path('<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('export/csv/', export_customers_csv, name='export-customers-csv'),


]

# customers/urls.py (додатково)
from .views import inline_edit_customer
urlpatterns += [
    path('ajax/inline-edit/', inline_edit_customer, name='inline-edit-customer'),
]
