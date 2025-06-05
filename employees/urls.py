from django.urls import path
from .views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    EmployeeDetailView
)

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee-list'),
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
]
