"""WSGI config for FitConnect - also used as Vercel entrypoint."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitconnect.settings')
app = get_wsgi_application()  # Vercel looks for `app`
application = app  # gunicorn / standard WSGI
