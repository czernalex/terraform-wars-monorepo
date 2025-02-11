import os

from celery import Celery
from decouple import AutoConfig
from django.conf import settings


config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE", default="main.settings"))

app = Celery("terraform-wars-celery")

app.config_from_object("django.conf.settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(CELERYBEAT_SCHEDULE=settings.CELERYBEAT_SCHEDULE)
