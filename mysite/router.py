import channels
from django.urls import path
import channels.auth
from django.conf import settings

from .schema import MyGraphqlWsConsumer

application = channels.routing.ProtocolTypeRouter({
    "websocket": channels.auth.AuthMiddlewareStack(
        channels.routing.URLRouter([
            path("ws/graphql", MyGraphqlWsConsumer.as_asgi(graphiql=settings.DEBUG)),
        ])
    ),
})