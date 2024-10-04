from django.apps import AppConfig


class JournalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "journal"
    
    def ready(self):
        from . import signals


# Path: journal/signals.py
# Compare this snippet from manage.py:
# """Django's command-line utility for administrative tasks."""
