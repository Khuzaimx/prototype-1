"""
ASGI config for classalarm_backend project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classalarm_backend.settings')

application = get_asgi_application()
