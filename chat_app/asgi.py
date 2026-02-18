import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

# Initialize Django FIRST
django.setup()

# Now import routing (after setup)
import chat.routing

# Get Django ASGI app
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
