# myproject/celery.py

from __future__ import absolute_import, unicode_literals
import logging
import os
from celery import Celery
import celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plutus.settings')

# create a Celery instance and configure it using the settings from Django.
app = Celery('plutus')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@celery.signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    return logging.getLogger('celery')
