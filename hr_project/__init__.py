from __future__ import absolute_import, unicode_literals

from .celery import cel_app as celery_app

__all__ = ("celery_app",)
"""
The line above is so that CELERY starts when django starts.
"""
