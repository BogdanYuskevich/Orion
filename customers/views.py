import csv
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Customer, CustomerTask
from .forms import CustomerForm, CustomerTaskForm
from django.views.decorators.http import require_POST

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')
        if sort_by:
            if order == 'desc':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо для кожного клієнта список завдань (тільки title та due_date)
        context['customer_tasks'] = {
            customer.id: list(
                CustomerTask.objects.filter(customer=customer)
                .values('title', 'due_date')
                .order_by('-due_date')
            )
            for customer in context['customers']
        }
        return context


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Клієнта успішно створено!")
        return response


def customer_tasks(request):
    """
    View для відображення списку завдань.
    Якщо в GET-параметрах задано customer_id, фільтруємо завдання по конкретному клієнту.
    """
    customer_id = request.GET.get('customer_id')
    tasks = CustomerTask.objects.all().order_by('-created_at')
    if customer_id:
        tasks = tasks.filter(customer_id=customer_id)
    context = {"tasks": tasks}
    return render(request, 'customers/customer_tasks.html', context)


def customer_task_create(request, customer_id):
    from .models import Customer
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Клієнта не знайдено")
        return redirect('customer-list')

    if request.method == "POST":
        form = CustomerTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.customer = customer  # Автоматичне призначення клієнта
            task.save()
            messages.success(request, "Завдання успішно створено!")
            return redirect('customer-tasks')
    else:
        form = CustomerTaskForm()

    context = {"form": form, "customer": customer}
    return render(request, 'customers/customer_task_form.html', context)


@require_POST
def inline_edit_customer(request):
    customer_id = request.POST.get('id')
    notes = request.POST.get('notes')
    if customer_id and notes is not None:
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.notes = notes
            customer.save()
            return JsonResponse({'status': 'success', 'message': 'Нотатки оновлено.'})
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Клієнта не знайдено.'})
    return JsonResponse({'status': 'error', 'message': 'Невірні параметри.'})


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Клієнта успішно оновлено!")
        return response


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Клієнта успішно видалено!")
        return response


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'


def export_customers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone'])
    for customer in Customer.objects.all():
        writer.writerow([customer.id, customer.first_name, customer.last_name, customer.email, customer.phone])
    return response
