from .models import Avatar, Item
from django.contrib.auth import get_user_model


def get_default_user():
    ##function to get the default user
    """
    Function to get the default user.
    """
def add_clothing_to_favorites(user, clothing_item):
    if hasattr(user, 'favorites'):
        user.favorites.add(clothing_item)
        user.save()
    else:
        raise AttributeError("User object has no attribute 'favorites'")
    user.favorites.add(clothing_item)
    user.save()
    


def get_premium_items():
    return Item.objects.filter(is_premium=True)


def create_avatar_for_user(user):
    avatar, created = Avatar.objects.get_or_create(user=user)
    return avatar, created
