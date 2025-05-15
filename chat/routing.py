# from django.urls import path, include
# from chat.consumers import ChatConsumer


# websocket_urlpatterns = [
#     path("", ChatConsumer.as_asgi()),
# ]

from django.urls import re_path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>[^/]+)/$", ChatConsumer.as_asgi()),
]
