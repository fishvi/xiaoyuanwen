from django.urls import path
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from xiaoyuanwen.messager.consumers import MessagesConsumer
from xiaoyuanwen.notifications.consumers import NotificationsConsumer


application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/notifications/', NotificationsConsumer),
                path('ws/<str:username>/', MessagesConsumer),
            ])
        )
    )
})
