from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Order, OrderItem
from products.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'notes']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показуємо лише товари, які є в наявності (in_stock=True і quantity > 0)
        self.fields['product'].queryset = Product.objects.filter(in_stock=True, quantity__gt=0)


class BaseOrderItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        has_item = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity')
                if product and quantity:
                    has_item = True
                    break

        if not has_item:
            raise forms.ValidationError("Необхідно додати хоча б один товар.")


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    formset=BaseOrderItemFormSet,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True
)
