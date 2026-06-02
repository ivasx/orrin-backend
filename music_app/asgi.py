import os

from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_app.settings.production")

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from users.ws_middleware import JWTAuthMiddleware
from users.consumers import NotificationConsumer
from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter([
            path("ws/notifications/", NotificationConsumer.as_asgi()),
            path("ws/chat/<int:chat_id>/", ChatConsumer.as_asgi()),
        ])
    ),
})
