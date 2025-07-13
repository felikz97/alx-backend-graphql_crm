# crm/__init__.py
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ['celery_app']
# This file is required to ensure that the celery app is loaded when Django starts.