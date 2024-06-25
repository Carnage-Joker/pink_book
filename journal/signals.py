from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile

# Behavioral Design Pattern: Observer pattern


class Observer:
    def update(self, message):
        pass


class UserObserver(Observer):
    def __init__(self, user):
        self.user = user

    def update(self, message):
        # Notify the user about updates
        self.user.notify(message)


class User:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
