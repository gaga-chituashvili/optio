from django.urls import path
from core.consumers import SegmentConsumer

websocket_urlpatterns = [
    path("ws/segments/", SegmentConsumer.as_asgi()),
]