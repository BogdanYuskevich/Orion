from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Product, Category
from decimal import Decimal
from unittest.mock import patch


class ProductModelTest(TestCase):

    def setUp(self):
        """Створення категорії та базового продукту для тестування."""
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('100.00'),
            discount=10,  # Знижка 10%
            quantity=10,
            in_stock=True,
            category=self.category
        )

    def test_final_price_with_discount(self):
        """Тестування розрахунку фінальної ціни при знижці 10%."""
        expected_price = Decimal('90.00')  # 100 * (1 - 0.10)
        self.assertEqual(self.product.final_price(), expected_price)

    def test_final_price_without_discount(self):
        """Тестування розрахунку ціни без знижки."""
        product_no_discount = Product.objects.create(
            name="Test Product No Discount",
            description="Test Description",
            price=Decimal('100.00'),
            discount=0,  # Без знижки
            quantity=10,
            in_stock=True,
            category=self.category
        )
        self.assertEqual(product_no_discount.final_price(), Decimal('100.00'))

    def test_product_name_validation(self):
        """
        Тест збереження продукту з короткою назвою.
        Оскільки у моделі немає обмеження на мінімальну довжину,
        валідація має пройти без помилок.
        """
        short_name_product = Product(
            name="AB",  # коротка назва
            price=Decimal('100.00'),
            discount=10,
            quantity=10,
            in_stock=True,
            category=self.category
        )
        try:
            short_name_product.full_clean()  # Немає додаткових валідаторів, тому помилки не повинно бути
        except ValidationError:
            self.fail("full_clean() викликала ValidationError для короткої назви, хоча валідаторів немає.")

    def test_product_price_validation(self):
        """
        Тест збереження продукту з негативною ціною.
        Оскільки додаткових валідаторів для ціни немає,
        продукт із негативною ціною має зберігатися, а розрахунок final_price проводитиметься згідно з логікою.
        """
        neg_price_product = Product(
            name="Product with Negative Price",
            price=Decimal('-10.00'),
            discount=10,
            quantity=10,
            in_stock=True,
            category=self.category
        )
        try:
            neg_price_product.full_clean()
        except ValidationError:
            self.fail("full_clean() викликала ValidationError для негативної ціни, хоча додаткових валідаторів немає.")
        # Перевіряємо розрахунок фінальної ціни:
        expected_final_price = round(Decimal('-10.00') * (Decimal(1) - Decimal(10) / Decimal(100)), 2)  # = -9.00
        self.assertEqual(neg_price_product.final_price(), expected_final_price)

    def test_product_discount_validation(self):
        """
        Тест збереження продукту із знижкою більше 100%.
        Оскільки обмеження на максимальну знижку не реалізовано, дані зберігаються,
        а розрахунок final_price проводиться відповідно: 100*(1 - 1.5) = -50.00.
        """
        discount_product = Product(
            name="Product with High Discount",
            price=Decimal('100.00'),
            discount=150,  # Знижка 150%
            quantity=10,
            in_stock=True,
            category=self.category
        )
        try:
            discount_product.full_clean()
        except ValidationError:
            self.fail("full_clean() викликала ValidationError для знижки більше 100%, хоча обмеження відсутнє.")
        expected_final_price = round(Decimal('100.00') * (Decimal(1) - Decimal(150) / Decimal(100)), 2)  # = -50.00
        self.assertEqual(discount_product.final_price(), expected_final_price)

    def test_product_belongs_to_category(self):
        """Перевірка правильної прив'язки продукту до категорії."""
        self.assertEqual(self.product.category.name, "Test Category")
        self.assertEqual(self.product.category, self.category)

    def test_product_creation(self):
        """Тест створення нового продукту."""
        product = Product.objects.create(
            name="New Product",
            price=Decimal('200.00'),
            discount=0,
            quantity=20,
            in_stock=True,
            category=self.category
        )
        # На даний момент має бути загалом 2 продукти (setUp + новий)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(product.name, "New Product")
        self.assertEqual(product.price, Decimal('200.00'))
        self.assertEqual(product.category.name, "Test Category")

    @patch('products.models.send_email_notification')  # Патчимо функцію там, де вона використовується
    def test_save_product_out_of_stock(self, mock_send_email_notification):
        """
        Перевірка, що при зменшенні quantity до 0 відбувається:
         - виклик функції send_email_notification (за допомогою патчу),
         - оновлення статусу in_stock на False,
         - додаткове збереження змін у базі даних.
        """
        # Переконуємось, що макет виклику ще не було
        mock_send_email_notification.assert_not_called()

        # Зменшуємо кількість до 0 та зберігаємо продукт
        self.product.quantity = 0
        self.product.save()

        # Перевірка виклику email-сповіщення
        mock_send_email_notification.assert_called_once_with(
            receiver_email="yuskevich12@gmail.com",
            product=self.product
        )

        # Перевірка, що статус товару оновлено
        self.assertFalse(self.product.in_stock)
        self.product.refresh_from_db()
        self.assertFalse(self.product.in_stock)

    def test_discount_change(self):
        """Тест зміни знижки та перевірки нового значення фінальної ціни."""
        # Початкова ціна 100.00, початкова знижка 10% дає final_price = 90.00
        self.product.discount = 20  # Змінюємо знижку на 20%
        self.product.save()
        expected_price = round(Decimal('100.00') * (Decimal(1) - Decimal(20) / Decimal(100)), 2)  # 80.00
        self.assertEqual(self.product.final_price(), expected_price)
