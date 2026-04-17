from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Customer, Segment
from core.services.queue import queue_update

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Customer)
def on_customer_update(sender, instance, **kwargs):

    queue_update(instance.id)

    channel_layer = get_channel_layer()

    segment = Segment.objects.first()

    if segment:
        async_to_sync(channel_layer.group_send)(
            "segments",
            {
                "type": "segment_update",
                "data": {
                    "segment_id": segment.id,
                    "added": [instance.id],
                    "removed": [],
                },
            },
        )