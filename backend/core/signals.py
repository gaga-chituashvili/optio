from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Customer, Segment
from core.tasks import evaluate_segment_task
from core.services.queue import queue_update


@receiver(post_save, sender=Customer)
def on_customer_update(sender, instance, **kwargs):
    segments = Segment.objects.filter(is_dynamic=True)

    for segment in segments:
        evaluate_segment_task.delay(segment.id)




@receiver(post_save, sender=Customer)
def on_customer_update(sender, instance, **kwargs):
    queue_update(instance.id)