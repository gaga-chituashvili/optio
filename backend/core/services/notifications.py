from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def notify(delta):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "segments",
        {
            "type": "segment_update",
            "data": {
                "segment_id": delta.segment.id,
                "added": delta.added,
                "removed": delta.removed
            }
        }
    )