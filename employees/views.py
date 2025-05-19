from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q
from .models import Employee
from .forms import EmployeeForm

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Пошук за ім'ям або прізвищем
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            )
        # Сортування за GET-параметрами sort_by та order (за замовчуванням - за прізвищем)
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')
        if sort_by:
            if order == 'desc':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('last_name')
        return queryset

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee-list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee-list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee-list')

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
