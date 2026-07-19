"""WSGI config for fitconnect project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitconnect.settings')

app = get_wsgi_application()
