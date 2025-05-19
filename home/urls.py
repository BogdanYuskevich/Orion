from django.urls import path
from views import home_view
from api import dashboard_stats

urlpatterns = [
    path('', home_view, name='home'),
    path('api/dashboard/stats/', dashboard_stats, name='dashboard-stats'),
]
