from django.urls import path
from .views import daily_report_view, export_pdf_report, export_excel_report

urlpatterns = [
    path('daily/', daily_report_view, name='daily_report'),
    path('export/pdf/', export_pdf_report, name='export_pdf_report'),
    path('export/excel/', export_excel_report, name='export_excel_report'),
]
