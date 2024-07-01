# utils.py
from django.contrib.auth import get_user_model


def get_default_user():
    ##function to get the default user
    return get_user_model().objects.get_or_create(username='defaultuser')[0]

