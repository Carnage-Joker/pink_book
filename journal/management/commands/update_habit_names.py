from django.core.management.base import BaseCommand
from django.db.models import Count
from journal.models import Habit


class Command(BaseCommand):
    help = 'Update duplicate habit names to make them unique'

    def handle(self, *args, **kwargs):
        duplicates = Habit.objects.values('name').annotate(
            name_count=Count('name')).filter(name_count__gt=1)

        for entry in duplicates:
            name = entry['name']
            duplicate_habits = Habit.objects.filter(name=name)

            for i, habit in enumerate(duplicate_habits):
                if i == 0:
                    continue
                habit.name = f"{habit.name}_{i}"
                habit.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully updated duplicate habit names'))
