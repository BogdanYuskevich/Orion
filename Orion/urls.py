from django.contrib import admin
from django.urls import path, include
from home.views import home_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('customers/', include('customers.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('employees/', include('employees.urls')),
    path('reports/', include('reports.urls')),
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls')),
]
