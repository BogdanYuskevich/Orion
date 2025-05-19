import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification = f"Нове замовлення #{instance.id} від {instance.order_date:%d-%m-%Y}"
        async_to_sync(channel_layer.group_send)(
            "dashboard",
            {
                "type": "dashboard.notification",  # метод у Consumer має називатися dashboard_notification
                "notification": notification,
            }
        )
