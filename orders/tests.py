from django.test import TestCase
from decimal import Decimal
from orders.models import Order, OrderItem
from customers.models import Customer
from products.models import Product, Category


class OrderModelTest(TestCase):
    def setUp(self):
        # Створення тестового клієнта з використанням полів вашої моделі Customer
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="Customer",
            email="test@example.com",
            phone="1234567890",
            address="Test Address",
            notes="Test Notes"
        )

        # Створення тестової категорії
        self.category = Category.objects.create(name="Test Category")

        # Створення тестового товару
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product",
            price=Decimal("50.00"),
            discount=0,
            quantity=10,
            in_stock=True,
            category=self.category
        )

        # Створення замовлення
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=Decimal("0.00"),
            status='pending'
        )

        # Створення позиції замовлення (OrderItem)
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_order=Decimal("50.00")
        )

    def test_order_default_values(self):
        """
        Тест перевіряє, що при створенні замовлення:
          - статус за замовчуванням 'pending',
          - total_amount дорівнює 0.00,
          - встановлено дату замовлення (order_date),
          - метод __str__ повертає очікуване представлення.
        """
        order = Order.objects.create(customer=self.customer)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, Decimal("0.00"))
        self.assertIsNotNone(order.order_date)
        expected_str = f"Order #{order.id} - {self.customer}"
        self.assertEqual(str(order), expected_str)

    def test_order_ordering(self):
        """
        Тест перевіряє, що замовлення впорядковані за спаданням order_date.
        Останнє створене замовлення має бути першим у списку.
        """
        order1 = Order.objects.create(customer=self.customer)
        order2 = Order.objects.create(customer=self.customer)
        orders = list(Order.objects.all())
        self.assertEqual(orders[0].id, order2.id)
        self.assertEqual(orders[1].id, order1.id)

    def test_order_item_str(self):
        """
        Тест перевіряє, що метод __str__ для OrderItem повертає рядок у форматі:
        "Назва товару x Кількість".
        """
        expected_str = f"{self.product.name} x {self.order_item.quantity}"
        self.assertEqual(str(self.order_item), expected_str)

    def test_order_items_relation(self):
        """
        Тест перевіряє, що для замовлення через пов'язаний менеджер (related_name 'items')
        повертається створена позиція замовлення.
        """
        self.assertEqual(self.order.items.count(), 1)
        self.assertIn(self.order_item, self.order.items.all())

    def test_order_cascade_delete(self):
        """
        Тест перевіряє, що при видаленні замовлення всі пов'язані позиції замовлення (OrderItem)
        видаляються завдяки каскадному видаленню.
        """
        order_id = self.order.id
        self.order.delete()
        self.assertFalse(OrderItem.objects.filter(order_id=order_id).exists())

    def test_total_amount_update(self):
        """
        Тест перевіряє, що поле total_amount замовлення може бути оновлено,
        і нове значення зберігається у базі даних.
        """
        self.order.total_amount = Decimal("100.00")
        self.order.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, Decimal("100.00"))
