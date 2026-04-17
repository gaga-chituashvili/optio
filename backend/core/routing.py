from django.urls import path, re_path
from core.consumers import SegmentConsumer

websocket_urlpatterns = [
    re_path(r"ws/segments/$", SegmentConsumer.as_asgi()),
]