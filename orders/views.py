from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Order
from .forms import OrderForm

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            # Шукаємо по імені клієнта або за статусом
            queryset = queryset.filter(customer__first_name__icontains=search_query) | queryset.filter(status__icontains=search_query)
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')
        if sort_by:
            if order == 'desc':
                sort_by = '-' + sort_by
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-order_date')
        return queryset

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order-list')

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order-list')

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('order-list')

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
