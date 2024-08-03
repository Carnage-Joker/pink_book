from django.core.management.base import BaseCommand
from journal.models import Habit
import uuid


class Command(BaseCommand):
    help = 'Update habit IDs to UUIDs'

    def handle(self, *args, **kwargs):
        habits = Habit.objects.all()
        for habit in habits:
            if not isinstance(habit.id, uuid.UUID):
                habit.id = uuid.uuid4()
                habit.save()
        self.stdout.write(self.style.SUCCESS(
            'Successfully updated habit IDs to UUIDs'))
