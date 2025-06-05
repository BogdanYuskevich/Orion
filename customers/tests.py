from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from customers.models import Customer, CustomerTask


class CustomerModelTest(TestCase):
    def setUp(self):
        # Створення початкового клієнта з усіма полями
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123456789",
            address="123 Main Street",
            notes="Test notes"
        )

    def test_str(self):
        """
        Тест перевіряє, що метод __str__ повертає 'first_name last_name'.
        """
        self.assertEqual(str(self.customer), "John Doe")

    def test_ordering(self):
        """
        Тест перевіряє, що клієнти впорядковані за збільшенням id.
        """
        customer2 = Customer.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            phone="987654321",
            address="456 Other St",
            notes=""
        )
        customers = list(Customer.objects.all())
        self.assertEqual(customers[0].id, self.customer.id)
        self.assertEqual(customers[1].id, customer2.id)

    def test_unique_email(self):
        """
        Тест перевіряє обмеження унікальності email.
        Повторне створення клієнта з уже існуючим email має викликати помилку.
        """
        with self.assertRaises(Exception):
            Customer.objects.create(
                first_name="Jane",
                last_name="Doe",
                email="john.doe@example.com",  # дублюючий email
                phone="111111111",
                address="",
                notes=""
            )

    def test_email_field_validation(self):
        """
        Тест перевіряє роботу валідатора для email.
        Якщо вказати некоректний email, має бути піднята ValidationError.
        """
        invalid_customer = Customer(
            first_name="Invalid",
            last_name="User",
            email="invalidemail",  # невалідний email
            phone="",
            address="",
            notes=""
        )
        with self.assertRaises(ValidationError):
            invalid_customer.full_clean()

    def test_blank_fields_allowed(self):
        """
        Тест перевіряє, що поля phone, address, notes можуть залишатися порожніми.
        """
        customer = Customer.objects.create(
            first_name="Blank",
            last_name="User",
            email="blank.user@example.com"
        )
        self.assertEqual(customer.phone, "")
        self.assertEqual(customer.address, "")
        self.assertEqual(customer.notes, "")


class CustomerTaskModelTest(TestCase):
    def setUp(self):
        # Створюємо клієнта для тестування завдань
        self.customer = Customer.objects.create(
            first_name="Lisa",
            last_name="Simpson",
            email="lisa.simpson@example.com",
            phone="555555555",
            address="742 Evergreen Terrace",
            notes="Loves learning"
        )
        # Створюємо завдання для даного клієнта
        self.task = CustomerTask.objects.create(
            customer=self.customer,
            title="Complete assignment",
            description="Finish the math assignment",
            due_date=date.today()
        )

    def test_str(self):
        """
        Тест перевіряє, що метод __str__ моделі CustomerTask повертає рядок у форматі:
        "<Назва завдання> - <Ім'я клієнта>".
        """
        expected = "Complete assignment - Lisa Simpson"
        self.assertEqual(str(self.task), expected)

    def test_task_relationship(self):
        """
        Тест перевіряє, що завдання можна отримати через пов'язаний менеджер (related_name 'tasks')
        з моделі Customer.
        """
        self.assertIn(self.task, self.customer.tasks.all())

    def test_task_null_customer(self):
        """
        Тест перевіряє, що можна створити завдання без прив'язки до клієнта (customer=None),
        і що метод __str__ правильно відображає це (повинен повернути "Title - None").
        """
        task_without_customer = CustomerTask.objects.create(
            customer=None,
            title="Independent Task",
            description="Task without a customer",
            due_date=date.today()
        )
        self.assertEqual(str(task_without_customer), "Independent Task - None")

    def test_due_date_manipulation(self):
        """
        Тест перевіряє, що поле due_date зберігається правильно.
        Наприклад, можна створити завдання з датою виконання в минулому.
        """
        past_date = date(2000, 1, 1)
        task_past = CustomerTask.objects.create(
            customer=self.customer,
            title="Past Task",
            description="Task with past due date",
            due_date=past_date
        )
        self.assertEqual(task_past.due_date, past_date)

    def test_cascade_delete_customer_tasks(self):
        """
        Тест перевіряє, що при видаленні клієнта всі пов'язані завдання видаляються (каскадне видалення).
        """
        customer_id = self.customer.id
        self.assertTrue(CustomerTask.objects.filter(customer=self.customer).exists())
        self.customer.delete()
        self.assertFalse(CustomerTask.objects.filter(customer__id=customer_id).exists())
