from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twentysixwordsday.settings.local')

app = Celery('twentysixwordsday')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_random_words': {
        'task': 'words.tasks.get_twenty_six_words_of_day',
        'schedule': crontab(minute=0, hour=0)
    }
}

app.conf.timezone = settings.TIME_ZONE


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
