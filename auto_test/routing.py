
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import app_test.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            app_test.routing.websocket_urlpatterns
        )
    ),
})
