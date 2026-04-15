from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Customer
from core.services.queue import queue_update


@receiver(post_save, sender=Customer)
def on_customer_update(sender, instance, **kwargs):
    queue_update(instance.id)