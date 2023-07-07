from .base import *
import os
import re

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASS'),
        'HOST': os.environ.get('PG_HOST'),
        'PORT': os.environ.get('PG_PORT'),
    }
}

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND')
CELERY_TIMEZONE = 'America/New_York'
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
