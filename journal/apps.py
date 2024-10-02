<<<<<<< HEAD
from django.apps import AppConfig


class JournalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "journal"
    
    def ready(self):
        from . import signals


# Path: journal/signals.py
=======
from django.apps import AppConfig





class JournalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "journal"
    
    def ready(self):
        import journal.signals
>>>>>>> bc61eea2aedc4e423bc10c64ed6a584fcf87a9cc
