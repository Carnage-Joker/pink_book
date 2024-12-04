# utils.py
from .models import ClothingItem, Avatar
from django.contrib.auth import get_user_model


def get_default_user():
    ##function to get the default user
    return get_user_model().objects.get_or_create(username='defaultuser')[0]


def add_clothing_to_favorites(user, clothing_item):
    


def get_premium_items():
    return ClothingItem.objects.filter(is_premium=True)


def create_avatar_for_user(user):
    avatar, created = Avatar.objects.get_or_create(user=user)
    return avatar, created
