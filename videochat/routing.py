# chat/routing.py
from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:lobby_code>/<str:username>', consumers.VideoConsumer.as_asgi()),
]
