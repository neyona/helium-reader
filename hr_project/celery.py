from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from hr_project.settings import base, development, production

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hr_project.settings.development")

cel_app = Celery("hr_project")

cel_app.conf.timezone = 'America/New_York'
# the following makes putting CELERY_ at the beginning of a variable work.
cel_app.config_from_object("hr_project.settings.development", namespace="CELERY"),

cel_app.autodiscover_tasks(lambda: base.INSTALLED_APPS)

cel_app.conf.beat_schedule = {
    'sample_task': {
        'task': 'apps.hotspots.tasks.sample_task',
        'schedule': crontab(minute="*/1"),
    },
    # Scheduler Name
    'reward_test_once_a_day': {
        # Task Name (Name Specified in Decorator)
        'task': 'apps.hotspots.tasks.update_helium_data',
        # Schedule
        'schedule': crontab(minute=30)
    }
}
