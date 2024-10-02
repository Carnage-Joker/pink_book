<<<<<<< HEAD
from django.core.management.base import BaseCommand
from datetime import datetime
from django.core.mail import send_mail
from models import Habit

class Command(BaseCommand):
    help = 'Send reminders for daily habits'

    def handle(self, *args, **options):
        today = datetime.today().weekday()
        habits = Habit.objects.filter(reminder_frequency='daily')
        for habit in habits:
            user_email = habit.user.email
            subject = "Habit Reminder"
            message = f"Hello {habit.user.sissy_name},\n\nThis is a reminder for your habit: {habit.name}.\n\nDescription: {habit.description}"
            from_email = 'huisnathan80@gmail.com'  # The same email you used in settings.py

            send_mail(subject, message, from_email, [user_email], fail_silently=False)
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders!'))

=======
from django.core.management.base import BaseCommand
from datetime import datetime
from django.core.mail import send_mail
from models import Habit

class Command(BaseCommand):
    help = 'Send reminders for daily habits'

    def handle(self, *args, **options):
        today = datetime.today().weekday()
        habits = Habit.objects.filter(reminder_frequency='daily')
        for habit in habits:
            user_email = habit.user.email
            subject = "Habit Reminder"
            message = f"Hello {habit.user.username},\n\nThis is a reminder for your habit: {habit.name}.\n\nDescription: {habit.description}"
            from_email = 'huisnathan80@gmail.com'  # The same email you used in settings.py

            send_mail(subject, message, from_email, [user_email], fail_silently=False)
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders!'))

>>>>>>> bc61eea2aedc4e423bc10c64ed6a584fcf87a9cc
