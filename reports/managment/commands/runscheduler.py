# reports/management/commands/runscheduler.py
import datetime
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, DjangoJobExecution
from orders.tasks import generate_daily_report

class Command(BaseCommand):
    help = "Запускає APScheduler для виконання періодичних завдань."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone="UTC")
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Використовуємо CronTrigger, щоб запускати завдання кожного дня о 00:00, наприклад.
        scheduler.add_job(
            generate_daily_report,
            trigger=CronTrigger(hour=0, minute=0),
            id="daily_report",                         # унікальний ID завдання
            max_instances=1,
            replace_existing=True,
        )
        self.stdout.write("Додано завдання щоденного звіту до APScheduler.")

        # Регистрация подій для збереження результатів виконання завдань в БД (опційно)
        register_events(scheduler)

        try:
            self.stdout.write("Запуск розкладу APScheduler. Натисніть Ctrl+C для зупинки.")
            scheduler.start()
        except Exception as e:
            self.stdout.write(f"Помилка: {e}")
            scheduler.shutdown()
