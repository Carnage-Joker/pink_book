"""
Package for Pink_Book.
"""
from .celery import app as celery_app

__all__ = ('celery_app',)
