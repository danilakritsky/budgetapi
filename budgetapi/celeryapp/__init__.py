import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "budgetapi.settings")

app = Celery("celeryapp")
app.config_from_object("django.conf:settings", namespace="CELERY")

# NOTE: celeryapp app must be registered in Django settings.py
app.autodiscover_tasks()
