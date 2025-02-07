"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from decouple import AutoConfig
from django.core.wsgi import get_wsgi_application

config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE", default="main.settings"))

application = get_wsgi_application()
