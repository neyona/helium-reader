from .base import *
import os
import re
import mimetypes

mimetypes.add_type("application/javascript", ".js", True)

ALLOWED_HOSTS = ['*']


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

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://127.0.0.1:8000\$",
    r"^http://127.0.0.1:3000\$",
    r"^http://127.0.0.1:4000\$",
    r"^http://localhost:8000\$",
    r"^http://localhost:3000\$",
    r"^http://localhost:4000\$"
]

# A list of trusted origins for unsafe requests (e.g. POST).
# the following is from Django itself
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:4000',
    'http://127.0.0.1:4000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:1337',
]
