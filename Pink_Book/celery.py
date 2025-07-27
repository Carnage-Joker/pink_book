import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pink_Book.settings')

app = Celery('Pink_Book')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
